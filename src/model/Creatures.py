import os
import pygame
import random
from src.data import Constants


class Creature(object):

    def __init__(self, x, y, initial_location, width, height, velocity, direction, form,
                 mapobject_hitbox_path, creature_hitbox_path, animations):
        self.initial_location = initial_location
        self.width = width
        self.height = height
        self.velocity = velocity
        self.direction = direction
        self.preferred_direction = self.direction
        self.form = form
        self.mapobject_hitbox = self.create_hitbox_of(mapobject_hitbox_path)
        self.creature_hitbox = self.create_hitbox_of(creature_hitbox_path)
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
        #TODO
        # if value < 0:
        #     raise ValueError("X cannot be assigned to negative value:", value)
        # if not isinstance(value, int) and not isinstance(value, float):
        #     raise TypeError("X cannot be assigned to non-numeric object:", type(value), value)

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
        #TODO
        # if value < 0:
        #     raise ValueError("Y cannot be assigned to negative value: ", value)
        # if not isinstance(value, int) and not isinstance(value, float):
        #     raise TypeError("Y cannot be assigned to non-numeric object:", type(value), value)

    @property
    def coord(self):
        return self.x, self.y

    @coord.setter
    def coord(self, value: tuple):
        if value[0] >= 0 and value[1] >= 0:
            self._x = value[0]
            self._y = value[1]
            return

        if value[0] < 0 or value[1] < 0:
            raise ValueError("coord cannot be assigned to tuple with negative coordinate(s):", value)

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
        #     raise ValueError("preferred_direction can only take these values: " + Constants.directions.__str__() + "\nInstead, it took:",value)
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

    def create_hitbox_of(self, path, x=0, y=0):
        """Returns sprite with mask created from given image"""

        if os.path.exists(path):
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (self.width, self.height))

            # Create sprite that has creature's size
            sprite = pygame.sprite.Sprite()
            sprite.surface = pygame.Surface((self.width, self.height))

            # Make image transparent
            sprite.image = img.convert_alpha()

            # Get mask out of the image
            sprite.mask = pygame.mask.from_surface(sprite.image)
            sprite.rect = sprite.image.get_rect()

            # Move sprite to the creature's position
            sprite.rect.move_ip(x, y)

            return sprite
        else:
            raise ValueError("Wrong path. Path does not exist.")

    @property
    def animations(self):
        return self._animations

    @animations.setter
    def animations(self, animations_paths: dict):

        if animations_paths and isinstance(animations_paths, dict):
            animations = dict()

            for animation_type, animation_paths_list in animations_paths.items():

                # Create list of images which are located at given path (at animations_paths)
                animation_images_list = []
                for path in animation_paths_list:
                    img = pygame.image.load(path)
                    img = pygame.transform.scale(img, (self.width, self.height))
                    img = img.convert_alpha()
                    animation_images_list.append(img)

                # Insert this list at corresponding key (animation type)
                animations[animation_type] = animation_images_list

            self._animations = animations
            return

        if not animations_paths:
            raise ValueError("Animations cannot be assigned to None:", animations_paths)
        if not isinstance(animations_paths, dict):
            raise TypeError("Animations cannot be assigned to non-dict object:", type(animations_paths), animations_paths)

    def __str__(self):
        return "x: " + str(self.x) + "; y: " + str(self.y) + "; initial_location: " + str(self.initial_location) + \
               "; width: " + str(self.width) + "; height: " + str(self.height) + \
               "; velocity: " + str(self.velocity) + "; direction: " + str(self.direction) + \
               "; form: " + str(self.form) + "; mapobject_hitbox: " + str(self.mapobject_hitbox.image) + \
               "; creature_hitbox: " + str(self.creature_hitbox.image) + \
               ";\nanimations: " + str(self.animations) + ";\n"


class PacMan(Creature):
    def __init__(self, x, y, initial_location, width, height, velocity, direction="left", form="random",
                 mapobject_hitbox=Constants.PACMAN_MAPOBJECT_HITBOX_PATH,
                 creature_hitbox=Constants.PACMAN_CREATURE_HITBOX_PATH,
                 animations=Constants.PACMAN_RED_ANIMATIONS_PATHS,
                 cooldown=5, mana=Constants.pacman_mana,
                 score=Constants.pacman_score, lives=Constants.pacman_lives, ghosts_eaten=0):
        super().__init__(x, y, initial_location, width, height, velocity, direction,
                         Constants.forms[random.randint(0, 2)] if form == "random" else form,
                         mapobject_hitbox, creature_hitbox, animations)
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
            if value == "red":
                self.animations = Constants.PACMAN_RED_ANIMATIONS_PATHS
            elif value == "green":
                self.animations = Constants.PACMAN_GREEN_ANIMATIONS_PATHS
            elif value == "blue":
                self.animations = Constants.PACMAN_BLUE_ANIMATIONS_PATHS
            return

    def __str__(self):
        return super().__str__() + \
               "cooldown: " + str(self.cooldown) + "; mana: " + str(self.mana) + \
               "; score: " + str(self.score) + "; lives: " + str(self.lives) + \
               "; ghosts_eaten:" + str(self._ghosts_eaten)


class Ghost(Creature):

    def __init__(self, x, y, initial_location, width, height, velocity, direction="up", form="random",
                 mapobject_hitbox=Constants.GHOST_MAPOBJECT_HITBOX_PATH,
                 creature_hitbox=Constants.GHOST_CREATURE_HITBOX_PATH,
                 animations=Constants.GHOST_RED_ANIMATIONS_PATHS,
                 is_chasing=Constants.ghost_is_chasing):
        super().__init__(x, y, initial_location, width, height, velocity, direction,
                         Constants.forms[random.randint(0, 2)] if form == "random" else form,
                         mapobject_hitbox, creature_hitbox, animations)
        self.is_chasing = is_chasing
        self.form = self.form

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
            if value == "red":
                self.animations = Constants.GHOST_RED_ANIMATIONS_PATHS
            elif value == "green":
                self.animations = Constants.GHOST_GREEN_ANIMATIONS_PATHS
            elif value == "blue":
                self.animations = Constants.GHOST_BLUE_ANIMATIONS_PATHS
            return

    def __str__(self):
        return super().__str__() + "is_chasing: " + str(self.is_chasing)
