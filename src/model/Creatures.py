from abc import ABC, abstractmethod


class Creature(ABC):

    @abstractmethod
    def x(self):
        pass


class PacMan(Creature):
    def __init__(self):
        pass

    @property
    def x(self):
        return 1



pac = PacMan()
