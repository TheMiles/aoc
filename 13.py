#!/usr/bin/python3

import argparse
import re
from collections import defaultdict
import curses
import time


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()

class Car(object):

    Directions = ['^', '>', 'v', '<']

    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.d = self.Directions.index(dir)
        self.crossDecision = [self.left, self.ident, self.right]


    def __str__(self):

        return self.Directions[self.d]


    def __eq__(self, other):

        if isinstance(other,Car):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):

        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result


    def __lt__(self,other):

        if isinstance(other, Car):
            if self.y == other.y:
                return self.x < other.x
            return self.y < other.y
        return NotImplemented

    def __le__(self, other):

        result = self.__lt__(other)
        if result is NotImplemented:
            return result
        return result or self.__eq__(other)


    def __gt__(self, other):

        result = self.__le__(other)
        if result is NotImplemented:
            return result
        return not result


    def __ge__(self, other):

        result = self.__lt__(other)
        if result is NotImplemented:
            return result
        return not result

    def ident(self):
        pass

    def right(self):
        self.d = (self.d + 1) % len(self.Directions)

    def left(self):
        if self.d == 0: self.d = len(self.Directions)
        self.d -= 1

    def cross(self):
        f = self.crossDecision[0]
        self.crossDecision = self.crossDecision[1:] + [f]
        f()

    def move(self,track):

        delta = [
            ( 0,-1), # '^'
            ( 1, 0), # '>'
            ( 0, 1), # 'v'
            (-1, 0)  # '<'
        ]

        self.x = self.x + delta[self.d][0]
        self.y = self.y + delta[self.d][1]

        t = getTrackElement(track, self.x, self.y)

        #  self.Directions = ['^', '>', 'v', '<']
        if t == '+':
            self.cross()
        elif t == '\\':
            turns = [ self.left, self.right, self.left, self.right ]
            f = turns[self.d]
            f()
        elif t == '/':
            turns = [ self.right, self.left, self.right, self.left ]
            f = turns[self.d]
            f()



def getTrackElement(track, x, y):

    if y < 0 or y >= len(track):
        return ' '

    if x < 0 or x >= len(track[y]):
        return ' '

    return track[y][x]


car = ['^', 'v', '>', '<']
trackConnectionMapping = {
    0:  ' ',
    1:  '|',
    2:  '-',
    3:  '\\',
    4:  '|',
    5:  '|',
    6:  '/',
    7:  '+',
    8:  '-',
    9:  '/',
    10: '-',
    11: '+',
    12: '\\',
    13: '+',
    14: '+',
    15: '+'
}

def getRealTrackElement(state,x,y):

    trackElement = getTrackElement(state,x,y)

    if trackElement not in car:
        return trackElement

    upConnection    = 1 if getTrackElement(state,x,  y-1) in ['|','\\','/','+','v','^'] else 0
    rightConnection = 2 if getTrackElement(state,x+1,y)   in ['-','\\','/','+','<','>'] else 0
    downConnection  = 4 if getTrackElement(state,x,  y+1) in ['|','\\','/','+','v','^'] else 0
    leftConnection  = 8 if getTrackElement(state,x-1,y)   in ['-','\\','/','+','<','>'] else 0

    return trackConnectionMapping[upConnection + rightConnection + downConnection + leftConnection]


def getWidthHeight(state):

    width     = max([len(x) for x in state])
    height    = len(state)
    return width, height


def printTrack(w, track, cars):

    for i,s in enumerate(track):
        w.addstr(i,0,s)

    for c in cars:
        w.addstr(c.y, c.x, str(c))

    w.refresh()



def main(stdscr):
    args         = getArguments()
    initialState = list(filter(None, [ x.rstrip() for x in args.input.readlines() ] ))
    width        = max([len(x) for x in initialState])
    height       = len(initialState)

    curses.curs_set(0)
    statusWindow = curses.newwin(3, curses.COLS)
    trackWindow  = curses.newwin(height, width, 3, 2)
    stdscr.clear()


    track = []
    cars  = []

    for y, line in enumerate(initialState):
        l = []
        for x, c in enumerate(line):
            l.append(getRealTrackElement(initialState,x,y))
            if c in car:
                cars.append(Car(x,y,c))
        track.append(''.join(l))

    def updateWindows(log):
        printTrack(trackWindow, track, cars)
        statusWindow.addstr(1,0, log)
        statusWindow.refresh()
        stdscr.refresh()


    i = 0
    running = True
    while running:
        updateWindows("Iteration {:> 6} ".format(i))

        # k = stdscr.getkey()
        # if k == 'q':
        #     running = False

        i += 1
        for c in cars:
            c.move(track)

            sameCars = [d for d in cars if d == c]
            if len(sameCars) >= 2:
                updateWindows("Iteration {:> 6} crash at coordinate [{},{}]".format(i,c.x,c.y))
                stdscr.getkey()
                running = False
                break
        cars.sort()
        time.sleep(0.1)







if __name__ == '__main__':
    curses.wrapper(main)