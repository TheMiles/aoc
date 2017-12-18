#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))


class Scanner(object):
    def __init__(self, layer, rangeLength):
        self.rangeLength = rangeLength
        self.layer       = layer
        self.position    = 0
        self.direction   = 1

    def advance(self):
        self.position += self.direction

        if self.position == self.rangeLength-1:
            self.direction = -1
        elif self.position == 0:
            self.direction = 1

class Santa(object):
    def __init__(self, startTime, position):
        self.startTime  = startTime
        self.layer      = -1
        self.position   = position
        self.caughtList = []

    def advance(self):
        self.layer    += 1

    def severity(self):
        s = 0
        for l,r in self.caughtList:
            s += l * r
        return s


def checkCollision(scanner, santa):
    if type(scanner) is list:
        for x in scanner:
            checkCollision(x, santa)
        return

    if type(santa) is list:
        for x in santa:
            checkCollision(scanner, x)
        return

    if scanner.layer == santa.layer and scanner.position == santa.position:
        santa.caughtList.append((scanner.layer,scanner.rangeLength))




args = parser.parse_args()

lines = [ x.strip() for x in args.input.readlines() ]

layers = []
number_of_layers = 0
for line in lines:
    layer_info = [ int(x.strip()) for x in line.split(":") ]
    layers.append(Scanner(layer_info[0],layer_info[1]))
    if number_of_layers < layer_info[0]: number_of_layers = layer_info[0]

s = Santa(0,0)

while s.layer <= number_of_layers:

    s.advance()
    checkCollision(layers, s)
    for x in layers: x.advance()


print(s.severity())
