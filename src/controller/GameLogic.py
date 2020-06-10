import sys

import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_1, K_2, QUIT
from src.controller.Abilities import SpeedAbility, TransformAbility
from src.data.Constants import SECTOR_SIZE, DESIRED_AI_TICK_TIME, DESIRED_PHYSICS_TICK_TIME, DESIRED_RENDER_TICK_TIME, \
    PACMAN_PX_PER_SECOND, GHOST_PX_PER_SECOND, GLOBAL_TICK_RATE, PACMAN_BOOST_PX_PER_SECOND
from src.debug.TickTimeDebugger import TickTimeDebugger
from src.model.Creatures import PacMan, Ghost
from src.controller.GhostsAI import PathFinder
from threading import Timer
from itertools import cycle
import time
from src.view.Renderer import Renderer


def get_sector_coord(x, y):
    return int(x // SECTOR_SIZE), int(y // SECTOR_SIZE)


def revive_ghost(ghost):
    if (ghost.x, ghost.y) == ghost.initial_location:
        ghost.is_alive = True


def ghost_died(ghost):  # TODO: Animations
    ghost.is_alive = False


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


def lean_pacman_to_wall(creature, wall):
    """ Leans creature to the wall if they have collision """

    if wall.coord[1] > creature.y:  # wall is below
        creature.y = wall.coord[1] - creature.height
    elif wall.coord[1] < creature.y:  # wall on top
        creature.y = wall.coord[1] + wall.height
    elif wall.coord[0] < creature.x:  # wall on left
        creature.x = wall.coord[0] + creature.width
    elif wall.coord[0] > creature.x:  # wall on right
        creature.x = wall.coord[0] - wall.width


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
            self.ability_timer = \
            self.ability_is_ready = \
            self.renderer = None
        self.ghost_update_exec_time = \
            self.physics_update_exec_time = \
            self.render_update_exec_time = \
            self.counter_physics_tick_time = 0
        self.counter_ai_tick_time = 0
        self.desired_render_tick_time = 0
        self.initial_setup()

    def initial_setup(self):
        self.game_over = False
        self.init_renderer()
        self.init_debugger()
        self.init_level()
        self.renderer.set_map_dimensions(self.current_level.level_map.dims)
        self.parse_level()
        self.init_pacman()
        self.init_ghosts()
        self.init_abilities()

    def init_renderer(self):
        pygame.init()
        self.renderer = Renderer((0, 0), is_fullscreen=False)

    def init_debugger(self):
        self.ticktime_debugger = TickTimeDebugger()

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
                                          self.pacman.velocity, self.current_level.pacman_boost)

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
                    if self.tick_time > DESIRED_PHYSICS_TICK_TIME:
                        boost_tick_time = self.tick_time
                    else:
                        boost_tick_time = DESIRED_PHYSICS_TICK_TIME

                    pacman_vel = boost_tick_time * PACMAN_PX_PER_SECOND
                    pacman_boost = boost_tick_time * PACMAN_BOOST_PX_PER_SECOND
                    self.speed_ability.run(pacman_vel, pacman_boost)
                    self.set_cooldown_timer()

                elif event.key == K_2:
                    if self.pacman.mana > 0 and self.ability_is_ready:
                        self.transform_ability.run()  # call set_cooldown_timer()
                        self.set_cooldown_timer()
                    elif self.transform_ability.is_active:
                        self.transform_ability.changeForm()

    def set_cooldown_timer(self):
        self.ability_is_ready = False
        self.ability_timer = Timer(self.current_level.pacman_cooldown, self.set_ability_ready)  # run timer for cooldown
        self.ability_timer.start()

    def set_ability_ready(self):
        self.ability_is_ready = True

    def deactivate_active_ability(self):
        if self.ability_timer is not None and self.ability_timer.is_alive:
            self.ability_is_ready = True

            if self.transform_ability.is_active:
                self.transform_ability.deactivate()

            else:
                self.speed_ability.deactivate()

            self.ability_timer.cancel()

    def collides_wall(self, creature):
        for wall in self.walls:
            if pygame.sprite.collide_mask(creature.mapobject_hitbox, wall.hitbox):
                return True
        else:
            return False

    def get_collided_wall(self, creature):
        for wall in self.walls:
            if pygame.sprite.collide_mask(creature.mapobject_hitbox, wall.hitbox):
                return wall

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
        self.teleport_activate(creature)
        if self.collides_wall(creature):
            lean_pacman_to_wall(creature, self.get_collided_wall(creature))

    def teleport_activate(self, creature):
        """ If coordinate of the pacman in teleport area then changes
            coordinate of pacman to the opposite map side"""
        map_width = self.current_level.level_map.width * SECTOR_SIZE
        map_height = self.current_level.level_map.height * SECTOR_SIZE

        if creature.x <= -SECTOR_SIZE:  # left teleport
            creature.x = map_width
        elif creature.x >= map_width:  # right teleport
            creature.x = 0
        elif creature.y <= -SECTOR_SIZE:  # top teleport
            creature.y = map_height
        elif creature.y >= map_height:  # bottom teleport
            creature.y = 0
        else:
            return False

    def update_pacman(self, counter_physics_tick_time):
        if not self.speed_ability.is_active:
            self.pacman.velocity = int(PACMAN_PX_PER_SECOND * counter_physics_tick_time)
        print("pacman: " + str(self.pacman.velocity))
        self.move_creature(self.pacman)
        self.check_pacman_ghost_collision()
        self.check_pellet_collision()
        self.check_mega_pellet_collision()

    def update_level(self):
        """ Jumps to the next level if all pellets are picked """
        if not self.pellets and not self.mega_pellets:
            self.init_level()
            self.map_restart()

    def map_restart(self):
        """ Restart current map """
        self.parse_level()
        self.init_pacman()
        self.init_ghosts()

    def resolve_ghost_direction(self, ghost, pacman_coord, used_sectors=[], used_val=0):
        ghost_coord = get_sector_coord(ghost.x + ghost.width / 2, ghost.y + ghost.height / 2)

        if not ghost.is_alive:
            revive_ghost(ghost)

        if pacman_coord != ghost_coord:
            path = self.path_finder.get_path(ghost_coord, pacman_coord, used_sectors, used_val)
            ghost.preferred_direction = self.path_finder.get_direction(ghost_coord, path)
        else:
            path = self.path_finder.get_path(ghost_coord, ghost.initial_location)
            ghost.preferred_direction = self.path_finder.get_direction(ghost_coord, path)

        return path

    def update_ghosts(self, tick_time, hardcore=True):
        self.counter_ai_tick_time += tick_time
        if self.counter_ai_tick_time > DESIRED_AI_TICK_TIME:
            start_time = time.time()
            pacman_coord = get_sector_coord(self.pacman.x + self.pacman.width / 2,
                                            self.pacman.y + self.pacman.height / 2)
            if hardcore:
                used_sectors = []
                for ghost in self.ghosts:
                    used_sectors.extend(
                        self.resolve_ghost_direction(ghost, pacman_coord, used_sectors, 4))  # Hardcore mode
            else:
                for ghost in self.ghosts:
                    self.resolve_ghost_direction(ghost, pacman_coord)
            end_time = time.time()
            self.ghost_update_exec_time = end_time - start_time
            # self.time_convert(self.ghost_update_exec_time)
            self.counter_ai_tick_time = 0

    def move_ghosts(self, counter_physics_tick_time):
        for ghost in self.ghosts:
            ghost.velocity = int(GHOST_PX_PER_SECOND * counter_physics_tick_time)
            print("GHOST: " + str(ghost.velocity))
            self.move_creature(ghost)

    def check_pacman_ghost_collision(self):
        for ghost in self.ghosts:
            if pygame.sprite.collide_mask(self.pacman.creature_hitbox, ghost.creature_hitbox):
                if self.pacman.form == ghost.form:
                    ghost_died(ghost)
                else:
                    self.pacman_die()

    def check_pellet_collision(self):
        for pellet in self.pellets:
            if pygame.sprite.collide_mask(self.pacman.mapobject_hitbox, pellet.hitbox):
                self.pacman.score += pellet.value
                self.pellets.remove(pellet)

    def check_mega_pellet_collision(self):
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
            self.map_restart()

        self.deactivate_active_ability()

    def physics_update(self, tick_time):
        if tick_time >= DESIRED_PHYSICS_TICK_TIME:
            self.counter_physics_tick_time = tick_time
        else:
            self.counter_physics_tick_time += tick_time

        if self.counter_physics_tick_time >= DESIRED_PHYSICS_TICK_TIME:
            start_time = time.time()
            self.update_pacman(DESIRED_PHYSICS_TICK_TIME)
            self.move_ghosts(DESIRED_PHYSICS_TICK_TIME)
            self.counter_physics_tick_time = 0
            end_time = time.time()
            self.physics_update_exec_time = end_time - start_time
            self.time_convert(self.physics_update_exec_time)

    def time_convert(self, sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        # print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))

    def render_update(self, tick_time):
        self.desired_render_tick_time += tick_time
        if self.desired_render_tick_time > DESIRED_RENDER_TICK_TIME:
            start_time = time.time()
            self.renderer.render([self.pellets, self.mega_pellets, self.walls, [], [self.pacman], self.ghosts],
                                 tick_time, showgrid=False, show_hitboxes=False)
            end_time = time.time()
            self.render_update_exec_time = end_time - start_time

    def run(self):
        clock = pygame.time.Clock()
        #self.ticktime_debugger.run()
        while True:
            miliseconds = clock.tick(GLOBAL_TICK_RATE)
            self.tick_time = miliseconds / 1000.0  # seconds

            if self.tick_time > 0.3:
                self.tick_time = 1 / GLOBAL_TICK_RATE

            self.handle_events()
            self.physics_update(self.tick_time)
            self.update_ghosts(self.tick_time, hardcore=False)
            self.update_level()

            self.render_update(self.tick_time)

            self.ticktime_debugger.update(self.physics_update_exec_time, self.ghost_update_exec_time,
                                          self.render_update_exec_time, self.tick_time)