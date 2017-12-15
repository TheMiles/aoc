#!/usr/bin/python3

import argparse
import re
from collections import defaultdict

parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
parser.add_argument('-s','--size', type=int, default=256)
parser.add_argument('-r','--rounds', type=int, default=64)

args = parser.parse_args()

def getHex(v):
    if type(v) is str or type(v) is list:
        if len(v) > 1:
            return getHex(v[0]) + getHex(v[1:])
        v = v[0]
    return hex(v)[2:].zfill(2)

def getSparseHash(sparseLength, rounds, hashValues):

    sparseHash  = list(range(sparseLength))
    lengths = [ ord(x) for x in hashValues ] + [17, 31, 73, 47, 23]

    i     = 0
    skip  = 0
    shift = 0

    for r in range(rounds):
        for l in lengths:
            assert l <= len(sparseHash)

            #rotate sparseHash according to i
            sparseHash = sparseHash[i:] + sparseHash[:i]

            #apply inversion
            sparseHash = list(reversed(sparseHash[:l])) + sparseHash[l:]

            #rotate back
            sparseHash = sparseHash[-i:] + sparseHash[:-i]

            #adjust i
            i += l + skip
            i %= len(sparseHash)
            skip += 1
    return sparseHash



def densifyHash(v):
    assert( len(v)%16 == 0 )

    sparseHash = v[:]
    denseHash  = [0] * int(len(sparseHash)/16)
    i = 0

    while sparseHash:
        block      = sparseHash[:16]
        sparseHash = sparseHash[16:]

        while block:
            denseHash[i] = denseHash[i] ^ block[0]
            block        = block[1:]

        i += 1

    return denseHash

lines = [ x.strip() for x in args.input.readlines() ]

for line in lines:

    sparseHash = getSparseHash(args.size, args.rounds, line)
    denseHash  = densifyHash(sparseHash)

    print(getHex(denseHash))

# print("The product of the first ot elements is", circle[0] * circle[1])