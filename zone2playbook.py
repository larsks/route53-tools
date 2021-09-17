import dns.zone
import jinja2
import sys


env = jinja2.Environment(
        extensions=['jinja2.ext.loopcontrols'],
        loader=jinja2.loaders.FileSystemLoader('.'),
        trim_blocks=True,
        lstrip_blocks=True,
        )

with open(sys.argv[1]) as fd:
    zone = dns.zone.from_text(fd.read(), allow_include=True)

template = env.get_template('playbook.j2.yml')
print(template.render(zone=zone))

if False:
    for name, data in zone.items():
        for rdataset in data.rdatasets:
            if rdataset.rdtype.name == 'SOA':
                continue

            for rdata in rdataset:
                if rdataset.rdtype.name == 'NS' and name in ['@', z.origin]:
                    continue

                print('zone:', z.origin)
                print('record:', f'{name}.{z.origin}')
                print('type', rdataset.rdtype.name)
                print('value:', str(rdata))
                print('ttl:', rdataset.ttl)
                print('---')
