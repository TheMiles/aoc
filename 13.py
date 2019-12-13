#!/usr/bin/python3

import argparse
import intcode as ic
from collections import defaultdict
import numpy as np
from PIL import Image


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

    return parser.parse_args()



if __name__ == '__main__':
    args = getArguments()
    lines = [[ int(y) for y in x.strip().split(',')] for x in list(filter(None, [ r for r in args.input.readlines() ] )) ]

    for p in lines:

        inBuffer  = ic.Fifo()
        outBuffer = ic.Fifo()
        cpu       = ic.CPU(p, inBuffer, outBuffer)

        cpu.run()

        o = np.array(outBuffer.buffer).reshape(int(len(outBuffer.buffer)/3),3)

        print(len(list(filter(lambda x: x==2,o[:,2]))))


