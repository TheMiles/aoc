#!/usr/bin/python3

import argparse
import itertools

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'), nargs='?')
    parser.add_argument('-d', '--direct', type=str)


    return parser.parse_args()

class Fifo(object):

    def __init__(self, data=None):
        self.buffer = []
        self.push(data)

    def push(self, data):
        if data is None: return
        self.buffer.append(data)

    def pop(self):
        if self.empty(): return None
        return self.buffer.pop(0)

    def empty(self):
        return len(self.buffer) == 0


class CPU(object):

    def __init__(self, memory, inBuffer=None, outBuffer=None):
        self.pc         = 0
        self.halted     = False
        self.memory     = memory
        self.inBuffer   = inBuffer
        self.outBuffer  = outBuffer
        self.operations = {
            1: [self.add,3],
            2: [self.mul,3],
            3: [self.input,1],
            4: [self.output,1],
            5: [self.jmptrue,2],
            6: [self.jmpfalse,2],
            7: [self.lt,3],
            8: [self.eq,3],
            99:[self.hacf,0]
        }

    def setInputBuffer(b):
        self.inBuffer = b

    def setOutputBuffer(b):
        self.outBuffer = b

    def run(self):
        while not self.halted:
            self.cycle()

    def cycle(self):
        # print("PC {} mnemo {}".format(self.pc, self.getMnemo()))
        self.getFunctor()()

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
        self.advance()

    def mul(self):
        params = self.resolveParameters()
        adr    = self.getWriteAdress()
        self.memory[adr] = params[0] * params[1]
        self.advance()

    def hacf(self):
        self.halted = True

    def input(self):
        if self.inBuffer and not self.inBuffer.empty():
            value = self.inBuffer.pop()
        else:
            value = int(input("Input needed: "))
        self.memory[self.getWriteAdress()] = value
        self.advance()

    def output(self):
        value = self.resolveParameters()[0]
        if self.outBuffer:
            self.outBuffer.push(value)
        else:
            print("Output:",value)
        self.advance()

    def jmptrue(self):
        params = self.resolveParameters()
        if(params[0] != 0):
            self.pc = params[1]
        else:
            self.advance()

    def jmpfalse(self):
        params = self.resolveParameters()
        if(params[0] == 0):
            self.pc = params[1]
        else:
            self.advance()

    def lt(self):
        params           = self.resolveParameters()
        adr              = self.getWriteAdress()
        self.memory[adr] = 1 if params[0]<params[1] else 0
        self.advance()

    def eq(self):
        params           = self.resolveParameters()
        adr              = self.getWriteAdress()
        self.memory[adr] = 1 if params[0]==params[1] else 0
        self.advance()

def runAmpCirc(program, sequence):

    numCPUs = len(sequence)
    pipes = [ Fifo(x) for x in sequence ]
    pipes.append(Fifo()) # append 1 additional Fifo for output
    cpus  = []
    for i in range(numCPUs):
        cpus.append(CPU(program, pipes[i], pipes[i+1]))

    # isert start value
    pipes[0].push(0)

    for c in cpus:
        c.run()

    return pipes[-1].pop()




if __name__ == '__main__':
    args = getArguments()
    lines = [args.direct] if args.direct else list(filter(None, [ x for x in args.input.readlines() ] ))
    lines = [[ int(y) for y in x.strip().split(',')] for x in lines ]

    for p in lines:

        print("Trying", p)

        sequences = list(itertools.permutations([0,1,2,3,4]))

        acValues  = [ runAmpCirc(p,s) for s in sequences ]
        maxAC     = max(acValues)
        print(maxAC, sequences[acValues.index(maxAC)])

