# -*- coding: utf-8 -*-
"""
Created on Thu May 28 16:13:38 2020

@author: Семен
"""
import pygame

import game_globals as glb
from scene_manager import SceneManager
from menu_scene import *
from game_scene import *

from splash import *

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.mouse.set_visible(0)
    scenes = [main_menu,
              options_menu,
              difficulty_menu,
              game_scene,
              you_loose_splash_screen,
              you_win_splash_screen,
              final_splash_screen
              ]
    
    # create scene manager
    scene_manager = SceneManager(glb.WIDTH, glb.HEIGHT, glb.FPS)
    
    # build and register scenes
    for scene in scenes:
        if scene != game_scene:
            # we build main game scene later, only when difficulty is chosen
            scene.build()
        scene.bind_scene_manager(scene_manager)

    # add starting scene and launch game loop
    scene_manager.push_scene(main_menu)
    scene_manager.main_loop()
