#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()

class Component(object):

    def __init__(self, index, ports):
        self.i = index
        self.p = [ int(y.strip()) for y in ports.split('/')]

    def __eq__(self, v):
        if type(v) is int:
            return v in self.p
        if type(v) is Component:
            return self.i == v.i and self.p == v.p

    def __str__(self):
        return "{0} [{1}/{2}]".format(self.i,self.p[0],self.p[1])

    def other(self, v):
        return self.p[1] if v == self.p[0] else self.p[0]


def findComponentsContaining(components, v):
    results = []
    for x in components:
        if v == x:
            results.append(x.i)
    return results

def removeInvalid(candidates, used):
    return [ x for x in candidates if x not in used ]

def bridgeStrength(components,bridge):
    result = 0
    for x in bridge:
        c = components[x]
        result += c.p[0] + c.p[1]
    return result

def getBridgePossibilities(components, bridge, v):
    results = []
    nextElements = removeInvalid(findComponentsContaining(components,v),bridge)
    for x in nextElements:
        b = bridge[:] + [x]
        r = getBridgePossibilities(components,b,components[x].other(v))
        results.extend(r if r else [b])
    return results


if __name__ == '__main__':
    args = getArguments()

    components = [ Component(i,x) for i,x in enumerate(args.input.readlines()) ]

    # for p in components:
    #     print(p)

    b = getBridgePossibilities(components,[],0)

    w = ""
    s = 0
    
    for x in b:
        m = ""
        for y in x:
            m += str(components[y]) + " -> "
        bs = bridgeStrength(components,x)
        m += "sum: " + str(bs)
        if(bs > s):
            s = bs
            w = m

    print(w)

