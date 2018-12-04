#!/usr/bin/python3

import argparse
import re
from collections import defaultdict
from functools import reduce

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()


def getTimestamp(m):

    return int( m[1] + m[2] + m[3] + m[4] + m[5] )


def grouped(l, n):

    return zip(*[iter(l)]*n)


def getMinutes(t):

    return int(str(t)[-2:])


def getNumOccurrances(l):

    occurences = defaultdict(int)
    for f,w in grouped(l,2):
        for m in range(getMinutes(f), getMinutes(w)):
            occurences[m] += 1

    numOccurrances = defaultdict(list)
    for k,v in occurences.items():
        numOccurrances[v].append(k)

    return numOccurrances


def getSleepingMostOftenAtMinute(o):

    return o[max(o.keys)][0]



def getSleeptime(l):

    sum = 0
    for f,w in grouped(l,2):
        sum += w - f
    return sum




beginShiftPattern  = re.compile(r"\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] Guard #(\d+) begins shift")
fallsAsleepPattern = re.compile(r"\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] falls asleep")
wakesUpPattern     = re.compile(r"\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] wakes up")


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))

    sleeptable = dict()
    for line in lines:

        m = wakesUpPattern.match(line)
        if m:
            sleeptable[getTimestamp(m)] = 'w'
            continue

        m = fallsAsleepPattern.match(line)
        if m:
            sleeptable[getTimestamp(m)] = 'f'
            continue

        m = beginShiftPattern.match(line)
        if m:
            sleeptable[getTimestamp(m)] = m[6]
            continue

        print("Couldn't parse sleeptable", line)
        exit(1)

    sortedTimestamps = list(sleeptable.keys())
    sortedTimestamps.sort()

    sleeppattern = defaultdict(list)
    currentElve  = None
    for t in sortedTimestamps:

        if sleeptable[t] in ['w','f']:
            sleeppattern[currentElve].append(t)

        else:
            currentElve = sleeptable[t]

    sleepTimes = {e: getSleeptime(sleeppattern[e]) for e in sleeppattern }

    sleepiestElve    = None
    longestSleepTime = 0
    for e,s in sleepTimes.items():
        if s > longestSleepTime:
            sleepiestElve    = e
            longestSleepTime = s

    sleepingFrequencies = { e : max(getNumOccurrances(sleeppattern[e]).keys()) for e in sleeppattern }
    sleepingMinutes     = { e : getNumOccurrances(sleeppattern[e])[sleepingFrequencies[e]][0] for e in sleeppattern }

    print("Longest sleeping elve is {0} with time {1}. Sleeping most often ({2} times) at minute {3}. So the result is {4}".format(sleepiestElve, sleepTimes[sleepiestElve], sleepingFrequencies[sleepiestElve], sleepingMinutes[sleepiestElve], int(sleepiestElve) * sleepingMinutes[sleepiestElve]))
