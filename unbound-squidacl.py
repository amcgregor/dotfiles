#!/usr/bin/env python3

"""Attempt to pull in a published Squid ACL description and convert to an Unbound zone definition.

This script trusts the ACL sufficiently that it applies the blacklist to the upper-level domain, e.g. instead of
blacklisting api.xyzzy.info, it'll blacklist [*.]xyzzy.info.

You'll need to:

	pip install tld
"""

import sys

from urllib.request import urlopen
from pathlib import Path

from tld import get_fld
from tld.exceptions import TldDomainNotFound


if not sys.argv[1:]:
	print("./unbound-squidacl.py <target-ip> <zone-file> <source>")
	sys.exit(-1)

ip, zone, source = sys.argv[1:]
lines = Path(source).read_text('utf-8').split('\n')
outfile = Path(zone).open('w', encoding='utf-8')
domains = set()

for line in lines:
	line = line.strip().strip('!').lstrip('.')
	
	if not line:
		continue
	
	if line[0] == '#':
		print(line)
		print(line, file=outfile)
		continue
	
	print(">>>", line)
	
	try:
		domain = get_fld(line, fix_protocol=True)
		if domain in domains:
			raise ValueError("Duplicate domain.")
	
	except TldDomainNotFound:
		print("!!! skipped")
		continue
	
	except ValueError:
		print("!!! duplicate")
	
	else:
		print("\t", domain)
		domains.add(domain)

for domain in sorted(domains):
	print(f"* {domain}")
	print(f'\nlocal-zone: "{domain}" redirect\nlocal-data: "{domain} A 192.168.2.32"', file=outfile)
