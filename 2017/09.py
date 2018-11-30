#!/usr/bin/python3

import argparse
import re
from collections import defaultdict

parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

args = parser.parse_args()

def default(s):
        s.i += 1
        if s.garbage:
            s.countGarbage += 1
        return s

def closeGarbage(s):
        s.i += 1
        s.garbage = False
        return s

def openGarbage(s):
        s.i += 1
        if s.garbage:
            s.countGarbage += 1
        s.garbage = True
        return s

def openGroup(s):
        s.i += 1
        if not s.garbage:
            s.score += 1
        else:
            s.countGarbage += 1
        return s

def closeGroup(s):
        s.i += 1
        if not s.garbage:
            s.totalscore += s.score
            s.score      += -1
        else:
            s.countGarbage += 1
        return s

def escapeChar(s):
        s.i += 2
        return s

parseChar = defaultdict( lambda: default )
parseChar['>'] = closeGarbage
parseChar['<'] = openGarbage
parseChar['{'] = openGroup
parseChar['}'] = closeGroup
parseChar['!'] = escapeChar


class State(object):

    def __init__(self):
        self.i            = 0
        self.score        = 0
        self.totalscore   = 0
        self.countGarbage = 0
        self.garbage      = False


lines = [ x.strip() for x in args.input.readlines() ]

for l in lines:
    s = State()
    while s.i < len(l):
        c = l[s.i]
        s = parseChar[l[s.i]](s)

    print("Total score",s.totalscore,"garbage chars",s.countGarbage)
