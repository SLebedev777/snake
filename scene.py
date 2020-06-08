# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:26:04 2020

@author: Семен
"""
import abc
import pygame
import sys

from collections import defaultdict


class Scene(abc.ABC):
    """
    Abstract MVC-entity in the game.
    Can be implemented as playable level, menu, splash screen etc.
    
    Scene supports Observer pattern. Scene itself is the subject. 
    First, observers (actors, game objects) can submit to events from the stream
    (keyboard/mouse...), and then Scene calls observer's method 
    when submitted event comes.

    Scene-derived subclass must override methods for game loop:
        .build()         - build scene, separatedly from light-weight init
        
        .handle_events() - controller for input events
        .update()        - model (logic)
        .draw()          - view (render)
        
    Each Scene subclass realizes State pattern.
    Override methods:
        .handle_transitions() - changing scenes logic
        .enter()              - optional method on entering scene when scene changes
        .leave()              - optional method on leaving scene when scene changes

    Scenes are operated by SceneManager class (the context class).

    In fact, concrete Scene subclasses are "static" classes, or singletons. 
    To do this work, each concrete Scene subclass should be made 
    in a separate module with one instance of that class, and then imported.
    For ex, consider module "my_scene.py":
        from scene import Scene
        
        class MyScene(Scene):
            # ...implementation...
            
        myscene = MyScene()

    Client code:
        from my_scene import myscene        
    """
    
    def __init__(self, rect): 
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        self.scene_manager = None
        self.group = None
        self.rect = rect
        self.background = pygame.Surface(self.rect.size)
        self.timer = None
        self.built = False

    def bind_scene_manager(self, scene_manager):
        self.scene_manager = scene_manager

    def set_rect(self, rect):
        self.rect = rect
        self.background = pygame.Surface(self.rect.size)

    def build(self):
        pass
        
    def update(self):
        pass

    def clear_screen(self, screen):
        pass
    
    def draw(self, screen):
        pass

    def handle_transitions(self, event):
        """
        Must implement logic of transitions from this scene to some other scenes.     
        """
        pass
    
    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # call submitted observers
        elif event.type == pygame.KEYDOWN:
            for handler in self.keydown_handlers[event.key]:
                handler(event.key)
        elif event.type == pygame.KEYUP:
            for handler in self.keydown_handlers[event.key]:
                handler(event.key)
        elif event.type in (pygame.MOUSEBUTTONDOWN, 
                            pygame.MOUSEBUTTONUP, 
                            pygame.MOUSEMOTION):
            for handler in self.mouse_handlers:
                handler(event.type, event.pos)

    def enter(self):
        pass
    
    def leave(self):
        pass
    
    def destroy(self):
        self.built = False