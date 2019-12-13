#!/usr/bin/python3

import argparse
import numpy as np
import re
from datetime import datetime


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-i','--iterations', type=int, default=10)

    return parser.parse_args()


class Progress(object):

    def __init__(self, number):
        self.number = number
        self.count  =  0
        self.prev   = -1
        self.start  = None

    def reset(self):
        self.count  = 0
        self.prev   = -1
        self.start  = None

    def __str__(self):
        percent    = self.percent()
        dt         = datetime.now() - self.start
        total_time = dt * 100 / percent if percent > 0 else -1
        return "{:.2f}% remaining time {} of  {}".format(self.percent(), (total_time-dt), total_time)

    def percent(self):
        return 100*self.count/self.number

    def tick(self):
        if self.start is None:  self.start = datetime.now()
        self.count += 1
        percent = int(self.percent())
        if percent != self.prev:
            self.prev = percent
            print(self)


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


def createFastMoon(moons, axis):
    return np.array([[m.pos[axis],m.vel[axis]] for m in moons])


def applyForceFastMoon(fastMoons):
    fastMoons[:,1] += np.array(list(map(lambda x: np.sum(np.sign(fastMoons[:,0]-x)), fastMoons[:,0])))
    fastMoons[:,0] += fastMoons[:,1]

def findCycleLengthFastMoon(moons, axis):
    fastMoons  = createFastMoon(moons,axis)
    firstMoon  = fastMoons.copy()

    i = 0
    while True:
        i += 1
        applyForceFastMoon(fastMoons)
        if np.array_equal(firstMoon, fastMoons):
            break
    return i



positionPattern = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")

if __name__ == '__main__':
    args = getArguments()
    lines = filter(None, [ x for x in args.input.readlines() ] )

    moons = []
    for p in lines:
        m = positionPattern.match(p)
        moons.append(Moon([int(m[1]),int(m[2]),int(m[3])]))

    iterations = [0,0,0]
    iterations[0] = findCycleLengthFastMoon(moons,0)
    iterations[1] = findCycleLengthFastMoon(moons,1)
    iterations[2] = findCycleLengthFastMoon(moons,2)

    lcm = np.lcm.reduce(iterations)

    print(iterations, lcm)
