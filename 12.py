#!/usr/bin/python3

import argparse
import re
from collections import defaultdict


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-i', '--iterations', default=20)
    return parser.parse_args()

inputPattern  = re.compile(r"initial state: (.*)$")
rulePattern  = re.compile(r"(.{5}) => (.)")


def getValue(origin, plants):

    v = 0
    o = 0 - origin
    for i,p in enumerate(plants):
        v += o+i if p == '#' else 0
    return v


def prependPathsIfNeeded(origin, plants):

    first = plants.index('#')
    if first < 5:
        prepend = ['.' for i in range(5-first)]
        origin += 5-first
        plants  = prepend + plants

    last = plants[::-1].index('#')
    if last < 5:
        plants.extend(['.' for i in range(5-last)])

    return origin, plants

def iterate(rules,plants):

    nextPlants = plants[:]
    for i in range(2, len(plants)-2):
        s             = plants[i-2:i+3]
        pattern       = ''.join(s)
        nextPlants[i] = rules[pattern] if pattern in rules else '.'

    return nextPlants




if __name__ == '__main__':
    args   = getArguments()
    lines  = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))
    plants = [list(m[1]) for m in [ inputPattern.match(l) for l in lines ] if m ][0]
    rules  = { m[1]: m[2] for m in [ rulePattern.match(l) for l in lines ] if m}
    origin = 0

    for i in range(args.iterations):
        origin, plants = prependPathsIfNeeded(origin, plants)
        print("{:> 3}: {}".format(i,''.join(plants)))
        plants = iterate(rules, plants)

    print("{:> 3}: {}".format(args.iterations,''.join(plants)))
    print("Value: ", getValue(origin,plants))