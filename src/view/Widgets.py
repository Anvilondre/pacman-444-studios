import enum
from copy import copy

import pygame

from src.view.ResourceManager import ResourceManager


class Icon(object):
    """This class represents an icon.
    animation_name stands for type of animation for Icon (e.g. "Default", "Lives", "Pause", etc)
    that specifies a folder from which animation frames are loaded."""

    def __init__(self, animation_name, animations_dims, x=0, y=0, icon_state="Default"):
        self.x = x
        self.y = y
        self._animation_name = animation_name
        self.animations = ResourceManager.get_animations_for(self, self._animation_name)
        self.animations = ResourceManager.rescale_animations(self.animations, animations_dims)
        self._width = 0
        self._height = 0
        self.icon_size = self.animations["Default"][0].get_rect().width
        self.current_state = icon_state
        self.icon_states = list(self.animations.keys())
        self._counter_upper_limit = len(self.animations[self.current_state]) - 1
        self.counter = 0

    def image(self):
        self.image = self.animations[self.current_state][self.counter]

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value):
        if 0 <= value <= self._counter_upper_limit:
            self._counter = value
        else:
            self._counter = 0

    @property
    def icon_size(self):
        return self._icon_size

    @icon_size.setter
    def icon_size(self, value):
        if int(value) >= 0:
            self.animations = ResourceManager.rescale_animations(self.animations, (int(value), int(value)))
            self._icon_size = int(value)
            self._width = self._icon_size
            self._height = self._icon_size
        else:
            raise ValueError("Cannot assign icon_size to " + str(value))

    @property
    def current_state(self):
        return self._icon_state

    @current_state.setter
    def current_state(self, value):
        if value in self.animations.keys():
            self._icon_state = value
            self._counter_upper_limit = len(self.animations[self.current_state]) - 1
        else:
            raise ValueError("Cannot assign icon_state to " + str(value) +
                             ". Unable to find appropriate animation type amongst these: " +
                             str(self.icon_states))

    def rescale_current_animations(self, size):
        self.animations[self.current_state][self.counter] = pygame.transform.scale(
            self.animations[self.current_state][self.counter], size)

    def draw(self, target_surface):
        target_surface.blit(self.animations[self.current_state][self.counter], (self.x, self.y))
        self.counter += 1

    def copy(self):
        """Returns a deep copy of an object."""
        copy_icon = Icon(self._animation_name, (self._width, self._height))
        copy_icon.x = copy(self.x)
        copy_icon.y = copy(self.y)
        copy_icon.icon_size = copy(self.icon_size)
        copy_icon._width = copy(self._width)
        copy_icon._height = copy(self._height)
        copy_icon.current_state = copy(self.current_state)
        copy_icon.icon_states = self.icon_states.copy()
        copy_icon._counter_upper_limit = copy(self._counter_upper_limit)
        copy_icon.counter = copy(self.counter)

        return copy_icon


