# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 14:43:58 2020

@author: Семен
"""

import pygame

import game_globals as glb
from game_grid import GameGrid
from actor import dirtyrects
from snake import SnakePart, Snake
from assets import Food, FoodFactory, Wall
from screen_text import ScreenText

from numpy import random

def clear_group(group, screen, background):
    for actor in group:
        actor.erase(screen, background)
        actor.update()

def draw_group(group, screen):
    for actor in group:
        actor.draw(screen)


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


##############################################################################

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((glb.WIDTH, glb.HEIGHT), 
                                     pygame.HWSURFACE #| pygame.FULLSCREEN
                                     )
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    grid = GameGrid(glb.SCREENRECT, glb.CELL_SIZE)

    # load images
    ground_image = load_image(f'{glb.DATA_DIR}/ground.png', False)
    banana_image = load_image(f'{glb.DATA_DIR}/banana.png', True)
    apple_image = load_image(f'{glb.DATA_DIR}/apple.png', True)
    mushroom_image = load_image(f'{glb.DATA_DIR}/mushroom.png', True)
    potion_image = load_image(f'{glb.DATA_DIR}/potion.png', True)
    wall_image = load_image(f'{glb.DATA_DIR}/wall.png', True)
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

    # place snake in the center and align to the grid    
    snake_x, snake_y = grid.cell2xy(*grid.xy2cell(glb.WIDTH//2, glb.HEIGHT//2))
    
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
    
    snake = Snake(parts)

    for part in snake.parts:
        grid.occupy_cell(*grid.xy2cell(*part.getpos()))

    # create some food
    food = []
    food_table = {'apple':  {'image': apple_image, 'health': 1, 'proba': 0.4},
                  'banana': {'image': banana_image, 'health': 1, 'proba': 0.4},
                  'mushroom': {'image': mushroom_image, 'health': -50, 'proba': 0.15},
                  'potion': {'image': potion_image, 'health': 50, 'proba': 0.05},
                  }
    food_factory = FoodFactory(food_table)
    
    for _ in range(10):
        fc = grid.get_random_free_cell()
        if fc:
            food_x, food_y = grid.cell2xy(*fc)
            grid.occupy_cell(*fc)
            food.append(food_factory.make_random(food_x, food_y))

    # create some walls
    walls = []
    for _ in range(5):
        fc = grid.get_random_free_cell()
        if fc:
            wall_x, wall_y = grid.cell2xy(*fc)
            grid.occupy_cell(*fc)
            walls.append( Wall(wall_x, wall_y, wall_image) )

    score = 0
                    
    text_score = ScreenText(f'ОЧКОВ: {score}', 10, 20, glb.WHITE)
    text_health = ScreenText(f'ЗДОРОВЬЕ: {snake.health}', 650, 20, glb.WHITE)
    
    texts =  [text_score, text_health]

    background = pygame.Surface(glb.SCREENRECT.size)
    # tile background with sand texture
    for cix in range(grid.n_cells_x):
        for ciy in range(grid.n_cells_y):
            background.blit(ground_image, grid.cell2xy(cix, ciy))
    screen.blit(background, (glb.SCREENRECT.left, glb.SCREENRECT.top))
    pygame.display.flip()
    
    running = True
    while running:
        clock.tick(glb.FPS)
        # manage events
        for event in pygame.event.get():
           if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
               running = False
        keystate = pygame.key.get_pressed()
                
        # handle input
        up = keystate[pygame.K_UP] - keystate[pygame.K_DOWN]
        right = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]

        # Clear screen and update actors
        dirtyrects.clear()
        clear_group([snake], screen, background)
        clear_group(walls, screen, background)
        clear_group(food, screen, background)
        clear_group(texts, screen, background)
        
        for part in snake.parts:
            grid.release_cell(*grid.xy2cell(*part.getpos()))
        
        snake.move(up, right, walls)

        for part in snake.parts:
            grid.occupy_cell(*grid.xy2cell(*part.getpos()))
    
        if snake.intersect_itself or not snake.within_world:
            snake.kill()   
        if not snake.alive:
            running = False
        
        # grow snake if it eats food
        for f in food:
            if snake.head.rect.colliderect(f.rect):
                snake.add_part()
                snake.parts[-2].dir2img_table = dir2img_body  # ugly code

                if f.health > 0:
                    score += 1
                    
                snake.health += f.health
                
                food_cix, food_ciy = grid.xy2cell(f.rect.x, f.rect.y)
                grid.release_cell(food_cix, food_ciy)
                food.remove(f)

                fc = grid.get_random_free_cell()
                if fc:
                    food_x, food_y = grid.cell2xy(*fc)
                    grid.occupy_cell(*fc)
                    food.append(food_factory.make_random(food_x, food_y))

        snake.update()

        # update texts
        text_score.set_text(f'ОЧКОВ: {score}')
        text_health.set_text(f'ЗДОРОВЬЕ: {snake.health}')

        # render actors
        draw_group([snake], screen)
        draw_group(walls, screen)
        draw_group(food, screen)
        draw_group(texts, screen)
        pygame.display.update(dirtyrects)
    
    pygame.quit()
    

if __name__ == '__main__':
    main()
    