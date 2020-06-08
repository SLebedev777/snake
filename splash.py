# -*- coding: utf-8 -*-
"""
Created on Sat May 30 19:08:56 2020

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

import game_scene as gs
import resources as rsc

class SplashScreenScene(Scene):
    caption = None
    texts = [ScreenText('Нажмите Пробел для продолжения...', 30, 100, glb.WHITE)]
    font_size = 50
    
    def build(self):
        self.group = Group([self.caption] + self.texts)
        for actor in self.group:
            actor.move(self.rect.left, self.rect.top)
        self.background.fill(glb.GREY)
        self.built = True
 
    def update(self):
        pass
    
    def clear_screen(self, screen):
        dirtyrects.clear()
        self.group.clear(screen, self.background)

    def draw(self, screen):
        self.group.draw(screen)
        pygame.display.update(dirtyrects)
        
    def handle_transitions(self, event):
       if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
           self.scene_manager.pop_scene()

    def handle_events(self, event):
        pass



class YouLooseSplashScreenScene(SplashScreenScene):
    caption = ScreenText('ПРОИГРЫШ', 10, 50, glb.WHITE, 70)
    texts = [ScreenText('Нажмите Пробел чтобы сыграть уровень заново...', 30, 100, glb.WHITE),
             ScreenText('Нажмите Escape для выхода в Главное меню', 30, 150, glb.WHITE)
             ]

    def enter(self):
        rsc.snd_you_loose.play()

    def leave(self):
        rsc.snd_you_loose.stop()

    def handle_transitions(self, event):
       if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
           # replay level
           self.scene_manager.pop_scene()
           return
       if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
           # return to Main Menu. New Game can be started.
           self.scene_manager.pop_scene()
           gs.game_scene.destroy()
           self.scene_manager.pop_scene()

class YouWinSplashScreenScene(SplashScreenScene):
    caption = ScreenText('ПОБЕДА!', 10, 50, glb.WHITE, 70)
    
    def enter(self):
        rsc.snd_you_win.play()

    def leave(self):
        rsc.snd_you_win.stop()

class FinalSplashScreenScene(SplashScreenScene):
    caption = ScreenText('ВСЯ ИГРА ПРОЙДЕНА!!!', 10, 50, glb.WHITE, 70)
    texts = [ScreenText('Нажмите Escape для выхода в Главное меню', 30, 150, glb.WHITE)
             ]

    def enter(self):
        rsc.snd_final_tune.play()

    def leave(self):
        rsc.snd_final_tune.stop()
        
    def handle_transitions(self, event):
       if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
           # return to Main Menu. New Game can be started.
           self.scene_manager.pop_scene()
           gs.game_scene.destroy()
           self.scene_manager.pop_scene()
    
you_loose_splash_screen = YouLooseSplashScreenScene(glb.MENURECT)
you_win_splash_screen = YouWinSplashScreenScene(glb.MENURECT)
final_splash_screen = FinalSplashScreenScene(glb.MENURECT)