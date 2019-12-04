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

def getSegmentPairs(a):
    return [a[i:i+2] for i in range(len(a)-1)]

def getIntersections(a,b):
    intersections = []
    if min(a[:,0])>max(b[:,0]) or max(a[:,0])<min(b[:,0]): return intersections
    if min(a[:,1])>max(b[:,1]) or max(a[:,1])<min(b[:,1]): return intersections

    aSteps        = getSteps(a)
    bSteps        = getSteps(b)

    for ca in aSteps:
        for cb in bSteps:
            if all(ca == cb):
                intersections.append(ca)
    return intersections

def indexInCoordinates(l,needle):
    for i in range(len(l)):
        if all(needle == l[i]):
            return i
    return None

if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ [ y for y in x.strip().split(',')] for x in args.input.readlines() ] ))

    poly = []
    for l in lines:

        pg = np.array([[0,0]])
        for d in l:
            pg = np.append(pg, [pg[-1] + getSegment(d)],0)

        poly.append(pg)

    a = getSegmentPairs(poly[0])
    b = getSegmentPairs(poly[1])

    intersections = []
    length = len(a)*len(b)
    count  = 0
    for pa in a:
        for pb in b:
            count +=1
            # print("{}%".format(int(100*count/length)))
            intersections.extend(getIntersections(pa,pb))

    print("Number of found intersections:",len(intersections))

    distances = [ sum(abs(p)) for p in intersections ]
    print("Closest intersection has distance:",min(distances))

    a = getSteps(poly[0])
    b = getSteps(poly[1])

    distances = []
    for i in intersections:
        da = indexInCoordinates(a,i)+1
        db = indexInCoordinates(b,i)+1
        if da and db:
            distances.append(da+db)

    print("Shortest length:", min(distances))


