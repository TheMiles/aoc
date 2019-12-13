#!/usr/bin/python3

import argparse
import intcode as ic
from collections import defaultdict
import numpy as np
from PIL import Image
from time import sleep
import sys, pygame
pygame.init()


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    parser.add_argument('-a','--auto', action='store_true')
    parser.add_argument('-s','--sleeptime', type=float, default=0.15)

    return parser.parse_args()



class Game(object):

    def __init__(self, program):
        self.input  = ic.Fifo()
        self.output = ic.Fifo()
        self.cpu    = ic.CPU(program, self.input, self.output)

        self.cpu.run()
        o = np.array(self.output.buffer).reshape(int(len(self.output.buffer)/3),3)
        x = o[:,0]
        y = o[:,1]
        self.size = np.array([max(x),max(y)])+1
        self.sizeMul = 32

        self.auto      = False
        self.ballPos   = 0
        self.paddlePos = 0

        self.images = {
            0: pygame.image.load("data/empty.png"),
            1: pygame.image.load("data/wall.png"),
            2: pygame.image.load("data/tile.png"),
            3: pygame.image.load("data/paddle.png"),
            4: pygame.image.load("data/ball.png"),
        }

        print("Size:",self.size)
        self.screen = pygame.display.set_mode(self.size*self.sizeMul)
        self.screen.fill((0,0,0))
        self.updateScreen()
        self.sleeptime = 0.15

        self.output.reset()
        self.cpu = ic.CPU(program, self.input, self.output)
        self.cpu.writeMem(0,2)


    def updateScreen(self):
        if self.output.empty(): return

        while not self.output.empty():
            x = self.output.pop()
            y = self.output.pop()
            v = self.output.pop()

            if(x<0):
                print("Score", v)
                continue

            if v==4: self.ballPos   = x
            if v==3: self.paddlePos = x

            self.screen.blit(self.images[v],(x*self.sizeMul,y*self.sizeMul))
        pygame.display.flip()

    def run(self):

        while True:
            joystik = 0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:  joystik = -1
                    if event.key == pygame.K_RIGHT: joystik =  1

            if self.auto:
                if   self.paddlePos == self.ballPos: joystik =  0
                elif self.paddlePos <  self.ballPos: joystik =  1
                elif self.paddlePos >  self.ballPos: joystik = -1


            if self.cpu.isHalted(): sys.exit()
            self.input.push(joystik)
            self.cpu.run()
            self.updateScreen()
            sleep(self.sleeptime)





if __name__ == '__main__':
    args = getArguments()
    lines = [[ int(y) for y in x.strip().split(',')] for x in list(filter(None, [ r for r in args.input.readlines() ] )) ]

    for p in lines:

        game = Game(p)
        game.auto = args.auto
        game.sleeptime = args.sleeptime
        game.run()


