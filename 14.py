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

if __name__ == '__main__':
    args = getArguments()

    lines = [ x.strip() for x in args.input.readlines() ]

    for line in lines:
        countOnes = 0
        for i in range(128):
            l = line + "-" + str(i)
            countOnes += hexToBin(getHex(densifyHash(getSparseHash(args.size, args.rounds, l)))).count('1')
        print(line,"has",countOnes,"ones")
