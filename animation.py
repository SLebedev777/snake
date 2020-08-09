# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 23:45:49 2020

@author: Семен
"""

import pygame
from collections import namedtuple

Frame = namedtuple('Frame', ['img_id', 'duration'])

class Animation:
    '''
    Class that changes images according to duration of each frame,
    measured in game loop iterations.

    Parameters
    ----------
    id2image_dict : dict
        Dictionary containing images (Surfaces) for animation and their ids.
        id2image_dict[img_id] -> pygame.Surface
    frames : list
        Description of animation sequence.
        [(img_id, duration in game loop iters), ...]
    loops : bool, optional
        Number of loops to play sequence. None - endless cycle
    '''
    def __init__(self, id2image_dict, frames, loops=None):
        assert all(img_id in id2image_dict for img_id, duration in frames)
        self.id2image_dict = id2image_dict
        self.frames = [Frame(img_id, duration) for img_id, duration in frames]
        self.tick = 0
        self.curr_frame_id = 0
        self.loops = loops
        self.loop = 0
        
    def rewind(self):
        self.tick = 0
        self.curr_frame_id = 0
        
    def next_tick(self):
        if self.over:
            self.rewind()
            return
                
        self.tick += 1
        if self.tick > self.curr_frame.duration - 1:
            self.tick = 0
            self.curr_frame_id += 1
        if self.curr_frame_id > len(self.frames) - 1:
            if self.loops is not None:
                self.loop += 1
            self.rewind()
        
    def get_image(self):
        return self.id2image_dict[self.curr_frame.img_id]
    
    @property
    def curr_frame(self):
        return self.frames[self.curr_frame_id]
    
    @property
    def over(self):
        return self.loops is not None and self.loop >= self.loops
        