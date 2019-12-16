#!/usr/bin/python3

import argparse
import intcode as ic
from collections import defaultdict
import numpy as np
import curses


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

    return parser.parse_args()

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


class Field(object):

    def __init__(self, screen):
        self.content = {
            0: ' ',
            1: '#',
            2: '.',
            3: 'O'
        }

        self.c      = np.array([[2]])
        self.offset = np.array([0,0])
        self.robot  = np.array([0,0])
        self.screen = screen


    def setRobot(self, pos):
        self.robot = pos+self.offset

    def printField(self):
        for y in range(self.c.shape[0]):
            for x in range(self.c.shape[1]):
                p = np.array([y,x])
                if np.equal(self.robot, p).all():
                    self.screen.addstr(y,x,'R')
                else:
                    self.screen.addstr(y,x,self.getContent(p-self.offset))
        self.screen.refresh()


    def getContent(self, pos):
        return self.content[self.getValue(pos)]

    def setContent(self, pos, content):
        for key, value in self.content.items():
            if value == content:
                self.setValue(pos,key)
                return


    def getValue(self, pos):
        p = pos+self.offset
        if np.less(p,0).any() or np.greater_equal(p,self.c.shape).any(): return 0
        return self.c[tuple(p)]

    def setValue(self, pos, value):
        p = pos+self.offset

        # print("setValue",p,pos,self.offset,self.c.shape)
        if np.less(p,0).any() or np.greater_equal(p,self.c.shape).any:
            self.growField(p)
            p = pos+self.offset
            # print("afterGrow",p,pos,self.offset,self.c.shape)

        self.c[tuple(p)] = value
        # print("field now",self.c)

    def growField(self,pos):

        height, width = self.c.shape
        if pos[1]<0:
            d = abs(pos[1])
            self.c = np.concatenate((np.zeros(d*height,dtype=np.uint8).reshape(height,d),self.c),axis=1)
            width += d
            self.offset[1] += d
            self.robot[1] += d
        elif pos[1]>=width:
            d = pos[1]-width+1
            self.c = np.concatenate((self.c,np.zeros(d*height,dtype=np.uint8).reshape(height,d)),axis=1)
            width += d

        if pos[0]<0:
            d = abs(pos[0])
            self.c = np.concatenate((np.zeros(d*width,dtype=np.uint8).reshape(d,width),self.c),axis=0)
            height += d
            self.offset[0] += d
            self.robot[0] += d
        elif pos[0]>=height:
            d = pos[0]-height+1
            self.c = np.concatenate((self.c,np.zeros(d*width,dtype=np.uint8).reshape(d,width)),axis=0)
            height += d



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

            # e = self.getExits()
            # n = getch()
            # if n in self.keymap:
            #     self.move(self.keymap[n])
            # if n == 'q':
            #     break

def main(stdscr):
    args = getArguments()
    lines = [[ int(y) for y in x.strip().split(',')] for x in list(filter(None, [ r for r in args.input.readlines() ] )) ]

    curses.curs_set(0)
    stdscr.clear()

    for p in lines:

        field = Field(stdscr)
        robot = Robot(p,field)
        robot.run()



if __name__ == '__main__':
    curses.wrapper(main)
