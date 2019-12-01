#!/usr/bin/python3

import argparse
import re
from collections import defaultdict


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


def getMinMax(l):
    min = l[0][0]
    max = min

    for p in l:
        if p[0][0] < min[0]: min = (p[0][0], min[1])
        if p[0][1] < min[1]: min = (min[0], p[0][1])
        if p[0][0] > max[0]: max = (p[0][0], max[1])
        if p[0][1] > max[1]: max = (max[0], p[0][1])

    return min, max

def printLights(l):

    min,max = getMinMax(l)

    string = []
    for y  in range(min[1]-1, max[1]+2):
        line = []
        for x in range(min[0]-1, max[0]+2):
            line.append('#' if any( x==p[0][0] and y == p[0][1] for p in l ) else '.')
        line.append('\n')
        string.append(''.join(line))
    print(''.join(string))

def iterateLights(l):

    return [ ((p[0][0]+p[1][0], p[0][1]+p[1][1]),p[1]) for p in l ]

lightPointPattern  = re.compile(r"position=< *(-?\d+),  *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>")

if __name__ == '__main__':
    args        = getArguments()
    lines       = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))
    lightPoints = [ ((int(m[1]), int(m[2])),(int(m[3]), int(m[4]))) for m in [ lightPointPattern.match(l) for l in lines ] ]

    i = 0
    while True:
        # printLights(lightPoints)
        before = getMinMax(lightPoints)
        newLights = iterateLights(lightPoints)
        after = getMinMax(newLights)

        dW = (after[1][0]-after[0][0])-(before[1][0]-before[0][0])
        dH = (after[1][1]-after[0][1])-(before[1][1]-before[0][1])
        print("{} dw {} dH {}".format(i, dW, dH))
        if dW > 0 or dH > 0:
            printLights(lightPoints)
            print(i, " seconds")
            break

        i+=1
        lightPoints = newLights