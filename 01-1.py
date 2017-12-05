#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Captcha')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'))


def calcCaptchaValue(c,shiftByDigits=1):
    if len(c)==0: return None

    sum = 0
    for z in zip(c, c[shiftByDigits:] + c[:shiftByDigits]):
        if z[0] == z[1]:
            sum += int(z[0])
    return sum

args = parser.parse_args()

lines = [ x.strip() for x in args.input.readlines() ]
for l in lines:
    shiftByDigits = int(len(l)/2)
    r = calcCaptchaValue(l, shiftByDigits)
    print("Result of {0} is {1}".format(l,r))