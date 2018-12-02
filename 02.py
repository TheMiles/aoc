#!/usr/bin/python3

import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Captcha')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

args = parser.parse_args()


def countOccurrences(line):
    d = defaultdict(int)
    for c in line:
        d[c] += 1
    return d


sumOccurrences = defaultdict(int)
lines     = [ x.strip() for x in args.input.readlines() ]
for l in lines:
    if l:
        occurrences    = countOccurrences(l)
        frequents      = set(occurrences.values())
        for f in frequents:
            sumOccurrences[f] += 1
print("Ergebnis {0}".format(sumOccurrences[2] * sumOccurrences[3]))
