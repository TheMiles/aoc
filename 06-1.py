#!/usr/bin/env python3

import argparse
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()


histogram = []
for l in [ x.strip() for x in args.file]:
	if len(histogram) < len(l):
		histogram.extend([{} for _ in range(len(l)-len(histogram))])

	for i, c in enumerate(l):
		d = histogram[i]
		d[c] = d.get(c,0) + 1

cleartext = ''
for d in histogram:
	max_number = 0;
	max_char   = '-'
	for key, value in d.items():
		if value > max_number:
			max_number = value
			max_char   = key

	cleartext += max_char

print(cleartext)

