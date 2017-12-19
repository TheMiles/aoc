#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-r','--range', type=int, default=40000000)
    return parser.parse_args()


class Generator(object):
    def __init__(self,factor,initialValue, criteria):
        self.factor   = int(factor)
        self.value    = int(initialValue)
        self.divisor  = 2147483647
        self.criteria = criteria

    def getNextValue(self):
        while True:
            self.value = (self.value * self.factor) % self.divisor
            if self.criteria(self.value):
                break

        return self.value

def getBin(v):
    return str(bin(v)[2:])

if __name__ == '__main__':
    args = getArguments()

    lines = [ x.strip().split()[-1] for x in args.input.readlines() ]
    a = Generator(16807,lines[0], lambda x: x % 4 == 0)
    b = Generator(48271,lines[1], lambda x: x % 8 == 0)

    matching_results = 0
    for i in range(args.range):
        aBin = getBin(a.getNextValue())
        bBin = getBin(b.getNextValue())

        if aBin[-16:] == bBin[-16:]:
            matching_results += 1


    print("There are",matching_results,"matching results")

