#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))


def reallocateMemory(currentMem):
    m    = list(currentMem)
    i    = m.index(max(m))
    v    = m[i]
    m[i] = 0

    while v > 0:
        i    += 1
        if i >= len(m): i = 0
        m[i] +=  1
        v    += -1

    return m

args = parser.parse_args()

history = []
count   = 0
memory  = [ int(x) for x in args.input.readline().split() ]

while memory not in history:
    history.append(memory)
    count += 1
    memory = reallocateMemory(memory)

history.append(memory)
print(history)
print("It took {0} reallocations".format(count))
