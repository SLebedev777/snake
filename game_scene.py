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
from splash import you_loose_splash_screen, you_win_splash_screen

from timer import RepeatedTimer

from numpy import random


def load_image(filename, transparent):
    "loads an image, prepares it for play"
    try:
        surface = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (filename, pygame.get_error()))
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, pygame.locals.RLEACCEL)
    return surface.convert()

def dir2img_template(image):
    """
    Basic template for creating table of images according to 4 directions without kinks:
        UP, RIGHT, DOWN, LEFT
    """
    return {
        (glb.DIRECTION_UP, glb.DIRECTION_UP): image,
        (glb.DIRECTION_RIGHT, glb.DIRECTION_RIGHT): pygame.transform.rotate(image, -90),
        (glb.DIRECTION_DOWN, glb.DIRECTION_DOWN): pygame.transform.rotate(image, 180),
        (glb.DIRECTION_LEFT, glb.DIRECTION_LEFT): pygame.transform.rotate(image, 90)
        }


class GameScene(Scene):    
    def build(self):
        # load images
        ground_image = load_image(f'{glb.DATA_DIR}/ground.png', False)
        banana_image = load_image(f'{glb.DATA_DIR}/banana.png', True)
        apple_image = load_image(f'{glb.DATA_DIR}/apple.png', True)
        mushroom_image = load_image(f'{glb.DATA_DIR}/mushroom.png', True)
        potion_image = load_image(f'{glb.DATA_DIR}/potion.png', True)
        
        wall_image = load_image(f'{glb.DATA_DIR}/wall.png', True)
        
        fence_horiz_image = load_image(f'{glb.DATA_DIR}/fence.png', True)
        fence_horiz_image_flip_v = pygame.transform.flip(fence_horiz_image, False, True)
        fence_vert_image = pygame.transform.rotate(fence_horiz_image, 90)
        fence_vert_image_flip_h = pygame.transform.rotate(fence_horiz_image, -90)
        fence_corner_image = load_image(f'{glb.DATA_DIR}/fence_corner.png', True)
        fence_corner_image_flip_h = pygame.transform.flip(fence_corner_image, True, False)
        fence_corner_image_flip_v = pygame.transform.flip(fence_corner_image, False, True)
        fence_corner_image_flip_hv = pygame.transform.flip(fence_corner_image, True, True)
        
        head_image = load_image(f'{glb.DATA_DIR}/head.png', True)
        tail_image = load_image(f'{glb.DATA_DIR}/tail.png', True)
        body_straight_image = load_image(f'{glb.DATA_DIR}/body_straight.png', True)
        body_curve_image = load_image(f'{glb.DATA_DIR}/body_curve.png', True)
        body_curve_90 = pygame.transform.rotate(body_curve_image, -90)
        body_curve_180 = pygame.transform.rotate(body_curve_image, 180)
        body_curve_270 = pygame.transform.rotate(body_curve_image, 90)
        body_curve_flip_h = pygame.transform.flip(body_curve_image, True, False)
        
        # create directional tables for sprites images by rotation/mirroring
        dir2img_head = dir2img_template(head_image)
        dir2img_tail = dir2img_template(tail_image)
        dir2img_body = dir2img_template(body_straight_image)
        # add kinks from -> to
        dir2img_body[(glb.DIRECTION_UP, glb.DIRECTION_RIGHT)] = body_curve_image
        dir2img_body[(glb.DIRECTION_UP, glb.DIRECTION_LEFT)] = body_curve_flip_h
        dir2img_body[(glb.DIRECTION_RIGHT, glb.DIRECTION_DOWN)] = body_curve_90
        dir2img_body[(glb.DIRECTION_DOWN, glb.DIRECTION_LEFT)] = body_curve_180
        dir2img_body[(glb.DIRECTION_LEFT, glb.DIRECTION_UP)] = body_curve_270
        dir2img_body[(glb.DIRECTION_RIGHT, glb.DIRECTION_UP)] = pygame.transform.flip(
            body_curve_270, True, False)
        dir2img_body[(glb.DIRECTION_DOWN, glb.DIRECTION_RIGHT)] = pygame.transform.flip(
            body_curve_180, True, False)     
        dir2img_body[(glb.DIRECTION_LEFT, glb.DIRECTION_DOWN)] = pygame.transform.flip(
            body_curve_270, False, True)  

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
        
        self.snake = Snake(parts)
        self.group_snake = Group([self.snake])

        for part in self.snake.parts:
            self.grid.occupy_cell(*self.grid.xy2cell(*part.getpos()))
    
        # create some food
        self.food = Group()
        food_table = {'apple':  {'image': apple_image, 'health': 1, 'proba': 0.4},
                      'banana': {'image': banana_image, 'health': 1, 'proba': 0.4},
                      'mushroom': {'image': mushroom_image, 'health': -50, 'proba': 0.15},
                      'potion': {'image': potion_image, 'health': 50, 'proba': 0.05},
                      }
        self.food_factory = FoodFactory(food_table)
        
        for _ in range(10):
            fc = self.grid.get_random_free_cell()
            if fc:
                food_x, food_y = self.grid.cell2xy(*fc)
                self.grid.occupy_cell(*fc)
                self.food.append(self.food_factory.make_random(food_x, food_y))
    
        # create some walls
        self.walls = Group()
        for _ in range(5):
            fc = self.grid.get_random_free_cell()
            if fc:
                wall_x, wall_y = self.grid.cell2xy(*fc)
                self.grid.occupy_cell(*fc)
                self.walls.append( Wall(wall_x, wall_y, wall_image) )
    
        self.score = 0
        self.score_needed = 15
                            
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
        self.max_time = 0
        if self.timer is not None and self.timer.is_running:
            self.timer.stop()
        self.timer = RepeatedTimer(1, self.increase_time, None)

        self.text_score = ScreenText(f'ОЧКОВ: {self.score} из {self.score_needed}', 
                                     10, 20, glb.WHITE)
        self.text_health = ScreenText(f'ЗДОРОВЬЕ: {self.snake.health}', 650, 20, glb.WHITE)        
        self.text_time = ScreenText(f'ВРЕМЯ: {self.time_elapsed} сек', glb.WIDTH//2, 20, glb.WHITE)        
        self.texts =  Group([self.text_score, self.text_health, 
                             self.text_time])


        self.built = True

    def increase_time(self, *args, **kwargs):
        # TODO: VERY UGLY CODE!!
        self.time_elapsed += 1
    
        
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

                if f.health > 0:
                    self.score += 1
                    
                snake.health += f.health
                
                food_cix, food_ciy = grid.xy2cell(f.rect.x, f.rect.y)
                grid.release_cell(food_cix, food_ciy)
                food.remove(f)

                fc = grid.get_random_free_cell()
                if fc:
                    food_x, food_y = grid.cell2xy(*fc)
                    grid.occupy_cell(*fc)
                    food.append(self.food_factory.make_random(food_x, food_y))

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

    def time_is_out(self):
        return self.time_elapsed >= self.max_time if self.max_time else False
        
    def handle_transitions(self):
        for event in pygame.event.get():
           if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
               self.scene_manager.pop_scene()
               return
        if not self.snake.alive or self.time_is_out():
            self.destroy()
            self.build()  # here we should rebuild current level
            self.scene_manager.push_scene(you_loose_splash_screen)
            return
        if self.score >= self.score_needed:
            self.destroy()
            self.build()  # here we should build next level
            self.scene_manager.push_scene(you_win_splash_screen)


    def handle_events(self):                
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


game_scene = GameScene(glb.SCREENRECT)