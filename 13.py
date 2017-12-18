#!/usr/bin/python3

import argparse
import time

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
    def __init__(self, start_time, position):
        self.start_time  = start_time
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
santas = []
number_of_layers = 0
for line in lines:
    layer_info = [ int(x.strip()) for x in line.split(":") ]
    layers.append(Scanner(layer_info[0],layer_info[1]))
    if number_of_layers < layer_info[0]: number_of_layers = layer_info[0]

waiting_time = None
start_time = 0

search_time = time.time()
notification_time = search_time

while not waiting_time:
    santas.append(Santa(start_time,0))
    start_time += 1

    for x in santas:
        x.advance()
        if x.layer > number_of_layers:
            waiting_time = x.start_time
            break

    checkCollision(layers, santas)

    for x in santas:
        if x.caughtList:
            santas.remove(x)

    for x in layers: x.advance()


    if (time.time() - notification_time) > 10:
        print("Still alive, running for {1} seconds, checking {0}".format(start_time, int(time.time() - search_time)))
        notification_time = time.time()

print("You should wait", waiting_time, "picoseconds")
