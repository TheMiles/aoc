#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')
parser.add_argument('-c', '--coloumns', type=int, default=50, help='width')
parser.add_argument('-r', '--rows', type=int, default=6, help='height')

args = parser.parse_args()

def rotate(l,n):
    n = n % len(l)
    return l[-n:] + l[:-n]

class Field(object):
    ON     = '#'
    OFF    = '.'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [self.OFF] * width * height

    def __str__(self):
        value = []
        for i in range(self.height):
            value.extend( self.get_row(i) )
            value.append( '\n' )
        return ''.join(value)

    def get_row(self, row):
        row = row % self.height
        index_left = row * self.width
        index_right = (row+1) * self.width
        return self.field[index_left:index_right]

    def set_row(self, row, data):
        if len(data) > self.width: data = data[:self.width]
        row = row % self.height
        index_left  = row * self.width
        index_right = row * self.width + len(data)
        self.field  = self.field[:index_left] + data + self.field[index_right:]

    def get_coloumn(self, coloumn):
        coloumn = coloumn % self.width
        c = []
        for i in range(self.height):
            c.append(self.field[i*self.width+coloumn])
        return c

    def set_coloumn(self, coloumn, data):
        if len(data) > self.height: data = data[:self.height]
        coloumn = coloumn % self.width
        for i,d in enumerate(data):
            self.field[i*self.width+coloumn] = d

def command_rect(f,c):
    dimensions = [ int(x) for x in c[1].split('x') ]
    for i in range(dimensions[1]):
        f.set_row(i, [Field.ON]*dimensions[0])

def command_rotate_row(f, c):
    row = int(c[2][2:])
    n = int(c[4])
    f.set_row(row, rotate(f.get_row(row),n))

def command_rotate_coloumn(f, c):
    coloumn = int(c[2][2:])
    n = int(c[4])
    f.set_coloumn(coloumn, rotate(f.get_coloumn(coloumn),n))

def command_rotate(f,c):
    commands[c[1]](f,c)


commands = { 'rect':command_rect, 'rotate':command_rotate, 'row':command_rotate_row, 'column':command_rotate_coloumn }

f = Field(args.coloumns, args.rows)

for l in [ x.strip() for x in args.file]:
    c = l.split()
    commands[c[0]](f,c)
    print()
    print()
    print(l)
    print(f)

print(len([x for x in str(f) if x == Field.ON]))


# print(f)
