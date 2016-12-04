#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()

def count_occurences(letters):
	count = dict()
	for c in letters:
		count[c] = count.get(c,0)+1
	return count

def get_n_most_occurrence(counts, n):
	vals = counts.values()
	vals.sort()
	return vals[-n] if len(vals) >= n else vals[0]

def is_real_room(counts, checksum):
	at_least_that_often = get_n_most_occurrence(counts,5)
	checks = [ counts.get(x,None) for x in checksum ]
	prev = checks[0]
	for c in checks:
		if prev < c or c < at_least_that_often:
			return False
		prev = c


	return True

sum_of_room_sectors = 0

for l in [ x.strip() for x in args.file]:
	elements = l.split('-')
	letters  = str().join(elements[:-1])
	tail     = elements[-1].split('[')
	sectorID = int(tail[0])
	checksum = tail[1][:-1]

	count    = count_occurences(letters)
	is_real  = is_real_room(count,checksum)

	# print(sectorID, letters, count, checksum, is_real)
	sum_of_room_sectors += sectorID if is_real else 0

print(sum_of_room_sectors)