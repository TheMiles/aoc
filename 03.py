#!/usr/bin/python3

import argparse
import re

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


class Rect(object):

    def __init__(self, l, t, r, b):

        self.l = l
        self.t = t
        self.r = r
        self.b = b


    def __str__(self):

        return "Rect lt({0}/{1}) rb({2}/{3}) a[{4}]".format(self.l,self.t,self.r, self.b, self.area())



    def w(self):

        return self.r - self.l


    def h(self):
        return self.b - self.t


    def area(self):
        return self.w() * self.h()


    def empty(self):

        return self.area() == 0


    def occupiedList(self):

        return [(x,y) for x in range(self.l,self.r) for y in range(self.t, self.b)]


    def overlap(self, other):

        l = self.l if self.l > other.l else other.l
        t = self.t if self.t > other.t else other.t
        r = self.r if self.r < other.r else other.r
        b = self.b if self.b < other.b else other.b

        if l < r and t < b:
            return Rect(l, t, r, b)

        return None


elveClaim = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))

    claims = list()
    for line in lines:
        m = elveClaim.match(line)
        if not m:
            print("Couldn't parse elven claims", line)
            exit(1)

        id = int(m[1])
        l  = int(m[2])
        t  = int(m[3])
        w  = int(m[4])
        h  = int(m[5])

        claims.append((id, Rect(l, t, l+w, t+h)))

    collisions = set()
    for i,c in enumerate(claims):
        for j, d in enumerate(claims[i+1:]):
            overlapRect = c[1].overlap(d[1])
            if overlapRect:
                collisions.update(overlapRect.occupiedList())

    print(collisions)
    print(len(collisions))