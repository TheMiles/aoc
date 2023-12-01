#!/usr/bin/python3

import argparse
import numpy as np
from collections import defaultdict


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'), nargs='?')
    return parser.parse_args()

def removeAsteroid(remove, asteroids):
    asteroids = asteroids[:]
    found = [np.array_equal(remove,x) for x in asteroids]
    if any(found):
        asteroids.pop(found.index(True))
    return asteroids

def getLength(a):
    return np.linalg.norm(a)

def getDirection(a):
    return a / getLength(a)

def getAngle(a):
    dir   = getDirection(a)
    inner = np.inner(np.array([0,-1]),dir)
    angle = np.arccos(inner)
    if a[0] < 0:
        angle = 2*np.pi - angle
    return angle


def getAsteroidInfo(a, asteroids):
    remaining  = removeAsteroid(a,asteroids[:])
    directions = defaultdict(lambda: [])

    for o in remaining:
        diff      = o-a
        length    = getLength(diff)
        dir       = getDirection(diff)
        angle     = int(getAngle(diff)*1000000000000.0)

        directions[angle].append((o,length,dir))

    for d in directions:
        sorted(directions[d], key=lambda l: l[1])

    return directions

if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x for x in args.input.readlines() ] ))

    asteroids = []

    for y,l in enumerate(lines):
        for x, s in enumerate(l):
            if s=='#':
                asteroids.append(np.array([x,y]))

    results = [ len(getAsteroidInfo(a,asteroids)) for a in asteroids ]

    i = results.index(max(results))
    print(asteroids[i], results[i])

    d = getAsteroidInfo(asteroids[i], asteroids)

    count = 0
    while count < 200:
        for a in sorted(d.keys()):
            if d[a]:
                count += 1
                if count == 200:
                    result = d[a][0][0]
                    print(result[0]*100+result[1])
                    print(d[a][0])

                d[a].pop()


