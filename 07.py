#!/usr/bin/python3

import argparse
import re

parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))


class Program(object):

    def __init__(self, name, weight, children):
        self.name     = name
        self.weight   = weight
        self.children = children

    def __str__(self):
        return "Name: {0} weight {1} children {2}".format(self.name, self.weight, self.children)

    def __eq__(self,other):

        if type(other) is str:
            return self.name == other

        if type(other) is Program:
            return self.name == other.name

        return False

    def isParentOf(self, name):
        return name in self.children


def findIndexOfParent(programs, name):
    for i,p in enumerate(programs):
        if p.isParentOf(name):
            return i
    return None


def findIndexOfRoot(programs):
    for i,p in enumerate(programs):
        if not findIndexOfParent(programs, p.name):
            return i
    return None


args = parser.parse_args()

splitNameWeight = re.compile(r"(\w+) +\((\d+)\)")

lines = [ x.strip() for x in args.input.readlines() ]

programs = []

for l in lines:
    childSplit = [ x.strip() for x in l.split('->') ]
    name = ""
    weight = 0
    children = []

    m = splitNameWeight.match(childSplit[0])
    if m:
        name   = m.group(1)
        weight = int(m.group(2))

    if len(childSplit) > 1:
        children = [ x.strip() for x in childSplit[1].split(',') ]

    programs.append(Program(name, weight, children))

r = findIndexOfRoot(programs)
print("Root program is", programs[r])
