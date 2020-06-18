import enum
import os
from copy import copy

import pygame

from src.data import Constants


class ResourceManager(object):

    animations = dict()

    class AnimationsOwners(enum.Enum):
        PacMan = "PacMan"
        Ghost = "Ghost"
        Icon = "Icon"
        ChargableIcon = "ChargableIcon"
        Background = "Background"

    """{"%animation_owner%": {"%animation_name%": %animation_dict%:, "%animation_name%": %animation_dict%, ..}}"""

    @staticmethod
    def load_resources():
        ResourceManager.load_animations()

    @staticmethod
    def load_animations():

        ResourceManager.animations[ResourceManager.AnimationsOwners.PacMan] = \
            {"Red": ResourceManager.get_animations_from(Constants.PACMAN_RED_ANIMATIONS_PATHS),
             "Green": ResourceManager.get_animations_from(Constants.PACMAN_GREEN_ANIMATIONS_PATHS),
             "Blue": ResourceManager.get_animations_from(Constants.PACMAN_BLUE_ANIMATIONS_PATHS)}

        ResourceManager.animations[ResourceManager.AnimationsOwners.Ghost] = \
            {"Red": ResourceManager.get_animations_from(Constants.GHOST_RED_ANIMATIONS_PATHS),
             "Green": ResourceManager.get_animations_from(Constants.GHOST_GREEN_ANIMATIONS_PATHS),
             "Blue": ResourceManager.get_animations_from(Constants.GHOST_BLUE_ANIMATIONS_PATHS)}

        ResourceManager.animations[ResourceManager.AnimationsOwners.Icon] =\
            {"Lives": ResourceManager.get_animations_from(Constants.LIVES_ICON_ANIMATIONS_PATH),
             "Boost": ResourceManager.get_animations_from(Constants.BOOST_ICON_ANIMATIONS_PATH),
             "Morph": ResourceManager.get_animations_from(Constants.MORPH_ICON_ANIMATIONS_PATH),
             "Mana": ResourceManager.get_animations_from(Constants.MANA_ICON_ANIMATIONS_PATH)}

        ResourceManager.animations[ResourceManager.AnimationsOwners.ChargableIcon] =\
            {"HorizontalBottom": ResourceManager.get_animations_from(Constants.ABILITIES_CHARGEBAR_ANIMATIONS_PATH)}

        ResourceManager.animations[ResourceManager.AnimationsOwners.Background] =\
            {"Default": ResourceManager.get_animations_from(Constants.BACKGROUND_ANIMATIONS_PATH)}

    @staticmethod
    def get_animations_for(animation_owner, animation_name):
        """This method returns a copy of animations dict for a class of given object"""
        animations_copy = dict()

        for animation_type, animation_frame in ResourceManager.animations[animation_owner][animation_name].items():

            # Create list of images which are located at given path (at animations_paths)
            animation_frames_list = []
            for frame in animation_frame:
                animation_frames_list.append(frame.copy())

            # Insert this list at corresponding key (animation type)
            animations_copy[animation_type] = animation_frames_list

        return animations_copy

    @staticmethod
    def get_animations_from(animations_paths_dict, dimensions="original"):

        if animations_paths_dict and isinstance(animations_paths_dict, dict):
            animations = dict()

            for animation_type, animation_paths_list in animations_paths_dict.items():

                # Create list of images which are located at given path (at animations_paths)
                animation_images_list = []
                for path in animation_paths_list:
                        animation_images_list.append(ResourceManager.get_image_from(path, dimensions))

                # Insert this list at corresponding key (animation type)
                animations[animation_type] = animation_images_list

            return animations

    @staticmethod
    def get_image_from(icon_path, dimensions: ()):
        img = pygame.image.load(icon_path)
        if dimensions != "original":
            img = pygame.transform.scale(img, dimensions)
        img = img.convert_alpha()
        return img

    @staticmethod
    def rescale_animations(animations, dimensions):

        animations_copy = dict()

        for animation_type, animation_frame in animations.items():

            # Create list of images which are located at given path (at animations_paths)
            animation_frames_list = []
            for frame in animation_frame:
                animation_frames_list.append(pygame.transform.scale(frame, dimensions))

            # Insert this list at corresponding key (animation type)
            animations_copy[animation_type] = animation_frames_list

        return animations_copy

        #
        # for key, animation in animations.items():
        #     for frame_i in range(len(animation)):
        #         animations[key][frame_i] = pygame.transform.scale(animations[key][frame_i], (size, size))

    @staticmethod
    def get_hitbox_of(path, dimensions, x=0, y=0):
        """Returns sprite with mask created from given image"""

        if os.path.exists(path):
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, dimensions)

            # Create sprite that has creature's size
            sprite = pygame.sprite.Sprite()
            sprite.surface = pygame.Surface(dimensions)

            # Make image transparent
            sprite.image = img.convert_alpha()

            # Get mask out of the image
            sprite.mask = pygame.mask.from_surface(sprite.image)
            sprite.rect = sprite.image.get_rect()

            # Move sprite to the creature's position
            sprite.rect.move_ip(x, y)

            return sprite
        else:
            raise ValueError("Wrong path. Path does not exist.")

    @staticmethod
    def copy_sprite(sprite):
        sprite_copy = pygame.sprite.Sprite()
        sprite_copy.surface = sprite.surface.copy()
        sprite_copy.image = sprite.image.copy()
        sprite_copy.mask = pygame.mask.from_surface(sprite_copy.image)
        sprite_copy.rect = sprite.rect.copy()

        return sprite_copy