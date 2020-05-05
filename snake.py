# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 14:43:58 2020

@author: Семен
"""

import pygame
from pygame.locals import *
import copy
import os

import game_grid

WIDTH, HEIGHT = 800, 600
SCREENRECT = pygame.Rect(0, 0, WIDTH, HEIGHT)
CELL_SIZE = 40
FPS = 20

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREY = (127, 127, 127)
DARK_GREY = (63, 63, 63)

PART_TYPES = {'head': GREEN,
              'body': RED,
              'tail': BLUE}

FOOD_TYPES = {'banana': YELLOW}

WALL_TYPES = {'stone': DARK_GREY}

SNAKE_PART_WIDTH = CELL_SIZE
SNAKE_PART_HEIGHT = CELL_SIZE

SNAKE_CAN_MOVE_ALONE = False  # debug option: snake moves along prev direction if no input

main_dir = os.getcwd()
data_dir = f'{main_dir}/data'

def load_image(filename, transparent):
    "loads an image, prepares it for play"
    try:
        surface = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (filename, pygame.get_error()))
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, RLEACCEL)
    return surface.convert()



# encode opposite directions with negation for easy checking
DIRECTION_NONE = 0
DIRECTION_UP = 1
DIRECTION_DOWN = -1
DIRECTION_LEFT = -2
DIRECTION_RIGHT = 2

dirtyrects = [] # list of update_rects

class Actor(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        self.rect = self.rect.clamp(SCREENRECT)
 
    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y



class SnakePart(Actor):
    """
    Actor that holds 2 directions: from and to.
    Also, it holds table of images, according to key tuple (dir_from, dir_to)
    """
    def __init__(self, x, y, image, 
                 direction=DIRECTION_NONE, 
                 direction_from=DIRECTION_NONE,
                 dir2img_table=None):
        super().__init__(x, y, image)
        # main direction, controlled by input
        self.direction = direction
        # previus direction, used for doing kinks of snake body
        self.direction_from = direction_from
        self.dir2img_table = dir2img_table

    def update_image_by_direction(self):
        if self.dir2img_table is not None:
            if (self.direction_from, self.direction) in self.dir2img_table:
                self.image = self.dir2img_table[(self.direction_from, self.direction)]
                
    def clone(self):
        return SnakePart(self.x, self.y, self.image, self.direction,
                         self.direction_from, self.dir2img_table)


class Food(Actor):
    pass


class Wall(Actor):
    pass

        
class Snake:
    """
    Player
    """
    def __init__(self, parts):
        self.parts = parts
        self.speed = SNAKE_PART_WIDTH  # BAD PLACE HERE: SNAKE CAN MOVE ONLY AT 1 CELL
        self.within_world = True
        self.intersect_itself = False
        self.alive = True

    def move(self, up, right, walls=[]):
        head_shift_x, head_shift_y = 0, 0
        new_direction = DIRECTION_NONE
        
        # if no key pressed, then move along current direction
        if not up and not right and SNAKE_CAN_MOVE_ALONE:
            if self.direction == DIRECTION_UP:
                up = 1
            if self.direction == DIRECTION_DOWN:
                up = -1
            if self.direction == DIRECTION_LEFT:
                right = -1
            if self.direction == DIRECTION_RIGHT:
                right = 1
        
        if up:
            if self.head.direction == -up * DIRECTION_UP:
                return
            head_shift_y -= up * self.speed
            new_direction = up * DIRECTION_UP
        elif right:
            if self.head.direction == -right * DIRECTION_RIGHT:
                return
            head_shift_x += right * self.speed
            new_direction = right * DIRECTION_RIGHT
        if new_direction != DIRECTION_NONE:
            # try to move the head and check if head goes outside the screen
            head_new_rect = self.head.rect.move(head_shift_x, head_shift_y)
            if not SCREENRECT.contains(head_new_rect):
                self.within_world = False
                return

            for w in walls:
                if head_new_rect.colliderect(w.rect):
                    return

            hpx, hpy = self.head.getpos()
            head_new_x = hpx + head_shift_x
            head_new_y = hpy + head_shift_y

            # shift snake parts from tail to neck
            for i in range(len(self.parts)-1, 0, -1):
                curr_part = self.parts[i]
                next_part = self.parts[i-1]
                curr_part.setpos(*next_part.getpos())
                curr_part.direction = next_part.direction
                curr_part.direction_from = next_part.direction_from
                curr_part.update_image_by_direction()

            # correct tail direction (no kinks allowed)
            self.tail.direction_from = self.tail.direction
            self.tail.update_image_by_direction()
            
            # kink neck if needed
            self.neck.direction_from = copy.deepcopy(self.neck.direction)
            self.neck.direction = new_direction
            self.neck.update_image_by_direction()
            
            # finally head
            self.head.setpos(head_new_x, head_new_y)
            self.head.direction = new_direction
            self.head.direction_from = new_direction
            self.head.update_image_by_direction()
            

    def erase(self, screen, background):
        for part in self.parts:
            part.erase(screen, background)
      
        
    def check_intersect_itself(self):
        for part in self.parts[1:]:
            if self.head.rect.colliderect(part.rect):
                self.intersect_itself = True
                return self.intersect_itself
        self.intersect_itself = False
        return self.intersect_itself

    def update(self):
        self.within_world = SCREENRECT.contains(self.parts[0].rect)
        self.check_intersect_itself()
        for part in self.parts:
            part.update()

    def draw(self, screen):
        for part in self.parts:
            part.draw(screen)

    def add_part(self):
        """
        Add new segment when snake eats food.
        """
        # TODO (later): In some cases, tail seems to attach in wrong place,
        # because first snake moves, and after that grows, and after 
        # elongation, tail seems to "jump" aside. Not major bug.
        
        tail = self.tail.clone()
        new_part = self.parts[-2].clone()
        new_part.setpos(*tail.getpos())
        new_part.direction = copy.deepcopy(new_part.direction_from)
        new_part.update_image_by_direction()
        
        if tail.direction == DIRECTION_UP:
            # shift down
            new_x = tail.rect.x
            new_y = tail.rect.y + SNAKE_PART_HEIGHT
        elif tail.direction == DIRECTION_DOWN:
            # shift up
            new_x = tail.rect.x
            new_y = tail.rect.y - SNAKE_PART_HEIGHT
        elif tail.direction == DIRECTION_LEFT:
            # shift right
            new_x = tail.rect.x + SNAKE_PART_WIDTH
            new_y = tail.rect.y
        elif tail.direction == DIRECTION_RIGHT:
            # shift left
            new_x = tail.rect.x - SNAKE_PART_WIDTH
            new_y = tail.rect.y
        tail.setpos(new_x, new_y)
        self.parts.append(tail)
        self.parts[-2] = new_part

    def kill(self):
        self.alive = False

    @property
    def head(self):
        return self.parts[0]

    @property
    def neck(self):
        return self.parts[1]

    @property
    def tail(self):
        return self.parts[-1]

    @property
    def direction(self):
        return self.head.direction
    

class ScreenText(Actor):
    def __init__(self, text, x, y):
        self.text = text
        self.font = pygame.font.Font(None, 20)
        self.color = WHITE 
        super().__init__(x, y, self.font.render(text, 0, self.color))

    def set_text(self, text):
        if text != self.text:
            self.text = text
            self.image = self.font.render(text, 0, self.color)
            x, y = self.getpos()
            self.rect = self.image.get_rect().move(x, y)

###############################################################################

def clear_group(group, screen, background):
    for actor in group:
        actor.erase(screen, background)
        actor.update()

def draw_group(group, screen):
    for actor in group:
        actor.draw(screen)

##############################################################################

def dir2img_template(image):
    """
    Basic template for creating table of images according to 4 directions without kinks:
        UP, RIGHT, DOWN, LEFT
    """
    return {
        (DIRECTION_UP, DIRECTION_UP): image,
        (DIRECTION_RIGHT, DIRECTION_RIGHT): pygame.transform.rotate(image, -90),
        (DIRECTION_DOWN, DIRECTION_DOWN): pygame.transform.rotate(image, 180),
        (DIRECTION_LEFT, DIRECTION_LEFT): pygame.transform.rotate(image, 90)
        }


##############################################################################

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 
                                     pygame.HWSURFACE #| pygame.FULLSCREEN
                                     )
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    global dirtyrects

    grid = game_grid.GameGrid(SCREENRECT, CELL_SIZE)

    # load images
    ground_image = load_image(f'{data_dir}/ground.png', False)
    banana_image = load_image(f'{data_dir}/banana.png', True)
    wall_image = load_image(f'{data_dir}/wall.png', True)
    head_image = load_image(f'{data_dir}/head.png', True)
    tail_image = load_image(f'{data_dir}/tail.png', True)
    body_straight_image = load_image(f'{data_dir}/body_straight.png', True)
    body_curve_image = load_image(f'{data_dir}/body_curve.png', True)
    body_curve_90 = pygame.transform.rotate(body_curve_image, -90)
    body_curve_180 = pygame.transform.rotate(body_curve_image, 180)
    body_curve_270 = pygame.transform.rotate(body_curve_image, 90)
    body_curve_flip_h = pygame.transform.flip(body_curve_image, True, False)
    
    # create directional tables for sprites images by rotation/mirroring
    dir2img_head = dir2img_template(head_image)
    dir2img_tail = dir2img_template(tail_image)
    dir2img_body = dir2img_template(body_straight_image)
    # add kinks from -> to
    dir2img_body[(DIRECTION_UP, DIRECTION_RIGHT)] = body_curve_image
    dir2img_body[(DIRECTION_UP, DIRECTION_LEFT)] = body_curve_flip_h
    dir2img_body[(DIRECTION_RIGHT, DIRECTION_DOWN)] = body_curve_90
    dir2img_body[(DIRECTION_DOWN, DIRECTION_LEFT)] = body_curve_180
    dir2img_body[(DIRECTION_LEFT, DIRECTION_UP)] = body_curve_270
    dir2img_body[(DIRECTION_RIGHT, DIRECTION_UP)] = pygame.transform.flip(
        body_curve_270, True, False)
    dir2img_body[(DIRECTION_DOWN, DIRECTION_RIGHT)] = pygame.transform.flip(
        body_curve_180, True, False)     
    dir2img_body[(DIRECTION_LEFT, DIRECTION_DOWN)] = pygame.transform.flip(
        body_curve_270, False, True)  

    # place snake in the center and align to the grid    
    snake_x, snake_y = grid.cell2xy(*grid.xy2cell(WIDTH//2, HEIGHT//2))
    
    # create snake parts
    head = SnakePart(snake_x, snake_y, head_image, DIRECTION_UP, DIRECTION_UP,
                     dir2img_head)
    neck = SnakePart(snake_x, snake_y + SNAKE_PART_HEIGHT, 
                     body_straight_image, DIRECTION_UP, DIRECTION_UP,
                     dir2img_body)
    body = SnakePart(snake_x, snake_y + SNAKE_PART_HEIGHT*2, 
                     body_straight_image, DIRECTION_UP, DIRECTION_UP,
                     dir2img_body)
    tail = SnakePart(snake_x, snake_y + SNAKE_PART_HEIGHT*3, 
                     tail_image, DIRECTION_UP, DIRECTION_UP,
                     dir2img_tail)
    parts = [head, neck, body, tail]
    
    snake = Snake(parts)

    for part in snake.parts:
        grid.occupy_cell(*grid.xy2cell(*part.getpos()))

    # create some food
    food = []
    for _ in range(10):
        fc = grid.get_random_free_cell()
        if fc:
            food_x, food_y = grid.cell2xy(*fc)
            grid.occupy_cell(*fc)
            food.append( Food(food_x, food_y, banana_image) )

    # create some walls
    walls = []
    for _ in range(5):
        fc = grid.get_random_free_cell()
        if fc:
            wall_x, wall_y = grid.cell2xy(*fc)
            grid.occupy_cell(*fc)
            walls.append( Wall(wall_x, wall_y, wall_image) )

    score = 0
                    
    text_score = ScreenText(f'SCORE: {score}', 10, 20)
    
    texts =  [text_score]

    background = pygame.Surface(SCREENRECT.size)
    # tile background with sand texture
    for cix in range(grid.n_cells_x):
        for ciy in range(grid.n_cells_y):
            background.blit(ground_image, grid.cell2xy(cix, ciy))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    running = True
    while running:
        clock.tick(FPS/2)
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
        dirtyrects = []
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
                snake.parts[-2].dir2img_table = dir2img_body
                
                food_cix, food_ciy = grid.xy2cell(f.rect.x, f.rect.y)
                grid.release_cell(food_cix, food_ciy)
                food.remove(f)

                fc = grid.get_random_free_cell()
                if fc:
                    food_x, food_y = grid.cell2xy(*fc)
                    grid.occupy_cell(*fc)
                    food.append( Food(food_x, food_y, banana_image) )
                score += 1

        # update texts
        text_score.set_text(f'SCORE: {score}')

        # render actors
        draw_group([snake], screen)
        draw_group(walls, screen)
        draw_group(food, screen)
        draw_group(texts, screen)
        pygame.display.update(dirtyrects)
    
    pygame.quit()
    

if __name__ == '__main__':
    main()
    