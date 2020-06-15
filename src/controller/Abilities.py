from abc import ABC, abstractmethod


class Ability(ABC):

    @abstractmethod
    def __init__(self, duration):
        self.duration = duration  # sec
        self.is_active = False
        self.elapsed_time_counter = 0

    def update(self, elapsed_time):
        if self.is_active:
            self.elapsed_time_counter += elapsed_time
        if self.elapsed_time_counter > self.duration:
            self.deactivate()
            self.elapsed_time_counter = 0

    @abstractmethod
    def deactivate(self):
        pass

    @abstractmethod
    def activate(self):
        pass


class SpeedAbility(Ability):
    """ Speeds pacman up while ability is active """

    def __init__(self, pacman, duration, pacman_vel, pacman_boost):
        self.pacman = pacman
        self.pacman_velocity = pacman_vel
        self.pacman_boost = pacman_boost
        self.is_active = False
        self.elapsed_time_counter = 0
        super().__init__(duration)

    def update(self, elapsed_time):
        if self.is_active:
            self.elapsed_time_counter += elapsed_time
        if self.elapsed_time_counter > self.duration:
            self.deactivate()
            self.elapsed_time_counter = 0

    def activate(self, pacman_vel, pacman_boost):
        self.pacman_velocity = pacman_vel
        self.pacman_boost = pacman_boost
        self.is_active = True
        self.pacman.velocity = int(pacman_vel + pacman_boost)

    def deactivate(self):
        self.is_active = False
        self.pacman.velocity = int(self.pacman_velocity)


class TransformAbility(Ability):
    """ Lets player freely cycle through forms while ability is active """

    def __init__(self, pacman, duration, ghosts, ghost_velocity, ghost_slowdown):
        self.pacman = pacman
        self.ghosts = ghosts
        self.ghost_velocity = ghost_velocity
        self.ghost_slowdown = ghost_slowdown
        self.is_active = False
        self.elapsed_time_counter = 0
        super().__init__(duration)

    def update(self, elapsed_time):
        if self.is_active:
            self.elapsed_time_counter += elapsed_time
        if self.elapsed_time_counter > self.duration:
            self.deactivate()
            self.elapsed_time_counter = 0

    def activate(self):
        self.is_active = True
        for ghost in self.ghosts:
            ghost.velocity -= self.ghost_slowdown

    def deactivate(self):
        self.is_active = False
        for ghost in self.ghosts:
            ghost.velocity = self.ghost_velocity

    def changeForm(self):

        # Hardcoded

        if self.is_active:
            if self.pacman.form == 'Red':
                self.pacman.form = 'Green'

            elif self.pacman.form == 'Green':
                self.pacman.form = 'Blue'

            else:
                self.pacman.form = 'Red'


class IterativeTimer():

    def __init__(self, pacman, duration):
        self.pacman = pacman
        self.ghosts = ghosts
        self.ghost_velocity = ghost_velocity
        self.ghost_slowdown = ghost_slowdown
        self.is_active = False
        self.elapsed_time_counter = 0
        super().__init__(duration)

    def update(self, elapsed_time):
        if self.is_active:
            self.elapsed_time_counter += elapsed_time
        if self.elapsed_time_counter > self.duration:
            self.deactivate()
            self.elapsed_time_counter = 0

    def activate(self):
        self.is_active = True
        for ghost in self.ghosts:
            ghost.velocity -= self.ghost_slowdown

    def deactivate(self):
        self.is_active = False
        for ghost in self.ghosts:
            ghost.velocity = self.ghost_velocity
