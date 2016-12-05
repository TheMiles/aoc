#!/usr/bin/env python3

import argparse
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()

for l in [ x.strip() for x in args.file]:
	password = ''
	i = -1
	while len(password) < 8:
		i += 1
		data = (l + str(i)).encode('utf-8')
		m = hashlib.md5(data)
		d = m.hexdigest()
		if d[:5] == '00000':
			password += d[5]
			print("Found a letter '{0}' at index {1}, password so far {2}".format(d[5],i,password))
	
	print("Password for {0} is: {1}".format(l, password))
