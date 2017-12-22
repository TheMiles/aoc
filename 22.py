#!/usr/bin/python3

import argparse


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-i','--iterations', type=int, default=5)
    return parser.parse_args()

def growField(field):
    f = [['.']*len(field)]
    f.extend([ ['.'] + x + ['.'] for x in field ])
    f.append(['.']*len(field))
    return f

class Virus(object):
    movement = {
        's':( 0, 1),
        'n':( 0,-1),
        'e':( 1, 0),
        'w':(-1, 0)
    }

    turn_direction = {
        's':['e','w'],
        'n':['w','e'],
        'e':['n','s'],
        'w':['s','n']
    }


    def __init__(self,field):
        middle = int(len(field)/2)
        self.field = field
        self.pos   = (middle,middle)
        self.dir   = 'n'
        self.count_infections = 0
        self.count_healings   = 0

    def isInBounds(self):
        n_bound = self.pos[1] >= 0
        s_bound = self.pos[1] < len(self.field)
        e_bound = self.pos[0] < len(self.field[0])
        w_bound = self.pos[0] >= 0
        return n_bound and e_bound and s_bound and w_bound

    def grow(self):
        self.field = growField(self.field)
        self.pos = (self.pos[0]+1, self.pos[1]+1)

    def getValue(self):
        if not self.isInBounds():
            self.grow()

        return self.field[self.pos[1]][self.pos[0]]

    def setValue(self,v):
        if not self.isInBounds():
            self.grow()

        self.field[self.pos[1]][self.pos[0]] = v

    def isCurrentCellClean(self):
        return self.getValue() == '.'

    def toggleCurrentCell(self):
        is_clean = self.isCurrentCellClean()
        if is_clean:
            self.count_infections += 1
        else:
            self.count_healings   += 1

        self.setValue('#' if is_clean else '.')

    def getNextDirection(self):
        return self.turn_direction[self.dir][ 0 if self.isCurrentCellClean() else 1 ]

    def move(self):
        m = self.movement[self.dir];
        self.pos = ( self.pos[0]+m[0], self.pos[1]+m[1] )

    def burst(self):

        self.dir = self.getNextDirection()
        self.toggleCurrentCell()
        self.move()

def printField(field):
    for x in field:
        print("".join(x))
    print()


if __name__ == '__main__':
    args = getArguments()

    field = [ [y for y in  x.strip()] for x in args.input.readlines() ]

    v = Virus(field)

    for i in range(args.iterations):
        v.burst()
        # printField(field)
        # input("Press enter...")

    printField(field)
    print("There were", v.count_infections, "new infections")
