from abc import ABC, abstractmethod
from copy import copy


class Ability(ABC):

    @abstractmethod
    def __init__(self, duration):
        self.duration = duration  # sec
        self.is_active = False
        self.duration_timer = IterativeTimer(self.duration, self.deactivate)
        self.elapsed_time_counter = 0

    def update(self, elapsed_time):
        self.duration_timer.update(elapsed_time)

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

    @abstractmethod
    def copy(self):
        pass


class SpeedAbility(Ability):
    """ Speeds pacman up while ability is active """

    def __init__(self, pacman, duration, pacman_vel, pacman_boost):
        self.pacman = pacman
        self.pacman_velocity = pacman_vel
        self.pacman_boost = pacman_boost
        self.is_active = False
        super().__init__(duration)

    def run(self, pacman_vel, pacman_boost):
        self.activate(pacman_vel, pacman_boost)
        self.duration_timer.start()

    def activate(self, pacman_vel, pacman_boost):
        self.pacman_velocity = pacman_vel
        self.pacman_boost = pacman_boost
        self.is_active = True
        self.pacman.velocity = pacman_vel + pacman_boost

    def deactivate(self):
        self.is_active = False
        self.pacman.velocity = self.pacman_velocity
        self.duration_timer.cancel()

    def copy(self):
        """Returns deepcopy of this SpeedAbility object."""
        speed_ability_copy = SpeedAbility(self.pacman.copy(), copy(self.duration),
                                          copy(self.pacman_velocity), copy(self.pacman_boost))
        speed_ability_copy.is_active = copy(self.is_active)
        speed_ability_copy.duration_timer = self.duration_timer.copy()
        return speed_ability_copy


class TransformAbility(Ability):
    """ Lets player freely cycle through forms while ability is active """

    def __init__(self, pacman, duration):
        self.pacman = pacman
        self.is_active = False
        super().__init__(duration)

    def run(self):
        super().run()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
        self.duration_timer.cancel()

    def changeForm(self):

        # TODO: Unhardcode it

        if self.is_active:
            if self.pacman.form == 'Red':
                self.pacman.form = 'Green'

            elif self.pacman.form == 'Green':
                self.pacman.form = 'Blue'

            else:
                self.pacman.form = 'Red'

    def copy(self):
        """Returns deepcopy of this TransformAbility object."""
        transform_ability_copy = TransformAbility(self.pacman.copy(), copy(self.duration))
        transform_ability_copy.is_active = copy(self.is_active)
        transform_ability_copy.duration_timer = self.duration_timer.copy()
        return transform_ability_copy


class IterativeTimer(object):
    """This class is an iterative single-threaded alternative for Timer class.
    - Call start() to start the timer. When time runs out cancel() method is automatically called.
      Thus, you can use this timer repeatedly.
    - Call update(elapsed_time) to update its internal clock. Elapsed time is time elapsed from
      previous tick in your program.
      If update() is not called at all, then timer would never go off.
    - Call cancel() to cancel the timer."""

    def __init__(self, interval, function):
        self.duration = interval
        self.elapsed_time = 0
        self._function = function
        self._is_alive = False
        self._elapsed_time_counter = 0

    def update(self, elapsed_time):
        # print("TIMER COUNTER:", self.get_elapsed_time())
        if self.is_alive() is True:
            self.elapsed_time = elapsed_time
            self._elapsed_time_counter += elapsed_time

            if self._elapsed_time_counter >= self.duration:
                self._function()
                self.cancel()

    def is_alive(self):
        return self._is_alive

    def start(self):
        self.elapsed_time = 0
        self._elapsed_time_counter = 0
        self._is_alive = True

    def cancel(self):
        self.elapsed_time = 0
        self._elapsed_time_counter = 0
        self._is_alive = False

    def copy(self):
        """Returns deepcopy of this object."""
        timer_copy = IterativeTimer(self.duration, self._function)
        timer_copy._is_alive = copy(self._is_alive)
        timer_copy.elapsed_time = copy(self.elapsed_time)
        timer_copy._elapsed_time_counter = copy(self._elapsed_time_counter)
        return timer_copy

    def get_elapsed_time(self):
        return self._elapsed_time_counter
