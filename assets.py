# -*- coding: utf-8 -*-
"""
Created on Sat May 23 20:45:37 2020

@author: Семен
"""
from actor import Actor
from numpy import random

class Food(Actor):
    def __init__(self, x, y, image, food_type, health=5, score=1):
        super().__init__(x, y, image)
        self.food_type = food_type
        self.health = health  # if health is negative, snake looses HP by eating this fruit
        self.score = score


class FoodFactory:
    """
    Produces various types of fruits, according to production table. 
    For example:
        table = {'apple':  {'image': apple_image, 'health': 5, 'proba': 0.4, 'score': 1},
                 'banana': {'image': banana_image, 'health': 5, 'proba': 0.4},
                 'mushroom': {'image': mushroom_image, 'health': -50, 'proba': 0.2}
                  }

    A fruit can be produced by random, according to its probability.
    Sum of probabilities of all fruit types must be 1 (Multinomial distribution).    
    """
    def __init__(self, table):
        for food_type in table:
            if not all(field in table[food_type] for field in ['image', 'health', 'proba']):
                raise ValueError(f"Missing field in {food_type}")
                
        probas = [table[food_type]['proba'] for food_type in table]
        assert round(sum(probas)) == 1.0
        
        self.table = table
        self.probas = probas
        
    def make(self, x, y, food_type):
        if food_type not in self.table:
            raise ValueError(f"Trying to create unknown food with type: {food_type}")
        return Food(x, y, 
                    self.table[food_type]['image'],
                    food_type,
                    self.table[food_type]['health'],
                    self.table[food_type].get('score', 1)
                    )

    def make_random(self, x, y):
        food_type = random.choice(list(self.table.keys()), 
                                  size = 1, 
                                  p = self.probas)[0]
        return self.make(x, y, food_type)
        

class Wall(Actor):
    pass