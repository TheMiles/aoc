#!/usr/bin/python3

import argparse
import intcode as ic
from collections import defaultdict
import numpy as np


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
        robot = Robot(p, hull)

        robot.run()

        sum = 0
        for r in hull:
            sum += len(hull[r])
        print(sum)

