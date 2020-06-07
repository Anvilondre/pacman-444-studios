"""
This module contains all the pre-defined values present in game
Structure:
    1. Creatures parameters - game settings
        a) General
        b) PacMan
        c) Ghost
    2. View parameters - window settings
        a) Window
        b) Game
    3. All file paths - self-explanatory
        a) Game
        b) PacMan
        c) Ghost
"""

''' Creatures parameters '''

# General

directions = ('left', 'up', 'right', 'down')
forms = ('red', 'green', 'blue')
PELLET_VALUE = 10
MEGAPELLET_VALUE = 50
CHERRY_VALUE = 100
GHOST_VALUE = 200

# PacMan

pacman_cooldown = 30
pacman_mana = 0
pacman_score = 0
pacman_lives = 3

# Ghost

ghost_is_chasing = True

''' View parameters '''

# Window

IS_FULLSCREEN = False
WINDOWED_SCREEN_WIDTH = 960
WINDOWED_SCREEN_HEIGHT = 684
TOP_BAR_HEIGHT_RATIO = 1 / 22
TOP_BAR_WIDTH_RATIO = 1000 / 1920
BOTTOM_BAR_HEIGHT_RATIO = 1 / 22
BOTTOM_BAR_WIDTH_RATIO = 1000 / 1920
BOTTOM_BAR_X_RATIO = 460 / 1920
BOTTOM_BAR_Y_RATIO = 1030 / 1080

LIVES_BAR_X_RATIO = BOTTOM_BAR_X_RATIO
LIVES_BAR_Y_RATIO = BOTTOM_BAR_Y_RATIO

ABILITIES_BAR_X_RATIO = BOTTOM_BAR_X_RATIO
ABILITIES_BAR_Y_RATIO = BOTTOM_BAR_Y_RATIO
FRUITS_BAR_X_RATIO = 470 / 1920
FRUITS_BAR_Y_RATIO = 1030 / 1920

# Game

SECTOR_SIZE = 36
LIVES_BAR_WIDTH = 350 / 1000
ABILITIES_BAR_WIDTH = 450 / 1000
FRUITS_BAR_WIDTH = 200 / 1000

GAMESCREEN_BOUNDBOX_SURF_WIDTH_RATIO = 1920 / 1920  # TODO: Add explanation
GAMESCREEN_BOUNDBOX_SURF_HEIGHT_RATIO = 980 / 1080
GAMESCREEN_CELL_SIZE_RATIO = 36 * 2 / 1920

# Animation
ANIMATION_PERIOD = 0.1  # seconds

# Debug
HITBOX_OPACITY = 96
HITBOX_COLOR = ((0, 255, 198))

''' All file paths '''

# Game

SCREEN_BACKGROUND_IMAGE = ...  # TODO: Add path

# PacMan

PACMAN_MAPOBJECT_HITBOX_PATH = "../res/hitbox/pacman_mapobject.png"
PACMAN_CREATURE_HITBOX_PATH = "../res/hitbox/pacman_creature.png"
pacman_animations_paths = {"move_left": ["../res/animations/pacman/move_left/0.png",
                                         "../res/animations/pacman/move_left/1.png",
                                         "../res/animations/pacman/move_left/2.png",
                                         "../res/animations/pacman/move_left/3.png"],
                           "move_up": ["../res/animations/pacman/move_up/0.png",
                                       "../res/animations/pacman/move_up/1.png",
                                       "../res/animations/pacman/move_up/2.png",
                                       "../res/animations/pacman/move_up/3.png"],
                           "move_right": ["../res/animations/pacman/move_right/0.png",
                                          "../res/animations/pacman/move_right/1.png",
                                          "../res/animations/pacman/move_right/2.png",
                                          "../res/animations/pacman/move_right/3.png"],
                           "move_down": ["../res/animations/pacman/move_down/0.png",
                                         "../res/animations/pacman/move_down/1.png",
                                         "../res/animations/pacman/move_down/2.png",
                                         "../res/animations/pacman/move_down/3.png"],
                           "dead": ["../res/animations/pacman/dead/0.png",
                                    "../res/animations/pacman/dead/1.png",
                                    "../res/animations/pacman/dead/2.png",
                                    "../res/animations/pacman/dead/3.png",
                                    "../res/animations/pacman/dead/4.png",
                                    "../res/animations/pacman/dead/5.png",
                                    "../res/animations/pacman/dead/6.png",
                                    "../res/animations/pacman/dead/7.png",
                                    "../res/animations/pacman/dead/8.png"]}

# Ghosts

GHOST_MAPOBJECT_HITBOX_PATH = "../res/hitbox/ghost_mapobject.png"
GHOST_CREATURE_HITBOX_PATH = "../res/hitbox/ghost_creature.png"
pinky_animations_paths = {"move_left": ["../res/animations/pinky/move_left/0.png",
                                        "../res/animations/pinky/move_left/1.png"],
                          "move_up": ["../res/animations/pinky/move_up/0.png",
                                      "../res/animations/pinky/move_up/1.png"],
                          "move_right": ["../res/animations/pinky/move_right/0.png",
                                         "../res/animations/pinky/move_right/1.png"],
                          "move_down": ["../res/animations/pinky/move_down/0.png",
                                        "../res/animations/pinky/move_down/1.png"],
                          "dead": ["../res/animations/pinky/dead/0.png",
                                   "../res/animations/pinky/dead/1.png",
                                   "../res/animations/pinky/dead/2.png",
                                   "../res/animations/pinky/dead/3.png"]}

# Wall
WALL_HITBOX_PATH = "../res/hitbox/wall.png"
WALL_TEXTURE_PATH = "../res/textures/wall.png"

# Cherry
CHERRY_HITBOX_PATH = "../res/hitbox/wall.png"
CHERRY_TEXTURE_PATH = "../res/textures/wall.png"

# Pellet
PELLET_HITBOX_PATH = "../res/hitbox/pellet.png"
PELLET_TEXTURE_PATH = "../res/textures/pellet.png"

# Mega pellet
MEGAPELLET_HITBOX_PATH = "../res/hitbox/mega_pellet.png"
MEGAPELLET_TEXTURE_PATH = "../res/textures/mega_pellet.png"
