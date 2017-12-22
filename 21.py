#!/usr/bin/python3

import argparse
import re
import math
from collections import defaultdict

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-i','--iterations', type=int, default=5)
    return parser.parse_args()

initial_field = ['.#.','..#','###']

def sliceSubField(field, x,y,size):
    sf = []
    for i in range(size):
        sf.append("".join(field[y+i][x:x+size]))
    return sf

def splitField(field):
    subsize  = 2 if (len(field)%2 == 0) else 3
    elements = int(len(field)/subsize)
    f        = [ sliceSubField(field,x*subsize,y*subsize,subsize) for y in range(elements) for x in range(elements) ]
    return f

def mergeField(field):
    f = []
    element_size   = len(field[0])
    element_number = int(math.sqrt(len(field)/element_size))

    for row  in range(element_number):
        row_offset = element_size * element_number * row
        for l in range(element_size):
            line_offset = row_offset + l
            f.append("".join([ field[i] for i in range(line_offset,line_offset+element_number*element_size,element_size) ]))
    return f

def growFields(fields,rules):
    results = []
    for f in fields:
        found = False

        for r in rules:
            if compareFields(f,r[0]):
                results.extend(r[1])
                found = True
                break

        assert(found)
    return mergeField(results)

def rotateField(field):
    f = []
    for j in reversed(range(len(field))):
        sf = []
        for i in range(len(field)):
            sf.append(field[i][j])
        f.append("".join(sf))
    return f

def mirrorField(field):
    f = []
    for x in field:
        f.append(x[::-1])
    return f

def countElements(field,c):
    return sum([x.count(c) for x in field])

def printField(field):
    for x in field:
        print(x)
    print()

def compareFields(a,b):
    if len(a) != len(b): return False

    if a == b: return True

    m = mirrorField(b)
    b = rotateField(b)
    if a == b: return True
    b = rotateField(b)
    if a == b: return True
    b = rotateField(b)
    if a == b: return True

    if a == m: return True
    m = rotateField(m)
    if a == m: return True
    m = rotateField(m)
    if a == m: return True
    m = rotateField(m)
    if a == m: return True

    return False



if __name__ == '__main__':
    args = getArguments()

    field = initial_field[:]
    rules = [ [ [ z for z in y.strip().split('/') ] for y in x.split('=>')] for x in args.input.readlines() ]

    for _ in range(args.iterations):
        split = splitField(field)
        field = growFields(split,rules)
        printField(field)
        input("Press enter....")

    print("There are", countElements(field,'#'),"elements set")
