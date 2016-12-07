#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()

hsRegEx    = re.compile(r"\[.*(\w)(\w)\2\1.*\]")
abbaRegEx  = re.compile(r"(\w)(\w)\2\1")
countSupport = 0

for l in [ x.strip() for x in args.file]:

	hsMatches    = [ x for x in hsRegEx.findall(l) if x[0] != x[1] ]
	abbasMatches = [ x for x in abbaRegEx.findall(l) if x[0] != x[1] ]

	tlsSupported = not hsMatches and not not abbasMatches
	countSupport += 1 if tlsSupported else 0
	print(l, tlsSupported)

print(countSupport)
