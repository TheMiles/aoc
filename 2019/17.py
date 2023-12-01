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


def convertIntToASCII(l):
    return [ str(chr(c)) for c in l ]

def convertASCIIToInt(l):
    return [ int(ord(c)) for c in l ]


class ScaffoldField(Field):

    def __init__(self, screen):
        Field.__init__(self)
        self.screen = screen

    def printField(self):
        l = self.getStringList()
        for y,r in enumerate(l):
            self.screen.addstr(y,0,"".join(convertIntToASCII(r)))
        self.screen.refresh()


def main(stdscr):
    args = getArguments()
    lines = [[ int(y) for y in x.strip().split(',')] for x in list(filter(None, [ r for r in args.input.readlines() ] )) ]

    curses.curs_set(0)
    stdscr.clear()

    statusWindow = curses.newwin(5, curses.COLS)
    fieldWindow  = curses.newwin(curses.LINES-5, curses.COLS-5, 5, 5)

    for p in lines:

        input  = ic.Fifo()
        output = ic.Fifo()
        cpu    = ic.CPU(p, input, output)

        cpu.run()

        scaffolds = ScaffoldField(fieldWindow)
        pos       = np.array([0,0])
        while not output.empty():
            c = output.pop()
            if c == 10:
                pos = np.array([pos[0]+1,0])
                continue
            scaffolds.setValue(pos,c)
            pos[1] += 1

        scaffolds.printField()

        sum = 0
        for y in range(1, scaffolds.getHeight()-2):
            for x in range(1,scaffolds.getWidth()-2):
                p = np.array([y,x])
                a = [ v[1] for v in scaffolds.getAdjacentValues(p)]
                a.append(scaffolds.getValue(p))
                if all([ x==ord('#') for x in a ]):
                    sum += x*y

        statusWindow.addstr(2,3,str(sum))
        statusWindow.refresh()
        getch()



if __name__ == '__main__':
    curses.wrapper(main)
