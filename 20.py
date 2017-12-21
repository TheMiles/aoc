#!/usr/bin/python3

import argparse
import re
import math
from collections import defaultdict

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()

getPosVelAcc = re.compile(r"p=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>,\s*v=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>,\s*a=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>")

class Particle(object):

    def __init__(self,id,line):
        m = getPosVelAcc.match(line)
        if not m:
            print("Couldn't parse particle info", line)
            exit(1)

        self.id  = id
        self.pos = [int(m[1]),int(m[2]),int(m[3])]
        self.vel = [int(m[4]),int(m[5]),int(m[6])]
        self.acc = [int(m[7]),int(m[8]),int(m[9])]
        self.speedIsIncreasing = False
        self.isRunningAway = False

    def __str__(self):
        return "{0}: p ({1},{2},{3}) {10}\tv ({4},{5},{6}) {11}\ta ({7},{8},{9}) {12} {13} {14}".format(
            self.id,
            self.pos[0],self.pos[1],self.pos[2],
            self.vel[0],self.vel[1],self.vel[2],
            self.acc[0],self.acc[1],self.acc[2],
            self.distance(),
            self.speed(),
            self.acceleration(),
            "Faster" if self.speedIsIncreasing else "Slower",
            "Further" if self.isRunningAway else "Closer"
            )

    def speed(self):
        return math.sqrt(self.vel[0]**2 + self.vel[1]**2 + self.vel[2]**2)

    def distance(self):
        return abs(self.pos[0]) + abs(self.pos[1]) + abs(self.pos[2])

    def acceleration(self):
        return math.sqrt(self.acc[0]**2 + self.acc[1]**2 + self.acc[2]**2)


    def tick(self):
        oldSpeed = self.speed()
        oldDist  = self.distance()
        self.vel = [ sum(x) for x in zip(self.vel, self.acc) ]
        self.pos = [ sum(x) for x in zip(self.pos, self.vel) ]
        self.speedIsIncreasing = self.speed() >= oldSpeed
        self.isRunningAway     = self.distance() >= oldDist

def removeCollisions(p):
    particles = p[:]
    collisions = defaultdict(lambda: [])
    for i,x in enumerate(particles):
        collisions[str(x.pos)].append(i)

    remove_indices = []
    for values in collisions.values():
        if len(values) > 1:
            remove_indices.extend(values)
    remove_indices.sort(reverse=True)
    for i in remove_indices:
        del particles[i]
    return particles


if __name__ == '__main__':
    args = getArguments()

    particles = [ Particle(i,x) for i,x in enumerate(args.input.readlines()) ]

    while any([ not x.speedIsIncreasing or not x.isRunningAway for x in particles ]):
        for x in particles:
            x.tick()
        particles = removeCollisions(particles)

    print(len(particles))