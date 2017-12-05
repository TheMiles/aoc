#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Spreadsheet')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))


def isDivisible(a,b):
    return float(int(a/b) == int(a)/int(b))

def divideByFirstDivisible(a,l):
    for v in l:
        if isDivisible(a,v):
            return int(a/v)
    return None

def calcChecksumOfValues(l):
    sortedList = list(l)
    sortedList.sort(reverse=True)
    for i in range(len(sortedList)):
        checksum = divideByFirstDivisible(sortedList[i],sortedList[i+1:])
        if checksum: return checksum
    return None

args = parser.parse_args()

lines = [ x.strip() for x in args.input.readlines() ]
sum = 0
for l in lines:
    values = [ int(x) for x in l.split()]
    sum += calcChecksumOfValues(values)

print("Result is", sum)