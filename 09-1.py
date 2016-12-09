#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')
parser.add_argument('-r', '--recursive', action='store_true', help='use recursive parsing')
parser.add_argument('-c', '--count', action='store_true', help='just count resulting size')

args = parser.parse_args()

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

def count(l,start,length):
    count_letters = 0
    i = start
    while i < start+length:
        if l[i] == '(':
            i, [repeat_length,repetitions] = read_marker(l,i)
            count_letters        += (count(l,i,repeat_length) if args.recursive else repeat_length) * repetitions
            i                    += repeat_length
        else:
            count_letters += 1
            i+=1
    return count_letters

count_length = 0
for l in [ x.strip() for x in args.file]:
    if args.count:
        out = count(l, 0, len(l))
        count_length += out
        print(l, out)
    else:
        out = parse(l)
        if args.recursive:
            while '(' in out:
                out = parse(out)
        count_length += len(out)
        print(l, len(out))

print(count_length)