class ChargableIcon(Icon):

    class States(enum.Enum):
        Default = "Default"
        ChargingActive = "ChargingActive"
        ChargingInactive = "ChargingInactive"
        IdleActive = "IdleActive"
        IdleInactive = "IdleInactive"
        DischargingActive = "DischargingActive"
        DischargingInactive = "DischargingInactive"

    class Modes(enum.Enum):
        # TODO UNSTUB
        Auto = "Auto"
        Manual = "Manual"

    def __init__(self, animation_name, animations_dims, discharging_time: int, charging_time: int, x=0, y=0,
                 icon_state="Default", mode=Modes.Manual.value):
        super().__init__(animation_name, animations_dims, x, y, icon_state)
        self.current_state = self.States.IdleInactive.value

        self.discharging_time = discharging_time  # sec
        """Indicates the time (in seconds) needed to discharge from any value."""

        self.charging_time = charging_time  # sec
        """Indicates the time (in seconds) needed to charge from any value."""

        self.MAX_VALUE = 1
        self.MIN_VALUE = 0
        self.current_value = 1  # belongs to [self.MIN_VALUE, self.MAX_VALUE]

    @property
    def current_state(self):
        return self._icon_state

    @current_state.setter
    def current_state(self, value):
        if value in self.animations.keys():
            self._icon_state = value
            self._counter_upper_limit = len(self.animations[self.current_state]) - 1
        else:
            raise ValueError("Cannot assign icon_state to " + str(value) +
                             ". Unable to find appropriate animation type amongst these: " +
                             str(self.icon_states))

    @property
    def current_value(self):
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        if self.MIN_VALUE <= value <= self.MAX_VALUE:
            self._current_value = value
            self._restretch_icon()
        else:
            raise ValueError("current_value cannot be assigned to number outside ["
                             + str(self.MIN_VALUE) + "; " + str(self.MAX_VALUE) + "] interval: ",
                             value)

    def update(self, elapsed_time):
        if self.is_charging():
            if self.current_value + elapsed_time / self.charging_time < self.MAX_VALUE:
                self.current_value += elapsed_time / self.charging_time
            else:
                self.start_idle()
                self.current_value = self.MAX_VALUE

        elif self.is_idle():
            pass

        elif self.is_discharging():
            if self.current_value - elapsed_time / self.discharging_time > self.MIN_VALUE:
                self.current_value -= elapsed_time / self.discharging_time
            else:
                self.start_idle()
                self.current_value = self.MIN_VALUE

    def deactivate(self):
        self.current_state = self.current_state.replace("Active", "Inactive")

    def activate(self):
        self.current_state = self.current_state.replace("Inactive", "Active")

    def is_active(self):
        return True if "Active" in self.current_state else False

    def start_charging(self):
        if self.is_active:
            self.current_state = self.States.ChargingActive.value
        else:
            self.current_state = self.States.ChargingInactive.value

    def start_discharging(self):
        if self.is_active:
            self.current_state = self.States.DischargingActive.value
        else:
            self.current_state = self.States.DischargingInactive.value

    def is_charging(self):
        return True if "Charging" in self.current_state else False

    def is_charged(self):
        return self.current_value == self.MAX_VALUE

    def is_discharging(self):
        return True if "Discharging" in self.current_state else False

    def is_discharged(self):
        return self.current_value == self.MIN_VALUE

    def is_idle(self):
        return True if "Idle" in self.current_state else False

    def charge(self):
        if self.is_active:
            self.current_state = self.States.IdleActive.value
        else:
            self.current_state = self.States.IdleInactive.value
        self.current_value = self.MAX_VALUE

    def discharge(self):
        if self.is_active:
            self.current_state = self.States.IdleActive.value
        else:
            self.current_state = self.States.IdleInactive.value
        self.current_value = self.MIN_VALUE

    def start_idle(self):
        if self.is_active():
            self.current_state = self.States.IdleActive.value
        else:
            self.current_state = self.States.IdleInactive.value

    def _restretch_icon(self):
        self._width = int(self.current_value * self.icon_size)
        self._height = self.icon_size
        self.animations[self.current_state][self.counter] = \
            pygame.transform.scale(
                ResourceManager.get_animations_for(self, self._animation_name)[self.current_state][self.counter],
                (self._width, self._height))

    def copy(self):
        copy_icon = ChargableIcon(self._animation_name, (self._width, self._height),
                                  self.discharging_time, self.charging_time)
        copy_icon.x = copy(self.x)
        copy_icon.y = copy(self.y)
        copy_icon.icon_size = copy(self.icon_size)
        copy_icon._width = copy(self._width)
        copy_icon._height = copy(self._height)
        copy_icon.current_state = copy(self.current_state)
        copy_icon.icon_states = copy(self.icon_states)
        copy_icon._counter_upper_limit = copy(self._counter_upper_limit)
        copy_icon.counter = copy(self.counter)
        copy_icon._restretch_icon()

        return copy_icon


