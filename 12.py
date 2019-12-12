#!/usr/bin/python3

import argparse
import numpy as np
import re


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-i','--iterations', type=int, default=10)

    return parser.parse_args()




class Moon(object):

    def __init__(self, pos):
        self.pos = np.array(pos)
        self.vel = np.array([0,0,0])

    def __str__(self):
        return "Pos ({},{},{}) Vel ({},{},{}) pE {} kE {} E {} ".format(self.pos[0],self.pos[1],self.pos[2],self.vel[0],self.vel[2],self.vel[2], self.potentialEnergy(), self.kineticEnergy(), self.energy())

    def potentialEnergy(self):
        return np.sum(np.abs(self.pos))

    def kineticEnergy(self):
        return np.sum(np.abs(self.vel))

    def energy(self):
        return self.potentialEnergy() * self.kineticEnergy()

    def applyForce(self, other):
        for i in range(3):
            if self.pos[i] == other.pos[i]: continue
            if self.pos[i] <  other.pos[i]: self.vel[i] +=  1
            if self.pos[i] >  other.pos[i]: self.vel[i] += -1

    def move(self):
        self.pos += self.vel


def iterateSystem(moons):

    for m in moons:
        for n in moons:
            m.applyForce(n)

    for m in moons:
        m.move()


positionPattern = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")

if __name__ == '__main__':
    args = getArguments()
    lines = filter(None, [ x for x in args.input.readlines() ] )

    moons = []
    for p in lines:
        m = positionPattern.match(p)
        moons.append(Moon([int(m[1]),int(m[2]),int(m[3])]))

    for i in range(args.iterations):
        print(i,[str(m) for m in  moons])
        iterateSystem(moons)

    print(args.iterations,[str(m) for m in  moons])
    print("Energy", sum([m.energy() for m in moons]))

