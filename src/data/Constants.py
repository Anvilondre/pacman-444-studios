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
forms = ('Red', 'Green', 'Blue')
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
BOTTOM_BAR_HEIGHT_RATIO = 1.25 / 22
BOTTOM_BAR_WIDTH_RATIO = 1000 / 1920
BOTTOM_BAR_X_RATIO = 460 / 1920
BOTTOM_BAR_Y_RATIO = 1030 / 1080

LIVES_BAR_X_RATIO = BOTTOM_BAR_X_RATIO
LIVES_BAR_Y_RATIO = BOTTOM_BAR_Y_RATIO

ABILITIES_BAR_X_RATIO = BOTTOM_BAR_X_RATIO
ABILITIES_BAR_Y_RATIO = BOTTOM_BAR_Y_RATIO
MANA_BAR_X_RATIO = 470 / 1920
MANA_BAR_Y_RATIO = 1030 / 1920

# GameLogic
DESIRED_PHYSICS_TICK_TIME = 0.001
DESIRED_AI_TICK_TIME = 0.2
DESIRED_RENDER_TICK_TIME = 0.001
PACMAN_PX_PER_SECOND = 36 * 5
PACMAN_BOOST_PX_PER_SECOND = 36 * 3.5
GHOST_PX_PER_SECOND = 36 * 5

GLOBAL_TICK_RATE = 60

# Game

SECTOR_SIZE = 36
# 5:9:5
LIVES_BAR_WIDTH = 5 / 19
ABILITIES_BAR_WIDTH = 9 / 19
MANA_BAR_WIDTH = 5 / 19

GAMESCREEN_BOUNDBOX_SURF_WIDTH_RATIO = 1920 / 1920
GAMESCREEN_BOUNDBOX_SURF_HEIGHT_RATIO = 900 / 1080
GAMESCREEN_CELL_SIZE_RATIO = 36 * 2 / 1920
GAMESCREEN_COLOR = ((42, 37, 105))

# Animation
ANIMATION_PERIOD = 0.1  # seconds

# Debug
HITBOX_OPACITY = 96
HITBOX_COLOR = ((0, 255, 198))

# TickTimeDebugger


''' All file paths '''

# Game

SCREEN_BACKGROUND_COLOR = ((35, 24, 89))
FONT_COLOR = (205, 245, 255)
FONT_SIZE_RATIO = 28 / 684

# PacMan

PACMAN_MAPOBJECT_HITBOX_PATH = "../res/hitbox/pacman_mapobject.png"
PACMAN_CREATURE_HITBOX_PATH = "../res/hitbox/pacman_creature.png"
PACMAN_RED_ANIMATIONS_PATHS = {"move_left": ["../res/animations/pacman/red/move_left/0.png",
                                             "../res/animations/pacman/red/move_left/1.png",
                                             "../res/animations/pacman/red/move_left/2.png",
                                             "../res/animations/pacman/red/move_left/3.png"],
                               "move_up": ["../res/animations/pacman/red/move_up/0.png",
                                           "../res/animations/pacman/red/move_up/1.png",
                                           "../res/animations/pacman/red/move_up/2.png",
                                           "../res/animations/pacman/red/move_up/3.png"],
                               "move_right": ["../res/animations/pacman/red/move_right/0.png",
                                              "../res/animations/pacman/red/move_right/1.png",
                                              "../res/animations/pacman/red/move_right/2.png",
                                              "../res/animations/pacman/red/move_right/3.png"],
                               "move_down": ["../res/animations/pacman/red/move_down/0.png",
                                             "../res/animations/pacman/red/move_down/1.png",
                                             "../res/animations/pacman/red/move_down/2.png",
                                             "../res/animations/pacman/red/move_down/3.png"],
                               "dead": ["../res/animations/pacman/red/dead/0.png",
                                        "../res/animations/pacman/red/dead/1.png",
                                        "../res/animations/pacman/red/dead/2.png",
                                        "../res/animations/pacman/red/dead/3.png",
                                        "../res/animations/pacman/red/dead/4.png",
                                        "../res/animations/pacman/red/dead/5.png",
                                        "../res/animations/pacman/red/dead/6.png",
                                        "../res/animations/pacman/red/dead/7.png",
                                        "../res/animations/pacman/red/dead/8.png"]}

