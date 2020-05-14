import random
import pygame

"""
MAP has a map of values
    0 - cell outside of boundaries
    1 - empty cell
    2 - gnome
    3 - gold
    4 - wall
    5 - exit
"""


def print_map(map):
    for row in map:
        print(row)


def get_state_size(vision_size):
    return ((vision_size ^ 2) + 1) ^ 2


def get_gnome_vision(map, gnome):
    gnome_vision = []
    for row in range((gnome.vision_size * 2) + 1):
        gnome_vision_row = []
        for col in range((gnome.vision_size * 2) + 1):
            gnome_vision_row.append(map[row + gnome.y][col + gnome.x])
        gnome_vision.append(gnome_vision_row)
    return gnome_vision


def get_gnome_vision_flat(map, gnome):
    gnome_vision_flat = []
    for row in range((gnome.vision_size * 2) + 1):
        for col in range((gnome.vision_size * 2) + 1):
            gnome_vision_flat.append(map[row + gnome.y][col + gnome.x])
    return gnome_vision_flat


def remove_old_gnome(map, gnome):
    map[gnome.y + gnome.vision_size][gnome.x + gnome.vision_size] = 1
    return map


def check_new_cell(map, gnome, option):
    if map[gnome.y + gnome.vision_size][gnome.x + gnome.vision_size] == option:
        return True
    return False


def add_new_gnome(map, gnome):
    map[gnome.y + gnome.vision_size][gnome.x + gnome.vision_size] = 2
    return map


def initialize_map_and_gold(gnome, gold_amount, cells, exit, walls):
    gold = []
    map = initialize_map(cells, gnome.vision_size)
    map = add_exit(map, exit, gnome.vision_size)
    map = add_gnome(map, gnome)
    map = add_walls(map, walls, gnome.vision_size)
    map = add_gold(map, gold_amount)
    print_map(map)
    return map


def initialize_map(cells, vision_size):
    map = []
    # Loop through cells horizontally
    for j in range(cells["y"] + 2 * vision_size):
        map_x_line = []
        # Loop through cells vertically
        for i in range(cells["x"] + 2 * vision_size):
            # Set for outside boundaries
            if i < vision_size or i >= vision_size + cells["x"] or j < vision_size or j >= vision_size + cells["y"]:
                map_x_line.append(0)
            else:
                map_x_line.append(1)
        map.append(map_x_line)
    return map


def add_exit(map, exit, vision_size):
    map[vision_size + exit["y"]][vision_size + exit["x"]] = 5
    return map


def add_gnome(map, gnome):
    map[gnome.vision_size + gnome.y][gnome.vision_size + gnome.x] = 2
    return map


def add_walls(map, walls, vision_size):
    for wall in walls:
        for cell in wall:
            map[vision_size + cell["y"]][vision_size + cell["x"]] = 4
    return map


def add_gold(map, gold_amount):
    def get_empty_cells():
        _empty_cells = []
        for _i in range(len(map)):
            for _j in range(len(map[_i])):
                if map[_i][_j] == 1:
                    _empty_cells.append({"x": _j, "y": _i})
        return _empty_cells

    empty_cells = get_empty_cells()

    for i in range(gold_amount):
        index = random.randrange(len(empty_cells))
        value = empty_cells.pop(index)
        map[value["y"]][value["x"]] = 3
    return map

