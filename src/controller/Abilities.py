from abc import ABC, abstractmethod
from threading import Timer
from src.data.Constants import pacman_boost, pacman_velocity, ghost_velocity, ghost_slowdown


class Ability(ABC):

    @abstractmethod
    def __init__(self, pacman):
        self.pacman = pacman

    @property
    @abstractmethod
    def duration(self):
        pass

    @property
    def duration_timer(self):
        return Timer(self.duration, self.deactivate)

    @abstractmethod
    def run(self):
        self.activate()
        self.duration_timer.start()

    @abstractmethod
    def deactivate(self):
        pass

    @abstractmethod
    def activate(self):
        pass


class SpeedAbility(Ability):

    """ Speeds pacman up while ability is active """

    duration = 5  # TODO

    def __init__(self, pacman):
        super().__init__(pacman)

    def run(self):
        super().run()

    def activate(self):
        self.pacman.velocity += pacman_boost

    def deactivate(self):
        self.pacman.velocity = pacman_velocity


class TransformAbility(Ability):

    """ Lets player freely cycle through forms while ability is active """

    duration = 5  # TODO

    def __init__(self, pacman, ghosts):
        self.ghosts = ghosts
        self.is_active = False
        super().__init__(pacman)

    def run(self):
        super().run()

    def activate(self):
        self.is_active = True
        for ghost in self.ghosts:
            ghost.velocity -= ghost_slowdown

    def deactivate(self):
        self.is_active = False
        for ghost in self.ghosts:
            ghost.velocity = ghost_velocity

    def changeForm(self):

        # Hardcoded

        if self.is_active:
            if self.pacman.form == 'red':
                self.pacman.form = 'green'

            elif self.pacman.form == 'green':
                self.pacman.form = 'blue'

            else:
                self.pacman.form = 'red'
