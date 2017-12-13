#!/usr/bin/python3

import argparse
import re
from collections import defaultdict

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

def findIndexOfProgram(programs, p):
    if type(p) is Program:
        return findIndexOfProgram(programs, p.name)

    assert(type(p) is str)

    for i,prog in enumerate(programs):
        if prog.name == p:
            return i
    return None


def buildChildIndicesList(programs):
    ci   = [ [] for _ in range(len(programs)) ]
    todo = [findIndexOfRoot(programs)]

    while todo:
        i        = todo[0]
        todo     = todo[1:]
        names    = programs[i].children
        children = ci[i]
        for n in names:
            children.append(findIndexOfProgram(programs,n))

        todo.extend(children)

    return ci

def buildWeightList(programs,childIndices):
    weights = [ 0 ] * len(programs)

    todo = [ (i,ci) for i,ci in enumerate(childIndices)]

    while todo:
        c    = todo[0]
        todo = todo[1:]
        cw   = [0]

        if c[1]:
            cw = [weights[x] for x in c[1]]

            if any([x == 0 for x in cw]):
                todo.append(c)
                continue

        weights[c[0]] = programs[c[0]].weight + sum(cw)

    return weights

def findIndexWithUnbalancedChildren(programs,childIndices,weights):

    todo = [ findIndexOfRoot(programs) ]

    indexUnbalanced = None

    while todo:
        i    = todo[0]
        todo = todo[1:]

        if not childIndices[i]: continue

        cw = [ weights[x] for x in childIndices[i] ]
        if len(set(cw)) > 1:
            cw              = getChildrenWeight(childIndices,weights,i)
            indexUnbalanced = i
            nextIndex       = getUnbalancedChild(cw)[0]
            todo.append(nextIndex)

    return indexUnbalanced

def getChildrenWeight(childIndices,weights,i):
    c = childIndices[i]
    w = [weights[x] for x in c]

    return list(zip(c,w))

def getUnbalancedChild(childWeights):

    count = defaultdict(lambda: 0)
    for i,w in childWeights:
        count[w] += 1
    assert(len(count) < 3)

    balanced   = 0
    unbalanced = 0

    for k,v in count.items():
        if v == 1:
            unbalanced = k
        else:
            balanced = k

    indexUnbalanced = None
    for i,w in childWeights:
        if w == unbalanced:
            indexUnbalanced = i

    return indexUnbalanced, unbalanced, balanced-unbalanced





args = parser.parse_args()

splitNameWeight = re.compile(r"(\w+) +\((\d+)\)")

lines = [ x.strip() for x in args.input.readlines() ]

programs     = []

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

ci      = buildChildIndicesList(programs)
w       = buildWeightList(programs,ci)
u       = findIndexWithUnbalancedChildren(programs,ci,w)
cw      = getChildrenWeight(ci,w,u)
i,uw,dw = getUnbalancedChild(cw)

print("Unbalanced child is {0} with a weight of {1}, wich differs by {2} new weight is {3}".format(programs[i].name, programs[i].weight, dw, programs[i].weight+dw))