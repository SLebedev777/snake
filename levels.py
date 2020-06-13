# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 21:56:51 2020

@author: Семен
"""

from level_settings import LevelSettings
from resources import *

default_food_table = {'apple':  {'image': apple_image, 'health': 1, 'proba': 0.4},
                      'banana': {'image': banana_image, 'health': 1, 'proba': 0.4},
                      'mushroom': {'image': mushroom_image, 'health': -50, 'proba': 0.15},
                      'potion': {'image': potion_image, 'health': 50, 'proba': 0.05},
                      }


default_level_settings = LevelSettings(
                 level_name='Level 1',
                 snake_starting_length=3,
                 food_table=default_food_table,
                 num_starting_food=10,
                 num_starting_walls=5,
                 score_needed=10,
                 max_time=120,
                 game_speed=glb.SNAKE_SHIFT_THRESHOLD_X / 7
                 )

level1 = default_level_settings
level2 = LevelSettings(
                 level_name='Level 2',
                 snake_starting_length=3,
                 food_table=default_food_table,
                 num_starting_food=8,
                 num_starting_walls=6,
                 score_needed=15,
                 max_time=90,
                 game_speed=glb.SNAKE_SHIFT_THRESHOLD_X / 6
                 )

level3_food_table =  {'apple':  {'image': apple_image, 'health': 1, 'proba': 0.35},
                      'banana': {'image': banana_image, 'health': 1, 'proba': 0.30},
                      'ananas': {'image': ananas_image, 'health': 1, 'score': 3, 'proba': 0.1},
                      'mushroom': {'image': mushroom_image, 'health': -50, 'proba': 0.15},
                      'potion': {'image': potion_image, 'health': 50, 'proba': 0.05},
                      'portal': {'image': portal_image, 'health': 0, 'proba': 0.05, 'once': True},
                      }

level3 = LevelSettings(
                 level_name='Level 3',
                 snake_starting_length=3,
                 food_table=level3_food_table,
                 num_starting_food=7,
                 num_starting_walls=8,
                 score_needed=20,
                 max_time=60,
                 game_speed=glb.SNAKE_SHIFT_THRESHOLD_X / 5.5
                 )

level4 = LevelSettings(
                 level_name='Level 4',
                 snake_starting_length=3,
                 food_table=level3_food_table,
                 num_starting_food=5,
                 num_starting_walls=10,
                 score_needed=30,
                 max_time=60,
                 game_speed=glb.SNAKE_SHIFT_THRESHOLD_X / 5
                 )


LEVELS = [level1, 
          level2,
          level3,
          level4]