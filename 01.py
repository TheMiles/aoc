#!/usr/bin/python3

import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


def replace_spelled_digits( line ):
    digits_spelled = [('one','1'), ('two','2'), ('three','3'), ('four','4'), ('five','5'), ('six','6'), ('seven','7'), ('eight','8'), ('nine','9')]

    found_words = []

    i = 0
    while i < len(line):
        increment = 1
        for d in digits_spelled:
            if d[0] == line[i:i+len(d[0])]:
                found_words.append((i,i+len(d[0]),d[1]))
                increment = len(d[0])
                break
        i += increment
        # print(i, " ", line[i:])

    l = line[:]
    for d in reversed(found_words):
        l = l[:d[0]] + d[2] + l[d[1]:]

    # print (line, ' -> ', l, '  /// ' ,found_words)
    return l


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))

    digits = ['0','1','2','3','4','5','6','7','8','9']

    lines = [ replace_spelled_digits(line) for line in lines ]

    numbers = [ [ int(y) for y in x if y in digits] for x in lines ]
    pairs = [ x[0]*10 + x[-1] for x in numbers ]

    print( sum(pairs) )

