import os

import pygame

from src.data import Constants
from src.data.Constants import PELLET_VALUE


# window = pygame.display.set_mode((200, 200))
class MapObject():

    def __init__(self, coord, width, height, hitbox_path, texture):
        self.coord = coord
        self.width = width
        self.height = height
        self.hitbox = self.create_hitbox_of(hitbox_path, coord[0], coord[1])
        self.texture = texture

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._width = value
            return
        if isinstance(value, float):
            self._width = round(value)
            return

        if value < 0:
            raise ValueError("Width cannot be assigned to negative value:", value)
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("Width cannot be assigned to non-numeric object:", type(value), value)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._height = value
            return
        if isinstance(value, float):
            self._height = round(value)
            return

        if value < 0:
            raise ValueError("Height cannot be assigned to negative value:", value)
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("Height cannot be assigned to non-numeric object:", type(value), value)

    @property
    def hitbox(self):
        return self._hitbox

    @hitbox.setter
    def hitbox(self, value):
        self._hitbox = value

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, texture_path):

        img = pygame.image.load(texture_path)
        img = pygame.transform.scale(img, (self.width, self.height))
        img = img.convert_alpha()

        self._texture = img

    def create_hitbox_of(self, path, x=0, y=0):
        """Returns sprite with mask created from given image"""
        if os.path.exists(path):
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (self.width, self.height))

            # Create sprite that has creature's size
            sprite = pygame.sprite.Sprite()
            sprite.surface = pygame.Surface((self.width, self.height))

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


class Pellet(MapObject):

    def __init__(self, coord, width=Constants.SECTOR_SIZE, height=Constants.SECTOR_SIZE,
                 hitbox_path=Constants.PELLET_HITBOX_PATH, texture=Constants.PELLET_TEXTURE_PATH,
                 value=PELLET_VALUE):
        self.value = value
        super().__init__(coord, width, height, hitbox_path, texture)

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: Pellet"


class MegaPellet(MapObject):

    def __init__(self, coord, width=Constants.SECTOR_SIZE, height=Constants.SECTOR_SIZE,
                 hitbox_path=Constants.MEGAPELLET_HITBOX_PATH, texture=Constants.MEGAPELLET_TEXTURE_PATH,
                 value=PELLET_VALUE):
        self.value = value
        super().__init__(coord, width, height, hitbox_path, texture)

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: MegaPellet"


class Cherry(MapObject):

    def __init__(self, coord, width=Constants.SECTOR_SIZE, height=Constants.SECTOR_SIZE,
                 hitbox_path=Constants.CHERRY_HITBOX_PATH, texture=Constants.CHERRY_TEXTURE_PATH,
                 value=PELLET_VALUE):
        self.value = value
        super().__init__(coord, width, height, hitbox_path, texture)

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: Cherry"


class Wall(MapObject):
    def __init__(self, coord, width=Constants.SECTOR_SIZE, height=Constants.SECTOR_SIZE,
                 hitbox_path=Constants.WALL_HITBOX_PATH, texture=Constants.WALL_TEXTURE_PATH):
        super().__init__(coord, width, height, hitbox_path, texture)

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: Wall"


class Floor(MapObject):
    def __init__(self, coord, width=Constants.SECTOR_SIZE, height=Constants.SECTOR_SIZE,
                 hitbox_path=Constants.FLOOR_HITBOX_PATH, texture=Constants.FLOOR_TEXTURE_PATH):
        super().__init__(coord, width, height, hitbox_path, texture)
