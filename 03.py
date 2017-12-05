#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Spreadsheet')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))


def getCorners(v):
    if v < 1: return None

    l = (v*2+1)
    c = [l**2]
    for x in range(3):
        c.append(c[-1]-l+1)
    return c

def getMiddles(v):
    c = getCorners(v)
    if c:
        return [x-v for x in getCorners(v)]
    return [1]

def findCircle(v):
    i = 0
    while v > (i*2+1)**2:
        i += 1
    return i

args = parser.parse_args()

lines = [ x.strip() for x in args.input.readlines() ]
sum = 0
for l in lines:
    value = int(l)
    circle = findCircle(value)
    middles = getMiddles(circle)
    distanceToMiddle = min([abs(value-x) for x in middles])
    print("Value {0} is on circle {1} middles {2} distanceToMiddle {3} also {4}".format(value, circle, middles, distanceToMiddle, distanceToMiddle+circle))