# -*- coding: utf-8 -*-
"""
Created on Sat May 23 20:51:55 2020

@author: Семен
"""
import pygame
from actor import Actor
from copy import copy

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


class BitmapFont:
    """
    Class that maps keyboard characters onto images,
    rendering strings of text.
    """
    def __init__(self, char2img_dict, spacing, double_size=False):
        self.char2img_dict = copy(char2img_dict)
        self.spacing = spacing
        if double_size:
            for ch, img in self.char2img_dict.items():
                nw = img.get_rect().width * 2
                nh = img.get_rect().height * 2
                self.char2img_dict[ch] = pygame.transform.scale(img,
                                                                (nw, nh))
        self.space_width = self.char2img_dict['A'].get_rect().width
        self.height = self.char2img_dict['A'].get_rect().height
        
    def render(self, text, left=0, top=0, surf=None):
        x = left
        y = top
        text = text.upper()
        if surf is None:
            x = 0
            y = 0
            surf_width = 0
            for ch in text:
                if ch is not ' ':
                    surf_width += self.char2img_dict[ch].get_rect().width
                else:
                    surf_width += self.space_width
                surf_width += self.spacing
            surf_width += 2*self.spacing
            surf = pygame.Surface((surf_width, self.height))  # TODO: width detection
            backcolor = (127, 127, 127)
            surf.fill(backcolor)
            surf.set_colorkey(backcolor)
        for i, ch in enumerate(text):
            if ch is not ' ':
                char_img = self.char2img_dict[ch]
                surf.blit(char_img, (x, y))
                x += char_img.get_rect().width
            else:
                x += self.space_width
            x += self.spacing
        #pygame.draw.rect(surf, (255, 255, 255), (left, top, x - left, self.height), 1)
        return surf
                

class ScreenTextBitmapFont(Actor):
    """
    Adapter of ScreenText that handles bitmap font.
    """
    def __init__(self, text, x, y, bitmap_font):            
        self.text = text
        self.font = bitmap_font
        super().__init__(x, y, bitmap_font.render(text))

    def set_text(self, text):
        if text != self.text:
            self.text = text
            self.image = self.font.render(text)
            x, y = self.getpos()
            self.rect = self.image.get_rect().move(x, y)
    
            