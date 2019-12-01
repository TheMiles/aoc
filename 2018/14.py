#!/usr/bin/python3

import argparse
import re
from collections import defaultdict
import time


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('-r', '--recipe', type=int, default=9)
    return parser.parse_args()

def main():
    args    = getArguments()
    recipes = [3,7]
    elves   = [0,1]

    recipeToLookFor = [int(i) for i in str(args.recipe)]
    recipeLength    = len(recipeToLookFor)

    last = time.time()

    while recipes[-recipeLength:] != recipeToLookFor:
        nextRecipe = str(recipes[elves[0]] + recipes[elves[1]])
        recipes.extend([int(i) for i in nextRecipe[-2:]])
        elves[:] = [ (i + 1 + recipes[i]) % len(recipes) for i in elves ]
        # print("{:> 7}: [{},{}] {} ".format(len(recipes), elves[0], elves[1],' '.join([str(k) for k in recipes])))

        if time.time() - last > 2:
            print("{:> 7} Recipes".format(len(recipes)))
            last = time.time()

    print(len(recipes)-recipeLength)

if __name__ == '__main__':
    main()