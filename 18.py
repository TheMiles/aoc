#!/usr/bin/python3

import argparse
import intcode as ic
from collections import defaultdict
import numpy as np
import curses
from utils.getch import getch
from utils.fields import ContentField


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

    return parser.parse_args()


def convertIntToASCII(l):
    return [ str(chr(c)) for c in l ]

def convertASCIIToInt(l):
    return [ int(ord(c)) for c in l ]


class CursesField(ContentField):

    def __init__(self, screen):
        ContentField.__init__(self,[' ', '#', '.', '@'])
        self.screen = screen
        self.size   = np.array(self.screen.getmaxyx())
        self.origin = np.array([0,0])


    def printField(self):
        l = self.getStringList()
        startingLine = min(len(l),self.origin[0])
        endLine      = min(len(l)-startingLine,self.size[0]-1)
        status.message("printField len(l) {} origin {} linespan {}".format(len(l), self.origin, [startingLine,endLine]))
        status.message("size screen {} gemerkt {} ".format(self.screen.getmaxyx(),self.size))
        for y,r in enumerate(l[startingLine:endLine]):
            startingColumn = min(len(r),self.origin[1])
            # status.message("iterate {} linelen {}, start".format(y, len(r), startingColumn))
            self.screen.addnstr(y,0,"".join(r[startingColumn:]),self.size[1])
        self.screen.refresh()

    def scroll(self, direction):
        self.origin = self.origin + direction
        self.origin = np.min([self.origin, (self.size-[1,1])],0)
        self.origin = np.max([self.origin,[0,0]],0)

        status.message("scroll {} - {} - {}".format(direction, self.origin, self.size))
        self.printField()

    # def setValue(self, pos, value):

    #     ContentField.setValue(self,pos,value)
    #     if np.greater_equal(pos,[self.h,self.w]).any():
    #         newSize = np.max([pos,[self.h,self.w]],0) + [3,3]
    #         status.message("Resize {} and {} to {} {}".format(pos, [self.h,self.w],newSize[0],newSize[1]))
    #         self.screen.resize(newSize[0],newSize[1])
    #         self.h,self.w = self.screen.getmaxyx()


class Debugger(object):

    def __init__(self, filename=None):
        self.screen   = None
        self.messages = []
        self.file     = None

        if filename is not None:
            self.file = open(filename,'w')

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def setScreen(self, screen):
        self.screen = screen
        h,w         = self.screen.getmaxyx()
        self.w      = w
        self.h      = h

    def message(self,m):
        self.messages.append(str(m))

        if self.file is not None:
            self.file.write(self.messages[-1])
            self.file.write('\n')

        if self.screen is not None:
            self.screen.clear()
            for i,t in enumerate(self.messages[-self.h:]):
                self.screen.addnstr(i,1,t, self.w)
            self.screen.refresh()

status = Debugger("log18.txt")


def main(stdscr):
    args = getArguments()
    lines = list(filter(None, [ r for r in args.input.readlines() ] ))

    curses.curs_set(0)
    stdscr.clear()

    statusWindow = curses.newwin(5, curses.COLS)
    status.setScreen(statusWindow)

    fieldWindow  = curses.newwin(curses.LINES-5, curses.COLS-5, 5, 5)
    field        = CursesField(fieldWindow)

    for y,p in enumerate(lines):
        for x,v in enumerate(p):
            field.setContent([y,x],v)


    field.printField()

    while True:
        k = getch()
        if   k == 'q': return
        elif k == 'k': field.scroll([ 1, 0])
        elif k == 'j': field.scroll([-1, 0])
        elif k == 'h': field.scroll([ 0, 1])
        elif k == 'l': field.scroll([ 0,-1])



if __name__ == '__main__':
    curses.wrapper(main)