class IconsPack(object):

    class Align(enum.Enum):
        Left = 0
        Center = 1
        Right = 2

    class Order(enum.Enum):
        PopRightAppendRight = 0
        PopLeftAppendLeft = 2

    def __init__(self, boundrect, box_size: int = 87,
                 align=Align.Left, pop_append_order=Order.PopRightAppendRight):
        self.icons = []  # list of Icon
        self.boundrect = boundrect  # icons bounding rect
        self._n = 0  # number of icons
        self.box_size = box_size  # size of box containing single image, px
        self.icons_size = int(box_size)
        self.align = align
        self.pop_append_order = pop_append_order

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, value):
        if value in self.Align:
            self._align = value
            self._rearrange()

    def _rearrange(self):
        if self.icons:
            delta = 0

            if self.align == self.Align.Left:
                delta = self.boundrect.x - min(icon.x for icon in self.icons)

            elif self.align == self.Align.Center:
                # We need to match middle of line of boxes and middle of boundrect
                delta = (self.boundrect.x + self.boundrect.width / 2) - (
                        self.icons[0].x + (self._n * self.box_size) / 2)

            elif self.align == self.Align.Right:
                delta = (self.boundrect.x + self.boundrect.width) - (max(icon.x for icon in self.icons) + self.box_size)

            for icon in self.icons:
                icon.x += delta

    def duplicate(self, n, duplicated_icon: Icon = "duplicate last"):
        """This method sets number of images in a line.
        If n > N, where N is a number of icons already placed in a line, it appends given image n-N times.
        If n < N, where N is a number of icons already placed in a line, it pops given image N-n times.
        If no image was given, it duplicates last image in a line."""

        while self._n > n:
            self.pop()

        while self._n < n:
            if duplicated_icon == "duplicate last":
                # Append last icon in the list
                if self._n >= 1:
                    self.append(self.icons[-1].copy())
                else:
                    raise ValueError("Cannot duplicate 0 icons")
            else:
                self.append(duplicated_icon.copy())

    def append(self, icon: Icon):
        """This method appends given Icon to the line and places after the last one.
        It resizes icons properly if they get bigger than boundrect."""

        icon.y = self.boundrect.y + (self.boundrect.height - self.icons_size) / 2

        if self.align == self.Align.Left:

            if self.pop_append_order == self.Order.PopRightAppendRight:
                if self._n == 0:
                    icon.x = self.boundrect.x
                else:
                    icon.x = max(icon.x for icon in self.icons) + self.box_size
                self.icons.append(icon)
                self._n += 1

            elif self.pop_append_order == self.Order.PopLeftAppendLeft:
                if self._n == 0:
                    icon.x = self.boundrect.x
                else:
                    icon.x = min(icon.x for icon in self.icons) - self.box_size
                self.icons.insert(0, icon)
                self._n += 1

        elif self.align == self.Align.Center:

            if self.pop_append_order == self.Order.PopRightAppendRight:
                if self._n == 0:
                    icon.x = self.boundrect.x
                else:
                    icon.x = max(icon.x for icon in self.icons) + self.box_size
                self.icons.append(icon)
                self._n += 1

            elif self.pop_append_order == self.Order.PopLeftAppendLeft:
                if self._n == 0:
                    icon.x = self.boundrect.x
                else:
                    icon.x = min(icon.x for icon in self.icons) - self.box_size
                self.icons.insert(0, icon)
                self._n += 1

        elif self.align == self.Align.Right:
            if self.pop_append_order == self.Order.PopRightAppendRight:
                if self._n == 0:
                    icon.x = self.boundrect.x + self.boundrect.width - self.box_size
                else:
                    icon.x = max(icon.x for icon in self.icons) + self.box_size
                self.icons.append(icon)
                self._n += 1

            elif self.pop_append_order == self.Order.PopLeftAppendLeft:
                if self._n == 0:
                    icon.x = self.boundrect.x + self.boundrect.width - self.box_size
                else:
                    icon.x = min(icon.x for icon in self.icons) - self.box_size
                self.icons.insert(0, icon)
                self._n += 1

        self._rearrange()
        self._fit_icons_into_boundrect()

    def _fit_icons_into_boundrect(self):
        # FIXME: buggy when n > 10

        # If icons width is greater than width of boundrect..
        icons_width = self._n * self.box_size
        if icons_width > self.boundrect.width:

            # ..then make every icon smaller and change its x position
            correction_ratio = self.boundrect.width / icons_width
            self.icons_size = int(self.icons_size * correction_ratio)
            self.box_size = int(self.box_size * correction_ratio)

            for i, icon in enumerate(self.icons):
                icon.animations = ResourceManager.rescale_animations(icon.animations,
                                                                     (self.icons_size, self.icons_size))
                icon.x = self.boundrect.x + i * self.box_size
                icon.y = self.boundrect.y + (self.boundrect.height - self.icons_size) / 4

    def pop(self):
        """This method pops last Icon in a line. It doesn't change size of Icons left"""
        if self._n > 0:
            self._n -= 1
            if self.pop_append_order == self.Order.PopRightAppendRight:
                self.icons.pop()
            elif self.pop_append_order == self.Order.PopLeftAppendLeft:
                self.icons.pop(0)


