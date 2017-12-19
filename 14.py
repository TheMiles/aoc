#!/usr/bin/python3

import argparse

getHex        = __import__('10').getHex
getSparseHash = __import__('10').getSparseHash
densifyHash   = __import__('10').densifyHash

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-s','--size', type=int, default=256)
    parser.add_argument('-r','--rounds', type=int, default=64)
    return parser.parse_args()

def hexToBin(v):
    assert(type(v) is str)

    num_of_bits = 4 * len(v)
    return str(bin(int(v, 16))[2:].zfill(num_of_bits))

def fillFieldWithColor(rows,x,y, color):
    if(x < 0): return
    if(y < 0): return
    if(y >= len(rows)): return
    if(x >= len(rows[0])): return
    if rows[y][x] != '#': return

    rows[y][x] = color
    fillFieldWithColor(rows, x-1, y,   color)
    fillFieldWithColor(rows, x+1, y,   color)
    fillFieldWithColor(rows, x,   y-1, color)
    fillFieldWithColor(rows, x,   y+1, color)


def colorizeField(rows):
    maxNumberOfColors = 0
    for i,r in enumerate(rows):
        for j,v in enumerate(r):
            if v == '#':
                maxNumberOfColors += 1
                fillFieldWithColor(rows,j,i,maxNumberOfColors)
    return maxNumberOfColors


if __name__ == '__main__':
    args = getArguments()

    lines = [ x.strip() for x in args.input.readlines() ]

    for line in lines:
        rows = []
        for i in range(128):
            l = line + "-" + str(i)
            rows.append(list(hexToBin(getHex(densifyHash(getSparseHash(args.size, args.rounds, l)))).replace('1','#').replace('0','.')))

        numColors = colorizeField(rows)
        for x in rows:
            print(x)

        print("There are", numColors, "fields")
