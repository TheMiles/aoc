#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()

def getLastItem(l):
    l = l.split()
    return l[-1][:-1]

def getInstruction(l,i):
    def getInstructionPart(l,i):
        readValue     = getLastItem(l[i+0])
        writeValue    = getLastItem(l[i+1])
        moveDirection = getLastItem(l[i+2])
        nextState     = getLastItem(l[i+3])
        return (readValue,writeValue,moveDirection,nextState)

    f = getInstructionPart(l,i+1)
    s = getInstructionPart(l,i+5)

    if(f[0]==1):
        f,s = s,f
    
    return(f,s)

def getStates(l):
    states = {}
    for i in range(3,len(l),10):
        states[getLastItem(l[i])] =  getInstruction(l,i)
    return states

def getInitialState(l):
    return getLastItem(l[0])

def getIterations(l):
    return int(l[1].split()[5])


class TuringMachine(object):

    def __init__(self, description):
        self.state        = getInitialState(description)
        self.instructions = getStates(description)
        self.tape         = [0]
        self.head         = 0

    def __str__(self):
        s = self.state + " ... "
        for i in range(len(self.tape)):
            f = "[{0}]" if i == self.head else " {0} "
            s += f.format(self.tape[i])
        return s + " ..."

    def moveHead(self, direction):
        if(direction == 'right'):
            self.head += 1
            while self.head >= len(self.tape):
                self.tape.append(0)

        else:
            self.head += -1
            if self.head < 0:
                self.head = 0
                self.tape = [0] + self.tape



    def iterate(self):
        nextInstruction = self.instructions[self.state][self.tape[self.head]]

        self.tape[self.head] = int(nextInstruction[1])
        self.moveHead(nextInstruction[2])
        self.state = nextInstruction[3]



if __name__ == '__main__':
    args = getArguments()

    lines = [ x.strip() for x in args.input.readlines() ]
    iterations = getIterations(lines)

    t = TuringMachine(lines)

    print(t)

    for i in range(iterations):
        t.iterate()
        # print(t)
        # input("Press enter...")

    print("There are ", sum(t.tape),"ones")
