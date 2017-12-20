#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('-r','--range', type=int, default=2017)
    parser.add_argument('-s','--steps', type=int, default=363)
    return parser.parse_args()

class CircularBuffer(object):
    def __init__(self):
        self.buffer = [0]
        self.position = 0
        self.length = 1

    def advance(self,steps):

        new_position = self.position + steps

        if new_position >= self.length:
            new_position %= self.length

        self.position = new_position

    def insert(self, value):
        self.position += 1
        self.length   += 1
        self.buffer    = self.buffer[:self.position] + [value] + self.buffer[self.position:]

    def getNextElement(self, pos=None):
        if pos is None:
            pos = self.position

        read_position = pos + 1

        if read_position == self.length:
            read_position = 0

        return self.buffer[read_position]

class TruncatedCircularBuffer(CircularBuffer):
    def __init__(self, max_length):
        CircularBuffer.__init__(self)
        self.max_length = max_length

    def insert(self,value):
        self.position += 1
        self.length   += 1

        if self.position < self.max_length:
            self.buffer = (self.buffer[:self.position] + [value] + self.buffer[self.position:])[:self.max_length]



if __name__ == '__main__':
    args = getArguments()

    b = TruncatedCircularBuffer(2)

    for v in range(1,args.range):
        b.advance(args.steps)
        b.insert(v)

    print("The second element is", b.getNextElement(0))

