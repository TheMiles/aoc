import itertools
from enum import Enum
from termcolor import colored


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

    class State(Enum):
        Running = 1
        Waiting = 2
        Halted  = 3


    def __init__(self, memory, inBuffer=None, outBuffer=None):
        self.pc          = 0
        self.state       = CPU.State.Running
        self.memory      = memory[:]
        self.relativeAdr = 0
        self.verbose     = False
        self.stepMode    = False
        self.inBuffer    = inBuffer
        self.outBuffer   = outBuffer
        self.operations  = {
            1: [self.add,3],
            2: [self.mul,3],
            3: [self.input,1],
            4: [self.output,1],
            5: [self.jmptrue,2],
            6: [self.jmpfalse,2],
            7: [self.lt,3],
            8: [self.eq,3],
            9: [self.addRelAdr,1],
            99:[self.hacf,0]
        }

    def setInputBuffer(b):
        self.inBuffer = b

    def setOutputBuffer(b):
        self.outBuffer = b

    def readMem(self, adr):
        if type(adr) is list:
            return [ self.readMem(a) for a in adr ]

        if adr < 0: raise IndexError("No read access with negative adresses")
        if adr >= len(self.memory): return 0
        return int(self.memory[adr])

    def writeMem(self, adr, value):
        if adr < 0: raise IndexError("No write access with negative adresses")
        if adr >= len(self.memory):
            self.memory.extend([0]*(adr+1-len(self.memory)))

        self.memory[adr] = value

    def isRunning(self):
        return self.state == CPU.State.Running

    def isWaiting(self):
        return self.state == CPU.State.Waiting

    def isHalted(self):
        return self.state == CPU.State.Halted

    def setVerbose(self, v):
        self.verbose = v

    def setStepMode(self, s=None):
        self.stepMode = s

    def printState(self):
        if self.verbose:
            paramStart = self.pc+1
            paramEnd   = paramStart+self.getParamLength()
            memory     = self.memory[:self.pc]
            memory.append(colored(self.memory[self.pc],'red'))
            memory.extend([colored(m,'green') for m in self.memory[paramStart:paramEnd] ])
            memory.extend(self.memory[paramEnd:])
            print("Mem: [", memory[0], end='')
            for m in memory[1:]:
                print(",",m,end='')
            print("]")
            print("pc {} is '{}' relativeAdr {} state {}".format(self.pc, self.getFunctor().__name__, self.relativeAdr, self.state))
            print("Params {} Mode {} resolvedAdress {} resolveParameters {}".format(self.getParameters(), self.getParameterMode(), self.resolveAdresses(), self.resolveParameters()))

    def run(self):
        while self.state != CPU.State.Halted:
            self.cycle()
            if self.state != CPU.State.Running:
                break

    def cycle(self):
        self.printState()
        if self.stepMode: input("Enter for next step")
        self.getFunctor()()

    def advance(self):
        self.pc += self.getParamLength()+1

    def getInstr(self):
        return str(self.readMem(self.pc))

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
        modes = {
         '0': 'p',  # parameter mode
         '1': 'i',  # imediate mode
         '2': 'r'   # relative mode
        }
        for i, p in enumerate(params):
            pm[i]=modes[p]

        return pm

    def getParameters(self):
        adr = [self.pc + 1 + x for x in range(self.getParamLength())]
        return self.readMem(adr)


    def resolveAdresses(self):
        adresses = self.getParameters()
        for i,pm in enumerate(zip(adresses,self.getParameterMode())):
            if   pm[1] == 'p':
                adresses[i] = pm[0]

            elif pm[1] == 'r':
                adresses[i] = self.relativeAdr + pm[0]

            else:
                adresses[i] = None
        return adresses


    def resolveParameters(self):
        params   = self.getParameters()
        adresses = self.resolveAdresses()
        for i, pa in enumerate(zip(params,adresses)):
            params[i] = self.readMem(pa[1]) if pa[1] is not None else pa[0]

        return params

    def getWriteAdress(self):
        adresses = self.resolveAdresses()
        return adresses[-1]

    def add(self):
        params = self.resolveParameters()
        adr    = self.getWriteAdress()
        self.writeMem(adr, params[0] + params[1])
        self.advance()

    def mul(self):
        params = self.resolveParameters()
        adr    = self.getWriteAdress()
        self.writeMem(adr, params[0] * params[1])
        self.advance()

    def hacf(self):
        self.state = CPU.State.Halted

    def input(self):
        if self.inBuffer and not self.inBuffer.empty():
            self.state = CPU.State.Running
            value = self.inBuffer.pop()
        elif self.inBuffer is None:
            self.state = CPU.State.Running
            value = input("Input: ")
        else:
            self.state = CPU.State.Waiting
            return
        self.writeMem(self.getWriteAdress(), value)
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
        self.writeMem(adr, 1 if params[0]<params[1] else 0)
        self.advance()

    def eq(self):
        params           = self.resolveParameters()
        adr              = self.getWriteAdress()
        self.writeMem(adr, 1 if params[0]==params[1] else 0)
        self.advance()

    def addRelAdr(self):
        params            = self.resolveParameters()
        self.relativeAdr += params[0]
        self.advance()

