#!/usr/bin/python3

import argparse
import intcode as ic
from collections import defaultdict
import numpy as np
import curses
from utils.getch import getch
from utils.fields import Field


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

    return parser.parse_args()


class ScreenField(Field):

    def __init__(self, screen):
        Field.__init__(self)
        self.screen = screen


    def printField(self):
        l = self.getStringList()
        for y,r in enumerate(l):
            self.screen.addstr(y,0,"".join(r))
        self.screen.refresh()


class Robot(object):

    def __init__(self, program, field):
        self.input  = ic.Fifo()
        self.output = ic.Fifo()
        self.cpu    = ic.CPU(program, self.input, self.output)

        self.directions = {
            'N': 1,
            'S': 2,
            'W': 3,
            'E': 4
        }
        self.inverted = {
            'N': 'S',
            'S': 'N',
            'W': 'E',
            'E': 'W'
        }

        self.deltaPos = {
            'N': np.array([-1, 0]),
            'S': np.array([ 1, 0]),
            'W': np.array([ 0,-1]),
            'E': np.array([ 0, 1])
        }

        self.keymap = {
            'w': 'N',
            'W': 'N',
            's': 'S',
            'S': 'S',
            'a': 'W',
            'A': 'W',
            'd': 'E',
            'D': 'E',
        }

        self.field  = field
        self.pos    = np.array([0,0])
        self.oxygen = np.array([0,0])
        self.decisions = {}

    def lookAround(self):
        self.lookDir('N')
        self.lookDir('S')
        self.lookDir('W')
        self.lookDir('E')

    def lookDir(self,d):
        current = self.pos

        self.move(d)
        if not np.equal(current, self.pos).all():
            self.move(self.inverted[d])

    def getExits(self):
        self.lookAround()
        exits = []
        def checkExit(d):
            v = self.field.getContent(self.pos+self.deltaPos[d])
            if v == '.' or v == 'O':
                exits.append(d)

        checkExit('N')
        checkExit('S')
        checkExit('W')
        checkExit('E')
        return exits

    def getDecisionsLeft(self):

        p = self.pos[0]*1000+self.pos[1]
        if p not in self.decisions:
            self.decisions[p] = self.getExits()

        return self.decisions[p]

    def move(self, direction):
        self.input.push(self.directions[direction])
        self.cpu.run()
        result = self.output.pop()

        # print("From {} starting {}".format(self.pos, direction))

        nextPos = self.pos+self.deltaPos[direction]
        if result == 0:
            self.field.setContent(nextPos,'#')
        elif result == 1:
            self.field.setContent(nextPos,'.')
            self.pos = nextPos
            self.field.setRobot(self.pos)
        elif result == 2:
            self.field.setContent(nextPos,'O')
            self.oxygen = nextPos
            self.pos = nextPos

        # print(" result: {} new pos {}".format(result,self.pos))


    def run(self):

        backtrack = []
        while True:
            self.lookAround()
            self.field.printField()

            d = self.getDecisionsLeft()
            if d:
                n = d.pop()
                self.move(n)
                backtrack.append(self.inverted[n])
                r = self.getDecisionsLeft()
                r.remove(self.inverted[n])
            else:
                n = backtrack.pop(-1)
                self.move(n)

            if not backtrack:
                break

def main(stdscr):
    args = getArguments()
    lines = [[ int(y) for y in x.strip().split(',')] for x in list(filter(None, [ r for r in args.input.readlines() ] )) ]

    curses.curs_set(0)
    stdscr.clear()

    for p in lines:

        field = ScreenField(stdscr)
        robot = Robot(p,field)
        robot.run()

        l= [robot.oxygen]
        i = 0
        while field.countContent('.') > 0:
            nextL = []
            for o in l:
                r = field.getAdjacentContent(o)
                for k in r:
                    if k[1]=='.':
                        nextL.append(k[0])
                        field.setContent(k[0],'O')
            l = nextL
            i += 1
            field.printField()
        stdscr.addstr(curses.LINES-5,3, "There are {} iterations".format(i))
        stdscr.refresh()
        getch()





if __name__ == '__main__':
    curses.wrapper(main)
