#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()

count_length = 0

def read_marker(l,i):
    data   = []
    select = 0
    while l[i] != ')':
        c = l[i]
        if c == '(':
            data.append('')
        elif c == 'x':
            data.append('')
            select += 1
        else:
            data[select] += c
        i += 1
    return i+1, [int(x) for x in data]


for l in [ x.strip() for x in args.file]:
    out = ''
    i = 0
    while i < len(l):
        c = l[i]

        if l[i] == '(':
            i, [length,repitions] = read_marker(l,i)
            out += l[i:i+length] * repitions
            i   += length
        else:
            out += l[i]
            i+=1
    count_length += len(out)
    print(l,out, len(out))

print(count_length)


