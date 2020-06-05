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
GAMEGRIDRECT = pygame.Rect(40, 80, WIDTH-80, HEIGHT-120)
MENURECT = pygame.Rect(80, 120, WIDTH-160, HEIGHT-200)
FPS = 10
FULLSCREEN_MODE = False

# need this before loading any image (resources.py)
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREY = (127, 127, 127)
DARK_GREY = (63, 63, 63)
BROWN = (116, 71, 48)
NAVY = (0, 64, 64)


SNAKE_PART_WIDTH = CELL_SIZE
SNAKE_PART_HEIGHT = CELL_SIZE

SNAKE_CAN_MOVE_ALONE = True  # debug option: snake moves along prev direction if no input

MAIN_DIR = os.getcwd()
DATA_DIR = f'{MAIN_DIR}/data'


# encode opposite directions with negation for easy checking
DIRECTION_NONE = 0
DIRECTION_UP = 1
DIRECTION_DOWN = -1
DIRECTION_LEFT = -2
DIRECTION_RIGHT = 2

