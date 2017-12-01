#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()

regexes = [re.compile(r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)"),
           re.compile(r"value (\d+) goes to bot (\d+)")]


bots   = dict()
output = dict()

class Bot(object):
    def __init__(self,id):
        self.id = id
        self.values = []
        self.commands = []

    def event_loop(self):
        if len(self.values) == 2 and self.commands:
            c = self.commands.pop(0)

            print(self.id, self.values, c)

            def give_to(receipient, id, value):
                if receipient == 'bot':
                    bot = bots.get(id,Bot(id))
                    bot.add_value(value)
                else:
                    output[id] = value

            v = self.values[:]
            self.values = []
            give_to(c[0],c[1],v[0])
            give_to(c[2],c[3],v[1])

            return True
        else:
            return False


    def add_value(self,value):
        self.values.append(value)
        self.values.sort()

    def add_command(self,command):
        self.commands.append(command)


for l in [ x.strip() for x in args.file]:
    m = regexes[0 if l[0]=='b' else 1].findall(l)
    if not m:
        print("Oh regex didn't work for line",l)
        continue

    if l[0]=='v':
        value = int(m[0][0])
        botID = int(m[0][1])
        bot   = bots.get(botID,Bot(botID))
        bot.add_value(value)
        bots[botID] = bot

    else:
        botID      = int(m[0][0])
        receipLow  = m[0][1]
        idLow      = int(m[0][2])
        receipHigh = m[0][3]
        idHigh     = int(m[0][4])
        bot        = bots.get(botID,Bot(botID))
        bot.add_command((receipLow,idLow,receipHigh,idHigh))
        bots[botID] = bot

while any(x.event_loop() for x in bots.values()):
    pass

for x in bots.values():
    print(x.id, x.values, x.commands)
print(output)

