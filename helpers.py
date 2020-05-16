import random
import constants
import pygame
import core
from enum import Enum

"""
MAP has a map of values
    0 - cell outside of boundaries
    1 - empty cell
    2 - gnome
    3 - gold
    4 - wall
    5 - exit
"""


class Map(Enum):
    BOUNDARY = 0
    EMPTY = 1
    GNOME = 2
    GOLD = 3
    WALL = 4
    EXIT = 5


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
    map[gnome.y + gnome.vision_size][gnome.x + gnome.vision_size] = Map.EMPTY.value
    return map


def check_new_cell(map, gnome, option):
    if map[gnome.y + gnome.vision_size][gnome.x + gnome.vision_size] == option:
        return True
    return False


def add_new_gnome(map, gnome):
    map[gnome.y + gnome.vision_size][gnome.x + gnome.vision_size] = Map.GNOME.value
    return map


def find_exit_distance(exit, gnome):
    return abs(exit["y"] - gnome.y) + abs(exit["x"] - gnome.x)


def initialize_map_and_gold(gnome, gold_amount, cells, exit, walls):
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
                map_x_line.append(Map.BOUNDARY.value)
            else:
                map_x_line.append(Map.EMPTY.value)
        map.append(map_x_line)
    return map


def add_exit(map, exit, vision_size):
    map[vision_size + exit["y"]][vision_size + exit["x"]] = Map.EXIT.value
    return map


def add_gnome(map, gnome):
    map[gnome.vision_size + gnome.y][gnome.vision_size + gnome.x] = Map.GNOME.value
    return map


def add_walls(map, walls, vision_size):
    for wall in walls:
        for cell in wall:
            map[vision_size + cell["y"]][vision_size + cell["x"]] = Map.WALL.value
    return map


def add_gold(map, gold_amount):
    def get_empty_cells():
        _empty_cells = []
        for _i in range(len(map)):
            for _j in range(len(map[_i])):
                if map[_i][_j] == Map.EMPTY.value:
                    _empty_cells.append({"x": _j, "y": _i})
        return _empty_cells

    empty_cells = get_empty_cells()

    for i in range(gold_amount):
        index = random.randrange(len(empty_cells))
        value = empty_cells.pop(index)
        map[value["y"]][value["x"]] = Map.GOLD.value
    return map


""" DRAWING """


def draw_game(screen, gnome, vision):
    draw_vision(screen, gnome, vision)
    draw_margins(screen)
    draw_scoreboard(screen)
    draw_grid(screen)
    draw_gnome(screen, gnome)
    

def draw_vision(screen, gnome, vision):
    def draw_vision_cell(vision_size):
        pygame.draw.rect(screen, constants.GNOME_VISION_COLOR,
                         ((col + gnome.x - vision_size) * constants.CELL_SIZE + constants.MARGIN,
                          (row + gnome.y - vision_size) * constants.CELL_SIZE + constants.MARGIN,
                          constants.CELL_SIZE, constants.CELL_SIZE))

    def draw_gold(vision_size):
        pygame.draw.circle(screen, constants.GOLD_COLOR,
                           [int((gnome.x + col - vision_size) * constants.CELL_SIZE + constants.CELL_SIZE / 2) +
                            constants.MARGIN,
                            int((gnome.y + row - vision_size) * constants.CELL_SIZE + constants.CELL_SIZE / 2) +
                            constants.MARGIN],
                           int(constants.GOLD_RADIUS))

    def draw_exit():
        pygame.draw.rect(screen, constants.EXIT_COLOR, ((col + gnome.x - gnome.vision_size) * constants.CELL_SIZE
                                                        + constants.MARGIN,
                                                        (row + gnome.y - gnome.vision_size) * constants.CELL_SIZE
                                                        + constants.MARGIN,
                                                        constants.CELL_SIZE, constants.CELL_SIZE))

    def draw_wall():
        pygame.draw.rect(screen, constants.WALL_COLOR, ((col + gnome.x - gnome.vision_size) * constants.CELL_SIZE
                                                        + constants.MARGIN,
                                                        (row + gnome.y - gnome.vision_size) * constants.CELL_SIZE
                                                        + constants.MARGIN,
                                                        constants.CELL_SIZE, constants.CELL_SIZE))
    
    for row in range(len(vision)):
        for col in range(len(vision[row])):
            draw_vision_cell(len(vision[0]) // 2)
            if vision[row][col] == Map.GOLD.value:
                draw_gold(len(vision[0]) // 2)
            elif vision[row][col] == Map.EXIT.value:
                draw_exit()
            elif vision[row][col] == Map.WALL.value:
                draw_wall()


def draw_margins(screen):
    # Left line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, constants.MARGIN,
                                                           constants.MARGIN, constants.GAME_PLAY_HEIGHT))
    # Right line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND,
                     (constants.MARGIN + constants.GAME_PLAY_WIDTH, constants.MARGIN,
                      constants.MARGIN, constants.GAME_PLAY_HEIGHT))
    # Top line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, 0,
                                                           constants.MARGIN * 2 + constants.GAME_PLAY_WIDTH,
                                                           constants.MARGIN))
    # Bottom line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, constants.MARGIN + constants.GAME_PLAY_HEIGHT,
                                                           constants.MARGIN * 2 + constants.GAME_PLAY_WIDTH,
                                                           constants.MARGIN))
    

