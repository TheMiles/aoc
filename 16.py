#!/usr/bin/python3

import argparse
import numpy as np

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-i','--iterations', type=int, default=10)

    return parser.parse_args()

def applyFFT(a, iterations):
    base  = np.array([0,1,0,-1])
    array = np.array(a)

    for i in range(iterations):
        length       = len(array)
        next = array.copy()
        for j in range(len(array)):
            patternIndex = np.array(range(1,length+1))
            patternIndex = np.array(list(map(lambda x: int(x/(j+1))%len(base), patternIndex )))
            pattern      = np.array([base[n] for n in patternIndex])
            next[j] = abs(np.inner(array, pattern))%10
        array=next
    return [ int(i) for i in array ]





def main():

    args = getArguments()
    lines = [[int(n)  for n in filter(lambda x: x.isdigit(),list(x))] for x in filter(None, args.input.readlines()) ]

    for p in lines:
        result = applyFFT(p, args.iterations)
        firstEight = "".join([ str(x) for x in result[:8]])
        print(result, firstEight)


if __name__ == '__main__':
    main()