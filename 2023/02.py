#!/usr/bin/python3

import argparse


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()

if __name__ == '__main__':
    args = getArguments()
    lines = list(filter(None, [ x.strip() for x in args.input.readlines() ] ))

    games = {}
    for l in lines:
        l = l[len("Game "):]
        id, draws = l.split(':')
        draws     = draws.split(';')
        draw_list = []

        for d in draws:
            cube_dict = {}
            cubes = d.split(',')
            for c in cubes:
                number, color = c.strip().split(' ')
                cube_dict[color] = int(number)
            draw_list.append(cube_dict)
        games[int(id)] = draw_list

    needed_cubes = []
    for id, game in games.items():
        needed_cube = { 'red': 0, 'green': 0, 'blue': 0 }
        needed_cubes.append(needed_cube)
        for g in game:
            for color, number in g.items():
                if number > needed_cube[color]: needed_cube[color] = number

    power_cubes = [ n['red']*n['green']*n['blue'] for n in needed_cubes ]
    # print(power_cubes)
    print(sum(power_cubes))