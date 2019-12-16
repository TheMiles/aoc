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
        pattern = np.array(range(len(array)*2), dtype=np.uint8)
        pattern = np.array(list(map(lambda x: int(x/(i+1))%len(base), pattern )))

        print(pattern)



def main():

    args = getArguments()
    lines = [[int(n)  for n in filter(lambda x: x.isdigit(),list(x))] for x in filter(None, args.input.readlines()) ]

    for p in lines:
        applyFFT(p, args.iterations)
        # print(p)

        break

if __name__ == '__main__':
    main()