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

    def __init__(self, idOfCPU, instructions, sockets):
        self.pc           = 0
        self.id           = idOfCPU
        self.sockets      = sockets
        self.instructions = instructions
        self.registers    = defaultdict(lambda: 0)
        self.waiting      = False
        self.send_counter = 0
        self.operations = {
            "snd": self.snd,
            "set": self.set,
            "add": self.add,
            "mul": self.mul,
            "mod": self.mod,
            "rcv": self.rcv,
            "jgz": self.jgz
        }
        self.registers['p'] = self.id

    def cycle(self):
        if self.pc >= len(self.instructions) or self.pc < 0:
            return False

        pc_before = self.pc
        i = [ x.strip() for x in self.instructions[self.pc].split() ]
        self.operations[i[0]](i[1:])
        self.waiting = pc_before == self.pc
        return True

    def advance(self):
        self.pc +=1

    def getValue(self, x):
        if isInt(x):
            return int(x)
        return self.registers[x]

    def snd(self, operands):
        otherSocket = abs(self.id - 1)
        self.sockets[otherSocket].append(self.getValue(operands[0]))
        self.send_counter += 1
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
        if self.sockets[self.id]:
            v = self.sockets[self.id][0]
            self.sockets[self.id] = self.sockets[self.id][1:]
            self.registers[operands[0]] = v
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

    sockets = [[],[]]
    a = CPU(0,instructions,sockets)
    b = CPU(1,instructions,sockets)

    while True:
        running_a = a.cycle()
        running_b = b.cycle()
        # print()
        # print(sockets)
        # print("a", a.pc, a.registers, a.waiting)
        # print("b", b.pc, b.registers, b.waiting)
        # input("Press Enter to continue...")

        both_waiting = a.waiting and b.waiting
        any_running  = running_a or  running_b

        if not any_running or both_waiting:
            break

print("Programm 1 sended", b.send_counter, "times")
