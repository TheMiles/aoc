#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))

    sleeptable = dict()
    for line in lines:

        polymers = [ x for x in line ]
        edited   = True
        while edited:
            edited = False

            for i in range(len(polymers)-1):
                if polymers[i].upper() == polymers[i+1].upper() and polymers[i] != polymers[i+1]:
                    del polymers[i:i+2]
                    edited = True
                    break

        print("Polymer is {0} long".format(len(polymers)))
