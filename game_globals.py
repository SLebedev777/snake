# -*- coding: utf-8 -*-
"""
Created on Sat May 23 19:28:19 2020

@author: Семен
"""

import pygame
from pygame.locals import *
import os


WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
SCREENRECT = pygame.Rect(0, 0, WIDTH, HEIGHT)
FPS = 10

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREY = (127, 127, 127)
DARK_GREY = (63, 63, 63)

PART_TYPES = {'head': GREEN,
              'body': RED,
              'tail': BLUE}

FOOD_TYPES = {'banana': YELLOW}

WALL_TYPES = {'stone': DARK_GREY}

SNAKE_PART_WIDTH = CELL_SIZE
SNAKE_PART_HEIGHT = CELL_SIZE

SNAKE_CAN_MOVE_ALONE = False  # debug option: snake moves along prev direction if no input

MAIN_DIR = os.getcwd()
DATA_DIR = f'{MAIN_DIR}/data'


# encode opposite directions with negation for easy checking
DIRECTION_NONE = 0
DIRECTION_UP = 1
DIRECTION_DOWN = -1
DIRECTION_LEFT = -2
DIRECTION_RIGHT = 2

