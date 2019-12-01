#!/usr/bin/python3

import argparse
import re
import sys
from collections import defaultdict

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('-g','--gridsize', default=300, type=int)
    parser.add_argument('-s','--serialnumber', default=5791, type=int)
    parser.add_argument('-c','--checkCell', nargs=2, type=int)
    parser.add_argument('-p','--printCell', nargs=2, type=int)
    parser.add_argument('-w','--areawidth', type=int)
    return parser.parse_args()




def computeFuelLevel(x, y, serial):

    rackID = x + 10
    powerLevel = rackID * y
    powerLevel += serial
    powerLevel *= rackID

    if powerLevel < 100:
        return 0

    return int(str(powerLevel)[-3]) - 5


def getIndex(gridsize, x, y):

    if x < 1 or y < 1 or x > gridsize or y > gridsize:
        return None

    return (y-1) * gridsize + (x-1)


def sum(field, gridsize, x, y, size):

    x -= 1
    y -= 1

    indexLeftTop     = getIndex(gridsize, x,      y)
    indexRightTop    = getIndex(gridsize, x+size, y)
    indexLeftBottom  = getIndex(gridsize, x,      y+size)
    indexRightBottom = getIndex(gridsize, x+size, y+size)


    valueLeftTop     = field[indexLeftTop] if indexLeftTop is not None else 0
    valueRightTop    = field[indexRightTop] if indexRightTop is not None else 0
    valueLeftBottom  = field[indexLeftBottom] if indexLeftBottom is not None else 0
    valueRightBottom = field[indexRightBottom] if indexRightBottom is not None else 0

    # print("[{},{}] lt {}>{} rt {}>{} lb {}>{} rb {}>{}".format(x,y,indexLeftTop,valueLeftTop,indexRightTop,valueRightTop,indexLeftBottom,valueLeftBottom,indexRightBottom,valueRightBottom))
    return valueRightBottom - valueLeftBottom - valueRightTop + valueLeftTop


if __name__ == '__main__':
    args         = getArguments()

    gridelements = args.gridsize * args.gridsize
    fuelCells    = [ computeFuelLevel(x,y,args.serialnumber) for y in range(1,args.gridsize+1) for x in range(1,args.gridsize+1) ]
    summedArea   = [None for i in range(len(fuelCells))]

    for y in range(1,args.gridsize+1):
        for x in range(1,args.gridsize+1):
            indexTarget = getIndex(args.gridsize, x,   y)
            indexUp     = getIndex(args.gridsize, x,   y-1)
            indexLeft   = getIndex(args.gridsize, x-1, y)
            indexUpLeft = getIndex(args.gridsize, x-1, y-1)

            valueTarget = fuelCells[indexTarget]
            valueUp     = summedArea[indexUp]     if indexUp is not None else 0
            valueLeft   = summedArea[indexLeft]   if indexLeft is not None else 0
            valueUpLeft = summedArea[indexUpLeft] if indexUpLeft is not None else 0

            # print("[{},{}] ul {}>{} u {}>{} l {}>{} t {}>{}".format(x,y,indexUpLeft,valueUpLeft,indexUp,valueUp,indexLeft,valueLeft,indexTarget,valueTarget))
            summedArea[indexTarget] = valueTarget + valueUp + valueLeft - valueUpLeft


    if args.printCell:
        x = max(1, min(args.printCell[0]-2, args.gridsize-4))
        y = max(1, min(args.printCell[1]-2, args.gridsize-4))

        computeFuelLevel(args.printCell[0],args.printCell[1],args.serialnumber)

        for j in range(y, y+5):
            index = getIndex(args.gridsize, x, j)
            print(' '.join(['{:> 4}'.format(c) for c in fuelCells[index:index+5]]))
        print()


    if args.checkCell:
        s = sum(summedArea, args.gridsize, args.checkCell[0], args.checkCell[1], 3)
        print("The Cell [{0},{1}] has sum {2}".format(args.checkCell[0], args.checkCell[1],s))
        sys.exit()


    bestCell= (-46000, -1, -1, -1)

    for y in range(1,args.gridsize+1):
        for x in range(1,args.gridsize+1):
            if args.areawidth:
                if x > args.gridsize-args.areawidth or y > args.gridsize-args.areawidth:
                    continue

                s = sum(summedArea, args.gridsize, x, y, args.areawidth)
                if s is not None and s > bestCell[0]:
                    bestCell = (s,x,y,args.areawidth)

            else:
                fieldsLeft = args.gridsize - max(x,y)
                for n in range(1,fieldsLeft):
                    s = sum(summedArea, args.gridsize, x, y, n)
                    if s is not None and s > bestCell[0]:
                        bestCell = (s,x,y,n)

    print("The best cell is [{1},{2}] which has load of {0} and field size of {3}".format(bestCell[0],bestCell[1],bestCell[2], bestCell[3]))


