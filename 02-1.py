#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Find pin to toilet')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'),
                    help='file directions on keypad starting on 5')

keypad = [1,2,3,4,5,6,7,8,9]
pos = [1,1]

def addDirection(pos, dir):
    def addElement(index,value):
        pos[index] = max(0, min(2, pos[index]+value))

    if dir in ['U','D']:
        addElement(0,-1 if dir == 'U' else 1)
    elif dir in ['L','R']:
        addElement(1,-1 if dir == 'L' else 1)

args = parser.parse_args()

commands = [ x.strip() for x in args.input.readlines() ]
print(commands)
pin = 0
for c in commands:
    for dir in c:
        addDirection(pos, dir)
    pin = pin * 10 + keypad[ pos[0]*3 + pos[1] ]

print("Pin is {0}".format(pin))

