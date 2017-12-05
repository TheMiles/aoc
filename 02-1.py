#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Spreadsheet')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))


def calcChecksumOfValues(l):
    return max(l) - min(l)

args = parser.parse_args()

lines = [ x.strip() for x in args.input.readlines() ]
sum = 0
for l in lines:
    values = [ int(x) for x in l.split()]
    sum += calcChecksumOfValues(values)

print("Result is", sum)