class AbilityIconPack(object):

    def __init__(self, boundrect, box_size: int = 87, align=IconsPack.Align.Left,
                 pop_append_order=IconsPack.Order.PopRightAppendRight, mode=ChargableIcon.Modes.Manual.value):

        self.boundrect = boundrect
        self.box_size = box_size
        self.align = align
        self.pop_append_order = pop_append_order
        self.is_cooldown_correction = False

        self._icons = None
        self._charge_icons = None

        self._init_icons(boundrect, box_size, align, pop_append_order)
        self._init_charge_icons(boundrect, box_size, align, pop_append_order, mode)
        self.activated_ability_index = None

    def _init_icons(self, boundrect, box_size, align, pop_append_order):
        self._icons = IconsPack(boundrect, box_size, align, pop_append_order)
        self.ability_boost_icon = Icon("Boost", animations_dims=(box_size, box_size))
        self._icons.append(self.ability_boost_icon)
        self.ability_morph_icon = Icon("Morph", animations_dims=(box_size, box_size))
        self._icons.append(self.ability_morph_icon)

    def _init_charge_icons(self, boundrect, box_size, align, pop_append_order, mode):
        self._charge_icon = ChargableIcon("HorizontalBottom", animations_dims=(box_size, box_size),
                                          discharging_time=30, charging_time=30, mode=mode)
        self._charge_icon.start_idle()
        self._charge_icon.deactivate()
        self._charge_icons = IconsPack(boundrect, box_size, align, pop_append_order)

        self._charge_icons.append(self._charge_icon)
        self._charge_icons.duplicate(len(self._icons.icons), self._charge_icon)

    def update(self, pacman, abilities, cooldown_timer, prev_abilities, prev_cooldown_timer, debug = False):

        # First we find index of ability that is active at the moment.
        # If there is no such ability, then the value of variable stays unchanged
        # (it refers to the ability that was activated in the past)
        # TODO: COULD BE OPTIMIZED AND SET ONCE IN IF(ACTIVATED): ...
        for i in range(len(abilities)):
            if abilities[i].is_active:
                self.activated_ability_index = i

        # If ability and cooldown are not active and pacman has no mana then unset activated_ability_index
        if pacman.mana == 0 and not cooldown_timer.is_alive():
            self.activated_ability_index = None

        if not self.activated_ability_index is None:
            activated_ability = abilities[self.activated_ability_index]

            activated_ability_time_elapsed = activated_ability.duration_timer.elapsed_time
            activated_ability_duration = activated_ability.duration
            cooldown_time_elapsed = cooldown_timer.elapsed_time
            cooldown_duration_corrected = cooldown_timer.duration - activated_ability_duration
        else:
            activated_ability_time_elapsed = 0
            activated_ability_duration = 1
            cooldown_time_elapsed = 0
            cooldown_duration_corrected = 1

        # DEFINE STATES
        for ability, prev_ability in zip(abilities, prev_abilities):

            # If ability has just been activated, then start discharging all charge_icons
            if ability.is_active and not prev_ability.is_active:
                for charge_icon in self._charge_icons.icons:
                    charge_icon.start_discharging()
                break

            # Ability is working right now
            elif ability.is_active:
                for charge_icon in self._charge_icons.icons:
                    charge_icon.start_discharging()
                break

            # Start idle if ability was suddenly deactivated while being active
            elif not ability.is_active and prev_ability.is_active and \
                 not cooldown_timer.is_alive() and prev_cooldown_timer.is_alive():
                for charge_icon in self._charge_icons.icons:
                    charge_icon.start_idle()
                    charge_icon.charge()
                    charge_icon.current_value = charge_icon.current_value

            # If activated_ability has become inactive, then start charging (cooldown)
            elif (self.activated_ability_index is not None and
                  abilities[self.activated_ability_index].is_active is False and
                  prev_abilities[self.activated_ability_index].is_active is True):
                # and charge_icon.is_discharged() is True
                # and charge_icon.is_idle() is False):
                for charge_icon in self._charge_icons.icons:
                    charge_icon.start_charging()
                    charge_icon.current_value = charge_icon.current_value

            # Start idle if cooldown was suddenly deactivated while being active
            elif not ability.is_active and not prev_ability.is_active and \
                 not cooldown_timer.is_alive() and prev_cooldown_timer.is_alive():
                for charge_icon in self._charge_icons.icons:
                    charge_icon.start_idle()
                    charge_icon.charge()
                    charge_icon.current_value = charge_icon.current_value

            # If cooldown is over, then start idle
            elif not cooldown_timer.is_alive():  # charge_icon.is_charging() and charge_icon.is_charged():
                for charge_icon in self._charge_icons.icons:
                    charge_icon.start_idle()
                    charge_icon.current_value = charge_icon.current_value

        # DEFINE ACTIVATION STATE
        for ability, prev_ability, charge_icon, icon in zip(abilities, prev_abilities,
                                                            self._charge_icons.icons, self._icons.icons):
            if ability.is_active or (charge_icon.is_charged() and pacman.mana > 0):
                charge_icon.activate()
                icon.current_state = "Active"
            else:
                charge_icon.deactivate()
                icon.current_state = "Disabled"

            if self.activated_ability_index is not None and \
                    charge_icon is self._charge_icons.icons[self.activated_ability_index]:
                charge_icon.activate()

        # RECALCULATE AND MODIFY CURRENT VALUE
        # Epsilon is used to round current_value to corresponding MIN/MAX VALUE during discharging/charging
        # TODO: epsilon should be a function of variables showing current system performance.
        #  Being a constant, it may perform badly on slow systems. Further investigation is needed.
        epsilon = 0.0050
        for n, charge_icon in zip(range(len(self._charge_icons.icons)), self._charge_icons.icons):

            if charge_icon.is_discharging():
                if debug:
                    print(n, "STATE:", charge_icon.current_state, "; VAL:", charge_icon.current_value, "; DECREMENT BY:",
                          activated_ability_time_elapsed / activated_ability_duration, "; ELAPSE:",
                          activated_ability_time_elapsed, "; DUR:",
                          activated_ability_duration)

                potential_value = charge_icon.current_value - activated_ability_time_elapsed/activated_ability_duration
                if potential_value > charge_icon.MIN_VALUE and activated_ability_time_elapsed >= 0:

                    # Round to charge_icon.MIN_VALUE if value is in epsilon-neighbourhood of charge_icon.MIN_VALUE
                    if charge_icon.MIN_VALUE <= potential_value <= charge_icon.MIN_VALUE + epsilon:
                        if debug:
                            print("FORCED ROUNDING AT", potential_value)
                        potential_value = charge_icon.MIN_VALUE
                    charge_icon.current_value = potential_value

                else:
                    charge_icon.current_value = charge_icon.MIN_VALUE

            elif charge_icon.is_charging():
                if debug:
                    print(n, "STATE:", charge_icon.current_state, "; VAL:", charge_icon.current_value, "; DECREMENT BY:",
                          cooldown_time_elapsed / cooldown_duration_corrected, "; ELAPSE:", cooldown_time_elapsed, "; DUR:",
                          cooldown_duration_corrected)

                potential_value = charge_icon.current_value + cooldown_time_elapsed/cooldown_duration_corrected
                if potential_value < charge_icon.MAX_VALUE and cooldown_time_elapsed >= 0:

                    # Round to charge_icon.MAX_VALUE if value is in epsilon-neighbourhood of charge_icon.MAX_VALUE
                    if charge_icon.MAX_VALUE - epsilon <= potential_value <= charge_icon.MAX_VALUE:
                        if debug:
                            print("FORCED ROUNDING AT", potential_value)
                        potential_value = charge_icon.MAX_VALUE

                    charge_icon.current_value = potential_value

                else:
                    charge_icon.current_value = charge_icon.MAX_VALUE

            elif charge_icon.is_idle():
                if debug:
                    print(n, "STATE:", charge_icon.current_state, "; VAL:", charge_icon.current_value)
                    charge_icon.current_value = charge_icon.current_value

    def draw(self, target_surface):
        for icon in self._icons.icons + self._charge_icons.icons:
            target_surface.blit(icon.animations[icon.current_state][icon.counter], (icon.x, icon.y))
            icon.counter += 1