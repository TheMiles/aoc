#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

    return parser.parse_args()


class CPU(object):

    def __init__(self, memory):
        self.pc         = 0
        self.cf         = False
        self.memory     = memory
        self.operations = {
            1: [self.add,3],
            2: [self.mul,3],
            3: [self.input,1],
            4: [self.output,1]
        }

    def cycle(self):
        if self.pc >= len(self.instructions) or self.pc < 0:
            return False

        i = [ x.strip() for x in self.instructions[self.pc].split() ]
        # print(i)
        self.operations[i[0]](i[1:])
        return True

    def advance(self):
        self.pc += self.getParamLength()+1

    def getValue(self, x):
        if isInt(x):
            return int(x)
        return self.registers[x]

    def getInstr(self):
        return self.memory[pc]

    def getMnemo(self):
        instr = self.getInstr()
        return int(instr[-2:])

    def getFunctor(self):
        return self.operations[self.getMnemo()][0]

    def getParamLength(self):
        return self.operations[self.getMnemo()][1]

    def getParameterMode(self):
        instr  = self.getInstr()
        params = instr[:-2]
        params = params[::-1]

        pm = ['p'] * self.getParamLength()
        for i, p in enumerate(params):
            if p=='1':
                pm[i]='i'
        return pm

    def getParameters(self):
        params  = self.memory[pc+1:pc+1+self.getParamLength]

    def resolveParameters(self):
        params = self.getParameters()
        for i,pm in enumerate(zip(params,self.getParameterMode())):
            if pm[1] == 'p':
                pm[0][i] = self.memory[pm[0][i]]
        return params

    def getWriteAdress(self):
        params = self.getParameters()
        return params[-1]

    def add(self):
        params = self.resolveParameters()
        adr    = self.getWriteAdress()
        self.memory[adr] = params[0] + params[1]

    def mul(self):
        params = self.resolveParameters()
        adr    = self.getWriteAdress()
        self.memory[adr] = params[0] * params[1]


    def hac(self):
        c[1] = -1

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
