#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'), nargs='?')
    parser.add_argument('-d', '--direct', type=str)


    return parser.parse_args()

class Object(object):

    def __init__(self, obj):
        self.obj      = obj
        self.parent   = None
        self.children = []

class Orbits(object):

    def __init__(self):
        self.objects = []
        self.lookup  = {}

    def getIndex(self, obj):
        if not obj in self.lookup:
            self.insertObj(obj)
        return self.lookup[obj]

    def insertObj(self, obj):
        if obj in self.lookup: return
        self.lookup[obj] = len(self.objects)
        self.objects.append(Object(obj))
        # print("Inserting", obj)

    def addChild(self, parent, child):
        parent_index = self.getIndex(parent)
        child_index  = self.getIndex(child)

        assert(self.objects[child_index].parent is None)

        # print("Adding to {} child {}".format(self.objects[parent_index].obj, self.objects[child_index].obj))
        self.objects[child_index].parent = parent_index
        self.objects[parent_index].children.append(child_index)

    def getPathForIndex(self, index):
        path = []
        i    = index
        while i is not None:
            path.append(i)
            i = self.objects[i].parent
        return path[::-1]


    def numberOfOrbitsForIndex(self, index):
        num = len(self.getPathForIndex(index))-1
        # print("Orbit number for {} is {} direct orbit of {}".format(self.objects[index].obj, num, self.objects[self.objects[index].parent].obj if self.objects[index].parent is not None else "NONE"))
        return num

    def totalNumberOfOrbits(self):
        num = 0
        for i in range(len(self.objects)):
            num += self.numberOfOrbitsForIndex(i)
        return num

    def getPathForObj(self, obj):
        return self.getPathForIndex(self.getIndex(obj))


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x.strip().split(')') for x in args.input.readlines() ] ))

    o = Orbits()

    for p in lines:
        o.addChild(p[0],p[1])

    print(o.totalNumberOfOrbits())
    you = o.getPathForObj('YOU')
    san = o.getPathForObj('SAN')

    # print(you)
    # print(san)

    for i in range(len(you)):
        if you[i] != san[i]:
            you = you[i:-1]
            san = san[i:-1]
            break

    # print(you)
    # print(san)
    print(len(you)+len(san))
