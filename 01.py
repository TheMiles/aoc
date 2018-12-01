#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Captcha')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))

args = parser.parse_args()

lines     = [ x.strip() for x in args.input.readlines() ]
sum       = 0
freqs     = set()
searching = True

while searching:
    for l in lines:
        if l:
            op = l[0]
            n  = int(l[1:])
            if op == '+':
                sum += n
            elif op == '-':
                sum -= n
            else:
                print("ERROR")
            searching = not sum in freqs
            freqs.add(sum)
            if not searching:
                break
print("Result is {0}".format(sum))