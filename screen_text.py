# -*- coding: utf-8 -*-
"""
Created on Sat May 23 20:51:55 2020

@author: Семен
"""
import pygame
from actor import Actor


class ScreenText(Actor):
    def __init__(self, text, x, y, color, size=20):
        if not pygame.font.get_init():
            pygame.font.init()
            
        self.text = text
        self.font = pygame.font.Font(None, size)
        self.color = color
        super().__init__(x, y, self.font.render(text, 0, self.color))

    def set_text(self, text):
        if text != self.text:
            self.text = text
            self.image = self.font.render(text, 0, self.color)
            x, y = self.getpos()
            self.rect = self.image.get_rect().move(x, y)
