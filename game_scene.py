# -*- coding: utf-8 -*-
"""
Created on Fri May 29 18:27:29 2020

@author: Семен
"""

import pygame

import game_globals as glb
from game_grid import GameGrid
from actor import dirtyrects
from snake import SnakePart, Snake
from assets import Food, FoodFactory, Wall
from screen_text import ScreenText

from scene import Scene
from scene_manager import SceneManager
from group import Group
from splash import you_loose_splash_screen, you_win_splash_screen, final_splash_screen

from timer import RepeatedTimer

# load once all images and sounds
from resources import *

from levels import *

class GameScene(Scene):
    def __init__(self, rect, levels):
        super().__init__(rect)
        self.levels = levels
        self.curr_level_index = 0
        self.num_levels = len(levels)
        
    def build(self, level=None):
        level = self.levels[self.curr_level_index] if level is None else level
        self.level_name = level['level_name']
        
        self.grid = GameGrid(glb.GAMEGRIDRECT, glb.CELL_SIZE)

        # place head of the snake in the center and align to the grid    
        snake_x, snake_y = self.grid.cell2xy(*self.grid.xy2cell(glb.GAMEGRIDRECT.centerx, 
                                                      glb.GAMEGRIDRECT.centery))
        
        # create snake parts
        head = SnakePart(snake_x, snake_y, head_image, glb.DIRECTION_UP, glb.DIRECTION_UP,
                         dir2img_head)
        neck = SnakePart(snake_x, snake_y + glb.SNAKE_PART_HEIGHT, 
                         body_straight_image, glb.DIRECTION_UP, glb.DIRECTION_UP,
                         dir2img_body)
        body = SnakePart(snake_x, snake_y + glb.SNAKE_PART_HEIGHT*2, 
                         body_straight_image, glb.DIRECTION_UP, glb.DIRECTION_UP,
                         dir2img_body)
        tail = SnakePart(snake_x, snake_y + glb.SNAKE_PART_HEIGHT*3, 
                         tail_image, glb.DIRECTION_UP, glb.DIRECTION_UP,
                         dir2img_tail)
        parts = [head, neck, body, tail]
        
        self.snake = Snake(parts, speed=level['game_speed'])
        self.group_snake = Group([self.snake])

        for part in self.snake.parts:
            self.grid.occupy_cell(*self.grid.xy2cell(*part.getpos()))
    
        # create some food
        self.food = Group()
        food_table = level.get('food_table', default_food_table)
        self.food_factory = FoodFactory(food_table)
        
        for _ in range(level['num_starting_food']):
            fc = self.grid.get_random_free_cell()
            if fc:
                food_x, food_y = self.grid.cell2xy(*fc)
                self.grid.occupy_cell(*fc)
                self.food.append(self.food_factory.make_random(food_x, food_y))
    
        # create some walls
        self.walls = Group()
        for _ in range(level['num_starting_walls']):
            fc = self.grid.get_random_free_cell()
            if fc:
                wall_x, wall_y = self.grid.cell2xy(*fc)
                self.grid.occupy_cell(*fc)
                self.walls.append( Wall(wall_x, wall_y, wall_image) )
    
        self.score = 0
        self.score_needed = level['score_needed']
                            
        # tile background with sand texture
        for cix in range(self.grid.n_cells_x):
            for ciy in range(self.grid.n_cells_y):
                self.background.blit(ground_image, self.grid.cell2xy(cix, ciy))
        # make bounding fence with electricity
        for cix in range(self.grid.n_cells_x):
            self.background.blit(fence_horiz_image, self.grid.cell2xy(cix, -1, False))
            self.background.blit(fence_horiz_image_flip_v, self.grid.cell2xy(cix, self.grid.n_cells_y, False))
        for ciy in range(self.grid.n_cells_y):
            self.background.blit(fence_vert_image, self.grid.cell2xy(-1, ciy, False))
            self.background.blit(fence_vert_image_flip_h, self.grid.cell2xy(self.grid.n_cells_x, ciy, False))
        self.background.blit(fence_corner_image, self.grid.cell2xy(-1, -1, False))
        self.background.blit(fence_corner_image_flip_h, self.grid.cell2xy(self.grid.n_cells_x, -1, False))
        self.background.blit(fence_corner_image_flip_v, self.grid.cell2xy(-1, self.grid.n_cells_y, False))
        self.background.blit(fence_corner_image_flip_hv, self.grid.cell2xy(self.grid.n_cells_x, self.grid.n_cells_y, False))

        # reset timer
        self.time_elapsed = 0
        self.max_time = level['max_time']
        if self.timer is not None and self.timer.is_running:
            self.timer.stop()
        self.timer = RepeatedTimer(1, self.increase_time, None)
        
        # reset texts
        self.text_score = ScreenText(f'ОЧКОВ: {self.score} из {self.score_needed}', 
                                     10, 20, glb.WHITE)
        self.text_health = ScreenText(f'ЗДОРОВЬЕ: {self.snake.health}', 650, 20, glb.WHITE)        
        self.text_time = ScreenText(f'ВРЕМЯ: {self.time_elapsed} сек', glb.WIDTH//2, 20, glb.WHITE)        
        self.text_level_name = ScreenText(f'{self.level_name}', glb.WIDTH//4, 20, glb.WHITE)
        self.texts =  Group([self.text_score, self.text_health, 
                             self.text_time,
                             self.text_level_name])

        # reset user events
        self.EVENT_PLAYER_LOOSE_LEVEL = pygame.USEREVENT + 1
        self.EVENT_PLAYER_WIN_LEVEL = pygame.USEREVENT + 2

        self.up = 0
        self.right = 0
        
        self.built = True

    def increase_time(self, *args, **kwargs):
        # TODO: VERY UGLY CODE!!
        self.time_elapsed += 1
        if self.time_is_out(10): 
            snd_clock_tick.play()
    
        
    def update(self):
        snake = self.snake
        grid = self.grid
        food = self.food
        
        for part in snake.parts:
            grid.release_cell(*grid.xy2cell(*part.getpos()))
        
        snake.move(self.up, self.right, self.walls)

        for part in snake.parts:
            grid.occupy_cell(*grid.xy2cell(*part.getpos()))
    
        if snake.intersect_itself or not snake.within_world:
            snake.kill()   
        
        # grow snake if it eats food
        for f in food:
            if snake.head.rect.colliderect(f.rect):
                snake.add_part()
                snake.parts[-2].dir2img_table = snake.neck.dir2img_table  # ugly code

                if f.food_type == 'potion':
                    snd_eat_potion.play()
                elif f.food_type == 'mushroom':
                    snd_eat_bad_food.play()
                else:
                    snd_eat_good_food.play()

                if f.health > 0:
                    self.score += f.score
                    
                snake.health += f.health
                
                food_cix, food_ciy = grid.xy2cell(f.rect.x, f.rect.y)
                grid.release_cell(food_cix, food_ciy)
                food.remove(f)

                fc = grid.get_random_free_cell()
                if fc:
                    food_x, food_y = grid.cell2xy(*fc)
                    grid.occupy_cell(*fc)
                    food.append(self.food_factory.make_random(food_x, food_y))

        if not self.snake.alive or self.time_is_out():
            pygame.event.post(pygame.event.Event(self.EVENT_PLAYER_LOOSE_LEVEL))
            return

        if self.score >= self.score_needed:
            pygame.event.post(pygame.event.Event(self.EVENT_PLAYER_WIN_LEVEL))

        snake.update()

        # update texts
        self.text_score.set_text(f'ОЧКОВ: {self.score} из {self.score_needed}')
        self.text_health.set_text(f'ЗДОРОВЬЕ: {snake.health}')
        if self.max_time:
            self.text_time.set_text(f'ВРЕМЯ: {self.time_elapsed} сек из {self.max_time}')
        else:
            self.text_time.set_text(f'ВРЕМЯ: {self.time_elapsed} сек')


    def clear_screen(self, screen):
        dirtyrects.clear()
        self.group_snake.clear(screen, self.background)
        self.walls.clear(screen, self.background)
        self.food.clear(screen, self.background)
        self.texts.clear(screen, self.background)

    def draw(self, screen):
        self.group_snake.draw(screen)
        self.walls.draw(screen)
        self.food.draw(screen)
        self.texts.draw(screen)
        pygame.display.update(dirtyrects)

    def time_is_out(self, delta=0):
        if self.max_time <= 0:
            return False
        return self.time_elapsed >= self.max_time - delta
        
    def handle_transitions(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.scene_manager.pop_scene()
            return

        if event.type == self.EVENT_PLAYER_LOOSE_LEVEL:
            self.build()  # here we should rebuild current level
            self.scene_manager.push_scene(you_loose_splash_screen)
            return
        
        if event.type == self.EVENT_PLAYER_WIN_LEVEL:
            if self.curr_level_index < self.num_levels - 1:
                self.curr_level_index += 1
                self.build()  # here we should build next level
                self.scene_manager.push_scene(you_win_splash_screen)
            else:
                self.scene_manager.push_scene(final_splash_screen)


    def handle_events(self, event):                
        keystate = pygame.key.get_pressed()                         
        # handle input
        self.up = keystate[pygame.K_UP] - keystate[pygame.K_DOWN]
        self.right = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]

    def enter(self):
        if self.timer is not None and not self.timer.is_running:
            self.timer.start()

    def leave(self):
        if self.timer is not None and self.timer.is_running:
            self.timer.stop()

    def destroy(self):
        self.curr_level_index = 0
        self.built = False

game_scene = GameScene(glb.SCREENRECT, LEVELS)