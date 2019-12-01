#!/usr/bin/python3

import argparse
import re
from collections import defaultdict

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-w','--workers', default=5, type=int)
    parser.add_argument('-b','--basetime', default=60, type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args         = getArguments()
    lines        = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))
    licenseFiles = [ [int(y) for y in x] for x in (l.split(' ') for l in lines) ]

    for license in licenseFiles:

        licenseSum     = 0
        nodeValues     = []
        nodesToRead    = [1]
        metaDataToRead = []
        numChildren    = []
        i              = 0
        while i < len(license):

            # print("i {0}: {1}  with nodesToRead {2} metaDataToRead {3} numChildren {5} nodeValues {6} sum {4}".format(i,license[i],nodesToRead,metaDataToRead,licenseSum, numChildren, nodeValues))

            if nodesToRead[-1] == 0:
                numReadMetaData = metaDataToRead.pop()
                nodeSum = 0
                nc = numChildren[-1]

                for m in range(numReadMetaData):
                    md = license[i+m]
                    licenseSum += md
                    # print("{3} Metadata {0} nodeSum {1} nodeValues {2}".format(md, nodeSum, nodeValues, i+m))
                    if nc == 0:
                        nodeSum += md
                    elif md <= nc:
                        nodeSum += nodeValues[-nc+md-1]

                i += numReadMetaData
                if nc > 0:
                    nodeValues = nodeValues[:-nc]
                nodeValues.append(nodeSum)
                numChildren.pop()
                nodesToRead.pop()
                continue

            nodesToRead[-1] -= 1
            nodesToRead.append(license[i])
            numChildren.append(license[i])
            metaDataToRead.append(license[i+1])
            i += 2

        print("The license sum is ", licenseSum, " and the value ", nodeValues[0])