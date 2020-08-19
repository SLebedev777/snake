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
from particles import Particle
from random import randint, uniform, gauss

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
    particles = []
   
    def update(self):
        # particle fireworks VFX
        # create new bunch of sparks
        if randint(0, glb.FPS) == 5:
            x = randint(self.rect.left + 30, self.rect.right - 30)
            y = randint(self.rect.top + 150, self.rect.bottom - 10)
            color = [randint(150, 255), randint(150, 255), randint(150, 255)]
            color[randint(0, 2)] -= 150
            gravity = 0.1
            bounding_rect = self.rect.inflate(-10, -10)
            for i in range(randint(80, 200)):
                vx = gauss(0, 3)
                vy = -uniform(6, 2)
                radius = randint(2, 5)
                glow_size = radius*2
                glow_value = 30
                lifetime = randint(3*glb.FPS, 5*glb.FPS)
                particle = Particle(x, y, vx, vy, color, radius, lifetime, gravity,
                              vx_func=lambda vx: vx - 0.02,
                              size_func=lambda size: size - 0.03,
                              rect=bounding_rect,
                              glow_size=glow_size, glow_value=glow_value,
                              glow_size_func=lambda gsz: gsz - 0.02,
                              glow_value_func=lambda gval: gval - 0.2)
                self.particles.append(particle)

        self.particles = [p for p in self.particles if p.alive]
        
        super().update()


    def draw(self, screen):
        # draw particles twice a frame: before and after coordinates update,
        # to emulate "spark trace" effect
        for particle in self.particles:
            particle.draw(screen)
            particle.update()
            particle.draw(screen)
        super().draw(screen)
    
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