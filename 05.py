#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

    return parser.parse_args()


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
