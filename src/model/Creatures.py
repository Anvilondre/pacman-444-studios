import os

import pygame
from src.data import Constants


class Creature(object):

    def __init__(self, x, y, width, height, velocity, direction, form, hitbox, animations):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.direction = direction
        self.form = form
        self.hitbox = hitbox
        self.animations = animations

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._x = value
            # Update hitbox x coordinate
            self.hitbox.rect.move_ip(value, self.y)
            return
        if isinstance(value, float):
            self._x = round(value)
            return

        if value < 0:
            raise ValueError("X cannot be assigned to negative value")
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("X cannot be assigned to non-numeric object.")

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._y = value
            # Update hitbox y coordinate
            self.hitbox.rect.move_ip(self.x, value)
            return
        if isinstance(value, float):
            self._y = round(value)
            return

        if value < 0:
            raise ValueError("Y cannot be assigned to negative value")
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("Y cannot be assigned to non-numeric object.")

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
            raise ValueError("Width cannot be assigned to negative value")
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("Width cannot be assigned to non-numeric object.")

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
            raise ValueError("Height cannot be assigned to negative value")
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("Height cannot be assigned to non-numeric object.")

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._velocity = value
        if value < 0:
            raise ValueError("Velocity cannot be assigned to negative value")
        if not isinstance(value, int):
            raise TypeError("Velocity cannot be assigned to non-int object")

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value: str):
        if value in Constants.directions and isinstance(value, str):
            self._direction = value
            return
        if value not in Constants.directions:
            raise ValueError("Direction can only take these values: " + Constants.directions.__str__())
        if not isinstance(value, str):
            raise TypeError("Direction cannot be assigned to non-str object")

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, value: str):
        if value in Constants.forms and isinstance(value, str):
            self._form = value
            return
        if value not in Constants.forms:
            raise ValueError("Form can only take these values: " + Constants.forms.__str__())
        if not isinstance(value, str):
            raise TypeError("Form cannot be assigned to non-str object")

    @property
    def hitbox(self):
        return self._hitbox

    @hitbox.setter
    def hitbox(self, path: str):
        """Assigns hitbox to the sprite with mask created from given image"""
        if os.path.exists(path):
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (self.width, self.height))

            # Create sprite that has creature's size
            sprite = pygame.sprite.Sprite()
            sprite.surface = pygame.Surface((self.width, self.height))

            # Make image opaque
            sprite.image = img.convert_alpha()

            # Get mask out of the image
            sprite.mask = pygame.mask.from_surface(sprite.image)
            sprite.rect = sprite.image.get_rect()

            # Move sprite to the creature's position
            sprite.rect.move_ip(self.x, self.y)

            self._hitbox = sprite
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

                # Create list of images corresponding to current dict-item's paths
                animation_images_list = []
                for path in animation_paths_list:
                    img = pygame.image.load(path).convert()
                    img = pygame.transform.scale(img, (self.width, self.height))
                    animation_images_list.append(img)

                # Insert this list at corresponding key (animation type)
                animations[animation_type] = animation_images_list

            self._animations = animations
            return

        if not animations_paths:
            raise ValueError("Animations cannot be assigned to None")
        if not isinstance(animations_paths, dict):
            raise TypeError("Animations cannot be assigned to non-dict object")

    def __str__(self):
        return "x: " + str(self.x) + "; y: " + str(self.y) + \
               "; width: " + str(self.width) + "; height: " + str(self.height) + \
               "; velocity: " + str(self.velocity) + "; direction: " + str(self.direction) + \
               "; form: " + str(self.form) + "; hitbox: " + str(self.hitbox.image) + \
               ";\nanimations: " + str(self.animations)


class PacMan(Creature):
    def __init__(self, x, y, width, height, velocity, direction, form,
                 hitbox=Constants.pacman_hitbox_path, animations=Constants.pacman_animations_paths,
                 cooldown=Constants.pacman_cooldown, mana=Constants.pacman_mana,
                 score=Constants.pacman_score, lives=Constants.pacman_lives):
        super().__init__(x, y, width, height, velocity, direction, form, hitbox, animations)
        self.cooldown = cooldown
        self.mana = mana
        self.score = score
        self.lives = lives

    @property
    def cooldown(self):
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._cooldown = value
            return
        if value < 0:
            raise ValueError("Cooldown cannot be assigned to negative value")
        if not isinstance(value, int):
            raise TypeError("Cooldown cannot be assigned to non-int object")

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._mana = value
            return
        if value < 0:
            raise ValueError("Mana cannot be assigned to negative value")
        if not isinstance(value, int):
            raise TypeError("Mana cannot be assigned to non-int object")

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value: int):
        if value >= 0 and isinstance(value, int):
            self._score = value
            return
        if value < 0:
            raise ValueError("Score cannot be assigned to negative value")
        if not isinstance(value, int):
            raise TypeError("Score cannot be assigned to non-int object")

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value: int):
        if value >= 0:
            self._lives = value
            return
        if value < 0:
            raise ValueError("Lives cannot be assigned to negative value")
        if not isinstance(value, int):
            raise TypeError("Lives cannot be assigned to non-int object")

    def __str__(self):
        return super().__str__() + \
               "; cooldown: " + str(self.cooldown) + "; mana: " + str(self.mana) + \
               "; score: " + str(self.score) + "; lives: " + str(self.lives)


class Ghost(Creature):

    def __init__(self, x, y, width, height, velocity, direction, form,
                 hitbox=Constants.ghost_hitbox_path, animations=Constants.pinky_animations_paths,
                 is_chasing=Constants.ghost_is_chasing):
        super().__init__(x, y, width, height, velocity, direction, form, hitbox, animations)
        self.is_chasing = is_chasing

    @property
    def is_chasing(self):
        return self._is_chasing

    @is_chasing.setter
    def is_chasing(self, value: bool):
        if isinstance(value, bool):
            self._is_chasing = value
        else:
            raise TypeError("Is_chasing cannot be assigned to non-boolean objects")

    def __str__(self):
        return super().__str__() + "; is_chasing: " + str(self.is_chasing)
