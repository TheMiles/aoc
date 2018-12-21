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

class Screen(object):

    def __init__(self, stdscr, caveWidth, caveHeight):

        curses.curs_set(0)
        self.statusWindowHeight = 5
        self.statusWindowWidth  = curses.COLS
        self.caveWindowHeight   = caveHeight + 2
        self.caveWindowWidth    = caveWidth + 2
        self.scoreWindowHeight  = curses.LINES-self.statusWindowHeight
        self.scoreWindowWidth   = 30
        self.statusWindow       = curses.newwin(self.statusWindowHeight, self.statusWindowWidth)
        self.caveWindow         = curses.newwin(self.caveWindowHeight, self.caveWindowWidth, int((curses.LINES - self.statusWindowHeight - self.caveWindowHeight)/2)+self.statusWindowHeight, int((curses.COLS -  2*self.scoreWindowWidth - self.caveWindowWidth)/2))
        self.scoreElvesWindow   = curses.newwin(self.scoreWindowHeight, self.scoreWindowWidth, self.statusWindowHeight, curses.COLS - 2*self.scoreWindowWidth)
        self.scoreGoblinsWindow = curses.newwin(self.scoreWindowHeight, self.scoreWindowWidth, self.statusWindowHeight, curses.COLS - self.scoreWindowWidth)
        stdscr.clear()

    def log(self,logText, wait=True):
        k = 'c'
        self.statusWindow.clear()
        self.statusWindow.addstr(1,1,logText)

        if wait:
            self.statusWindow.addstr(4,1,'Press key')
            k = self.statusWindow.getkey()
            self.statusWindow.addstr(4,1,'         ')
        self.statusWindow.refresh()
        return k

    def printCave(self, cave, agents, mode):

        for y,c in enumerate(cave):
            self.caveWindow.addstr(y,0, ''.join(c))

        for i,a in enumerate(agents):
            a.ord = i
            show = a.type
            if mode == 'ord':
                show = str(i)
            self.caveWindow.addstr(a.pos.y,a.pos.x,show)
        self.caveWindow.refresh()

    def updateCave(self, updates):

        for u in updates:
            self.caveWindow.addstr(u[0].y, u[0].x, u[1])
        self.caveWindow.refresh()

    def printStats(self, agents):

        def _printStats(w, agents, title):
            w.clear()

            height, width = w.getmaxyx()
            w.addstr(1,1, "{}:{:> 3}".format(title, len(agents)))

            offset = 3
            for y,a in enumerate(agents):
                if y < height - offset:
                    w.addstr(y+offset,1,str(a))

            w.refresh()

        _printStats(self.scoreElvesWindow, [a for a in agents if a.type == 'E'], "Elves")
        _printStats(self.scoreGoblinsWindow, [a for a in agents if a.type == 'G'], "Goblins")

screen = None

class Position(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __str__(self):

        return "[{},{}]".format(self.x, self.y)

    def __eq__(self, other):

        if isinstance(other,Position):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, Agent):
            return self.__eq__(other.pos)
        return NotImplemented

    def __ne__(self, other):

        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result


    def __lt__(self,other):

        if isinstance(other, Position):
            if self.y == other.y:
                return self.x < other.x
            return self.y < other.y
        elif isinstance(other, Agent):
            return self.__lt__(other.pos)
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

    def distance(self, other):

        if isinstance(other, Agent):
            return self.distance(other.pos)

        if isinstance(other, Position):
            d  = abs(self.x - other.x)
            d += abs(self.y - other.y)
            return d
        return NotImplemented


    def up(self):    return Position(self.x, self.y-1)
    def down(self):  return Position(self.x, self.y+1)
    def left(self):  return Position(self.x-1, self.y)
    def right(self): return Position(self.x+1, self.y)


class Agent(object):

    def __init__(self, x, y, t, hp=300):
        self.pos    = Position(x,y)
        self.type   = t
        self.hp     = hp
        self.damage = 3
        self.alive  = True
        self.ord    = -1


    def __str__(self):

        return "({}) {} {} HP {}".format(self.ord, self.type, str(self.pos), self.hp)


    def __eq__(self, other):

        if isinstance(other,Agent):
            return self.pos == other.pos
        elif isinstance(other, Position):
            return self.pos == other
        return NotImplemented

    def __ne__(self, other):

        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result


    def __lt__(self,other):

        if isinstance(other, Agent):
            return self.pos < other.pos
        elif isinstance(other, Position):
            return self.pos < other
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

    def distance(self, other):

        if isinstance(other, Agent):
            return self.pos.distance(other.pos)
        elif isinstance(other, Position):
            return self.pos.distance(other)
        return NotImplemented

    def getAdjacentPositions(self):

        return [self.pos.up(), self.pos.down(), self.pos.left(), self.pos.right()]


    def getAdjacentElements(self, state, filterBy=None):

        elements = [ (p,getElement(state, p)) for p in self.getAdjacentPositions() ]
        if filterBy is not None:
            if not isinstance(filterBy, list):
                filterBy = [filterBy]
            elements[:] = [ e for e in elements if e[1] in filterBy ]
        return elements


    def getAdjacentFoes(self, state, agents):

        adjacentFoePos = self.getAdjacentElements(state, ('G' if self.type == 'E' else 'E'))
        return [ a for a in agents if a in [b[0] for b in adjacentFoePos] and a.alive ]


    def filterFoes(self, agents):

        return [b for b in agents if b.type == ('G' if self.type == 'E' else 'E') and b.alive]


    def tick(self, state, agents):

        if not self.alive: return

        foes = self.getAdjacentFoes(state, agents)
        if not foes:
            self.move(state, agents)
            foes = self.getAdjacentFoes(state, agents)
        if foes:
            self.attack(state, agents)


    def move(self, state, agents):

        coloredState                  = colorCave(state, agents)
        foes                          = self.filterFoes(agents)
        foesPositions                 = getNeighbouringFields(coloredState,[f.pos for f in foes])
        reachablePositions            = getReachableFields(coloredState, self.pos, foesPositions)

        if not reachablePositions: return

        targetPosition                = filterFieldsByDistance(reachablePositions, self.pos)

        nextStepCandidates            = [p for p in self.getAdjacentPositions() if getElement(state,p) == '.']
        nextStep                      = filterFieldsByDistance(nextStepCandidates, targetPosition)

        updateList = [(self.pos,'.'),(nextStep,self.type)]
        self.pos                      = nextStep
        screen.updateCave(updateList)
        updateElements(state, updateList)


    def attack(self, state, agents):

        agentsToAttack = self.getAdjacentFoes(state, agents)
        if agentsToAttack:
            agentsToAttackSorted = sorted(agentsToAttack, key=lambda x: x.hp)
            agentsToAttackSorted[:] = [ a for a in agentsToAttackSorted if a.hp == agentsToAttackSorted[0].hp ]
            agentsToAttackSorted = sorted(agentsToAttackSorted, key= lambda x: x.pos)

            agentToAttack = agentsToAttackSorted[0]
            agentToAttack.hit(state, self.damage)

    def hit(self, state, damage):

        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            updateList = [(self.pos,'.')]
            screen.updateCave(updateList)
            updateElements(state, updateList)




