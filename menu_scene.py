# -*- coding: utf-8 -*-
"""
Created on Fri May 29 20:07:41 2020

@author: Семен
"""

import pygame
from scene import Scene
from scene_manager import SceneManager
from screen_text import ScreenText, ScreenTextBitmapFont
import game_globals as glb
from actor import dirtyrects, Actor
from group import Group

import os, sys

from game_scene import *
from resources import *

class MenuScene(Scene):
    caption = None
    options = []
    font_size = 50
    
    def build(self):
        self.pointer = ScreenTextBitmapFont('>', 
                                            self.options[0].x - 50, 
                                            self.options[0].y,
                                            bitmap_font_large)
        self.group = Group([self.caption, self.pointer] + self.options)
        for actor in self.group:
            actor.move(self.rect.left, self.rect.top)
        self.num_options = len(self.options)
        self.selected_option = 0
        self.prev_option = -1
        self.move_up = 0
        self.background.fill(glb.NAVY)
        self.built = True
 
    def update(self):
        self.prev_option = self.selected_option
        if self.move_up:
            self.selected_option -= self.move_up
            self.selected_option = min(self.num_options-1, max(0, self.selected_option))
            self.pointer.setpos(self.pointer.x, 
                                self.options[0].y + self.font_size * self.selected_option)
        pygame.time.wait(100)

    def clear_screen(self, screen):
        dirtyrects.clear()
        self.group.clear(screen, self.background)

    def draw(self, screen):
        self.group.draw(screen)
        pygame.display.update(dirtyrects)
       
    def handle_transitions(self, event):
        pass

    def handle_events(self, event):                
        keystate = pygame.key.get_pressed()                         
        # handle input
        self.move_up = keystate[pygame.K_UP] - keystate[pygame.K_DOWN]


class MainMenuScene(MenuScene):
    font_size = bitmap_font_large.height
    caption = ScreenTextBitmapFont('JUST SNAKE!', 70, 10, bitmap_font_large)
    options = [ScreenTextBitmapFont('NEW GAME', 70, 32+font_size, bitmap_font_large),
              ScreenTextBitmapFont('OPTIONS', 70, 32+2*font_size, bitmap_font_large),
              ScreenTextBitmapFont('QUIT', 70, 32+3*font_size, bitmap_font_large)
              ]

    def handle_transitions(self, event):
       if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
           snd_menu_enter.play()
           if self.selected_option == 0:
               if not difficulty_menu.built:
                   difficulty_menu.build()
               self.scene_manager.push_scene(difficulty_menu)
           elif self.selected_option == 1:
               self.scene_manager.push_scene(options_menu)
           elif self.selected_option == 2:
               self.scene_manager.running = False
       if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
           if game_scene.built:
               self.scene_manager.push_scene(game_scene)


class OptionsMenuScene(MenuScene):
    font_size = bitmap_font_large.height
    caption = ScreenTextBitmapFont('OPTIONS', 70, 10, bitmap_font_large)
    options = [ScreenTextBitmapFont('FULLSCREEN ON/OFF', 70, 32+font_size, bitmap_font_large),
              ScreenTextBitmapFont('BACK', 70, 32+2*font_size, bitmap_font_large),
              ]

    def handle_transitions(self, event):
       if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
           snd_menu_enter.play()
           if self.selected_option == 0:
               glb.FULLSCREEN_MODE = not glb.FULLSCREEN_MODE 
               self.scene_manager.toggle_fullscreen()
           if self.selected_option == self.num_options-1:
               self.scene_manager.pop_scene()
       if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
           self.scene_manager.pop_scene()

class DifficultyMenuScene(MenuScene):
    font_size = bitmap_font_large.height
    caption = ScreenTextBitmapFont('DIFFICULTY', 70, 10, bitmap_font_large)
    options = [ScreenTextBitmapFont('EASY', 70, 32+font_size, bitmap_font_large),
              ScreenTextBitmapFont('NORMAL', 70, 32+2*font_size, bitmap_font_large),
              ScreenTextBitmapFont('BACK', 70, 32+3*font_size, bitmap_font_large),
              ]


    def handle_transitions(self, event):
       if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
           snd_menu_enter.play()
           # select difficilty and start new game from level 0
           if self.selected_option in [0, 1]:
               glb.SNAKE_CAN_MOVE_ALONE = bool(self.selected_option)
               game_scene.destroy()
               game_scene.build()
               self.scene_manager.pop_scene()
               self.scene_manager.push_scene(game_scene)
               game_scene.enter()
           elif self.selected_option == self.num_options-1:
               self.scene_manager.pop_scene()
       if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
           self.scene_manager.pop_scene()


main_menu = MainMenuScene(glb.MENURECT)
options_menu = OptionsMenuScene(glb.MENURECT)
difficulty_menu = DifficultyMenuScene(glb.MENURECT)