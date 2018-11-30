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

    def __init__(self, idOfCPU, instructions):
        self.pc           = 0
        self.id           = idOfCPU
        self.instructions = instructions
        self.registers    = defaultdict(lambda: 0)
        self.mul_counter  = 0
        self.operations = {
            "set": self.set,
            "sub": self.sub,
            "mul": self.mul,
            "jnz": self.jnz
        }

    def cycle(self):
        if self.pc >= len(self.instructions) or self.pc < 0:
            return False

        i = [ x.strip() for x in self.instructions[self.pc].split() ]
        # print(i)
        self.operations[i[0]](i[1:])
        return True

    def advance(self):
        self.pc +=1

    def getValue(self, x):
        if isInt(x):
            return int(x)
        return self.registers[x]

    def set(self, operands):
        r = operands[0]
        v = self.getValue(operands[1])
        self.registers[r] = v
        self.advance()

    def sub(self, operands):
        r = operands[0]
        v = self.getValue(operands[1])
        self.registers[r] -= v
        self.advance()

    def mul(self, operands):
        r = operands[0]
        v = self.getValue(operands[1])
        self.registers[r] *= v
        self.advance()
        self.mul_counter += 1

    def jnz(self, operands):
        j = 1
        if self.getValue(operands[0]) != 0:
            j = self.getValue(operands[1])
        self.pc += j


if __name__ == '__main__':
    args = getArguments()

    instructions = [ x.strip() for x in args.input.readlines() ]

    # for i,x in enumerate(instructions):
    #     print(i, x)

    a = CPU(0,instructions)
    # a.registers['a'] = 1

    c = 0

    while True:
        running_a = a.cycle()
        # print()
        # print("a", a.pc, a.registers)
        # input("Press Enter to continue...")
        # print()
            
        c += 1

        if not running_a:
            break

print("Programm ended after",c,"iterations with", a.mul_counter, "multiplications")
print(a.registers)
