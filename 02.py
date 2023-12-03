#!/usr/bin/python3

import argparse


def getArguments():
    parser = argparse.ArgumentParser(description='Advent of code')
    parser.add_argument('input', metavar='file', type=argparse.FileType('r'))
    return parser.parse_args()

available_cubes = {
    'red': 12,
    'green': 13, 
    'blue': 14
}


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

    valid_games = []
    for id, game in games.items():
        valid = True
        for g in game:
            for color, number in g.items():
                if number > available_cubes[color]: valid = False
        if valid: valid_games.append(id)

    print(sum(valid_games))