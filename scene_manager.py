# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:40:49 2020

@author: Семен
"""
import pygame
import sys
import game_globals as glb

class SceneManager:
    """
    Context class (in terms of State pattern), that executes current scene
    and manipulates the stack of scenes (simple Pushdown Automata).
    
    With SceneManager and concrete scenes, we can implement graph of scenes
    in the game, with transitions between them, depending on various events.
    """   
    def __init__(self, width, height, fps):
        self.running = True
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.toggle_fullscreen()
        self.rect = pygame.Rect(0, 0, width, height)
        self.fps = fps 
        self.clock = pygame.time.Clock()
        self.stack = []
        
    def push_scene(self, scene):
        if not scene.built:
            raise SceneManagerException("SceneManager: can't push unbuilt scene to stack")
        if self.stack:
            self.active_scene.leave()
        self.stack.append(scene)
        self.active_scene.enter()
    
    def pop_scene(self):
        self.check_stack()
        self.active_scene.leave()
        self.stack.pop()
        if self.stack:
            self.active_scene.enter()

    def check_stack(self):
        if not self.stack:
            raise SceneManagerException("SceneManager: stack is empty")
        
    @property
    def active_scene(self):
        self.check_stack()
        return self.stack[-1]
    
    def main_loop(self):
        while self.running:
            self.screen.blit(self.active_scene.background, 
                             (self.active_scene.rect.left, self.active_scene.rect.top))
            self.active_scene.clear_screen(self.screen)
            self.active_scene.handle_events()
            self.active_scene.update()
            self.active_scene.draw(self.screen)            
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.active_scene.handle_transitions()
        pygame.quit()
        sys.exit()            

    def toggle_fullscreen(self):
        if glb.FULLSCREEN_MODE:
            self.screen = pygame.display.set_mode((self.width, self.height), 
                                                  pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))

            

class SceneManagerException(Exception): 
    pass