def getElement(state, pos):

    if pos.y < 0 or pos.y >= len(state):
        return '#'

    if pos.x < 0 or pos.x >= len(state[pos.y]):
        return '#'

    return state[pos.y][pos.x]

def updateElements(state, updates):

    for u in updates:
        p = u[0]

        if p.x < 0 or p.y < 0 or p.y >= len(state) or p.x >= len(state[p.y]):
            return
        state[p.y][p.x] = u[1]





def colorizeField(cave,pos, color):

    if getElement(cave,pos) != '.':
        return

    cave[pos.y][pos.x] = color

    colorizeField(cave,pos.up(),color)
    colorizeField(cave,pos.down(),color)
    colorizeField(cave,pos.left(),color)
    colorizeField(cave,pos.right(),color)


def colorCave(cave,agents):
    colors = []
    for c in cave:
        colors.append(c[:])
    colorCount = 0

    for a in agents:
        if a.alive:
            colors[a.pos.y][a.pos.x] = a.type

    for y,c in enumerate(colors):
        line = []
        for x,e in enumerate(c):
            if e == '.':
                colorizeField(colors, Position(x,y), str(colorCount))
                colorCount += 1

    return colors

def getNeighbouringFields(state, positions):

    def checkAndAddNeighbour(state, pos, l):
        e = getElement(state,pos)
        if e not in ['#','G','E']:
            l.append(pos)

    neighbours = []
    for p in positions:
        checkAndAddNeighbour(state, p.up(), neighbours)
        checkAndAddNeighbour(state, p.down(), neighbours)
        checkAndAddNeighbour(state, p.left(), neighbours)
        checkAndAddNeighbour(state, p.right(), neighbours)

    return neighbours


def getReachableFields(state, position, targets):

    n      = getNeighbouringFields(state,[position])
    colors = set([ getElement(state, p) for p in n ])
    return [t for t in targets if getElement(state,t) in colors]


def filterFieldsByDistance(positions, target):

            positionsSorted  = sorted(positions, key=lambda b: target.distance(b))
            d                = target.distance(positionsSorted[0])
            positionsClosest = sorted([b for b in positionsSorted if target.distance(b) == d])
            return positionsClosest[0]


def main(stdscr):
    global screen
    args         = getArguments()
    initialState = list(filter(None, [ x.rstrip() for x in args.input.readlines() ] ))
    width        = max([len(x) for x in initialState])
    height       = len(initialState)

    cave    = []
    agents  = []

    for y,l in enumerate(initialState):
        c = []
        for x,e in enumerate(l):
            if e == '#' or e == '.':
                c.append(e)
            elif e == 'G' or e == 'E':
                c.append('.')
                agents.append(Agent(x,y,e))
        cave.append(c)

    mode = 'names'
    screen = Screen(stdscr, width, height)
    screen.printCave(cave,agents,mode)

    iterations = 0

    while True:

        agents.sort()
        screen.printStats(agents)

        for a in agents:

            a.tick(cave, agents)

        elvesLeft = [a for a in agents if a.type == 'E' and a.alive]
        goblinsLeft = [a for a in agents if a.type == 'G' and a.alive]

        iterations += 1

        if not elvesLeft or not goblinsLeft:
            s = 0
            for a in agents:
                s += a.hp if a.alive else 0
            screen.log("It's over {} Elves, {} Goblins, {} HPs {} iterations {} score".format(len(elvesLeft), len(goblinsLeft), s, iterations, s*iterations))
            break

        # k = screen.log("Select 'q': Quit, 'n': Agent names, 'o': agent numbers")
        # if k == 'q':
        #     break
        # if k == 'n':
        #     mode = 'names'
        # elif k == 'o':
        #     mode = 'ord'

        time.sleep(0.3)


if __name__ == '__main__':
    curses.wrapper(main)