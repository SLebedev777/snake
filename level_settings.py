# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:32:45 2020

@author: Семен
"""

class LevelSettings(dict):
    def __init__(self, 
                 level_name,
                 snake_starting_length,
                 food_table,
                 num_starting_food,
                 num_starting_walls,
                 score_needed,
                 max_time,
                 game_speed
                 ):
        self['level_name'] = level_name
        self['snake_starting_length'] = snake_starting_length
        self['food_table'] = food_table
        self['num_starting_food'] = num_starting_food
        self['num_starting_walls'] = num_starting_walls
        self['score_needed'] = score_needed
        self['max_time'] = max_time
        self['game_speed'] = game_speed  # should be between 5 (slow) and 20 (very fast)