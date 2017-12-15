#!/usr/bin/python3

import argparse
import re


parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

args = parser.parse_args()

def findAllGraphContaining(g,v):
    foundGraphs=[]
    notFoundGraphs=[]

    for x in g:
        if v in x:
            foundGraphs.append(x)
        else:
            notFoundGraphs.append(x)
    return foundGraphs, notFoundGraphs

def isInGraphList(g,v):
    return any([v in x for x in g])


splitConnection = re.compile(r"(\d+) <->(.*)")
lines = [ x.strip() for x in args.input.readlines() ]
graphs = []

for line in lines:
    m = splitConnection.match(line)
    s = int(m[1])
    c = [ int(x.strip()) for x in m[2].split(',') ]

    if not isInGraphList(graphs,s):
        graphs.append(set([s]))

    found,notFound = findAllGraphContaining(graphs,s)

    g = set.union(*found)
    for x in c:
        g.add(x)

    graphs = notFound
    graphs.append(g)


g,_ = findAllGraphContaining(graphs,0)
assert(len(g)==1)
print("There are {0} programs in the list containing 0".format(len(g[0])))