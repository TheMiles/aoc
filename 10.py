#!/usr/bin/python3

import argparse
import re
from collections import defaultdict

parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('size', type=int)
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

args = parser.parse_args()





circle  = list(range(args.size))
lengths = [ int(x.strip()) for x in args.input.readline().split(',')]

i     = 0
skip  = 0
shift = 0

for l in lengths:
    assert l <= len(circle)

    #rotate circle according to i
    circle = circle[i:] + circle[:i]

    #apply inversion
    circle = list(reversed(circle[:l])) + circle[l:]

    #rotate back
    circle = circle[-i:] + circle[:-i]

    #adjust i
    i += l + skip
    i %= len(circle)
    skip += 1

print("The product of the first ot elements is", circle[0] * circle[1])