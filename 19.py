#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()

def searchRow(field, row, value):
    for x,v in enumerate(field[row]):
        if v == value:
            return (x,row, 's' if row == 0 else 'n')
    return None

def searchColumn(field, column, value):
    for y, row in enumerate(field):
        if row[column] == value:
            return (column,y, 'e' if column == 0 else 'w')
    return None


def findEntrance(field):
    result = []
    result.append(searchRow(field, 0, '|'))
    result.append(searchRow(field, len(field)-1, '|'))
    result.append(searchColumn(field, 0, '-'))
    result.append(searchColumn(field, len(field[0])-1, '-'))
    result = [x for x in result if x is not None]
    return result[0]


def getFieldElement(field, pos):
    return field[pos[1]][pos[0]]

def isInsideField(field, pos):
    return  pos[1] >= 0 and pos[1] < len(field) and pos[0] >=0 and pos[0] < len(field[0])


class WalkingProgram(object):
    movement = {
        's':( 0, 1),
        'n':( 0,-1),
        'e':( 1, 0),
        'w':(-1, 0)
    }

    movement_possibilities = {
        's':['s','e','w'],
        'n':['n','w','e'],
        'e':['e','n','s'],
        'w':['w','s','n']
    }

    def __init__(self,x,y,direction):
        self.direction  = direction
        self.pos        = (x,y)
        self.collection = []

    def __str__(self):
        return "Heading {0} Pos {1} collection{2}".format(self.direction, self.pos, self.collection)

    def computePositionInDirection(self, position, direction):
        m = self.movement[direction]
        position = (position[0]+m[0], position[1]+m[1])
        return position


    def getNextDirection(self, field):
        for d in self.movement_possibilities[self.direction]:
            p = self.computePositionInDirection(self.pos,d)
            if isInsideField(field,p) and getFieldElement(field,p) != ' ':
                return d
        return None

    def walk(self, field):

        if self.direction:
            self.pos = self.computePositionInDirection(self.pos, self.direction)

            v = getFieldElement(field,self.pos)
            if v.isalpha():
                self.collection.append(v)

            self.direction = self.getNextDirection(field)

        return self.direction is not None



if __name__ == '__main__':
    args = getArguments()

    field = [ list(x) for x in args.input.readlines() ]
    
    # for x in field:
    #     print(x)

    start = findEntrance(field)

    w = WalkingProgram(start[0],start[1],start[2])

    # print(w)
    while w.walk(field):
        # print(w)
        # input("Press Enter to continue...")
        pass

    # print(w)

    print("Found:","".join(w.collection))




