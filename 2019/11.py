#!/usr/bin/python3

import argparse
import intcode as ic
from collections import defaultdict
import numpy as np
from PIL import Image


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'), nargs='?')
    parser.add_argument('-d', '--direct', type=str)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-s', '--stepmode', action='store_true')


    return parser.parse_args()



class Robot(object):

    def __init__(self, program, hull):
        self.input  = ic.Fifo()
        self.output = ic.Fifo()
        self.cpu    = ic.CPU(program, self.input, self.output)
        self.hull   = hull
        self.pos    = np.array([0,0])
        self.dir    = '^'

        self.nextDirection = {
            '^': { 0: '<', 1: '>' },
            '<': { 0: 'v', 1: '^' },
            'v': { 0: '>', 1: '<' },
            '>': { 0: '^', 1: 'v' }
        }

        self.movement = {
            '^': np.array([ 0,-1]),
            '<': np.array([-1, 0]),
            'v': np.array([ 0, 1]),
            '>': np.array([ 1, 0])
        }

    def step(self):

        self.input.push(self.hull[self.pos[0]][self.pos[1]])
        self.cpu.run()

        color     = self.output.pop()
        changeDir = self.output.pop()

        self.hull[self.pos[0]][self.pos[1]] = color

        self.dir = self.nextDirection[self.dir][changeDir]
        self.pos = self.pos + self.movement[self.dir]


    def run(self):
        while not self.cpu.isHalted():
            self.step()



if __name__ == '__main__':
    args = getArguments()
    lines = [args.direct] if args.direct else list(filter(None, [ x for x in args.input.readlines() ] ))
    lines = [[ int(y) for y in x.strip().split(',')] for x in lines ]

    for p in lines:

        # print("Trying", p)

        hull = defaultdict(lambda: defaultdict(lambda:0))
        hull[0][0]=1
        robot = Robot(p, hull)

        robot.run()

        xDims = [min(hull.keys()),max(hull.keys())]
        yDims = [1000000,-10000000]
        sum   = 0
        for r in hull:
            minimum = min(hull[r])
            maximum = max(hull[r])
            if minimum < yDims[0]: yDims[0] = minimum
            if maximum > yDims[1]: yDims[1] = maximum
            sum += len(hull[r])
        print("sum is",sum)


        xOffset = -1 * xDims[0]
        yOffset = -1 * yDims[0]

        print(xDims, yDims, xOffset, yOffset)
        image = np.zeros((yDims[1]-yDims[0]+1, xDims[1]-xDims[0]+1), dtype=np.uint8)
        for c in hull:
            for r in hull[c]:
                v = hull[c][r]
                image[r+yOffset][c+xOffset]=v

        im = Image.fromarray(np.uint8(image*255),'L')
        im.show()


