import boto3
import dns.rdatatype
import dns.zone
import json
import sys

client = boto3.client("route53")

with open(sys.argv[1]) as fd:
    zone = dns.zone.from_file(fd, allow_include=True)

changes = []
for name, data in zone.items():
    for rdataset in data.rdatasets:
        if rdataset.rdtype == dns.rdatatype.SOA:
            continue

        if rdataset.rdtype == dns.rdatatype.NS and str(name) in ["@", zone.origin]:
            continue

        if str(name) == "@":
            recname = str(zone.origin)
        else:
            recname = f"{name}.{zone.origin}"

        changes.append(
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": recname,
                    "Type": str(rdataset.rdtype.name),
                    "TTL": rdataset.ttl,
                    "ResourceRecords": [{"Value": str(rdata)} for rdata in rdataset],
                },
            }
        )

print(json.dumps(changes, indent=2))
res = client.change_resource_record_sets(
    HostedZoneId=sys.argv[2], ChangeBatch={"Changes": changes}
)
