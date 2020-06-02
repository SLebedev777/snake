# -*- coding: utf-8 -*-
"""
Created on Sat May 23 20:32:56 2020

@author: Семен
"""
import game_globals as glb
import copy
from actor import Actor

class SnakePart(Actor):
    """
    Actor that holds 2 directions: from and to.
    Also, it holds table of images, according to key tuple (dir_from, dir_to)
    """
    def __init__(self, x, y, image, 
                 direction=glb.DIRECTION_NONE, 
                 direction_from=glb.DIRECTION_NONE,
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


        
class Snake:
    """
    Player
    """
    def __init__(self, parts, max_health=100):
        self.parts = parts
        self.speed = glb.SNAKE_PART_WIDTH  # BAD PLACE HERE: SNAKE CAN MOVE ONLY AT 1 CELL
        self.within_world = True
        self.intersect_itself = False
        self.alive = True
        assert max_health > 0
        self.max_health = max_health
        self.health = max_health

    def move(self, up, right, walls=[]):
        head_shift_x, head_shift_y = 0, 0
        new_direction = glb.DIRECTION_NONE
        
        # if no key pressed, then move along current direction
        if not up and not right and glb.SNAKE_CAN_MOVE_ALONE:
            if self.direction == glb.DIRECTION_UP:
                up = 1
            if self.direction == glb.DIRECTION_DOWN:
                up = -1
            if self.direction == glb.DIRECTION_LEFT:
                right = -1
            if self.direction == glb.DIRECTION_RIGHT:
                right = 1
        
        if up:
            if self.head.direction == -up * glb.DIRECTION_UP:
                return
            head_shift_y -= up * self.speed
            new_direction = up * glb.DIRECTION_UP
        elif right:
            if self.head.direction == -right * glb.DIRECTION_RIGHT:
                return
            head_shift_x += right * self.speed
            new_direction = right * glb.DIRECTION_RIGHT
        if new_direction != glb.DIRECTION_NONE:
            # try to move the head and check if head goes outside the game world
            head_new_rect = self.head.rect.move(head_shift_x, head_shift_y)
            if not glb.GAMEGRIDRECT.contains(head_new_rect):
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

    def check_health(self):
        if self.health <= 0:
            self.health = 0
            self.kill()
        if self.health > self.max_health:
            self.health = self.max_health

        
    def update(self):
        self.within_world = glb.GAMEGRIDRECT.contains(self.parts[0].rect)
        self.check_intersect_itself()
        self.check_health()
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
        # Also, sometimes tail overlaps asset (food or wall) that lies near tail,
        # when snake eats fruit at head.
        # Maybe it's needed to take not only walls but all game grid.

        
        tail = self.tail.clone()
        new_part = self.parts[-2].clone()
        new_part.setpos(*tail.getpos())
        new_part.direction = copy.deepcopy(new_part.direction_from)
        new_part.update_image_by_direction()
        
        if tail.direction == glb.DIRECTION_UP:
            # shift down
            new_x = tail.rect.x
            new_y = tail.rect.y + glb.SNAKE_PART_HEIGHT
        elif tail.direction == glb.DIRECTION_DOWN:
            # shift up
            new_x = tail.rect.x
            new_y = tail.rect.y - glb.SNAKE_PART_HEIGHT
        elif tail.direction == glb.DIRECTION_LEFT:
            # shift right
            new_x = tail.rect.x + glb.SNAKE_PART_WIDTH
            new_y = tail.rect.y
        elif tail.direction == glb.DIRECTION_RIGHT:
            # shift left
            new_x = tail.rect.x - glb.SNAKE_PART_WIDTH
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
