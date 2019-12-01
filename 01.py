#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()

def getFuel(mass):
    fuel = int(mass/3)-2
    if fuel < 0: fuel = 0
    # print("div", mass/3, "cast", int(mass/3))
    # print("mass",mass,"fuel",fuel)
    return fuel

if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ int(x.strip()) for x in args.input.readlines() ] ))

    sum = 0
    for mass in lines:
        module_fuel = 0
        fuel = getFuel(mass)
        while fuel > 0:
            module_fuel += fuel
            fuel = getFuel(fuel)
        sum += module_fuel
        print("Module:", mass, "fuel:",module_fuel)

    print("Sum:", sum)
