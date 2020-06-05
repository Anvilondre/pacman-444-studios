from abc import ABC, abstractmethod


class Ability(ABC):

    @abstractmethod
    def __init__(self, pacman):
        self.pacman = pacman

    @property
    @abstractmethod
    def duration(self):
        pass

    @property
    @abstractmethod
    def duration_timer(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def deactivate(self):
        pass

    @abstractmethod
    def activate(self):
        pass


class SpeedAbility(Ability):
    duration = 10  # TODO
    duration_timer = ...  # TODO

    def __init__(self, pacman):
        super().__init__(pacman)

    def run(self):
        raise NotImplementedError

    def activate(self):
        raise NotImplementedError

    def deactivate(self):
        raise NotImplementedError


class TransformAbility(Ability):
    duration = 10  # TODO
    duration_timer = ...  # TODO

    def __init__(self, pacman, ghosts):
        self.ghosts = ghosts
        super().__init__(pacman)

    def run(self):
        raise NotImplementedError

    def activate(self):
        raise NotImplementedError

    def deactivate(self):
        raise NotImplementedError