PACMAN_GREEN_ANIMATIONS_PATHS = {"move_left": ["../res/animations/pacman/green/move_left/0.png",
                                               "../res/animations/pacman/green/move_left/1.png",
                                               "../res/animations/pacman/green/move_left/2.png",
                                               "../res/animations/pacman/green/move_left/3.png"],
                                 "move_up": ["../res/animations/pacman/green/move_up/0.png",
                                             "../res/animations/pacman/green/move_up/1.png",
                                             "../res/animations/pacman/green/move_up/2.png",
                                             "../res/animations/pacman/green/move_up/3.png"],
                                 "move_right": ["../res/animations/pacman/green/move_right/0.png",
                                                "../res/animations/pacman/green/move_right/1.png",
                                                "../res/animations/pacman/green/move_right/2.png",
                                                "../res/animations/pacman/green/move_right/3.png"],
                                 "move_down": ["../res/animations/pacman/green/move_down/0.png",
                                               "../res/animations/pacman/green/move_down/1.png",
                                               "../res/animations/pacman/green/move_down/2.png",
                                               "../res/animations/pacman/green/move_down/3.png"],
                                 "dead": ["../res/animations/pacman/green/dead/0.png",
                                          "../res/animations/pacman/green/dead/1.png",
                                          "../res/animations/pacman/green/dead/2.png",
                                          "../res/animations/pacman/green/dead/3.png",
                                          "../res/animations/pacman/green/dead/4.png",
                                          "../res/animations/pacman/green/dead/5.png",
                                          "../res/animations/pacman/green/dead/6.png",
                                          "../res/animations/pacman/green/dead/7.png",
                                          "../res/animations/pacman/green/dead/8.png"]}

PACMAN_BLUE_ANIMATIONS_PATHS = {"move_left": ["../res/animations/pacman/blue/move_left/0.png",
                                              "../res/animations/pacman/blue/move_left/1.png",
                                              "../res/animations/pacman/blue/move_left/2.png",
                                              "../res/animations/pacman/blue/move_left/3.png"],
                                "move_up": ["../res/animations/pacman/blue/move_up/0.png",
                                            "../res/animations/pacman/blue/move_up/1.png",
                                            "../res/animations/pacman/blue/move_up/2.png",
                                            "../res/animations/pacman/blue/move_up/3.png"],
                                "move_right": ["../res/animations/pacman/blue/move_right/0.png",
                                               "../res/animations/pacman/blue/move_right/1.png",
                                               "../res/animations/pacman/blue/move_right/2.png",
                                               "../res/animations/pacman/blue/move_right/3.png"],
                                "move_down": ["../res/animations/pacman/blue/move_down/0.png",
                                              "../res/animations/pacman/blue/move_down/1.png",
                                              "../res/animations/pacman/blue/move_down/2.png",
                                              "../res/animations/pacman/blue/move_down/3.png"],
                                "dead": ["../res/animations/pacman/blue/dead/0.png",
                                         "../res/animations/pacman/blue/dead/1.png",
                                         "../res/animations/pacman/blue/dead/2.png",
                                         "../res/animations/pacman/blue/dead/3.png",
                                         "../res/animations/pacman/blue/dead/4.png",
                                         "../res/animations/pacman/blue/dead/5.png",
                                         "../res/animations/pacman/blue/dead/6.png",
                                         "../res/animations/pacman/blue/dead/7.png",
                                         "../res/animations/pacman/blue/dead/8.png"]}

# Ghosts

GHOST_MAPOBJECT_HITBOX_PATH = "../res/hitbox/ghost_mapobject.png"
GHOST_CREATURE_HITBOX_PATH = "../res/hitbox/ghost_creature.png"
GHOST_RED_ANIMATIONS_PATHS = {"move_left": ["../res/animations/ghost/red/move_left/0.png",
                                            "../res/animations/ghost/red/move_left/1.png"],
                              "move_up": ["../res/animations/ghost/red/move_up/0.png",
                                          "../res/animations/ghost/red/move_up/1.png"],
                              "move_right": ["../res/animations/ghost/red/move_right/0.png",
                                             "../res/animations/ghost/red/move_right/1.png"],
                              "move_down": ["../res/animations/ghost/red/move_down/0.png",
                                            "../res/animations/ghost/red/move_down/1.png"],
                              "dead": ["../res/animations/ghost/red/dead/0.png",
                                       "../res/animations/ghost/red/dead/1.png",
                                       "../res/animations/ghost/red/dead/2.png",
                                       "../res/animations/ghost/red/dead/3.png"]}

