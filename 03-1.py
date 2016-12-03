#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()


def is_possible_triangle(l):
	l.sort()
	return sum(l[:-1]) > l[-1]



count_good = 0
count_total = 0

for line in args.file.readlines():
	triangle = [ int(x) for x in line.strip().split()]
	if len(triangle) != 3:
		raise ValueError('Wrong number of entries in a line')
	if is_possible_triangle(triangle):
		count_good += 1
	count_total += 1

print("Found {0} triangles, and {1} are possible".format(count_total,count_good))
