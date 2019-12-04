#!/usr/bin/python3

import argparse
import numpy as np


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


def getSegment(d):
    orientation, length = d[:1], d[1:]
    change = {
        'U': np.array([ 0, 1]),
        'D': np.array([ 0,-1]),
        'L': np.array([-1, 0]),
        'R': np.array([ 1, 0])
    }

    # print("orientation", orientation, "length", length)
    return (change[orientation])*int(length)

def getStepsSegment(a):
    dir    = a[1]-a[0]
    length = int(np.linalg.norm(dir))
    dir    = (dir/length).astype(int)

    return np.array([a[0]+dir*(x+1) for x in range(length)])

def getSteps(a):
    return np.concatenate([ getStepsSegment(a[i:i+2]) for i in range(len(a)-1) ])



if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ [ y for y in x.strip().split(',')] for x in args.input.readlines() ] ))

    poly = []
    for l in lines:

        pg = np.array([[0,0]])
        for d in l:
            pg = np.append(pg, [pg[-1] + getSegment(d)],0)

        poly.append(pg)

    a = getSteps(poly[0])
    b = getSteps(poly[1])

    print(b)

    # for i in range(len(b)-1):
    #     getSteps(b[i:i+2])
