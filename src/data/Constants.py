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

# PacMan

pacman_cooldown = 30
pacman_mana = 0
pacman_score = 0
pacman_lives = 3

# Ghost

ghost_is_chasing = True

''' View parameters '''

# Window

IS_FULLSCREEN = True
WINDOWED_SCREEN_WIDTH = 960
WINDOWED_SCREEN_HEIGHT = 540
TOP_BAR_HEIGHT_RATIO = 1 / 22
TOP_BAR_WIDTH_RATIO = 1000 / 1920
BOTTOM_BAR_HEIGHT_RATIO = 1 / 22
BOTTOM_BAR_WIDTH_RATIO = 1000 / 1920

# Game

SECTOR_SIZE = 36
LIVES_BAR_WIDTH = 350 / 1000
ABILITIES_BAR_WIDTH = 450 / 1000
FRUITS_BAR_WIDTH = 200 / 1000

GAMESCREEN_BOUNDBOX_SURF_WIDTH_RATIO = 1920 / 1920  # TODO: Add explanation
GAMESCREEN_BOUNDBOX_SURF_HEIGHT_RATIO = 980 / 1080
GAMESCREEN_CELL_SIZE_RATIO = 36 / 1920


''' All file paths '''

# Game

SCREEN_BACKGROUND_IMAGE = ...  # TODO: Add path

# PacMan

pacman_hitbox_path = "../../res/hitbox/pacman.png"
pacman_animations_paths = {"move_left": ["../../res/animations/pacman/move_left/0.png",
                                         "../../res/animations/pacman/move_left/1.png",
                                         "../../res/animations/pacman/move_left/2.png",
                                         "../../res/animations/pacman/move_left/3.png"],
                           "move_up": ["../../res/animations/pacman/move_up/0.png",
                                       "../../res/animations/pacman/move_up/1.png",
                                       "../../res/animations/pacman/move_up/2.png",
                                       "../../res/animations/pacman/move_up/3.png"],
                           "move_right": ["../../res/animations/pacman/move_right/0.png",
                                          "../../res/animations/pacman/move_right/1.png",
                                          "../../res/animations/pacman/move_right/2.png",
                                          "../../res/animations/pacman/move_right/3.png"],
                           "move_down": ["../../res/animations/pacman/move_down/0.png",
                                         "../../res/animations/pacman/move_down/1.png",
                                         "../../res/animations/pacman/move_down/2.png",
                                         "../../res/animations/pacman/move_down/3.png"],
                           "dead": ["../../res/animations/pacman/dead/0.png",
                                    "../../res/animations/pacman/dead/1.png",
                                    "../../res/animations/pacman/dead/2.png",
                                    "../../res/animations/pacman/dead/3.png"]}

# Ghosts

ghost_hitbox_path = "../../res/hitbox/ghost.png"
pinky_animations_paths = {"move_left": ["../../res/animations/pinky/move_left/0.png",
                                        "../../res/animations/pinky/move_left/1.png",
                                        "../../res/animations/pinky/move_left/2.png",
                                        "../../res/animations/pinky/move_left/3.png"],
                          "move_up": ["../../res/animations/pinky/move_up/0.png",
                                      "../../res/animations/pinky/move_up/1.png",
                                      "../../res/animations/pinky/move_up/2.png",
                                      "../../res/animations/pinky/move_up/3.png"],
                          "move_right": ["../../res/animations/pinky/move_right/0.png",
                                         "../../res/animations/pinky/move_right/1.png",
                                         "../../res/animations/pinky/move_right/2.png",
                                         "../../res/animations/pinky/move_right/3.png"],
                          "move_down": ["../../res/animations/pinky/move_down/0.png",
                                        "../../res/animations/pinky/move_down/1.png",
                                        "../../res/animations/pinky/move_down/2.png",
                                        "../../res/animations/pinky/move_down/3.png"],
                          "dead": ["../../res/animations/pinky/dead/0.png",
                                   "../../res/animations/pinky/dead/1.png",
                                   "../../res/animations/pinky/dead/2.png",
                                   "../../res/animations/pinky/dead/3.png"]}