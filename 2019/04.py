#!/usr/bin/python3

import argparse
from collections import defaultdict

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('value', type=int, nargs='+')

    return parser.parse_args()

def check(p):
    passwd = str(p)
    prev   = -1
    mults  = defaultdict(lambda: 1)

    hasLength = len(passwd) == 6
    hasDouble = False
    hasRising = True

    for c in passwd:
        value = int(c)
        if value < prev:  hasRising=False
        if value == prev:
            hasDouble=True
            mults[value] += 1
        prev = value

    # print("Password {} hasLenght {}, doubleDigits {}, isRising {}".format(passwd, hasLength, hasDouble, hasRising))
    return hasLength and hasDouble and hasRising and 2 in mults.values()


if __name__ == '__main__':
    args = getArguments()

    lowValue = args.value[0]
    upValue  = args.value[1] if len(args.value) > 1 else args.value[0]

    sum = 0
    for passwd in range(lowValue, upValue+1):
        isValid = check(passwd)
        if isValid: sum += 1
        # print("Checking {} which is {}".format(passwd, "valid" if isValid else "INvalid"))

    print("There are {} valid passwords".format(sum))