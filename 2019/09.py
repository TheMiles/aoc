#!/usr/bin/python3

import argparse
import intcode as ic
def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'), nargs='?')
    parser.add_argument('-d', '--direct', type=str)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-s', '--stepmode', action='store_true')


    return parser.parse_args()


if __name__ == '__main__':
    args = getArguments()
    lines = [args.direct] if args.direct else list(filter(None, [ x for x in args.input.readlines() ] ))
    lines = [[ int(y) for y in x.strip().split(',')] for x in lines ]

    for p in lines:

        # print("Trying", p)

        c = ic.CPU(p)
        c.setStepMode(args.stepmode)
        c.setVerbose(args.verbose)
        c.run()

