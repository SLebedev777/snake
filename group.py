# -*- coding: utf-8 -*-
"""
Created on Fri May 29 18:17:32 2020

@author: Семен
"""
from actor import Actor

class Group(list):
    """
    Group of sprites (actors).
    """
    def clear(self, screen, background):
        for actor in self:
            actor.erase(screen, background)
            actor.update()
    
    def draw(self, screen):
        for actor in self:
            actor.draw(screen)
