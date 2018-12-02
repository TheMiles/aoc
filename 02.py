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

def differingChars(first, second):
    sum = 0
    for p in zip(first,second):
        sum += 0 if p[0] == p[1] else 1
    return sum

sumOccurrences = defaultdict(int)
lines     = [ x.strip() for x in args.input.readlines() ]
for l in lines:
    if l:
        occurrences    = countOccurrences(l)
        frequents      = set(occurrences.values())
        for f in frequents:
            sumOccurrences[f] += 1

differentCharactersMap = defaultdict(list)
for i, l in enumerate(lines):
    for j, k in enumerate(lines[i+1:]):
        differentCharactersMap[differingChars(l,k)].append((l,k))

for ones in differentCharactersMap[1]:
    l = str()
    for t in zip(ones[0], ones[1]):
        l += t[0] if t[0] == t[1] else ''
    print("Remaining characters '{0}'".format(l))


print("Result {0}".format(sumOccurrences[2] * sumOccurrences[3]))
