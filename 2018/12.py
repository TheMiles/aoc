#!/usr/bin/python3

import argparse
import re
from collections import defaultdict


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-i', '--iterations', type=int, default=20)
    return parser.parse_args()

inputPattern  = re.compile(r"initial state: (.*)$")
rulePattern  = re.compile(r"(.{5}) => (.)")


def getValue(origin, plants):

    v = 0
    o = origin
    for i,p in enumerate(plants):
        v += o+i if p == '#' else 0
    return v


def adjustPlantList(origin, plants):

    plants = plants[:]
    while ''.join(plants[:5])== '.....':
        plants  = plants[5:]
        origin += 5

    while ''.join(plants[-6:])== '.....':
        plants  = plants[:-5]


    first = plants.index('#')
    if first < 5:
        prepend = ['.' for i in range(5-first)]
        origin -= 5-first
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
    args      = getArguments()
    lines     = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))
    plants    = [list(m[1]) for m in [ inputPattern.match(l) for l in lines ] if m ][0]
    rules     = { m[1]: m[2] for m in [ rulePattern.match(l) for l in lines ] if m}
    origin    = 0
    plantLog  = []
    originLog = []
    i         = 0

    while i < args.iterations:
        origin, plants = adjustPlantList(origin, plants)
        plantString    = ''.join(plants)
        if plantString in plantLog:
            print("{:> 16}: {:> 16} {}".format(i, origin,plantString))
            cycleStart  = plantLog.index(plantString)
            cycleLength = i - cycleStart
            cyclesLeft  = int((args.iterations - cycleStart) / cycleLength)-1
            i           = cycleStart + cyclesLeft * cycleLength + 1
            origin     += (origin - originLog[cycleStart]) * cyclesLeft
            plantLog    = []
            originLog   = []
            continue


        plantLog.append(plantString)
        originLog.append(origin)
        print("{:> 16}: {:> 16} {}".format(i, origin,plantString))
        plants = iterate(rules, plants)
        i += 1

    print("{:> 16}: {:> 16} {}".format(args.iterations,origin,''.join(plants)))
    print("Value: ", getValue(origin,plants))