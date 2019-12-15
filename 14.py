#!/usr/bin/python3

import argparse
from collections import defaultdict
import math


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


class RefinementUnit(object):

    def __init__(self, recipes):
        self.recipes      = recipes
        self.amountNeeded      = defaultdict(lambda:0)
        self.dependencies = defaultdict(lambda:0)
        self.baseChemical = 'ORE'

    def fillDependencies(self, chemical):

        self.dependencies.clear()
        self.dependencies[chemical] = 0
        stack = [chemical]

        while stack:
            current = stack.pop()
            if current not in self.recipes: continue

            for c in self.neededChemicalsFor(current):
                # print("{} adds dependency to {}".format(current,c))
                self.dependencies[c] += 1
                stack.append(c)

    def recipeFor(self, chemical):
        recipes = self.recipes[chemical]
        if len(recipes) > 1: print("There are {} recipes for {}".format(len(recipes, chemical)))
        r = recipes[0]
        return r[0], r[1:]

    def neededChemicalsFor(self, chemical):
        d,recipes = self.recipeFor(chemical)
        return [ r[1] for r in recipes]

    def popNextCandidate(self):
        dependencies, candidate = sorted(zip(self.dependencies.values(), self.dependencies.keys()))[0]

        if candidate != self.baseChemical:
            for c in self.neededChemicalsFor(candidate):
                self.dependencies[c] -= 1
        self.dependencies.pop(candidate)
        return candidate

    def resolve(self,chemical):

        amountNeeded = self.amountNeeded[chemical]
        amountProduced, recipes = self.recipeFor(chemical)
        multiplier = int(math.ceil(amountNeeded/amountProduced))

        # print("Producing {} amount {}, using {} times {}".format(chemical,amountNeeded, multiplier, recipes), end='')
        for n in recipes:
            needed = n[0]*multiplier
            # print(" adding {} of {}".format(needed,n[1]), end='')
            self.amountNeeded[n[1]] += needed
        # print("")


    def calculateAmountsFor(self, amount, chemical):

        self.amountNeeded.clear()
        self.amountNeeded[chemical] = amount
        self.fillDependencies(chemical)

        n = self.popNextCandidate()
        while n != self.baseChemical:
            self.resolve(n)
            n = self.popNextCandidate()

        return self.amountNeeded[self.baseChemical]


if __name__ == '__main__':
    args = getArguments()
    lines = [[ y.strip() for y in x.strip().split('=>')] for x in list(filter(None, [ r for r in args.input.readlines() ] )) ]

    reactions = defaultdict(lambda:[])
    for p in lines:

        amount, result = p[1].split(' ')
        needed = [int(amount)]
        for i in p[0].split(','):
            a,c=i.strip().split(' ')
            needed.append((int(a),c))
        reactions[result].append(needed)

    r = RefinementUnit(reactions)
    needed = r.calculateAmountsFor(1,'FUEL')
    print("For 1 FUEL I need {} ORE".format(needed))

    increment = 1024
    supply    = 1000000000000
    current   = math.floor(supply/needed)

    needed = r.calculateAmountsFor(current,'FUEL')
    while True:
        next   = current+increment
        needed = r.calculateAmountsFor(next,'FUEL')

        if needed>supply:
            if increment==1: break
            increment /= 2
        else:
            current = next

    print("So I can produce {} FUEL".format(int(current)))
