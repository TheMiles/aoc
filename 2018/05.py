#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


def isReacting(p, i):

    if len(p) <= 1 or i < 0 or i >= len(p)-1:
        return False
    return p[i].upper() == p[i+1].upper() and p[i] != p[i+1]


def reducePolymer(p):

    p              = p[:]
    i              = 0
    polymer_length = len(p)

    if polymer_length <= 1:
        return p

    while i < polymer_length:
        if isReacting(p, i):
            # print("SPLIT {0}  --{3}--> {1} | {2}".format(p, p[:i], p[i+2:], i))
            p = p[:i] + p[i+2:]
            i -= 2
            i = max(-1,i)
            polymer_length -= 2
        i += 1

    return p

if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))

    sleeptable = dict()
    for line in lines:

        polymers = [ x for x in line ]

        reducedPolymers = reducePolymer(polymers)

        types = list(set([ x.lower() for x in reducedPolymers ]))

        cleanedPolymerLengths = dict()
        for t in types:
            cleanedPolymer = [ x for x in reducedPolymers if x.lower() != t ]
            reducedCleanedPolymer = reducePolymer(cleanedPolymer)
            cleanedPolymerLengths[t] = len(reducedCleanedPolymer)


        shortestPolymerType = None
        shortestPolymerLen  = len(reducedPolymers)
        for k,v in cleanedPolymerLengths.items():
            if v < shortestPolymerLen:
                shortestPolymerLen = v
                shortestPolymerType = k

        print("Reduced Polymer is {0} long. By removing {1} it will be {2} long".format(len(reducedPolymers), shortestPolymerType, shortestPolymerLen))
