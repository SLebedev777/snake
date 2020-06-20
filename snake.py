# -*- coding: utf-8 -*-
"""
Created on Sat May 23 20:32:56 2020

@author: Семен
"""
import game_globals as glb
import copy
from actor import Actor
from numpy import sign

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
    def __init__(self, parts, speed=glb.SNAKE_PART_WIDTH, max_health=100,
                 wrap_around=False):
        self.parts = parts
        self.speed = speed
        self.within_world = True
        self.intersect_itself = False
        self.alive = True
        assert max_health > 0
        self.max_health = max_health
        self.health = max_health
        self.vel = [0, 0]
        self.wrap_around = wrap_around

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
        
        # handle single arrow pressed
        if up != 0 and right == 0:
            if self.head.direction == -sign(up) * glb.DIRECTION_UP:
                return False
            head_shift_y -= up * self.speed
            new_direction = sign(up) * glb.DIRECTION_UP
        if right != 0 and up == 0:
            if self.head.direction == -sign(right) * glb.DIRECTION_RIGHT:
                return False
            head_shift_x += right * self.speed
            new_direction = sign(right) * glb.DIRECTION_RIGHT
            
        # handle combo when 2 arrows are pressed simultaneously
        if up != 0 and right != 0:
            # cases when 1 arrow is the same as snake head direction
            if self.head.direction == sign(up) * glb.DIRECTION_UP:
                if not self.move(0, right, walls):
                    self.move(up, 0, walls)
            elif self.head.direction == sign(right) * glb.DIRECTION_RIGHT:
                if not self.move(up, 0, walls):
                    self.move(0, right, walls)            
            # cases when 1 arrow is the opposite to snake head direction
            elif self.head.direction == -sign(up) * glb.DIRECTION_UP:
                self.move(0, right, walls)
                up = -up
                right = 0
                head_shift_y -= up * self.speed
                new_direction = sign(up) * glb.DIRECTION_UP
            elif self.head.direction == -sign(right) * glb.DIRECTION_RIGHT:
                self.move(up, 0, walls)
                up = 0
                right = -right
                head_shift_x += right * self.speed
                new_direction = sign(right) * glb.DIRECTION_RIGHT
            else:
                return False
            
        if new_direction != glb.DIRECTION_NONE:
            # try to move the head and check if head goes outside the game world
            head_new_rect = self.head.rect.move(head_shift_x, head_shift_y)
            if not self.wrap_around and not glb.GAMEGRIDRECT.inflate(2*self.speed, 2*self.speed).contains(head_new_rect):
                self.within_world = False
                self.vel = [0, 0]
                return False

            for w in walls:
                if head_new_rect.colliderect(w.rect):
                    return False

            self.vel[0] += head_shift_x
            self.vel[1] += head_shift_y
            
            hpx, hpy = self.head.getpos()
            
            if self.wrap_around:
                if head_new_rect.top < glb.GAMEGRIDRECT.top:
                    hpy = glb.GAMEGRIDRECT.bottom
                if head_new_rect.bottom > glb.GAMEGRIDRECT.bottom:
                    hpy = glb.GAMEGRIDRECT.top - glb.CELL_SIZE
                if head_new_rect.left < glb.GAMEGRIDRECT.left:
                    hpx = glb.GAMEGRIDRECT.right
                if head_new_rect.right > glb.GAMEGRIDRECT.right:
                    hpx = glb.GAMEGRIDRECT.left - glb.CELL_SIZE

            fin_shift_x = 0
            fin_shift_y = 0
            if self.vel[0] >= glb.SNAKE_SHIFT_THRESHOLD_X:
                fin_shift_x = glb.SNAKE_PART_WIDTH
            if self.vel[0] <= -glb.SNAKE_SHIFT_THRESHOLD_X:
                fin_shift_x = -glb.SNAKE_PART_WIDTH
            if self.vel[1] >= glb.SNAKE_SHIFT_THRESHOLD_Y:
                fin_shift_y = glb.SNAKE_PART_HEIGHT
            if self.vel[1] <= -glb.SNAKE_SHIFT_THRESHOLD_Y:
                fin_shift_y = -glb.SNAKE_PART_HEIGHT

            if fin_shift_x == 0 and fin_shift_y == 0:
                return False
                
            head_new_x = hpx + fin_shift_x
            head_new_y = hpy + fin_shift_y
            
            if self.wrap_around:
                head_new_rect.left = head_new_x
                head_new_rect.top = head_new_y
                for w in walls:
                    if head_new_rect.colliderect(w.rect):
                        self.vel = [0, 0]
                        return False
                            
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
            
            self.vel = [0, 0]
            return True

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
        self.check_intersect_itself()
        self.check_health()
        for part in self.parts:
            part.update()
        

    def draw(self, screen):
        for part in self.parts:
            part.draw(screen)

    def add_part(self, grid):
        """
        Add new segment when snake eats food.
        """
        
        tail = self.tail.clone()
        new_part = self.parts[-2].clone()
        new_part.setpos(*tail.getpos())
        new_part.direction = copy.deepcopy(new_part.direction_from)
        new_part.update_image_by_direction()

        tail_shifts = {glb.DIRECTION_UP:    (0, glb.SNAKE_PART_HEIGHT),
                       glb.DIRECTION_DOWN:  (0, -glb.SNAKE_PART_HEIGHT),
                       glb.DIRECTION_LEFT:  (glb.SNAKE_PART_WIDTH, 0),
                       glb.DIRECTION_RIGHT: (-glb.SNAKE_PART_WIDTH, 0)
                       }
        
        try_tail_directions = [tail.direction] + \
            [d for d in tail_shifts.keys() if d != tail.direction and \
             d != glb.opposite(tail.direction)]
        
        tail_old_pos = tail.getpos()
        tail_new_pos_found = False
        for d in try_tail_directions:
            tail.setpos(*tail_old_pos)
            new_x = tail.rect.x + tail_shifts[d][0]
            new_y = tail.rect.y + tail_shifts[d][1]
            tail.setpos(new_x, new_y)
            if not glb.GAMEGRIDRECT.contains(tail.rect):
                continue
            if grid.cell_occupied(*grid.xy2cell(new_x, new_y)):
                continue
            tail.direction = d
            tail.direction_from = d
            tail.update_image_by_direction()
            tail_new_pos_found = True
            break
        if not tail_new_pos_found:
            #  i can't imagine this situation
            return
            
        new_part.direction_from = tail.direction
        new_part.dir2img_table = self.neck.dir2img_table  # kinks can occur
        new_part.update_image_by_direction()
        
        self.parts.append(tail)
        self.parts[-2] = new_part
        grid.occupy_cell(*grid.xy2cell(tail.x, tail.y))

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
