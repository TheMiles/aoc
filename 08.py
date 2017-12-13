#!/usr/bin/python3

import argparse
import re
from collections import defaultdict

parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

operations = {
    "inc": lambda x,y: x+y,
    "dec": lambda x,y: x-y
}

comparison = {
    "==": lambda x,y: x==y,
    ">":  lambda x,y: x>y,
    "<":  lambda x,y: x<y,
    ">=": lambda x,y: x>=y,
    "<=": lambda x,y: x<=y,
    "!=": lambda x,y: x!=y
}

args = parser.parse_args()

splitCommand = re.compile(r"(\w+) +(\w+) +(-?\d+) +if +(\w+) +(\S+) +(-?\d+)")
registers = defaultdict(lambda: 0)

lines = [ x.strip() for x in args.input.readlines() ]

for l in lines:
    m = splitCommand.match(l)

    if not m:
        print("Couldn't match", l)
        continue

    targetRegister      = m.group(1)
    opcode              = m.group(2)
    operand             = int(m.group(3))
    conditionRegister   = m.group(4)
    conditionComparator = m.group(5)
    conditionValue      = int(m.group(6))

    if comparison[conditionComparator](registers[conditionRegister], conditionValue):
        registers[targetRegister] = operations[opcode](registers[targetRegister], operand)

print("The largest value is", max(registers.values()))