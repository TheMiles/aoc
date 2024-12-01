#!/usr/bin/python3

import argparse


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()

digits = ['0','1','2','3','4','5','6','7','8','9']

if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))

    numbers = []
    for i,l in enumerate(lines):
        inNumber = False
        start = 0
        number = []
        for j,c in enumerate(l):
            if c in digits:
                print(i,j,c)
                if inNumber == False:
                    start = j
                    inNumber = True
                number.append(c)
            elif inNumber == True:
                inNumber = False
                numbers.append((int(''.join(number)),i,start,j))
                number = []
        if inNumber:
            inNumber = False
            numbers.append((int(''.join(number)),i,start,len(l)))
            number = []

    print(numbers)
