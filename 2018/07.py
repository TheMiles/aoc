#!/usr/bin/python3

import argparse
import re
from collections import defaultdict

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-w','--workers', default=5, type=int)
    parser.add_argument('-b','--basetime', default=60, type=int)
    return parser.parse_args()


def getFreeSteps(d):
    return sorted([ s for s in d if not d[s] ])

def reduceDependency(d, f):
    return { k: set([e for e in v if e != f]) for k, v in d.items() }

def findFreeWorkers(w, t):
    return  [ i for i, e in enumerate(w) if e <= t ]


finishedPattern  = re.compile(r"Step (.) must be finished before step (.) can")

if __name__ == '__main__':
    args            = getArguments()
    lines           = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))
    dependencyInput = [ (m[1], m[2]) for m in [ finishedPattern.match(l) for l in lines ] ]

    dependencies = defaultdict(set)

    for d in dependencyInput:
        dependencies[d[0]]
        dependencies[d[1]].add(d[0])

    sortedDependencies   = []
    workerEndTimes       = [ 0 for i in range(args.workers) ]
    clock                = 0
    nextSteps            = []
    stepsInProgressUntil = defaultdict(list)

    while dependencies or stepsInProgressUntil:
        for s in stepsInProgressUntil[clock]:
            sortedDependencies.append(s)
            dependencies = reduceDependency(dependencies, s)
        del stepsInProgressUntil[clock]

        nextSteps = getFreeSteps(dependencies)
        freeWorkers = findFreeWorkers(workerEndTimes, clock)

        for f in freeWorkers:
            if nextSteps:
                step              = nextSteps[0]
                endTime           = clock + args.basetime + ord(step) - ord('A') + 1
                workerEndTimes[f] = endTime
                stepsInProgressUntil[endTime].append(step)
                del nextSteps[0]
                del dependencies[step]

        clock += 1


    print("Sorted dependencies ",''.join(sortedDependencies))
    print("It took {0} workers {1} seconds".format(args.workers, clock-1))
