#!/usr/bin/python3

import argparse
import re
from collections import defaultdict
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


class Field(object):

    def __init__(self, vertices):

        self.vertices = vertices
        self.min      = (min([x[0] for x in self.vertices]), min([x[1] for x in self.vertices]))
        self.max      = (max([x[0] for x in self.vertices]), max([x[1] for x in self.vertices]))
        self.field    = [ (None, None) for i in range(self.w() * self.h()) ]

        print("min {0} max {1} w {2} h {3}".format(self.min, self.max, self.w(), self.h()))

        for j in range(self.min[1], self.max[1]):
            for i in range(self.min[0], self.max[0]):
                self.set((i,j), self.getSmallestDistance((i,j)))

    def __str__(self):

        string = ''
        for j in range(self.min[1], self.max[1]):
            for i in range(self.min[0], self.max[0]):
                v = self.get((i,j))
                name = '.'
                if v[0] is not None:
                    name = chr(ord('A')+v[0])

                    if v[1]>0:
                        name = name.lower()

                string += " {0} ".format(name)
            string += '\n'
        return string



    def w(self):
        return self.offset(self.max)[0]


    def h(self):
        return self.offset(self.max)[1]


    def offset(self, coord):
        return (coord[0] - self.min[0], coord[1] - self.min[0])

    def addCoords(self, a, b):
        return (a[0]+b[0], a[1]+b[1])

    def isValidCoord(self, coord):
        c = self.offset(coord)

        if c[0] < 0 or c[0] >= self.w() or c[1] < 0 or c[1] >= self.h():
            return False
        return True


    def fieldIndex(self, coord):
        o     = self.offset(coord)
        # print("fieldIndex {0}  {1}  {2}".format(o[0],o[1], o[0] + o[1] * self.w()))
        return o[0] + o[1] * self.w()


    def get(self, coord):
        return self.field[self.fieldIndex(coord)]


    def set(self, coord, value):
        self.field[self.fieldIndex(coord)] = value


    def getSmallestDistance(self, coord):

        smallestDistance = self.max[0] + self.max[1]
        smallestName     = set()
        for i, v in enumerate(self.vertices):
            d = self.distance(coord, v)
            if d < smallestDistance:
                smallestDistance = d
                smallestName.clear()
                smallestName.add(i)

            if d == smallestDistance:
                smallestName.add(i)

        if len(smallestName) > 1:
            return (None, None)

        return (smallestName.pop(), smallestDistance)


    def forgetAbout(self):

        forget = set()
        for i in range(self.min[1], self.max[1]):
            v = self.get((self.min[0], i))
            u = self.get((self.max[0]-1, i))

            if v[0] is not None: forget.add(v[0])
            if u[0] is not None: forget.add(u[0])

        for i in range(self.min[0], self.max[0]):
            v = self.get((i, self.min[1]))
            u = self.get((i, self.max[1]-1))

            if v[0] is not None: forget.add(v[0])
            if u[0] is not None: forget.add(u[0])

        return list(forget)


    def getCount(self):

        f = self.forgetAbout()

        count = defaultdict(int)
        for v in self.field:
            name = v[0]
            if name is None or name in f:
                continue
            count[name] += 1

        return count



    def distance(self, a, b):
        return abs(b[0]-a[0]) + abs(b[1]-a[1])



vertexPattern  = re.compile(r"(\d+), (\d+)")

if __name__ == '__main__':
    args     = getArguments()
    lines    = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))
    vertices = [ (int(m[1]), int(m[2])) for m in [ vertexPattern.match(l) for l in lines ] ]
    vertices.sort()

    field = Field(vertices)
    c = field.getCount()
    print("Hugest Field ", max(c.values()))

