#!/usr/bin/env python3

import argparse
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()

number_of_lines = 0
histogram = []
for l in [ x.strip() for x in args.file]:

	number_of_lines += 1
	
	if len(histogram) < len(l):
		histogram.extend([{} for _ in range(len(l)-len(histogram))])

	for i, c in enumerate(l):
		d = histogram[i]
		d[c] = d.get(c,0) + 1

cleartext = ''
for d in histogram:
	min_number = number_of_lines;
	min_char   = '-'
	for key, value in d.items():
		if value < min_number:
			min_number = value
			min_char   = key

	cleartext += min_char

print(cleartext)

