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


def splitAndMergePolymer(p):

    p              = p[:]
    i              = 0
    polymer_length = len(p)

    if polymer_length <= 1:
        return p

    while i < polymer_length:
        if isReacting(p, i):
            split = i+1
            # print("SPLIT {0}  --{3}--> {1} | {2}".format(p, p[:split-1], p[split:], split))
            k, p = mergePolymers(p[:split], p[split:])
            i -= k
            polymer_length -= 2*k
        i += 1

    return p

def mergePolymers(p1, p2):

    if not p1:
        # print("Merge {0} | {1} -select2-> {1}".format(p1, p2))
        return 0, p2

    if not p2:
        # print("Merge {0} | {1} -select1-> {0}".format(p1, p2))
        return 0, p1

    if p1[-1].upper() == p2[0].upper() and p1[-1] != p2[0]:
        # print("Merge {0} | {1} -R-> {2} | {3}".format(p1, p2, p1[:-1], p2[1:]))
        k, p = mergePolymers(p1[:-1], p2[1:])
        return k+1, p

    # print("Merge {0} | {1} -M-> {2}".format(p1, p2, p1 + p2))
    return 0, p1 + p2


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))

    sleeptable = dict()
    for line in lines:

        polymers = [ x for x in line ]

        reducedPolymers = splitAndMergePolymer(polymers)

        types = list(set([ x.lower() for x in reducedPolymers ]))

        cleanedPolymerLengths = dict()
        for t in types:
            cleanedPolymer = [ x for x in reducedPolymers if x.lower() != t ]
            reducedCleanedPolymer = splitAndMergePolymer(cleanedPolymer)
            cleanedPolymerLengths[t] = len(reducedCleanedPolymer)


        shortestPolymerType = None
        shortestPolymerLen  = len(reducedPolymers)
        for k,v in cleanedPolymerLengths.items():
            if v < shortestPolymerLen:
                shortestPolymerLen = v
                shortestPolymerType = k

        print("Reduced Polymer is {0} long. By removing {1} it will be {2} long".format(len(reducedPolymers), shortestPolymerType, shortestPolymerLen))
