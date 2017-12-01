#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()


def is_possible_triangle(l):
	l.sort()
	return sum(l[:-1]) > l[-1]


triangles = [[] for x in range(3)]
count_good = 0
count_total = 0

for lnumber,data in enumerate(args.file.readlines()):
	line = [ int(x) for x in data.strip().split()]
	if len(line) != 3:
		raise ValueError('Wrong number of entries in a line')
	
	for i,d in enumerate(line):
		triangles[i].append(d)

	if lnumber%3 == 2:
		for t in triangles:
			if is_possible_triangle(t):
				count_good += 1
			count_total += 1
			del t[:]

print("Found {0} triangles, and {1} are possible".format(count_total,count_good))
