import os
import pygame
import random
from src.data import Constants
from src.view.ResourceManager import ResourceManager


class Creature(object):

    def __init__(self, x, y, initial_location, width, height, velocity, direction, form,
                 mapobject_hitbox, creature_hitbox, animations):
        self.initial_location = initial_location
        self.width = width
        self.height = height
        self.velocity = velocity
        self.direction = direction
        self.preferred_direction = self.direction
        self.form = form
        self.mapobject_hitbox = mapobject_hitbox #ResourceManager.create_hitbox_of(mapobject_hitbox_path, (self.width, self.height))
        self.creature_hitbox = creature_hitbox #ResourceManager.create_hitbox_of(creature_hitbox_path, (self.width, self.height))
        self._x = 0
        self._y = 0
        self.x = x
        self.y = y
        self.coord = (self.x, self.y)
        self.animations = animations
        self.animation_count = 0
        self.is_alive = True

    @property
    def is_alive(self):
        return self._is_alive

    @is_alive.setter
    def is_alive(self, value):
        if value is True:
            self._is_alive = True
        elif value is False:
            self._is_alive = False
        else:
            raise ValueError("is_alive cannot be assigned to non-bool object:", type(value), value)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):

        if isinstance(value, int) or isinstance(value, float):
            if isinstance(value, float):
                value = round(value)

            # Update hitbox x coordinate
            self.mapobject_hitbox.rect.move_ip(value - self.x, 0)
            self.creature_hitbox.rect.move_ip(value - self.x, 0)
            # Update creature's x coordinate
            self._x = value
            return

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):

        if isinstance(value, int) or isinstance(value, float):
            if isinstance(value, float):
                value = round(value)

            # Update hitbox y coordinate
            self.mapobject_hitbox.rect.move_ip(0, value - self.y)
            self.creature_hitbox.rect.move_ip(0, value - self.y)
            # Update creature's y coordinate
            self._y = value
            return

    @property
    def coord(self):
        return self.x, self.y

    @coord.setter
    def coord(self, value: tuple):
        if value[0] >= 0 and value[1] >= 0:
            self._x = value[0]
            self._y = value[1]
            return

    @property
    def initial_location(self):
        return self._initial_location

    @initial_location.setter
    def initial_location(self, value: tuple):
        if value[0] >= 0 and value[1] >= 0:
            value = (int(value[0]), int(value[1]))
            self._initial_location = value
            return

        if value[0] < 0 or value[1] < 0:
            raise ValueError("initial_value cannot be assigned to tuple with negative coordinate(s):", value)

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
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._velocity = value
        if value < 0:
            raise ValueError("Velocity cannot be assigned to negative value:", value)
        if not isinstance(value, int):
            raise TypeError("Velocity cannot be assigned to non-int object:", type(value), value)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value: str):
        if value in Constants.directions and isinstance(value, str):
            self._direction = value
            return
        if value not in Constants.directions:
            raise ValueError("Direction can only take these values: " + Constants.directions.__str__() + "\nInstead, it took:", value)
        if not isinstance(value, str):
            raise TypeError("Direction cannot be assigned to non-str object:", type(value), value)

    @property
    def preferred_direction(self):
        return self._preferred_direction

    @preferred_direction.setter
    def preferred_direction(self, value: str):
        if value in Constants.directions and isinstance(value, str):
            self._preferred_direction = value
            return
        # if value not in Constants.directions:
        #     raise ValueError("preferred_direction can only take these values: " +
        #                      Constants.directions.__str__() + "\nInstead, it took:",value)
        # if not isinstance(value, str):
        #     raise TypeError("preferred_direction cannot be assigned to non-str object:", type(value), value)

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, value: str):
        if value in Constants.forms and isinstance(value, str):
            self._form = value
            return

        if value not in Constants.forms:
            raise ValueError("Form can only take these values: " + Constants.forms.__str__() + "\nInstead, it took:", value)
        if not isinstance(value, str):
            raise TypeError("Form cannot be assigned to non-str object:", type(value), value)

    @property
    def mapobject_hitbox(self):
        return self._mapobject_hitbox

    @mapobject_hitbox.setter
    def mapobject_hitbox(self, value):
        if isinstance(value, pygame.sprite.Sprite):
            self._mapobject_hitbox = value
            return

        if not isinstance(value, pygame.sprite.Sprite):
            raise TypeError("mapobject_hitbox cannot be assigned to non-sprite object: ", type(value), value)

    @property
    def creature_hitbox(self):
        return self._creature_hitbox

    @creature_hitbox.setter
    def creature_hitbox(self, value):
        if isinstance(value, pygame.sprite.Sprite):
            self._creature_hitbox = value
            return

        if not isinstance(value, pygame.sprite.Sprite):
            raise TypeError("creature_hitbox cannot be assigned to non-sprite object: ", type(value), value)

    @property
    def animations(self):
        return self._animations

    @animations.setter
    def animations(self, animations: dict):
        self._animations = animations

    def __str__(self):
        return "x: " + str(self.x) + "; y: " + str(self.y) + "; initial_location: " + str(self.initial_location) + \
               "; width: " + str(self.width) + "; height: " + str(self.height) + \
               "; velocity: " + str(self.velocity) + "; direction: " + str(self.direction) + \
               "; form: " + str(self.form) + "; mapobject_hitbox: " + str(self.mapobject_hitbox.image) + \
               "; creature_hitbox: " + str(self.creature_hitbox.image) + \
               ";\nanimations: " + str(self.animations) + ";\n"


