#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()

class Field(object):
    self.ON     = '#'
    self.OFF    = '.'

    def __init__(self, width=50, height=6)
        self.width = width
        self.height = height
        self.field = [OFF] * width * height

    def __str__(self):

        value = ''
        return value


f = Field()
print(f)