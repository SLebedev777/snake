# -*- coding: utf-8 -*-
"""
Created on Fri May 29 20:07:41 2020

@author: Семен
"""

import pygame
from scene import Scene
from scene_manager import SceneManager
from screen_text import ScreenText
import game_globals as glb
from actor import dirtyrects
from group import Group

import os, sys

from game_scene import *
from resources import *

class MenuScene(Scene):
    caption = None
    options = []
    font_size = 50
    
    def build(self):
        self.pointer = ScreenText('--> ', self.options[0].x - 50, self.options[0].y, 
                                  glb.WHITE, self.font_size)
        self.group = Group([self.caption, self.pointer] + self.options)
        for actor in self.group:
            actor.move(self.rect.left, self.rect.top)
        self.num_options = len(self.options)
        self.selected_option = 0
        self.prev_option = -1
        self.move_up = 0
        self.background.fill(glb.NAVY)
        #self.background.blit(logo_image, (50, 50))
        self.built = True
 
    def update(self):
        self.prev_option = self.selected_option
        if self.move_up:
            self.selected_option -= self.move_up
            self.selected_option = min(self.num_options-1, max(0, self.selected_option))
            self.pointer.setpos(self.pointer.x, 
                                self.options[0].y + self.font_size * self.selected_option)

    def clear_screen(self, screen):
        dirtyrects.clear()
        self.group.clear(screen, self.background)

    def draw(self, screen):
        self.group.draw(screen)
        pygame.display.update(dirtyrects)
        
    def handle_transitions(self):
        pass

    def handle_events(self):
        keystate = pygame.key.get_pressed()                         
        # handle input
        self.move_up = keystate[pygame.K_UP] - keystate[pygame.K_DOWN]


class MainMenuScene(MenuScene):
    font_size = 50
    caption = ScreenText('ГЛАВНОЕ МЕНЮ', 100, 10, glb.WHITE, font_size)
    options = [ScreenText('Новая игра', 100, 10+font_size, glb.WHITE, font_size),
               ScreenText('Настройки', 100, 10+2*font_size, glb.WHITE, font_size),
               ScreenText('Выход', 100, 10+3*font_size, glb.WHITE, font_size)
               ]

    def handle_transitions(self):
        for event in pygame.event.get():
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
    font_size = 50
    caption = ScreenText('НАСТРОЙКИ', 100, 10, glb.WHITE, font_size)
    options = [
               ScreenText('Полный экран вкл/выкл', 100, 10+font_size, glb.WHITE, font_size),
               ScreenText('Назад', 100, 10+2*font_size, glb.WHITE, font_size),
               ]

    def handle_transitions(self):
        for event in pygame.event.get():
           if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
               snd_menu_enter.play()
               if self.selected_option == 0:
                   glb.FULLSCREEN_MODE = not glb.FULLSCREEN_MODE 
                   self.scene_manager.toggle_fullscreen()
               if self.selected_option == self.num_options-1:
                   self.scene_manager.pop_scene()
                   break
           if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
               self.scene_manager.pop_scene()
               break

class DifficultyMenuScene(MenuScene):
    font_size = 50
    caption = ScreenText('СЛОЖНОСТЬ', 100, 10, glb.WHITE, font_size)
    options = [ScreenText('Легкая', 100, 10+font_size, glb.WHITE, font_size),
               ScreenText('Нормальная', 100, 10+2*font_size, glb.WHITE, font_size),
               ScreenText('Назад', 100, 10+3*font_size, glb.WHITE, font_size),
               ]

    def handle_transitions(self):
        for event in pygame.event.get():
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
                   break
           if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
               self.scene_manager.pop_scene()
               break


main_menu = MainMenuScene(glb.MENURECT)
options_menu = OptionsMenuScene(glb.MENURECT)
difficulty_menu = DifficultyMenuScene(glb.MENURECT)