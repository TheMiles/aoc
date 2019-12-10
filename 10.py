#!/usr/bin/python3

import argparse
import numpy as np


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'), nargs='?')
    return parser.parse_args()

def removeAsteroid(remove, asteroids):
    asteroids = asteroids[:]
    found = [np.array_equal(remove,x) for x in asteroids]
    if any(found):
        asteroids.pop(found.index(True))
    return asteroids


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x for x in args.input.readlines() ] ))

    asteroids = []

    for y,l in enumerate(lines):
        for x, s in enumerate(l):
            if s=='#':
                asteroids.append(np.array([x,y]))

    # size = np.amax(np.array(asteroids),0)
    # print(size)

    results = []
    count   = 0
    for a in asteroids:
        remaining = asteroids[:]
        remaining = removeAsteroid(a,remaining)
        for o in remaining[:]:
            diff_o   = o-a
            length_o = np.linalg.norm(diff_o)
            dir_o    = diff_o / length_o

            for p in remaining[:]:
                if all(np.equal(o,p)): continue

                diff_p   = p-a
                length_p = np.linalg.norm(diff_p)
                dir_p    = diff_p / length_p

                if np.allclose(dir_p,dir_o) and length_p > length_o:
                    remaining = removeAsteroid(p,remaining)


        count += 1
        # print("{}%".format(int(100*(count/len(asteroids)))))
        results.append(len(remaining))

    i = results.index(max(results))
    print(asteroids[i], results[i])
