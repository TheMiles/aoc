#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

def strJumpOffsets(p,o):
    s = [str(x) for x in o]
    if p < len(o):
        s[p] = "({0})".format(s[p])
    s = ' '.join(s)
    return "[{0}]".format(s)

args = parser.parse_args()

pointer = 0
offsets = [ int(x.strip()) for x in args.input.readlines() ]
length  = len(offsets)
count   = 0

print(strJumpOffsets(pointer, offsets))

while pointer < length:
    count += 1
    nextPointer = pointer + offsets[pointer]
    offsets[pointer] += 1
    pointer = nextPointer

print(strJumpOffsets(pointer,offsets))
print("There were {0} steps".format(count))