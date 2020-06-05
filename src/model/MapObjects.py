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
    def __init__(self, coord, hitbox, texture, value):
        super().__init__(coord, hitbox, texture)
        self.value = value

    def hitbox(self):
        pass

    def texture(self):
        pass


class Pellet(MapObject):
    value = 10

    def __init__(self, coord, hitbox, texture):
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass


class MegaPellet(MapObject):
    value = 50

    def __init__(self, coord, hitbox, texture):
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass


class MegaPellet(MapObject):
    value = 100

    def __init__(self, coord, hitbox, texture):
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass


class MegaPellet(MapObject):
    def __init__(self, coord, hitbox, texture):
        super().__init__(coord, hitbox, texture)

    def hitbox(self):
        pass

    def texture(self):
        pass
