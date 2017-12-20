#!/usr/bin/python3

import argparse
import string

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-r','--range', type=int, default=16)
    parser.add_argument('-i','--iterations', type=int, default=1000000000)
    return parser.parse_args()

def spin(operand, data):
    op = -1 * int(operand)
    data = data[op:] + data[:op]
    return data

def exchange(operand, data):
    ops = [ int(x) for x in operand.split("/") ]
    data=data[:]
    data[ops[0]], data[ops[1]] = data[ops[1]],data[ops[0]]
    return data

def partner(operand, data):
    ops = operand.split("/")
    indices = "/".join([ str(data.index(x)) for x in ops])
    return exchange(indices,data)

instructions = {
    "s" : spin,
    "x" : exchange,
    "p" : partner
}

def runDance(moves, programs):
    for m in moves:
        i, op = m[0], m[1:]
        programs = instructions[i](op,programs)
    return programs

if __name__ == '__main__':
    args = getArguments()

    moves = [ x.strip() for x in args.input.readline().split(',') ]
    programs = list(string.ascii_lowercase)[:args.range]
    initial_programs = programs[:]
    cycle_length = None

    for i in range(args.iterations):

        programs = runDance(moves, programs)
        if programs == initial_programs:
            cycle_length = i+1
            break

    if cycle_length:
        remaining_iterations = args.iterations % cycle_length
        print("Found cycle with length", cycle_length, "remaining iterations", remaining_iterations)

        for _ in range(remaining_iterations):
            programs = runDance(moves,programs)

    print("".join(programs))
