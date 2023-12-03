#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


def replace_spelled_digits( line ):
    digits = [
      ('one',1), ('two',2), ('three',3), ('four',4), ('five',5), ('six',6), ('seven',7), ('eight',8), ('nine',9),
      ('1',1), ('2',2), ('3',3), ('4',4), ('5',5), ('6',6), ('7',7), ('8',8), ('9',9)]

    found_digits = []

    i = 0
    while i < len(line):
        increment = 1
        for d in digits:
            if d[0] == line[i:i+len(d[0])]:
                found_digits.append(d[1])
                # increment = len(d[0])
                break
        i += increment
        # print(i, " ", line[i:])

    # print(found_digits)
    return found_digits


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))

    digits = [ replace_spelled_digits(line) for line in lines ]

    pairs = [ x[0]*10 + x[-1] for x in digits ]

    print( sum(pairs) )

