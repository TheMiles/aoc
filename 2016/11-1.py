#!/usr/bin/env python3

import argparse
import re
import itertools
import copy

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'),
                    help='the input file')

args = parser.parse_args()

r = re.compile(r"a (\w+)-compatible (microchip)|a (\w+) (generator)")

class House(object):

    def __init__(self):
        self.elements = set()
        self.floors   = []
        self.elevator = 0

    def __str__(self):

        floor_layout = ''
        for i, f in reversed(list(enumerate(self.floors))):
            floor_layout += 'F' + str(i+1) + ' '
            floor_layout += 'E ' if self.elevator == i else '  '
            for e in self.elements:
                floor_layout += e+'G ' if (e+'G') in f else '.  '
                floor_layout += e+'M ' if (e+'M') in f else '.  '
            floor_layout += '\n'
        return floor_layout

    def __eq__(self,other):
        return self.floors == other.floors and self.elevator == other.elevator

    def is_possible(self):
        for f in self.floors:
            disconnected_microchips = False
            generators_found        = False
            for i in f:
                if i[1] == 'M':
                    wanted_generator = i[0]+'G'
                    disconnected_microchips |= wanted_generator not in f
                if i[1] == 'G':
                    generators_found = True
            return not (disconnected_microchips and generators_found)

    def get_possible_step(self):
        candidates = []
        f = self.floors[self.elevator]
        moved_items = list(itertools.product(f,repeat=2))
        moved_items = [list(set(x)) for x in moved_items]
        next_elevator = []
        if self.elevator < 3: next_elevator.append(self.elevator+1)
        if self.elevator > 0: next_elevator.append(self.elevator-1)

        for e in next_elevator:
            for items in moved_items:
                h = copy.deepcopy(self)
                h.elevator = e
                for i in items:
                    h.floors[self.elevator].remove(i)
                    h.floors[e].append(i)

                if h.is_possible():
                    candidates.append(h)
        return candidates

    def is_final_state(self):
        return self.elevator == 3 and self.floors[3] and not all(len(x)==0 for x in self.floors[:2])

    def do_iteration(self, i):
        
        groundhog_day.append(self)
        i += 1

        if self.is_final_state(): 
            print("Final state reached in {0} steps".format(i))
            print(self)
            # groundhog_day.remove(self)
            return

        for s in self.get_possible_step():

            if s in groundhog_day:
                continue

            s.do_iteration(i)

        # groundhog_day.remove(self)
        return

groundhog_day = []


h = House()
for i,l in enumerate([ x.strip() for x in args.file]):
    h.floors.append([])
    match = r.findall(l)
    for m in match:
        element   =  (m[0] if m[0] else m[2])[0].upper()
        microchip = 'M' if m[1] else 'G'
        h.elements.add( element )
        h.floors[i].append(element+microchip)

print(h)
h.do_iteration(0)
