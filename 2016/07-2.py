#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()

abaRegEx  = re.compile(r"(?=(\w)(\w)\1)")
countSupport = 0

for l in [ x.strip() for x in args.file]:

    foundAbas = [[],[]]
    l = l.replace(']','[')
    groups = l.split("[")

    for i,g in enumerate(groups):
        foundAbas[i%2].extend( [ x for x in abaRegEx.findall(g) if x[0] != x[1] ] )

    supportsSSL = False
    for aba in foundAbas[0]:
        supportsSSL |= (aba[1],aba[0]) in foundAbas[1]

    countSupport += 1 if supportsSSL else 0
print(countSupport)