import sys

import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_1, K_2, QUIT
from src.controller.Abilities import SpeedAbility, TransformAbility
from src.data.Constants import SECTOR_SIZE
from src.model.Creatures import PacMan, Ghost
from src.controller.GhostsAI import PathFinder
from threading import Timer
from itertools import cycle


def move_ghost(ghost):
    """ Move ghost """
    if ghost.direction == 'left':
        ghost.x -= ghost.velocity
    elif ghost.direction == 'up':
        ghost.y -= ghost.velocity
    elif ghost.direction == 'right':
        ghost.x += ghost.velocity
    elif ghost.direction == 'down':
        ghost.y += ghost.velocity


def get_sector_coord(x, y):
    return x // SECTOR_SIZE, y // SECTOR_SIZE


class Controller:
    def __init__(self, levels):
        self.levels = cycle(levels)
        self.game_over = \
        self.window = \
        self.current_level = \
        self.pellets = \
        self.mega_pellets = \
        self.pacman = \
        self.path_finder = \
        self.ghosts = \
        self.speed_ability = \
        self.transform_ability = \
        self.ability_is_ready = None
        self.initial_setup()

    def initial_setup(self):
        self.init_render()
        self.init_level()
        self.init_pacman()
        self.init_ghosts()

    def init_render(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))

    def init_level(self):
        self.current_level = next(self.levels)
        self.pellets = self.current_level.level_map.pellets
        self.mega_pellets = self.current_level.level_map.mega_pellets

    def init_pacman(self):
        self.pacman = PacMan(*self.current_level.level_map.pacman_initial_coord,
                             SECTOR_SIZE, SECTOR_SIZE, self.current_level.pacman_velocity, 'up', 'blue')

    def init_ghosts(self):
        self.path_finder = PathFinder(self.current_level.level_map.hash_map)
        self.ghosts = []
        for ghost_coord in self.current_level.level_map.ghosts_initial_coords:
            self.ghosts.append(
                Ghost(*ghost_coord, SECTOR_SIZE, SECTOR_SIZE, self.current_level.ghosts_velocity, 'up', 'red'))

    def init_abilities(self):
        self.speed_ability = SpeedAbility(self.pacman, self.current_level.speed_ability_duration,
                                          self.pacman.velocity, self.current_level.pacman_boost)

        self.transform_ability = TransformAbility(self.pacman, self.current_level.speed_ability_duration, self.ghosts,
                                                  self.current_level.ghosts_velocity,
                                                  self.current_level.ghosts_slowdown)

    def key_input(self):
        """Get key input from player"""

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT and self.pacman.direction != 'left':
                    self.pacman.direction = 'left'
                elif event.key == K_UP and self.pacman.direction != 'up':
                    self.pacman.direction = 'up'
                elif event.key == K_RIGHT and self.pacman.direction != 'right':
                    self.pacman.direction = 'right'
                elif event.key == K_DOWN and self.pacman.direction != 'down':
                    self.pacman.direction = 'down'

                elif event.key == K_1 and self.pacman.mana > 0 and self.ability_is_ready:
                    self.speed_ability.run()
                    self.set_cooldown_timer()

                elif event.key == K_2 and self.pacman.mana > 0 and self.ability_is_ready:
                    self.transform_ability.run()  # call set_cooldown_timer()
                    self.set_cooldown_timer()

    def set_cooldown_timer(self):
        self.ability_is_ready = False
        return Timer(self.current_level.pacman_cooldown, self.set_ability_ready)  # run timer for cooldown

    def set_ability_ready(self):
        self.ability_is_ready = True

    def move_pacman(self, pacman):
        """ Move pac-man and check collision with wall-list """

        if pacman.direction == 'left':
            pacman.x -= pacman.velocity
            for wall in self.current_level.level_map.walls:
                if pygame.sprite.collide_mask(pacman.hitbox, wall.hitbox):
                    pacman.x += pacman.velocity

        elif pacman.direction == 'up':
            pacman.y -= pacman.velocity
            for wall in self.current_level.level_map.walls:
                if pygame.sprite.collide_mask(pacman.hitbox, wall.hitbox):
                    pacman.y += pacman.velocity

        elif pacman.direction == 'right':
            pacman.x += pacman.velocity
            for wall in self.current_level.level_map.walls:
                if pygame.sprite.collide_mask(pacman.hitbox, wall.hitbox):
                    pacman.x -= pacman.velocity

        elif pacman.direction == 'down':
            pacman.y += pacman.velocity
            for wall in self.current_level.level_map.walls:
                if pygame.sprite.collide_mask(pacman.hitbox, wall.hitbox):
                    pacman.y += pacman.velocity

    def pacman_update(self):
        self.move_pacman(self.pacman)
        self.check_ghost_collision()
        self.check_pellet_collision()
        self.check_mega_pellet_collision()

    def ghost_update(self):
        for ghost in self.ghosts:
            if ghost.is_chasing:
                ghost.direction = self.path_finder.get_direction(get_sector_coord(ghost.x, ghost.y), (1, 1))

    def check_ghost_collision(self):
        for ghost in self.ghosts:
            if pygame.sprite.collide_mask(self.pacman.hitbox, ghost.hitbox):
                if self.pacman.form == ghost.form:
                    self.ghost_die()
                else:
                    self.pacman_die()

    def check_pellet_collision(self):
        for pellet in self.pellets:
            if pygame.sprite.collide_mask(self.pacman.hitbox, pellet.hitbox):
                self.pacman.score += pellet.value
                self.pellets.remove(pellet)

    def check_mega_pellet_collision(self):
        for mega_pellet in self.mega_pellets:
            if pygame.sprite.collide_mask(self.pacman.hitbox, mega_pellet.hitbox):
                self.pacman.score += mega_pellet.value
                self.pacman.mana += 1
                self.mega_pellets.remove(mega_pellet)

    def ghost_die(self):
        pass

    def pacman_die(self):
        if self.pacman.lives > 0:
            self.pacman.lives -= 1
            self.pacman.x = self.current_level.level_map.pacman_initial_coord(0)
            self.pacman.y = self.current_level.level_map.pacman_initial_coord(1)
        else:
            self.game_over = True

    def run(self):
        pygame.init()
        self.game_over = False
        while True:
            self.key_input()
            self.pacman_update()