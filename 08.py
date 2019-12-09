#!/usr/bin/python3

import argparse
import numpy as np
from PIL import Image

def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-w','--width', type=int, default=25)
    parser.add_argument('-t','--height', type=int, default=6)

    return parser.parse_args()


def compositeImages(a,b):
    chooser = lambda x,y: y if x == 2 else x
    c = np.array([chooser(d[0],d[1]) for d in zip(a.flatten(),b.flatten())])
    c = c.reshape(a.shape)
    return c


if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x for x in args.input.readlines() ] ))

    for p in lines:

        image = np.array([int(i) for i in p]).reshape(int(len(p)/(args.width*args.height)), args.height, args.width)

        counts = []
        for layer in image:
            u, c = np.unique(layer,return_counts=True)
            counts.append(dict(zip(u,c)))

        zeros= args.width*args.height
        sum  = 0

        # for c in counts:
        #     # print("Layer",c[0] if 0 in c else 0, c[1], c[2], c[1]*c[2], c)
        #     if 0 in c and c[0]< zeros:
        #         sum   = c[1]*c[2]
        #         zeros = c[0]
        # print("Answer:",sum)

        composite = image[0]
        for layer in image[1:]:
            composite = compositeImages(composite,layer)

        im = Image.fromarray(np.uint8(composite*255),'L')
        im.show()