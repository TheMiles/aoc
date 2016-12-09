#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')
parser.add_argument('-r', '--recursive', action='store_true', help='use recursive parsing')

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

def parse(l):
    out = ''
    i = 0
    while i < len(l):
        if l[i] == '(':
            i, [length,repitions] = read_marker(l,i)
            out += l[i:i+length] * repitions
            i   += length
        else:
            out += l[i]
            i+=1
    return out

for l in [ x.strip() for x in args.file]:
    out = parse(l)
    if args.recursive:
        while '(' in out:
            out = parse(out)
    count_length += len(out)
    print(l, len(out))

print(count_length)


