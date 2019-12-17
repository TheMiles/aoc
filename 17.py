#!/usr/bin/python3

import argparse
import intcode as ic
from collections import defaultdict
import numpy as np
from utils.getch import getch
from utils.fields import ContentField


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

    return parser.parse_args()


def getCross(scaffolds, pos):
    l = [
        scaffolds[pos[0]][pos[1]],
        scaffolds[pos[0]-1][pos[1]],
        scaffolds[pos[0]+1][pos[1]],
        scaffolds[pos[0]][pos[1]-1],
        scaffolds[pos[0]][pos[1]+1]
    ]
    return l



def main():
    args = getArguments()
    lines = [[ int(y) for y in x.strip().split(',')] for x in list(filter(None, [ r for r in args.input.readlines() ] )) ]

    for p in lines:

        input  = ic.Fifo()
        output = ic.Fifo()
        cpu    = ic.CPU(p, input, output)

        cpu.run()

        scaffolds = []
        l = []
        while not output.empty():
            c = output.pop()
            if c == 10:
                scaffolds.append(l)
                l = []
                continue
            l.append(str(chr(c)))

        for l in scaffolds:
            print("".join(l))

        sum = 0
        for y in range(1, len(scaffolds)-2):
            for x in range(1,len(scaffolds[0])-2):
                c = getCross(scaffolds, (y,x))
                if all([ x=='#' for x in c ]):
                    sum += x*y
        print(sum)



if __name__ == '__main__':
    main()
