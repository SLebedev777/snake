# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 00:39:47 2020

@author: Семен
"""

import numpy as np

class GameGrid:
    def __init__(self, rect, cell_size):
        assert rect.width % cell_size == 0
        assert rect.height % cell_size == 0
        
        self.rect = rect
        self.cell_size = cell_size
        self.n_cells_x = rect.width // cell_size
        self.n_cells_y = rect.height // cell_size
        self.shape = (self.n_cells_x, self.n_cells_y)
        self.cells = np.zeros(self.shape)

       
    def align(self, actor):
        # align actor to the nearest grid cell
        dx = actor.rect.x % self.cell_size
        dy = actor.rect.y % self.cell_size
        actor.move(-dx, -dy)
        actor.rect = actor.rect.clamp(self.rect)
        return actor

    def bound2rect(self, cix, ciy):
        # bound cell indices by grid outer rect
        bcix = min(max(0, cix), self.n_cells_x - 1)
        bciy = min(max(0, ciy), self.n_cells_y - 1)
        return bcix, bciy
        
    def xy2cell(self, x, y):
        # transform xy coordinates to cell indices
        dx = x % self.cell_size
        dy = y % self.cell_size
        cix = (x - dx) // self.cell_size
        ciy = (y - dy) // self.cell_size
        cix, ciy = self.bound2rect(cix, ciy)
        return cix, ciy
    
    def cell2xy(self, cix, ciy):
        # transform cell indices to xy coordinates
        cix, ciy = self.bound2rect(cix, ciy)
        x = cix * self.cell_size
        y = ciy * self.cell_size
        return x, y

    def cell_occupied(self, cix, ciy):
        cix, ciy = self.bound2rect(cix, ciy)
        return self.cells[cix, ciy] > 0
        
    def occupy_cell(self, cix, ciy):
        cix, ciy = self.bound2rect(cix, ciy)
        self.cells[cix, ciy] = 1
        
    def release_cell(self, cix, ciy):
        cix, ciy = self.bound2rect(cix, ciy)
        self.cells[cix, ciy] = 0

    def get_random_free_cell(self):
        free_indices = np.where(self.cells.ravel() == 0)[0]
        if free_indices.size > 0:
            choice = np.random.choice(free_indices)
            return np.unravel_index([choice], self.shape)
        return None
