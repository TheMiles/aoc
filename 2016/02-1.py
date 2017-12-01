#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Find pin to toilet')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'),
                    help='file directions on keypad starting on 5')

keypad = ['1','2','3','4','5','6','7','8','9','A','B','C','D']
shiftval = [2,5,6,7,10]
pos = [0,-2]

def addDirection(pos, dir):
    def addElement(index,value):
        global pos
        tmp = list(pos)
        tmp[index] = pos[index]+value
        if sum([abs(x) for x in tmp]) <= 2:
            pos = tmp

    if dir in ['U','D']:
        addElement(0,-1 if dir == 'U' else 1)
    elif dir in ['L','R']:
        addElement(1,-1 if dir == 'L' else 1)

def getKey(pos):
    def computeIndex(pos):
        i = [x+2 for x in pos]
        index = i[0]*5 + i[1]
        shift = shiftval[i[0]]
        return index - shift

    return keypad[ computeIndex(pos) ]

args = parser.parse_args()

commands = [ x.strip() for x in args.input.readlines() ]
pin = ''
for c in commands:
    for dir in c:
        addDirection(pos, dir)
    pin += getKey(pos)

print("Pin is {0}".format(pin))

