#!/usr/bin/python3

import argparse
import intcode as ic
from collections import defaultdict
import numpy as np


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

    return parser.parse_args()

class Field(object):

    def __init__(self):
        self.content = {
            0: ' ',
            1: '#',
            2: '.',
            3: 'O'
        }

        self.c      = np.array([[0]])
        self.offset = np.array([0,0])
        self.robot  = np.array([0,0])


    def setRobot(self, pos):
        self.robot = pos+self.offset

    def printField(self):
        for y in range(self.c.shape[0]):
            for x in range(self.c.shape[1]):
                p = np.array([y,x])
                if np.equal(self.robot, p).all():
                    print('R',end='')
                else:
                    print(self.getContent(p), end='')
            print()
        print()


    def getContent(self, pos):
        return self.content[self.getValue(pos)]

    def setContent(self, pos, content):
        print("setContent", pos, content, self.c.shape)
        for key, value in self.content.items():
            if value == content:
                self.setValue(pos,key)
                return


    def getValue(self, pos):
        p = pos+self.offset

        if np.less(p,0).any() or np.greater_equal(p,self.c.shape).any: return 0
        return self.c[tuple(p)]

    def setValue(self, pos, value):
        p = pos+self.offset

        print("setValue orig {} offset {} effective {} shape {} value {}".format(pos,self.offset,p,self.c.shape,value))

        if np.less(p,0).any() or np.greater_equal(p,self.c.shape).any: self.growField(p)
        self.c[tuple(p)] = value

    def growField(self,pos):

        height, width = self.c.shape
        if pos[1]<0:
            print("Grow width before", self.c)
            d = abs(pos[1])
            self.c = np.concatenate((np.zeros(d*height,dtype=np.uint8).reshape(height,d),self.c),axis=1)
            width += d
            self.offset[1] += d
            self.robot[1] += d
        elif pos[1]>=width:
            print("Grow width after", self.c)
            d = pos[1]-width+1
            self.c = np.concatenate((self.c,np.zeros(d*height,dtype=np.uint8).reshape(height,d)),axis=1)
            width += d

        if pos[0]<0:
            print("Grow height before", self.c)
            d = abs(pos[0])
            self.c = np.concatenate((np.zeros(d*width,dtype=np.uint8).reshape(d,width),self.c),axis=0)
            height += d
            self.offset[0] += d
            self.robot[0] += d
        elif pos[1]>=width:
            print("Grow height after", self.c)
            d = pos[1]-width+1
            self.c = np.concatenate((self.c,np.zeros(d*width,dtype=np.uint8).reshape(d,width)),axis=0)
            height += d

        print("after grow",self.c.shape, self.c)



class Robot(object):

    def __init__(self, program):
        self.input  = ic.Fifo()
        self.output = ic.Fifo()
        self.cpu    = ic.CPU(program, self.input, self.output)

        self.directions = {
            'N': 1,
            'S': 2,
            'W': 3,
            'E': 4
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

        self.field  = Field()
        self.pos    = np.array([0,0])


    def move(self, direction):
        self.input.push(self.directions[direction])
        self.cpu.run()
        result = self.output.pop()

        print("From {} starting {}".format(self.pos, direction))

        nextPos = self.pos+self.deltaPos[direction]
        if result == 0:
            self.field.setContent(nextPos,'#')
        elif result == 1:
            self.field.setContent(nextPos,'.')
            self.pos = nextPos
            self.Field.setRobot(self.pos)
        elif result == 2:
            self.field.setContent(nextPos,'O')
            self.pos = nextPos

        print(" result: {} new pos {}".format(result,self.pos))


    def run(self):

        while True:
            self.field.printField()
            n = input("Where next: ")
            if n in self.keymap:
                self.move(self.keymap[n])
            if n == 'q':
                break



if __name__ == '__main__':
    args = getArguments()
    lines = [[ int(y) for y in x.strip().split(',')] for x in list(filter(None, [ r for r in args.input.readlines() ] )) ]

    for p in lines:

        robot = Robot(p)
        robot.run()


