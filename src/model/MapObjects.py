from abc import ABC, abstractmethod


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
    value = 10

    def __init__(self, coord, hitbox="", texture=""):
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: Pellet "

class MegaPellet(MapObject):
    value = 50

    def __init__(self, coord, hitbox="", texture=""):
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: MegaPellet "


class Cherry(MapObject):
    value = 100

    def __init__(self, coord, hitbox="", texture=""):
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: Cherry "


class Wall(MapObject):
    def __init__(self, coord, hitbox="", texture=""):
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass

    def __str__(self):
        return "coord: " + str(self.coord) + "; type: Wall "
