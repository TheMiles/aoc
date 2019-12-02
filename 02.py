#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


def add(c):
    m  = c[0]
    pc = c[1]

    a  = m[m[pc+1]]
    b  = m[m[pc+2]]
    m[m[pc+3]] = a + b

    c[1] = pc+4

def mul(c):
    m  = c[0]
    pc = c[1]

    a  = m[m[pc+1]]
    b  = m[m[pc+2]]
    m[m[pc+3]] = a * b

    c[1] = pc+4


def hac(c):
    c[1] = -1


opcodes = {
    1:  add,
    2:  mul,
    99: hac
}


def run(c):
    while c[1] >= 0:
        p  = c[0]
        pc = c[1]
        opcodes[p[pc]](c)



if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ [ int(y) for y in x.strip().split(',')] for x in args.input.readlines() ] ))

    for p in lines:
        c = [p[:], 0]
        run(c)
        print(p,c[0])
