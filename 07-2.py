#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()

abbaRegEx  = re.compile(r"(\w)(\w)\2\1")
countSupport = 0

for l in [ x.strip() for x in args.file]:

    l = l.replace(']','[')
    groups = l.split("[")
    foundAbbas = [0,0]

    for i,g in enumerate(groups):
        abbasMatches = [ x for x in abbaRegEx.findall(g) if x[0] != x[1] ]
        foundAbbas[i%2] += 1 if (len(abbasMatches)>0) else 0

    tlsSupported = foundAbbas[0] > 0 and foundAbbas[1] == 0
    countSupport += 1 if tlsSupported else 0

print(countSupport)
