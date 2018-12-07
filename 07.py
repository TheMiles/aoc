#!/usr/bin/python3

import argparse
import re
from collections import defaultdict

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


def getFreeSteps(d):
    return sorted([ s for s in d if not d[s] ])

def reduceDependency(d, f):
    return { k: set([e for e in v if e != f]) for k, v in d.items() }



finishedPattern  = re.compile(r"Step (.) must be finished before step (.) can")

if __name__ == '__main__':
    args            = getArguments()
    lines           = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))
    dependencyInput = [ (m[1], m[2]) for m in [ finishedPattern.match(l) for l in lines ] ]

    dependencies = defaultdict(set)

    for d in dependencyInput:
        dependencies[d[0]]
        dependencies[d[1]].add(d[0])

    sortedDependencies = []
    while dependencies:
        nextStep = getFreeSteps(dependencies)[0]
        sortedDependencies.append( nextStep )
        del dependencies[nextStep]
        dependencies = reduceDependency(dependencies, nextStep)

    print (''.join(sortedDependencies))


