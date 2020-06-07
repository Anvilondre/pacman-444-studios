import sys

import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_1, K_2, QUIT
from src.controller.Abilities import SpeedAbility, TransformAbility
from src.data.Constants import SECTOR_SIZE
from src.model.Creatures import PacMan, Ghost
from src.controller.GhostsAI import PathFinder
from threading import Timer
from itertools import cycle

from src.view.Renderer import Renderer


def get_sector_coord(x, y):
    return int(x / 36), int(y / 36)


def revive_ghost(ghost):
    if (ghost.x, ghost.y) == ghost.initial_location:
        ghost.is_alive = True


def ghost_died(ghost):  # TODO: Animations
    ghost._is_alive = False


def move_creature_direction(creature, direction, vel=None):
    if vel is None:
        vel = creature.velocity

    if direction == 'up':
        creature.y -= vel

    elif direction == 'down':
        creature.y += vel

    elif direction == 'left':
        creature.x -= vel

    elif direction == 'right':
        creature.x += vel

    else:
        raise Exception('Illegal direction')


class Controller:
    def __init__(self, levels):
        self.levels = cycle(levels)
        self.game_over = \
            self.window = \
            self.current_level = \
            self.walls = \
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
        self.game_over = False
        self.init_render()
        self.init_level()
        self.renderer.set_map_dimensions(self.current_level.level_map.dims)
        self.parse_level()
        self.init_pacman()
        self.init_ghosts()
        self.init_abilities()

    def init_render(self):
        pygame.init()
        self.renderer = Renderer((0, 0), is_fullscreen=False)
        # self.window = pygame.display.set_mode((800, 600))

    def init_level(self):
        self.current_level = next(self.levels)

    def parse_level(self):
        self.current_level.level_map.pre_process()
        self.walls = self.current_level.level_map.walls
        self.pellets = self.current_level.level_map.pellets
        self.mega_pellets = self.current_level.level_map.mega_pellets

    def init_pacman(self):
        self.pacman = PacMan(*self.current_level.level_map.pacman_initial_coord,
                             self.current_level.level_map.pacman_initial_coord,
                             SECTOR_SIZE, SECTOR_SIZE, self.current_level.pacman_velocity)
        self.ability_is_ready = True

    def init_ghosts(self):
        self.path_finder = PathFinder(self.current_level.level_map.hash_map)
        self.ghosts = []
        for ghost_coord in self.current_level.level_map.ghosts_initial_coords:
            self.ghosts.append(
                Ghost(*ghost_coord, ghost_coord, SECTOR_SIZE, SECTOR_SIZE, self.current_level.ghosts_velocity))

    def init_abilities(self):
        self.speed_ability = SpeedAbility(self.pacman, self.current_level.speed_ability_duration,
                                          self.current_level.pacman_velocity, self.current_level.pacman_boost)

        self.transform_ability = TransformAbility(self.pacman, self.current_level.speed_ability_duration, self.ghosts,
                                                  self.current_level.ghosts_velocity,
                                                  self.current_level.ghosts_slowdown)

    def handle_events(self):
        """Get key input from player"""

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    self.pacman.preferred_direction = 'left'
                elif event.key == K_UP:
                    self.pacman.preferred_direction = 'up'
                elif event.key == K_RIGHT:
                    self.pacman.preferred_direction = 'right'
                elif event.key == K_DOWN:
                    self.pacman.preferred_direction = 'down'

                elif event.key == K_1 and self.pacman.mana > 0 and self.ability_is_ready:
                    self.speed_ability.run()
                    self.set_cooldown_timer()

                elif event.key == K_2:
                    if self.pacman.mana > 0 and self.ability_is_ready:
                        self.transform_ability.run()  # call set_cooldown_timer()
                        self.set_cooldown_timer()
                    elif self.transform_ability.is_active:
                        self.transform_ability.changeForm()

    def set_cooldown_timer(self):
        self.ability_is_ready = False
        timer = Timer(self.current_level.pacman_cooldown, self.set_ability_ready)  # run timer for cooldown
        timer.start()

    def set_ability_ready(self):
        self.ability_is_ready = True

    def collides_wall(self, creature):
        for wall in self.walls:
            if pygame.sprite.collide_mask(creature.mapobject_hitbox, wall.hitbox):
                return True
        else:
            return False

    def move_creature(self, creature):
        """ Move pac-man and check collision with wall-list """
        creature_coords = (creature.x, creature.y)
        direction = creature.preferred_direction

        if direction != creature.direction:
            move_creature_direction(creature, direction, creature.width / 2)
            if not self.collides_wall(creature):
                (creature.x, creature.y) = creature_coords
                move_creature_direction(creature, direction)
                creature.direction = direction
                return
            else:
                (creature.x, creature.y) = creature_coords

        move_creature_direction(creature, creature.direction)
        if self.collides_wall(creature):
            (creature.x, creature.y) = creature_coords

    def update_pacman(self):
        self.move_creature(self.pacman)
        self.check_pacman_ghost_collision()
        self.check_pellet_collision()
        self.check_mega_pellet_collision()

    def resolve_ghost_direction(self, ghost, pacman_coord, used_sectors=[], used_val=0):
        ghost_coord = get_sector_coord(ghost.x + ghost.width / 2, ghost.y + ghost.height / 2)

        if not ghost.is_alive:
            revive_ghost(ghost)

        if ghost.is_chasing and ghost.is_alive:
            path = self.path_finder.get_path(ghost_coord, pacman_coord, used_sectors, used_val)
            ghost.preferred_direction = self.path_finder.get_direction(ghost_coord, path)
        else:
            path = self.path_finder.get_path(ghost_coord, ghost.initial_location)
            ghost.preferred_direction = self.path_finder.get_direction(ghost_coord, path)

        return path

    def update_ghosts(self, hardcore=True):
        pacman_coord = get_sector_coord(self.pacman.x + self.pacman.width / 2, self.pacman.y + self.pacman.height / 2)
        if hardcore:
            used_sectors = []
            for ghost in self.ghosts:
                used_sectors.extend(self.resolve_ghost_direction(ghost, pacman_coord, used_sectors))  # Hardcore mode
                self.move_creature(ghost)
        else:
            for ghost in self.ghosts:
                self.resolve_ghost_direction(ghost, pacman_coord)
                self.move_creature(ghost)

    def check_pacman_ghost_collision(self):  # TODO: Change hitbox
        for ghost in self.ghosts:
            if pygame.sprite.collide_mask(self.pacman.creature_hitbox, ghost.creature_hitbox):
                if self.pacman.form == ghost.form:
                    ghost_died(ghost)
                else:
                    self.pacman_die()

    def check_pellet_collision(self):  # TODO: Change hitbox
        for pellet in self.pellets:
            if pygame.sprite.collide_mask(self.pacman.mapobject_hitbox, pellet.hitbox):
                self.pacman.score += pellet.value
                self.pellets.remove(pellet)

    def check_mega_pellet_collision(self):  # TODO: Change hitbox
        for mega_pellet in self.mega_pellets:
            if pygame.sprite.collide_mask(self.pacman.mapobject_hitbox, mega_pellet.hitbox):
                self.pacman.score += mega_pellet.value
                self.pacman.mana += 1
                self.mega_pellets.remove(mega_pellet)

    def pacman_die(self):  # TODO: Animations
        if self.pacman.lives > 0:
            self.pacman.lives -= 1
            (self.pacman.x, self.pacman.y) = self.current_level.level_map.pacman_initial_coord
        else:
            self.game_over = True

    def run(self):
        clock = pygame.time.Clock()
        while True:
            miliseconds = clock.tick(3)
            elapsed_time = miliseconds / 1000.0  # seconds

            self.handle_events()
            self.update_pacman()
            self.update_ghosts(hardcore=True)

            # TODO: Implement renderer
            self.renderer.render([self.pellets, self.mega_pellets, self.walls, [], [self.pacman], self.ghosts],
                                 elapsed_time, showgrid=False, show_hitboxes=True)
