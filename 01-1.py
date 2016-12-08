#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Find way to bunny HQ')
parser.add_argument('directions', metavar='dir', type=str, nargs=1,
                    help='directions to bunny HQ')

class Santa(object):
    directions = [
    ( 1, 0), #N
    ( 0, 1), #E
    (-1, 0), #S
    ( 0,-1)  #W
    ]

    def __init__(self):
        self.dir=0
        self.pos=(0,0)

    def change_direction(self,d):
        self.dir = (self.dir + (-1 if d=='L' else 1)) % 4

    def walk(self,distance):
        l = []
        for i in range(int(distance)):
            self.pos = tuple([ x[0] + x[1] for x in zip(self.pos, self.directions[self.dir])])
            l.append(self.pos)
        return l

args = parser.parse_args()
print(args.directions)

commands = [ x.strip() for x in args.directions[0].split(',') ]
print(commands)

s = Santa()
visited = []

for c in commands:
    r = c[0]
    w = c[1:]
    s.change_direction(r)
    l = s.walk(w)
    print("Santa gets command {0}-{1}, is now at {2} and faces {3}, current distance {4}".format(r,w,s.pos,s.dir, (abs(s.pos[0])+ abs(s.pos[1]))))

    for p in l:
        if p in visited:
            print("Visited again {0} with distance {1}".format(p, abs(p[0])+abs(p[1])))
    visited.extend(l)



