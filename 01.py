#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))

    digits = ['0','1','2','3','4','5','6','7','8','9']

    numbers = [ [ int(y) for y in x if y in digits] for x in lines ]

    pairs = [ x[0]*10 + x[-1] for x in numbers ]

    print( sum(pairs) )

