#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-n','--noun', type=int, default=12)
    parser.add_argument('-v','--verb', type=int, default=2)
    parser.add_argument('-t','--target', type=int)

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

        print("Trying", p)

        noun = args.noun
        verb = args.verb

        if args.target:
            nount = 0
            verb  = 0

        while True:
            c = [p[:], 0]
            c[0][1] = noun
            c[0][2] = verb
            run(c)

            if(not args.target or args.target == c[0][0]):
                break

            noun += 1
            if noun > 99:
                verb += 1
                if verb > 99:
                    break
                noun = 0


        print(noun, verb, c[0])
        print(100 * noun + verb)
