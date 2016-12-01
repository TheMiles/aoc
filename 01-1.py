#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Find way to bunny HQ')
parser.add_argument('directions', metavar='dir', type=str, nargs=1,
                    help='directions to bunny HQ')

class Santa(object):
    def __init__(self):
        self.dir=(1,0)
        self.pos=(0,0)

    def change_direction(self,d):
        if self.dir == ( 1, 0):
            self.dir = (0,1) if d == 'R' else (0,-1)

        elif self.dir == ( 0, 1):
            self.dir = (-1,0) if d == 'R' else (1,0)

        elif self.dir == (-1, 0):
            self.dir = (0,-1) if d == 'R' else (0,1)

        elif self.dir == ( 0,-1):
            self.dir = (1,0) if d == 'R' else (-1,0)

    def walk(self,d):
        self.pos = (self.pos[0] + int(d) * self.dir[0], self.pos[1] + int(d) * self.dir[1] )


args = parser.parse_args()
print(args.directions)

commands = [ x.strip() for x in args.directions[0].split(',') ]
print(commands)

s = Santa()

for c in commands:
    r = c[0]
    w = c[1:]
    s.change_direction(r)
    s.walk(w)
    print("Santa gets command {0}-{1}, is now at {2} and faces {3}, current distance {4}".format(r,w,s.pos,s.dir, (abs(s.pos[0])+ abs(s.pos[1]))))



