# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 10:52:02 2020

@author: Семен
"""
import pygame

class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime, gravity=0, border_size=0,
                 vx_func=None, vy_func=None, size_func=None, color_func=None, rect=None,
                 border_size_func=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.gravity = gravity
        self.vx_func = vx_func
        self.vy_func = vy_func
        self.size_func = size_func
        self.color_func = color_func
        self.rect = rect
        self.border_size = border_size
        self.border_size_func = border_size_func
        
    def update(self):
        if not self.alive:
            return
        if self.vx_func is not None:
            self.vx = self.vx_func(self.vx)

        if self.vy_func is not None:
            self.vy = self.vy_func(self.vy)
        self.vy += self.gravity

        if self.size_func is not None:
            self.size = self.size_func(self.size)
        self.size = max(0, self.size)

        if self.color_func is not None:
            self.color = self.color_func(self.color)
        self.color = [max(0, c) for c in self.color] 

        if self.border_size_func is not None:
            self.border_size = self.border_size_func(self.border_size, self.size)
        self.border_size = max(0, self.border_size)
        self.border_size = min(self.size, self.border_size)
        
        self.x += self.vx
        self.y += self.vy
        
        self.lifetime -= 1
        self.lifetime = max(0, self.lifetime)
        
    def draw(self, surface):
        if self.alive:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 
                               int(self.size), int(self.border_size))
    
    @property
    def alive(self):
        return self.lifetime > 0 and \
            (self.rect.collidepoint(self.x, self.y) if self.rect is not None else True)