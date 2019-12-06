#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

    return parser.parse_args()


class CPU(object):

    def __init__(self, memory):
        self.pc         = 0
        self.halted     = False
        self.memory     = memory
        self.operations = {
            1: [self.add,3],
            2: [self.mul,3],
            3: [self.input,1],
            4: [self.output,1],
            99:[self.hacf,0]
        }

    def run(self):
        while not self.halted:
            self.cycle()

    def cycle(self):
        self.getFunctor()()
        self.advance()

    def advance(self):
        self.pc += self.getParamLength()+1

    def getInstr(self):
        return str(self.memory[self.pc])

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
        return self.memory[self.pc+1:self.pc+1+self.getParamLength()]


    def resolveParameters(self):
        params = self.getParameters()
        for i,pm in enumerate(zip(params,self.getParameterMode())):
            if pm[1] == 'p':
                params[i] = self.memory[pm[0]]
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


    def hacf(self):
        self.halted = True

    def input(self):
        value = int(input("Input needed:"))
        self.memory[self.getWriteAdress()] = value

    def output(self):
        print("Output:",self.resolveParameters()[0])


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ [ int(y) for y in x.strip().split(',')] for x in args.input.readlines() ] ))

    for p in lines:

        print("Trying", p)

        c = CPU(p)
        c.run()
        print(c.memory)
