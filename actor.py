# -*- coding: utf-8 -*-
"""
Created on Sat May 23 19:33:37 2020

@author: Семен
"""
import pygame
from game_globals import SCREENRECT

dirtyrects = []

class Actor(pygame.sprite.Sprite):
    def __init__(self, x, y, image, animation=None):
        super().__init__()
        self.image = image
        self.still_image = image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation = animation

    def setpos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def getpos(self):
        return self.rect.x, self.rect.y

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        r = screen.blit(self.image, self.rect)
        dirtyrects.append(r)
        
    def erase(self, screen, background):
        r = screen.blit(background, self.rect, self.rect)
        dirtyrects.append(r)

    def update(self):
        if self.animation is not None and not self.animation.over:
            self.animation.next_tick()
            old_center = self.rect.center
            self.image = self.animation.get_image()
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    
        self.rect = self.rect.clamp(SCREENRECT)
 
    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

