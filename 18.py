#!/usr/bin/python3

import argparse
from collections import defaultdict

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class CPU(object):

    def __init__(self, instructions):
        self.pc           = 0
        self.instructions = instructions
        self.registers    = defaultdict(lambda: 0)
        self.lastPlayed   = -1
        self.operations = {
            "snd": self.snd,
            "set": self.set,
            "add": self.add,
            "mul": self.mul,
            "mod": self.mod,
            "rcv": self.rcv,
            "jgz": self.jgz
        }

    def cycle(self):
        if self.pc >= len(self.instructions) or self.pc < 0:
            return False

        i = [ x.strip() for x in self.instructions[self.pc].split() ]
        self.operations[i[0]](i[1:])
        return True

    def advance(self):
        self.pc +=1

    def getValue(self, x):
        if isInt(x):
            return int(x)
        return self.registers[x]

    def playSound(self, f):
        print("Playing sound", f)
        self.lastPlayed = f


    def snd(self, operands):
        self.playSound(self.getValue(operands[0]))
        self.advance()

    def set(self, operands):
        r = operands[0]
        v = self.getValue(operands[1])
        self.registers[r] = v
        self.advance()

    def add(self, operands):
        r = operands[0]
        v = self.getValue(operands[1])
        self.registers[r] += v
        self.advance()

    def mul(self, operands):
        r = operands[0]
        v = self.getValue(operands[1])
        self.registers[r] *= v
        self.advance()

    def mod(self, operands):
        r = operands[0]
        v = self.getValue(operands[1])
        self.registers[r] %= v
        self.advance()

    def rcv(self, operands):
        if self.getValue(operands[0]) != 0:
            print("recover",self.lastPlayed)
            self.pc = len(self.instructions)
        else:
            self.advance()

    def jgz(self, operands):
        j = 1
        if self.getValue(operands[0]) > 0:
            j = self.getValue(operands[1])
        self.pc += j

if __name__ == '__main__':
    args = getArguments()

    instructions = [ x.strip() for x in args.input.readlines() ]

    # for i,x in enumerate(instructions):
    #     print(i, x)

    c = CPU(instructions)
    while c.cycle():
        # print(c.pc, c.registers)
        # input("Press Enter to continue...")
        pass