class PacMan(Creature):
    def __init__(self, x, y, initial_location, width, height, velocity, direction="left", form="random",
                 mapobject_hitbox=None, creature_hitbox=None, animations=None,
                 cooldown=5, mana=Constants.pacman_mana,
                 score=Constants.pacman_score, lives=Constants.pacman_lives, ghosts_eaten=0):

        # FIXME Messy workaround. Width and height and form could have wrong values

        if mapobject_hitbox is None:
            mapobject_hitbox = ResourceManager.get_hitbox_of(Constants.PACMAN_MAPOBJECT_HITBOX_PATH, (width, height))

        if creature_hitbox is None:
            creature_hitbox = ResourceManager.get_hitbox_of(Constants.PACMAN_CREATURE_HITBOX_PATH, (width, height))

        form = Constants.forms[random.randint(0, 2)] if form == "random" else form

        if animations is None:
            animations = ResourceManager.get_animations_for(self, form)

        super().__init__(x, y, initial_location, width, height, velocity, direction,
                         form, mapobject_hitbox, creature_hitbox, animations)

        self.form = self.form
        self.cooldown = cooldown
        self.mana = mana
        self.score = score
        self.lives = lives
        self.ghosts_eaten = ghosts_eaten

    @property
    def cooldown(self):
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._cooldown = value
            return
        if value < 0:
            raise ValueError("Cooldown cannot be assigned to negative value:", value)
        if not isinstance(value, int):
            raise TypeError("Cooldown cannot be assigned to non-int object:", type(value), value)

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._mana = value
            return
        if value < 0:
            raise ValueError("Mana cannot be assigned to negative value:", value)
        if not isinstance(value, int):
            raise TypeError("Mana cannot be assigned to non-int object:", type(value), value)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._score = value
            return
        if value < 0:
            raise ValueError("Score cannot be assigned to negative value:", value)
        if not isinstance(value, int):
            raise TypeError("Score cannot be assigned to non-int object:", type(value), value)

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value: int):
        if value >= 0:
            self._lives = value
            return
        if value < 0:
            raise ValueError("Lives cannot be assigned to negative value:", value)
        if not isinstance(value, int):
            raise TypeError("Lives cannot be assigned to non-int object:", type(value), value)

    @property
    def ghosts_eaten(self):
        return self._ghosts_eaten

    @ghosts_eaten.setter
    def ghosts_eaten(self, value: int):
        if value >= 0:
            self._ghosts_eaten = value
            return
        if value < 0:
            raise ValueError("Lives cannot be assigned to negative value:", value)
        if not isinstance(value, int):
            raise TypeError("Lives cannot be assigned to non-int object:", value)

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, value: str):
        if value in Constants.forms and isinstance(value, str):
            self._form = value
            self.animations = ResourceManager.get_animations_for(self, value)
            return

    def copy(self):
        """Returns a shallow copy of PacMan object. Use with caution!!!!!"""
        return PacMan(self.x, self.y, self.initial_location, self.width, self.height,
                      self.velocity, self.direction, self.form, ResourceManager.copy_sprite(self.mapobject_hitbox),
                      ResourceManager.copy_sprite(self.creature_hitbox), self.animations, self.cooldown,
                      self.mana, self.score, self.lives, self.ghosts_eaten)

    def __str__(self):
        return super().__str__() + \
               "cooldown: " + str(self.cooldown) + "; mana: " + str(self.mana) + \
               "; score: " + str(self.score) + "; lives: " + str(self.lives) + \
               "; ghosts_eaten:" + str(self._ghosts_eaten)


class Ghost(Creature):

    def __init__(self, x, y, initial_location, width, height, velocity, direction="up", form="random",
                 mapobject_hitbox=None, creature_hitbox=None, animations=None,
                 is_chasing=Constants.ghost_is_chasing):

        # FIXME Messy workaround. Width and height could have wrong values

        if mapobject_hitbox is None:
            mapobject_hitbox = ResourceManager.get_hitbox_of(Constants.GHOST_MAPOBJECT_HITBOX_PATH, (width, height))

        form = Constants.forms[random.randint(0, 2)] if form == "random" else form

        if creature_hitbox is None:
            creature_hitbox = ResourceManager.get_hitbox_of(Constants.GHOST_CREATURE_HITBOX_PATH, (width, height))

        if animations is None:
            animations = ResourceManager.get_animations_for(self, form)


        super().__init__(x, y, initial_location, width, height, velocity, direction,
                         form, mapobject_hitbox, creature_hitbox, animations)
        self.is_chasing = is_chasing
        self.form = self.form
        self.target_coord = target_coord
    @property
    def is_chasing(self):
        return self._is_chasing

    @is_chasing.setter
    def is_chasing(self, value: bool):
        if isinstance(value, bool):
            self._is_chasing = value
        else:
            raise TypeError("Is_chasing cannot be assigned to non-boolean objects:", type(value), value)

    @property
    def is_alive(self):
        return self._is_alive

    @is_alive.setter
    def is_alive(self, value):
        if value is True:
            self._is_alive = True
        elif value is False:
            self._is_alive = False
            self._is_chasing = False
        else:
            raise ValueError("is_alive cannot be assigned to non-bool object:", type(value), value)

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, value: str):
        if value in Constants.forms and isinstance(value, str):
            self._form = value
            self.animations = ResourceManager.get_animations_for(self, value)
            return

    def copy(self):
        """Returns a shallow copy of Ghost object. Use with caution!!!!!"""
        return Ghost(self.x, self.y, self.initial_location, self.width, self.height,
                     self.velocity, self.direction, self.form, ResourceManager.copy_sprite(self.mapobject_hitbox),
                     ResourceManager.copy_sprite(self.creature_hitbox), self.animations, self.is_chasing)

    def __str__(self):
        return super().__str__() + "is_chasing: " + str(self.is_chasing)