GHOST_GREEN_ANIMATIONS_PATHS = {"move_left": ["../res/animations/ghost/green/move_left/0.png",
                                              "../res/animations/ghost/green/move_left/1.png"],
                                "move_up": ["../res/animations/ghost/green/move_up/0.png",
                                            "../res/animations/ghost/green/move_up/1.png"],
                                "move_right": ["../res/animations/ghost/green/move_right/0.png",
                                               "../res/animations/ghost/green/move_right/1.png"],
                                "move_down": ["../res/animations/ghost/green/move_down/0.png",
                                              "../res/animations/ghost/green/move_down/1.png"],
                                "dead": ["../res/animations/ghost/green/dead/0.png",
                                         "../res/animations/ghost/green/dead/1.png",
                                         "../res/animations/ghost/green/dead/2.png",
                                         "../res/animations/ghost/green/dead/3.png"]}

GHOST_BLUE_ANIMATIONS_PATHS = {"move_left": ["../res/animations/ghost/blue/move_left/0.png",
                                             "../res/animations/ghost/blue/move_left/1.png"],
                               "move_up": ["../res/animations/ghost/blue/move_up/0.png",
                                           "../res/animations/ghost/blue/move_up/1.png"],
                               "move_right": ["../res/animations/ghost/blue/move_right/0.png",
                                              "../res/animations/ghost/blue/move_right/1.png"],
                               "move_down": ["../res/animations/ghost/blue/move_down/0.png",
                                             "../res/animations/ghost/blue/move_down/1.png"],
                               "dead": ["../res/animations/ghost/blue/dead/0.png",
                                        "../res/animations/ghost/blue/dead/1.png",
                                        "../res/animations/ghost/blue/dead/2.png",
                                        "../res/animations/ghost/blue/dead/3.png"]}

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

# Floor
FLOOR_HITBOX_PATH = "../res/hitbox/floor.png"
FLOOR_TEXTURE_PATH = "../res/textures/floor.png"

# Icons
LIVES_ICON_ANIMATIONS_PATH = {"Default": ["../res/icons/lives/default/0.png"]}

ABILITIES_CHARGEBAR_ANIMATIONS_PATH = {"Default": ["../res/icons/abilities/chargebar/default/0.png"],
                                       "ChargingActive": ["../res/icons/abilities/chargebar/ChargingActive/0.png"],
                                       "ChargingInactive": ["../res/icons/abilities/chargebar/ChargingInactive/0.png"],
                                       "IdleActive": ["../res/icons/abilities/chargebar/IdleActive/0.png"],
                                       "IdleInactive": ["../res/icons/abilities/chargebar/IdleInactive/0.png"],
                                       "DischargingActive": ["../res/icons/abilities/chargebar/DischargingActive/0.png"],
                                       "DischargingInactive": ["../res/icons/abilities/chargebar/DischargingInactive/0.png"]}
BOOST_ICON_ANIMATIONS_PATH = {"Default": ["../res/icons/boost/default/0.png"],
                              "Active": ["../res/icons/boost/active/0.png"],
                              "Disabled": ["../res/icons/boost/disabled/0.png"],
                              "Pushed": ["../res/icons/boost/pushed/0.png"]}
MORPH_ICON_ANIMATIONS_PATH = {"Default": ["../res/icons/morph/default/0.png"],
                              "Active": ["../res/icons/morph/active/0.png"],
                              "Disabled": ["../res/icons/morph/disabled/0.png"],
                              "Pushed": ["../res/icons/morph/pushed/0.png"]}
MANA_ICON_ANIMATIONS_PATH = {"Default": ["../res/icons/mana/default/0.png"]}

# Debugger
DEFAULT_GRAPH_SAVEPATH = "debug/graphs/ticktime.png"

# Fonts
FRANKLIN_FONT_PATH = "../res/fonts/orange kid.ttf"
