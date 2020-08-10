# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 21:24:09 2020

@author: Семен
"""
import pygame
import game_globals as glb
import os
from screen_text import BitmapFont
from animation import Animation

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

def extract_spritesheet(image, x_start, y_start, tile_width, tile_height, 
                        rows, spacing):
    """
    Extract spritesheet from loaded image.

    Parameters
    ----------
    image : pygame.Surface
    rows : list
        list of number of tiles for every row.
    spacing : int
        spacing (in pixels) between neighbor tiles on image (separating lines)

    Returns
    -------
    result : list of lists of pygame.Surface
        list of lists of surfaces with dimension as specified in 'rows'.

    """
    image_rect = image.get_rect()
    result = []
    for i, num_tiles_in_row in enumerate(rows):
        result.append(list())
        for j in range(num_tiles_in_row):
            tile = pygame.Surface((tile_width, tile_height))
            x = x_start + (tile_width + spacing) * j
            y = y_start + (tile_height + spacing) * i
            tile_rect = pygame.Rect(x, y, tile_width, tile_height)
            if not image_rect.contains(tile_rect):
                raise ValueError(f'tile ({i}, {j}) is not within the image')
                
            tile.blit(surface, (0, 0), (x, y, tile_width, tile_height))
            result[i].append(tile)
    return result

# load images
logo_image = load_image(f'{glb.DATA_DIR}/logo2.png', True)

ground_image = load_image(f'{glb.DATA_DIR}/ground.png', False)
banana_image = load_image(f'{glb.DATA_DIR}/banana.png', True)
apple_image = load_image(f'{glb.DATA_DIR}/apple.png', True)
mushroom_image = load_image(f'{glb.DATA_DIR}/mushroom.png', True)
potion_image = load_image(f'{glb.DATA_DIR}/potion.png', True)
ananas_image = load_image(f'{glb.DATA_DIR}/ananas.png', True)
portal_image = load_image(f'{glb.DATA_DIR}/portal.png', True)

banana_animation_params = {'id2image_dict': {i: v for i, v in enumerate([
                                banana_image,
                                pygame.transform.rotate(banana_image, -5),
                                pygame.transform.rotate(banana_image, 5),
                                ])
                             },
                    'frames': [(0, glb.FPS*3), (1, 10), (2, 10), (1, 10), (2, 10) ]
                    }

apple_animation_params = {'id2image_dict': {i: v for i, v in enumerate([
                                apple_image,
                                pygame.transform.scale(apple_image, (40, 35)),
                                ])
                             },
                    'frames': [(0, glb.FPS*3), (1, 10), (0, 10), (1, 10) ]
                    }

mushroom_animation_params = {'id2image_dict': {i: v for i, v in enumerate([
                                mushroom_image,
                                pygame.transform.scale(mushroom_image, (40, 35)),
                                ])
                             },
                    'frames': [(0, glb.FPS*3), (1, 10), (0, 10), (1, 10) ]
                    }

ananas_animation_params = {'id2image_dict': {i: v for i, v in enumerate([
                                ananas_image,
                                pygame.transform.rotate(ananas_image, -5),
                                pygame.transform.rotate(ananas_image, 5),
                                ])
                             },
                    'frames': [(0, glb.FPS*3), (1, 10), (2, 10), (1, 10), (2, 10) ]
                    }

potion_animation_params = {'id2image_dict': {i: v for i, v in enumerate([
                                potion_image,
                                pygame.transform.scale(potion_image, (40, 35)),
                                ])
                             },
                    'frames': [(0, glb.FPS*3), (1, 10), (0, 10), (1, 10) ]
                    }

portal_animation_params = {'id2image_dict': {i: v for i, v in enumerate([
                                portal_image,
                                pygame.transform.rotate(portal_image, -90),
                                pygame.transform.rotate(portal_image, -180),
                                pygame.transform.rotate(portal_image, 90),
                                ])
                             },
                           'frames':  [(i, 10) for i in range(4)]
                            }

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
tail_curve_image = load_image(f'{glb.DATA_DIR}/tail_curve.png', True)
tail_curve_90 = pygame.transform.rotate(tail_curve_image, -90)
tail_curve_180 = pygame.transform.rotate(tail_curve_image, 180)
tail_curve_270 = pygame.transform.rotate(tail_curve_image, 90)
tail_curve_flip_h = pygame.transform.flip(tail_curve_image, True, False)

# create directional tables for sprites images by rotation/mirroring
dir2img_head = dir2img_template(head_image)
dir2img_body = dir2img_template(body_straight_image)
# add kinks from -> to for body segment
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

dir2img_tail = dir2img_template(tail_image)
# add kinks from -> to for tail segment
dir2img_tail[(glb.DIRECTION_UP, glb.DIRECTION_RIGHT)] = tail_curve_image
dir2img_tail[(glb.DIRECTION_UP, glb.DIRECTION_LEFT)] = tail_curve_flip_h
dir2img_tail[(glb.DIRECTION_RIGHT, glb.DIRECTION_DOWN)] = tail_curve_90
dir2img_tail[(glb.DIRECTION_DOWN, glb.DIRECTION_LEFT)] = tail_curve_180
dir2img_tail[(glb.DIRECTION_LEFT, glb.DIRECTION_UP)] = tail_curve_270
dir2img_tail[(glb.DIRECTION_RIGHT, glb.DIRECTION_UP)] = pygame.transform.flip(
    tail_curve_270, True, False)
dir2img_tail[(glb.DIRECTION_DOWN, glb.DIRECTION_RIGHT)] = pygame.transform.flip(
    tail_curve_180, True, False)     
dir2img_tail[(glb.DIRECTION_LEFT, glb.DIRECTION_DOWN)] = pygame.transform.flip(
    tail_curve_270, False, True)  


# load custom font
charset = (f" !\"#$%&'()*+,-./0123456789:;<=>?@"
           "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
           "[\\]^_`{|}~"
           )

char2img_dict = {}
FONT_DIR = f'{glb.DATA_DIR}/fonts/BoxyBold/Double'
for filename in os.listdir(FONT_DIR):
    img_id = int(filename.split('.')[0])
    char_img = pygame.image.load(f'{FONT_DIR}/{filename}')
    char2img_dict[charset[img_id]] = char_img

bitmap_font = BitmapFont(char2img_dict, spacing=2, double_size=False) 
bitmap_font_large = BitmapFont(char2img_dict, spacing=4, double_size=True) 


# load sounds
def load_sound(filename, volume=glb.SOUND_VOLUME):
    s = pygame.mixer.Sound(filename)
    s.set_volume(volume)
    return s

snd_eat_good_food = load_sound(f'{glb.DATA_DIR}/sound/eat_good_food.wav')
snd_eat_bad_food = load_sound(f'{glb.DATA_DIR}/sound/eat_bad_food.ogg')
snd_eat_potion = load_sound(f'{glb.DATA_DIR}/sound/eat_potion.ogg')
snd_you_win = load_sound(f'{glb.DATA_DIR}/sound/you_win.wav')
snd_you_loose = load_sound(f'{glb.DATA_DIR}/sound/you_loose.wav')
snd_menu_blip = load_sound(f'{glb.DATA_DIR}/sound/menu_blip.wav')
snd_menu_enter = load_sound(f'{glb.DATA_DIR}/sound/menu_enter.wav')
snd_final_tune = load_sound(f'{glb.DATA_DIR}/sound/final_tune.ogg')
snd_clock_tick = load_sound(f'{glb.DATA_DIR}/sound/tick.wav')