from abc import ABC, abstractmethod
from src.data.Constants import CHERRY_VALUE, MEGAPELLET_VALUE, PELLET_VALUE


class MapObject(ABC):

    @abstractmethod
    def __init__(self, coord, hitbox, texture):
        self.coord = coord
        self.hitbox = hitbox
        self.texture = texture

    @property
    @abstractmethod
    def hitbox(self):
        pass

    @property
    @abstractmethod
    def texture(self):
        pass


class Pellet(MapObject):

    def __init__(self, coord, hitbox="", texture="", value = PELLET_VALUE):
        self.value = value
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: Pellet"


class MegaPellet(MapObject):

    def __init__(self, coord, hitbox="", texture="", value=MEGAPELLET_VALUE):
        self.value = value
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: MegaPellet"


class Cherry(MapObject):

    def __init__(self, coord, hitbox="", texture="", value=CHERRY_VALUE):
        self.value = value
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: Cherry"


class Wall(MapObject):
    def __init__(self, coord, hitbox="", texture=""):
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: Wall"
