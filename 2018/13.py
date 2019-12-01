#!/usr/bin/python3

import argparse
import re
from collections import defaultdict
import curses
import time


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-s','--step', type=int, default=0)
    return parser.parse_args()

class Car(object):

    Directions = ['^', '>', 'v', '<']

    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.d = self.Directions.index(dir)
        self.crossDecision = [self.left, self.ident, self.right]
        self.crashed = False


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

    def move(self, w, track):

        if self.crashed:
            return

        delta = [
            ( 0,-1), # '^'
            ( 1, 0), # '>'
            ( 0, 1), # 'v'
            (-1, 0)  # '<'
        ]

        x = self.x + delta[self.d][0]
        y = self.y + delta[self.d][1]

        w.addstr(self.y, self.x, getTrackElement(track,self.x,self.y))
        w.addstr(y, x, str(self))


        if not coordinateIsInBounds(track, x, y):
            ff = open("bla_move", 'a')
            ff.write("Problem car [{},{}] out of bounds, old trackElement {} old coordinate [{},{}] {}\n".format(x,y,getTrackElement(track, self.x, self.y),self.x, self.y, str(self)))
            ff.close


        self.x = x
        self.y = y
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

def coordinateIsInBounds(track, x, y):

    if x < 0 or y < 0: return False

    width, height = getWidthHeight(track)
    if x >= width or y >= height: return False
    return True


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

    upConnection    = 1 if getTrackElement(state,x,  y-1) in ['|','+','v','^'] else 0
    rightConnection = 2 if getTrackElement(state,x+1,y)   in ['-','+','<','>'] else 0
    downConnection  = 4 if getTrackElement(state,x,  y+1) in ['|','+','v','^'] else 0
    leftConnection  = 8 if getTrackElement(state,x-1,y)   in ['-','+','<','>'] else 0

    upConnection    = 1 if getTrackElement(state,x,  y-1) == '\\' and getTrackElement(state, x-1, y-1) in ['-','\\','/','+','<','>'] else upConnection
    rightConnection = 2 if getTrackElement(state,x+1,y)   == '\\' and getTrackElement(state, x+1, y+1) in ['|','\\','/','+','v','^'] else rightConnection
    downConnection  = 4 if getTrackElement(state,x,  y+1) == '\\' and getTrackElement(state, x+1, y+1) in ['-','\\','/','+','<','>'] else downConnection
    leftConnection  = 8 if getTrackElement(state,x-1,y)   == '\\' and getTrackElement(state, x-1, y-1) in ['|','\\','/','+','v','^'] else leftConnection

    upConnection    = 1 if getTrackElement(state,x,  y-1) == '/'  and getTrackElement(state, x+1, y-1) in ['-','\\','/','+','<','>'] else upConnection
    rightConnection = 2 if getTrackElement(state,x+1,y)   == '/'  and getTrackElement(state, x+1, y-1) in ['|','\\','/','+','v','^'] else rightConnection
    downConnection  = 4 if getTrackElement(state,x,  y+1) == '/'  and getTrackElement(state, x-1, y+1) in ['-','\\','/','+','<','>'] else downConnection
    leftConnection  = 8 if getTrackElement(state,x-1,y)   == '/'  and getTrackElement(state, x-1, y+1) in ['|','\\','/','+','v','^'] else leftConnection

    return trackConnectionMapping[upConnection + rightConnection + downConnection + leftConnection]


def getWidthHeight(state):

    width     = max([len(x) for x in state])
    height    = len(state)
    return width, height


def printTrack(w, track, cars):

    width, height = getWidthHeight(track)

    for i,s in enumerate(track):
        w.addstr(i,0,s)

    for c in cars:
        if c.x >= width or c.y >= height or c.x < 0 or c.y < 0:
            ff = open("bla", 'a')
            ff.write("Problem car [{},{}] out of bounds [{},{}]\n".format(c.x,c.y,width,height))
            ff.close
            continue
        w.addstr(c.y, c.x, str(c))

    w.refresh()



def main(stdscr):
    args         = getArguments()
    initialState = list(filter(None, [ x.rstrip() for x in args.input.readlines() ] ))
    width        = max([len(x) for x in initialState])
    height       = len(initialState)

    curses.curs_set(0)
    statusWindow = curses.newwin(3, curses.COLS)
    trackWindow  = curses.newwin(height+1, width+1, 3, 2)
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

    printTrack(trackWindow, track, cars)

    i = 0
    running = True
    while running:
        i += 1
        statusWindow.addstr(1,0, "Iteration {:> 6} remaining cars {}".format(i,len(cars)))

        if args.step and i > args.step:
            k = statusWindow.getkey()
            if k == 'q':
                running = False

        for c in cars:
            c.move(trackWindow, track)

            sameCars = [d for d in cars if d == c]
            if len(sameCars) >= 2:
                statusWindow.addstr(1,0, "Iteration {:> 6} crash at coordinate [{},{}]".format(i,c.x,c.y))
                # statusWindow.getkey()
                for d in sameCars:
                    d.crashed = True

        cars[:] = [c for c in cars if not c.crashed]
        cars.sort()

        offtrackCars = [c for c in cars if not coordinateIsInBounds(track,c.x,c.y)]
        if offtrackCars:
            statusWindow.addstr(1,0, "Iteration {:> 6}  car left at [{},{}]".format(i,offtrackCars[0].x,offtrackCars[0].y))
            statusWindow.getkey()
            running = False


        if len(cars) == 1:
            statusWindow.addstr(1,0, "Iteration {:> 6} last remaining car at [{},{}]".format(i,cars[0].x,cars[0].y))
            statusWindow.getkey()
            running = False

        if not cars:
            statusWindow.addstr(1,0, "Iteration {:> 6} no more remaining cars".format(i))
            statusWindow.getkey()
            running = False

        statusWindow.refresh()
        trackWindow.refresh()
        time.sleep(0.01)



if __name__ == '__main__':
    curses.wrapper(main)