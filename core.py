import constants
import helpers
import pygame
import random
import numpy as np
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


class Gnome:
    def __init__(self, gnome):
        self.x = gnome["x"]
        self.y = gnome["y"]
        self.vision_size = gnome["vision_size"]

    # Note: there is no checking for boundaries. All required checks must be done before calling this method
    def move(self, direction):
        # Move the gnome in the given direction
        if direction == 0:
            self.x -= 1
        elif direction == 1:
            self.y -= 1
        elif direction == 2:
            self.x += 1
        elif direction == 3:
            self.y += 1


class Model:
    """Creates an example of a deep learning model instance"""

    def __init__(self):
        self.placeholder = True

    # predict function will be replaced by trained model
    def predict(self, state):
        action = random.randrange(4)
        return action


class Game:
    def __init__(self, mode=constants.GAME_MODE, speed=constants.GAME_SPEED, gold_amount=constants.GOLD_AMOUNT):
        self.__mode = mode
        self.__gold_amount = gold_amount
        self.__action_frequency = constants.FPS / speed
        self.gnome = Gnome(constants.GNOME)
        self.map = helpers.initialize_map_and_gold(
            self.gnome, gold_amount, constants.CELLS, constants.EXIT, [constants.WALL_1, constants.WALL_2])

        self.step_counter = 0
        self.collected_gold = 0
        # state_size is input of training model
        # 4 stands for gnome_x, gnome_y, distance_to_exit, collected_gold
        self.state_size = helpers.get_state_size(constants.GNOME_VISION_SIZE) + 4
        # action_size is output of training model
        self.action_size = len(constants.POSSIBLE_ACTIONS["gnome"])
        self.model = Model()

    def get_gnome_vision(self):
        return helpers.get_gnome_vision(self.map, self.gnome)

    def get_gnome_vision_flat(self):
        return helpers.get_gnome_vision_flat(self.map, self.gnome)

    def step(self, direction):
        def make_step(_direction):
            self.map = helpers.remove_old_gnome(self.map, self.gnome)
            self.gnome.move(_direction)
            self.step_counter += 1

        if direction in constants.POSSIBLE_ACTIONS["gnome"]:
            # Move gnome in the given direction if not next ot the wall
            if direction == 0:
                # Check if there is a wall or boundary on the left by finding the center of the gnome's vision
                if self.get_gnome_vision()[self.gnome.vision_size][self.gnome.vision_size - 1] != 0 or \
                        self.get_gnome_vision()[self.gnome.vision_size][self.gnome.vision_size - 1] != 4:
                    make_step(0)

            elif direction == 1:
                # Check if there is a wall or boundary on the top by finding the center of the gnome's vision
                if self.get_gnome_vision()[self.gnome.vision_size - 1][self.gnome.vision_size] != 0 or \
                        self.get_gnome_vision()[self.gnome.vision_size - 1][self.gnome.vision_size] != 4:
                    make_step(1)

            elif direction == 2:
                # Check if there is a wall or boundary on the right by finding the center of the gnome's vision
                if self.get_gnome_vision()[self.gnome.vision_size][self.gnome.vision_size + 1] != 0 or \
                        self.get_gnome_vision()[self.gnome.vision_size][self.gnome.vision_size + 1] != 4:
                    make_step(2)

            elif direction == 3:
                # Check if there is a wall or boundary on the bottom by finding the center of the gnome's vision
                if self.get_gnome_vision()[self.gnome.vision_size + 1][self.gnome.vision_size] != 0 or \
                        self.get_gnome_vision()[self.gnome.vision_size + 1][self.gnome.vision_size] != 4:
                    make_step(3)

            # Check if gnome has stepped on a gold
            if helpers.check_new_cell(self.map, self.gnome, Map.GOLD):
                self.collected_gold += 1
                print('collected gold - ', self.collected_gold)

            # Check if gnome has stepped on the exit
            if helpers.check_new_cell(self.map, self.gnome, Map.EXIT):
                print('Congratulations!\nExit Found!')

            print('step counter -', self.step_counter)

            self.map = helpers.add_new_gnome(self.map, self.gnome)

