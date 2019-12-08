#!/usr/bin/python3

import argparse
import numpy as np

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-w','--width', type=int, default=25)
    parser.add_argument('-t','--height', type=int, default=6)

    return parser.parse_args()


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x for x in args.input.readlines() ] ))

    for p in lines:

        image = np.array([int(i) for i in p]).reshape(int(len(p)/(args.width*args.height)), args.height, args.width)

        counts = []
        for layer in image:
            u, c = np.unique(layer,return_counts=True)
            counts.append(dict(zip(u,c)))

        zeros= args.width*args.height
        sum  = 0

        for c in counts:
            # print("Layer",c[0] if 0 in c else 0, c[1], c[2], c[1]*c[2], c)
            if 0 in c and c[0]< zeros:
                sum   = c[1]*c[2]
                zeros = c[0]
        print("Answer:",sum)