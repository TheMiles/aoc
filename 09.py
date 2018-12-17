#!/usr/bin/python3

import argparse
from collections import defaultdict

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('-p','--players', default=9, type=int)
    parser.add_argument('-m','--marbles', default=25, type=int)
    return parser.parse_args()


def marblesString(m, c):
    s = [ (' (' + str(x) + ') ') if i == c else ('  ' +  str(x) + '  ') for i, x in enumerate(m) ]
    return ''.join(s)

if __name__ == '__main__':

    args         = getArguments()
    playerValues = [ 0 for i in range(args.players)]
    marbles      = [0]
    current      = 0
    player       = -1
    for nextMarble in range(1,args.marbles + 1):

        player = (player + 1) % args.players
        if nextMarble and nextMarble % 23 == 0:

            current -= 7
            if current < 0:
                current = len(marbles) + current
            playerValues[player] += nextMarble + marbles[current]
            del marbles[current]
        else:
            current = (current + 1) % (len(marbles) ) + 1
            marbles.insert(current, nextMarble)
        # print ("nextMarble ", nextMarble, " marbles ", marblesString(marbles, current))

    print("The winning score is ", max(playerValues))

