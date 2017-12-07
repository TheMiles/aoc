#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Advent of code')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

def isInList(s,l):
    for x in l:
        if s == x: return True
    return False


args = parser.parse_args()

countValid = 0
lines = [ x.strip() for x in args.input.readlines() ]
for l in lines:
    words = [ ''.join(sorted(x)) for x in  l.split() ]

    # print(words)

    isValid = True
    for i in range(len(words)):
        isValid = isValid and not isInList(words[i],words[i+1:])
    print("The passphrase '{0}' is {1}".format(l, "valid" if isValid else "INVALID"))
    countValid += 1 if isValid else 0

print("There are {0} valid passphrases".format(countValid))