# -*- coding: utf-8 -*-
"""
Created on Sat May 30 19:08:56 2020

@author: Семен
"""

import pygame
from scene import Scene
from scene_manager import SceneManager
from screen_text import ScreenText, ScreenTextBitmapFont
import game_globals as glb
from actor import dirtyrects
from group import Group

import os, sys

import game_scene as gs
import resources as rsc

class SplashScreenScene(Scene):
    caption = None
    texts = [ScreenTextBitmapFont('Press Space to continue', 50, 100, rsc.bitmap_font)]
    
    def build(self):
        self.group = Group([self.caption] + self.texts)
        for actor in self.group:
            actor.move(self.rect.left, self.rect.top)
        self.background.fill(glb.DARK_GREY)
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
    font_size = rsc.bitmap_font.height
    caption = ScreenTextBitmapFont('YOU LOOSE :(', 50, 50, rsc.bitmap_font_large)
    texts = [ScreenTextBitmapFont('Press Space to replay', 50, 100, rsc.bitmap_font),
             ScreenTextBitmapFont('Press Esc to main menu', 50, 110+font_size, rsc.bitmap_font),
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
    caption = ScreenTextBitmapFont('YOU WIN!', 110, 50, rsc.bitmap_font_large)
    
    def enter(self):
        rsc.snd_you_win.play()

    def leave(self):
        rsc.snd_you_win.stop()

class FinalSplashScreenScene(SplashScreenScene):
    caption = ScreenTextBitmapFont('ALL GAME FINISHED!!!', 60, 100, rsc.bitmap_font_large)
    texts = [ScreenTextBitmapFont('Press Esc to Main Menu', 170, 400, rsc.bitmap_font)]
    
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
    
you_loose_splash_screen = YouLooseSplashScreenScene(glb.SPLASHRECT)
you_win_splash_screen = YouWinSplashScreenScene(glb.SPLASHRECT)
final_splash_screen = FinalSplashScreenScene(glb.FINALSPLASHRECT)