def draw_scoreboard(screen):
    pygame.draw.rect(screen, constants.SCOREBOARD_BACKGROUND, (0, constants.GAME_PLAY_HEIGHT + constants.MARGIN * 2,
                                                               constants.GAME_PLAY_WIDTH + constants.MARGIN * 2,
                                                               constants.SCOREBOARD_HEIGHT))
    

def draw_grid(screen):
    # Draws a grid to separate each game cell
    for i in range(constants.CELLS["x"] - 1):
        pygame.draw.rect(screen, constants.GRID_LINE_COLOR, (constants.MARGIN + i * constants.CELL_SIZE +
                                                             constants.CELL_SIZE - constants.GRID_LINE_WIDTH / 2,
                                                             constants.MARGIN,
                                                             constants.GRID_LINE_WIDTH,
                                                             constants.CELL_SIZE * constants.CELLS["y"]))

    for i in range(constants.CELLS["y"] - 1):
        pygame.draw.rect(screen, constants.GRID_LINE_COLOR, (constants.MARGIN,
                                                             constants.MARGIN + i * constants.CELL_SIZE +
                                                             constants.CELL_SIZE - constants.GRID_LINE_WIDTH / 2,
                                                             constants.CELL_SIZE * constants.CELLS["x"],
                                                             constants.GRID_LINE_WIDTH))


def draw_gnome(screen, gnome):
    pygame.draw.circle(screen, constants.GNOME_COLOR,
                       [int(gnome.x * constants.CELL_SIZE + constants.CELL_SIZE / 2) + constants.MARGIN,
                        int(gnome.y * constants.CELL_SIZE + constants.CELL_SIZE / 2) + constants.MARGIN],
                       int(constants.GNOME_RADIUS))


""" TEXT """


def update_gold_text_placeholder(font):
    text = font.render("GOLD: ", True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = (constants.SCREEN_WIDTH // 2 - constants.FONT_SIZE * 1.5 - constants.TEXT_WIDTH,
                        (constants.SCOREBOARD_HEIGHT + constants.SCREEN_HEIGHT // 2) - constants.FONT_SIZE * 1.5)
    return text, text_rect


def update_step_text_placeholder(font):
    text = font.render("STEP: ", True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = (constants.SCREEN_WIDTH // 2 - constants.FONT_SIZE * 1.5 - constants.TEXT_WIDTH,
                        (constants.SCOREBOARD_HEIGHT + constants.SCREEN_HEIGHT // 2) + constants.FONT_SIZE // 2)
    return text, text_rect


def update_exit_text_placeholder(font):
    text = font.render("EXIT: ", True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = (constants.SCREEN_WIDTH // 2 + constants.FONT_SIZE * 2.5,
                        (constants.SCOREBOARD_HEIGHT + constants.SCREEN_HEIGHT // 2) - constants.FONT_SIZE * 1.5)
    return text, text_rect


def update_gold_text(font, collected_gold):
    text = font.render(str(collected_gold), True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = ((constants.SCREEN_WIDTH // 2) - constants.FONT_SIZE * 1.5,
                        (constants.SCOREBOARD_HEIGHT + constants.SCREEN_HEIGHT // 2) - constants.FONT_SIZE * 1.5)
    return text, text_rect


def update_step_text(font, step_counter):
    text = font.render(str(step_counter), True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = ((constants.SCREEN_WIDTH // 2) - constants.FONT_SIZE * 1.5,
                        (constants.SCOREBOARD_HEIGHT + constants.SCREEN_HEIGHT // 2) + constants.FONT_SIZE // 2)
    return text, text_rect


def update_exit_text(font, exit_distance):
    text = font.render(str(exit_distance), True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = ((constants.SCREEN_WIDTH // 2) + constants.FONT_SIZE * 2.5 + constants.TEXT_WIDTH,
                        (constants.SCOREBOARD_HEIGHT + constants.SCREEN_HEIGHT // 2) - constants.FONT_SIZE * 1.5)
    return text, text_rect
