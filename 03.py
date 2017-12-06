#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Spreadsheet')
parser.add_argument('input', type=int)


def getRingNumber(coordinate):
    return abs(coordinate[0]) if abs(coordinate[0]) > abs(coordinate[1]) else abs(coordinate[1])

def isCorner(coordinate):
    return abs(coordinate[0]) == abs(coordinate[1])


def getHeading(coordinate):
    if abs(coordinate[0]) >= abs(coordinate[1]):
        if coordinate[0] == -coordinate[1]:
            return 3 if coordinate[0]>= 0 else 1
        else:
            return 0 if coordinate[0] >= 0 else 2
    else:
        return 1 if coordinate[1] >= 0 else 3


def getLinearIndex(coordinate):
    r = getRingNumber(coordinate)
    if r == 0: return 0

    linearOffset = ((r-1)*2+1)**2

    heading = getHeading(coordinate)
    linearOffset += heading*r*2


    subIndex  = coordinate[0] if heading % 2 == 1 else coordinate[1]
    subIndex *= 1 if (heading == 0 or heading == 3) else -1
    subIndex += r-1

    return linearOffset + subIndex

def getNextCoordinate(coordinate):
    h = getHeading(coordinate)
    c = isCorner(coordinate)

    if h == 3 or (h == 2 and c):
        return (coordinate[0]+1,coordinate[1])
    if h == 2 or (h == 1 and c):
        return (coordinate[0],  coordinate[1]-1)
    if h == 1 or (h == 0 and c):
        return (coordinate[0]-1,coordinate[1])
    else:
        return (coordinate[0],  coordinate[1]+1)



class SpiralMemory:

    def __init__(self):
        self.data = [1]
        self.initializedRings = 0

    def getValue(self, coordinate):
        r = getRingNumber(coordinate)

        if r > self.initializedRings: return 0

        i = getLinearIndex(coordinate)
        return self.data[i]

    def setValue(self, coordinate, value):
        r = getRingNumber(coordinate)

        while self.initializedRings < r:
            self.initializedRings += 1
            self.data.extend([0]*self.initializedRings*8)

        self.data[getLinearIndex(coordinate)] = value


def getCorners(v):
    if v < 1: return None

    l = (v*2+1)
    c = [l**2]
    for x in range(3):
        c.append(c[-1]-l+1)
    return c

def getMiddles(v):
    c = getCorners(v)
    if c:
        return [x-v for x in getCorners(v)]
    return [1]

def findCircle(v):
    i = 0
    while v > (i*2+1)**2:
        i += 1
    return i


neighbours = [(-1, 1), (0, 1), (1, 1),
              (-1, 0),         (1, 0),
              (-1,-1), (0,-1), (1,-1)]

args = parser.parse_args()

sm = SpiralMemory()
coordinate = (1,0)

value = 0

while value < args.input:
    value = 0
    for neighbour in neighbours:
        nCoordinate = [sum(x) for x in zip(coordinate,neighbour)]
        value += sm.getValue(nCoordinate)
    sm.setValue(coordinate, value)
    coordinate = getNextCoordinate(coordinate)

print(sm.data)

