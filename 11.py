#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

args = parser.parse_args()

move = {
    "n":  ( 0, 1, 1),
    "ne": ( 1, 0, 1),
    "se": ( 1,-1, 0),
    "s":  ( 0,-1,-1),
    "sw": (-1, 0,-1),
    "nw": (-1, 1, 0)
}

def distanceHex(a,b):
    return int((abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2]))/2)

lines = [ x.strip() for x in args.input.readlines() ]

for line in lines:
    directions = [ x.strip() for x in line.split(',') ]

    pos = (0,0,0)
    maxDistance = 0

    for d in directions:
        m = move[d]
        pos = (pos[0]+m[0], pos[1]+m[1], pos[2]+m[2])
        distance = distanceHex(pos, (0,0,0))
        if distance > maxDistance:
            maxDistance = distance

    print("End position is", pos, "which is distance",distanceHex(pos, (0,0,0)), "highest distance was", maxDistance)
