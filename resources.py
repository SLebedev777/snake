# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 21:24:09 2020

@author: Семен
"""
import pygame
import game_globals as glb

def load_image(filename, transparent):
    "loads an image, prepares it for play"
    try:
        surface = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (filename, pygame.get_error()))
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, pygame.locals.RLEACCEL)
    return surface.convert()

def dir2img_template(image):
    """
    Basic template for creating table of images according to 4 directions without kinks:
        UP, RIGHT, DOWN, LEFT
    """
    return {
        (glb.DIRECTION_UP, glb.DIRECTION_UP): image,
        (glb.DIRECTION_RIGHT, glb.DIRECTION_RIGHT): pygame.transform.rotate(image, -90),
        (glb.DIRECTION_DOWN, glb.DIRECTION_DOWN): pygame.transform.rotate(image, 180),
        (glb.DIRECTION_LEFT, glb.DIRECTION_LEFT): pygame.transform.rotate(image, 90)
        }


# load images
logo_image = load_image(f'{glb.DATA_DIR}/logo2.png', True)

ground_image = load_image(f'{glb.DATA_DIR}/ground.png', False)
banana_image = load_image(f'{glb.DATA_DIR}/banana.png', True)
apple_image = load_image(f'{glb.DATA_DIR}/apple.png', True)
mushroom_image = load_image(f'{glb.DATA_DIR}/mushroom.png', True)
potion_image = load_image(f'{glb.DATA_DIR}/potion.png', True)
ananas_image = load_image(f'{glb.DATA_DIR}/ananas.png', True)


wall_image = load_image(f'{glb.DATA_DIR}/wall.png', True)

fence_horiz_image = load_image(f'{glb.DATA_DIR}/fence.png', True)
fence_horiz_image_flip_v = pygame.transform.flip(fence_horiz_image, False, True)
fence_vert_image = pygame.transform.rotate(fence_horiz_image, 90)
fence_vert_image_flip_h = pygame.transform.rotate(fence_horiz_image, -90)
fence_corner_image = load_image(f'{glb.DATA_DIR}/fence_corner.png', True)
fence_corner_image_flip_h = pygame.transform.flip(fence_corner_image, True, False)
fence_corner_image_flip_v = pygame.transform.flip(fence_corner_image, False, True)
fence_corner_image_flip_hv = pygame.transform.flip(fence_corner_image, True, True)

head_image = load_image(f'{glb.DATA_DIR}/head.png', True)
tail_image = load_image(f'{glb.DATA_DIR}/tail.png', True)
body_straight_image = load_image(f'{glb.DATA_DIR}/body_straight.png', True)
body_curve_image = load_image(f'{glb.DATA_DIR}/body_curve.png', True)
body_curve_90 = pygame.transform.rotate(body_curve_image, -90)
body_curve_180 = pygame.transform.rotate(body_curve_image, 180)
body_curve_270 = pygame.transform.rotate(body_curve_image, 90)
body_curve_flip_h = pygame.transform.flip(body_curve_image, True, False)

# create directional tables for sprites images by rotation/mirroring
dir2img_head = dir2img_template(head_image)
dir2img_tail = dir2img_template(tail_image)
dir2img_body = dir2img_template(body_straight_image)
# add kinks from -> to
dir2img_body[(glb.DIRECTION_UP, glb.DIRECTION_RIGHT)] = body_curve_image
dir2img_body[(glb.DIRECTION_UP, glb.DIRECTION_LEFT)] = body_curve_flip_h
dir2img_body[(glb.DIRECTION_RIGHT, glb.DIRECTION_DOWN)] = body_curve_90
dir2img_body[(glb.DIRECTION_DOWN, glb.DIRECTION_LEFT)] = body_curve_180
dir2img_body[(glb.DIRECTION_LEFT, glb.DIRECTION_UP)] = body_curve_270
dir2img_body[(glb.DIRECTION_RIGHT, glb.DIRECTION_UP)] = pygame.transform.flip(
    body_curve_270, True, False)
dir2img_body[(glb.DIRECTION_DOWN, glb.DIRECTION_RIGHT)] = pygame.transform.flip(
    body_curve_180, True, False)     
dir2img_body[(glb.DIRECTION_LEFT, glb.DIRECTION_DOWN)] = pygame.transform.flip(
    body_curve_270, False, True)  

# load sounds
snd_eat_good_food = pygame.mixer.Sound(f'{glb.DATA_DIR}/sound/eat_good_food.wav')
snd_eat_bad_food = pygame.mixer.Sound(f'{glb.DATA_DIR}/sound/eat_bad_food.ogg')
snd_eat_potion = pygame.mixer.Sound(f'{glb.DATA_DIR}/sound/eat_potion.ogg')
snd_you_win = pygame.mixer.Sound(f'{glb.DATA_DIR}/sound/you_win.wav')
snd_you_loose = pygame.mixer.Sound(f'{glb.DATA_DIR}/sound/you_loose.wav')
snd_menu_blip = pygame.mixer.Sound(f'{glb.DATA_DIR}/sound/menu_blip.wav')
snd_menu_enter = pygame.mixer.Sound(f'{glb.DATA_DIR}/sound/menu_enter.wav')
snd_final_tune = pygame.mixer.Sound(f'{glb.DATA_DIR}/sound/final_tune.ogg')
snd_clock_tick = pygame.mixer.Sound(f'{glb.DATA_DIR}/sound/tick.wav')