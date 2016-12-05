#!/usr/bin/env python3

import argparse
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()

for l in [ x.strip() for x in args.file]:
	password = '--------'
	i = -1
	while '-' in password:
		i += 1
		data = (l + str(i)).encode('utf-8')
		m = hashlib.md5(data)
		d = m.hexdigest()

		if i % 1000 == 0:
			print(" Password {0}  {1}".format(password,i), end='\r')

		if d[:5] == '00000':
			if ord(d[5]) >= ord('0') and ord(d[5]) < ord('8'):
				position = int(d[5])
				if password[position] == '-':
					password = password[:position] + d[6] + password[position+1:]
	
	print(" Password {0}".format(password))
