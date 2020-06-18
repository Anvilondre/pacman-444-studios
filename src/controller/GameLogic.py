import copy
import random
import sys
import time

import pygame
from pygame.constants import K_F1, K_f
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_1, K_2, QUIT

from src.controller.Abilities import SpeedAbility, TransformAbility, IterativeTimer
from src.controller.GhostsAI import PathFinder
from src.data import Constants
from src.data.Constants import SECTOR_SIZE, DESIRED_AI_TICK_TIME, DESIRED_PHYSICS_TICK_TIME, DESIRED_RENDER_TICK_TIME, \
    GLOBAL_TICK_RATE, forms
from src.data.Levels import Level5
from src.debug.TickTimeDebugger import TickTimeDebugger, Modes
from src.model.Creatures import PacMan, Ghost
from src.view.Renderer import Renderer, RenderModes


def calculate_L1(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def get_closed_mp(pellets, ghost_coord):
    closest = pellets[0]
    closest_val = calculate_L1(ghost_coord, pellets[0].coord)
    for pel in pellets[1::]:
        val = calculate_L1(ghost_coord, pel.coord)
        if val < closest_val:
            closest = pel
            closest_val = val
    return closest


def get_sector_coord(x, y):
    return int(x // SECTOR_SIZE), int(y // SECTOR_SIZE)


def revive_ghost(ghost):
    if (ghost.x, ghost.y) == ghost.initial_location:
        ghost.is_alive = True


def ghost_died(ghost):
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
        self.levels = levels
        self.game_over = \
        self.is_playing = \
        self.is_game_complete = \
        self.window = \
        self.current_level = \
        self.current_level_id = 0
        self.walls = \
        self.pellets = \
        self.mega_pellets = \
        self.teleports = \
        self.pacman = \
        self.path_finder = \
        self.ghosts = \
        self.speed_ability = \
        self.transform_ability = \
        self.cooldown_timer = \
        self.ability_is_ready = \
        self.is_game_restart = \
        self.renderer = \
        self.ghost_update_exec_time = \
        self.physics_update_exec_time = \
        self.render_update_exec_time = \
        self.counter_physics_tick_time = \
        self.tick_time = \
        self.map_width = \
        self.map_height = \
        self.copy_pellets = \
        self.copy_mega_pellets = \
        self.counter_ai_tick_time = \
        self.mega_pellets_counter = \
        self.player_score = \
        self.ticktime_debugger = \
        self.floors = \
        self.counter_render_tick_time = 0
        self.initial_setup()

    def initial_setup(self):
        self.game_over = False
        self.init_renderer()
        self.init_debugger()
        self.load_level()

    def load_level(self):
        self.init_level()
        self.renderer.set_map_dimensions(self.current_level.level_map.dims)
        self.parse_level()
        self.init_pacman()
        self.init_ghosts()
        self.init_abilities()

    def init_renderer(self):
        pygame.init()
        self.renderer = Renderer(map_dimensions=(0, 0), is_fullscreen=True)

    def init_debugger(self):
        self.ticktime_debugger = TickTimeDebugger(mode=Modes.Store)

    def init_level(self):
        self.current_level = self.levels[self.current_level_id]

    def parse_level(self):
        self.current_level.level_map.pre_process()
        self.walls = self.current_level.level_map.walls
        self.floors = self.current_level.level_map.floors
        self.pellets = self.current_level.level_map.pellets
        self.mega_pellets = self.current_level.level_map.mega_pellets
        self.map_width = self.current_level.level_map.width * SECTOR_SIZE
        self.map_height = self.current_level.level_map.height * SECTOR_SIZE
        self.copy_pellets = copy.copy(self.pellets)
        self.copy_mega_pellets = copy.copy(self.mega_pellets)
        self.teleports = self.current_level.level_map.teleports

    def init_pacman(self):
        self.pacman = PacMan(*self.current_level.level_map.pacman_initial_coord,
                             self.current_level.level_map.pacman_initial_coord,
                             SECTOR_SIZE, SECTOR_SIZE, int(self.current_level.PACMAN_PX_PER_SECOND * self.tick_time),
                             cooldown=self.current_level.pacman_cooldown, score=self.player_score)
        self.ability_is_ready = True

    def init_ghosts(self):
        self.path_finder = PathFinder(self.current_level.level_map.hash_map)
        self.ghosts = []
        for ghost_coord in self.current_level.level_map.ghosts_initial_coords:
            self.ghosts.append(
                Ghost(*ghost_coord, ghost_coord, SECTOR_SIZE, SECTOR_SIZE, int(self.current_level.GHOST_PX_PER_SECOND *
                                                                               self.tick_time)))

    def init_abilities(self):
        self.speed_ability = SpeedAbility(self.pacman, self.current_level.speed_ability_duration,
                                          self.pacman.velocity, self.current_level.pacman_boost)

        self.transform_ability = TransformAbility(self.pacman, self.current_level.speed_ability_duration)

        self.cooldown_timer = IterativeTimer(self.pacman.cooldown, self.set_ability_ready)  # run timer for cooldown

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
                elif event.key == K_F1:
                    self.ticktime_debugger.save_as_image()

                elif event.key == K_1 and self.pacman.mana > 0 and self.ability_is_ready:
                    self.pacman.mana -= 1
                    if self.tick_time > DESIRED_PHYSICS_TICK_TIME:
                        boost_tick_time = self.tick_time
                    else:
                        boost_tick_time = DESIRED_PHYSICS_TICK_TIME

                    pacman_vel = boost_tick_time * self.current_level.PACMAN_PX_PER_SECOND
                    pacman_boost = boost_tick_time * self.current_level.PACMAN_BOOST_PX_PER_SECOND
                    self.speed_ability.run(int(pacman_vel), int(pacman_boost))
                    self.set_cooldown_timer()

                elif event.key == K_2:
                    if self.pacman.mana > 0 and self.ability_is_ready:
                        self.pacman.mana -= 1
                        self.transform_ability.run()  # call set_cooldown_timer()
                        self.set_cooldown_timer()
                    elif self.transform_ability.is_active:
                        self.transform_ability.changeForm()

    def set_cooldown_timer(self):
        self.ability_is_ready = False
        self.cooldown_timer = IterativeTimer(self.pacman.cooldown, self.set_ability_ready)  # run timer for cooldown
        self.cooldown_timer.start()

    def set_ability_ready(self):
        self.ability_is_ready = True

    def deactivate_active_ability(self):
        if self.cooldown_timer is not None and self.cooldown_timer.is_alive():
            self.ability_is_ready = True

            if self.transform_ability.is_active:
                self.transform_ability.deactivate()
            else:
                self.speed_ability.deactivate()

            self.cooldown_timer.cancel()

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

        if direction != creature.direction and not self.is_off_map(creature_coords):
            move_creature_direction(creature, direction, creature.width / 2)
            if not self.collides_wall(creature):
                (creature.x, creature.y) = creature_coords
                move_creature_direction(creature, direction)
                creature.direction = direction
                return
            else:
                (creature.x, creature.y) = creature_coords
                self.change_direction(creature, creature_coords)

        move_creature_direction(creature, creature.direction)
        self.teleport_activate(creature)
        if self.collides_wall(creature):
            lean_pacman_to_wall(creature, self.get_collided_wall(creature))

    def change_direction(self, creature, creature_coords):
        """ Change creature direction at optimal time"""
        direction = creature.preferred_direction
        px_delay = 5

        if creature.direction == 'right':
            change_direction_coord = creature.x - creature.x % SECTOR_SIZE + SECTOR_SIZE
            if creature.x + px_delay >= change_direction_coord or creature.x - px_delay >= change_direction_coord:
                change_direction_coords = (change_direction_coord, creature.y)
                self.check_change_direction(creature, direction, change_direction_coords, creature_coords)

        elif creature.direction == 'left':
            change_direction_coord = creature.x - creature.x % SECTOR_SIZE
            if creature.x - px_delay <= change_direction_coord or creature.x + px_delay <= change_direction_coord:
                change_direction_coords = (change_direction_coord, creature.y)
                self.check_change_direction(creature, direction, change_direction_coords, creature_coords)

        elif creature.direction == 'up':
            change_direction_coord = creature.y - creature.y % SECTOR_SIZE
            if creature.y - px_delay <= change_direction_coord or creature.y + px_delay <= change_direction_coord:
                change_direction_coords = (creature.x, change_direction_coord)
                self.check_change_direction(creature, direction, change_direction_coords, creature_coords)

        elif creature.direction == 'down':
            change_direction_coord = creature.y - creature.y % SECTOR_SIZE + SECTOR_SIZE
            if creature.y + px_delay >= change_direction_coord or creature.y - px_delay >= change_direction_coord:
                change_direction_coords = (creature.x, change_direction_coord)
                self.check_change_direction(creature, direction, change_direction_coords, creature_coords)

    def is_off_map(self, coords):
        """ Checks if the object is behind the map """
        x = coords[0]
        y = coords[1]

        if x < 0:
            return True
        elif x > self.map_width - SECTOR_SIZE:
            return True
        elif y < 0:
            return True
        elif y > self.map_height - SECTOR_SIZE:
            return True
        else:
            return False

    def check_change_direction(self, creature, direction, change_direction_coords, creature_coords):
        (creature.x, creature.y) = change_direction_coords
        move_creature_direction(creature, direction, creature.width / 2)
        if not self.collides_wall(creature):
            if creature.x != change_direction_coords[0]:
                creature.x = change_direction_coords[0]
            else:
                creature.y = change_direction_coords[1]
            creature.direction = direction
        else:
            (creature.x, creature.y) = creature_coords

    def teleport_activate(self, creature):
        """ If coordinate of the pacman in teleport area then changes
            coordinate of pacman to the opposite map side"""

        if creature.x <= -SECTOR_SIZE:  # left teleport
            creature.x = self.map_width
        elif creature.x >= self.map_width:  # right teleport
            creature.x = 0
        elif creature.y <= -SECTOR_SIZE:  # top teleport
            creature.y = self.map_height
        elif creature.y >= self.map_height:  # bottom teleport
            creature.y = 0
        else:
            return False

    def update_pacman(self, counter_physics_tick_time):
        if not self.speed_ability.is_active:
            self.pacman.velocity = int(self.current_level.PACMAN_PX_PER_SECOND * counter_physics_tick_time)
        self.move_creature(self.pacman)
        self.check_pacman_ghost_collision()
        self.check_pellet_collision()
        self.check_mega_pellet_collision()

    def update_level(self):
        """ Jumps to the next level if all pellets are picked """
        if not self.pellets and not self.mega_pellets:

            # Render one more frame in order to show that PacMan has eaten the last pellet
            self.render_update(1 / Constants.GLOBAL_TICK_RATE)
            self.current_level_id += 1
            if self.current_level.level_name == Level5.level_name:
                self.player_score = self.pacman.score
                self.renderer.render_label("Level complete", " ", bg_full_opacity=True)
                time.sleep(2.5)
                self.renderer.fade_out()
                self.current_level_id = 0
                self.is_game_complete = True
            else:
                self.player_score = self.pacman.score
                self.renderer.render_label("Level complete", " ", bg_full_opacity=True)
                time.sleep(2.5)
                self.renderer.fade_out()
            self.load_level()
            self.renderer.restart()

    def game_restart(self):
        """ Restart current map """
        self.is_game_restart = True
        self.current_level_id = 0
        self.init_level()
        self.load_level()
        self.is_playing = False

    def get_random_coord(self, ghost_coord, radius):
        r_c = random.choice(self.floors).coord
        if calculate_L1(r_c, ghost_coord) > radius:
            return r_c
        return self.get_random_coord(ghost_coord, radius)

    def resolve_ghost_direction(self, ghost, pacman_coord, used_sectors=[], used_val=0):
        ghost_coord = get_sector_coord(ghost.x + SECTOR_SIZE / 2, ghost.y + SECTOR_SIZE / 2)
        ghost_init_coord = get_sector_coord(ghost.initial_location[0] + ghost.width / 2, ghost.initial_location[1] +
                                            ghost.width / 2)
        if not ghost.is_alive:
            if ghost_coord == ghost_init_coord:
                ghost.form = random.choice(forms)
                ghost.is_alive = True

        if ghost.is_alive and self.pacman.is_alive:
            path = self.path_finder.get_path(ghost_coord, pacman_coord, used_sectors, used_val)
            ghost.preferred_direction = self.path_finder.get_direction(ghost_coord, path)
        else:
            path = self.path_finder.get_path(ghost_coord, ghost_init_coord)
            ghost.preferred_direction = self.path_finder.get_direction(ghost_coord, path)

        return path

    def pacman_in_radius(self, ghost, radius=4):
        return calculate_L1(self.pacman.coord, ghost.coord) < radius * SECTOR_SIZE

    def mp_finder(self, ghost):  # FIXME revision
        if len(self.mega_pellets) < self.mega_pellets_counter + 1:
            self.mega_pellets_counter = 0
        while True:
            checked_mp = self.mega_pellets[self.mega_pellets_counter]
            target = get_sector_coord(*checked_mp.coord)
            if len(self.mega_pellets) <= 1:
                return target
            if not target == ghost.previous_target_coord or ghost.previous_target_coord is None:
                checked_mp.patrolled = True
                self.mega_pellets_counter += 1
                return target
            if len(self.mega_pellets) > self.mega_pellets_counter + 1:
                self.mega_pellets_counter += 1
            else:
                self.mega_pellets_counter = 0

    def update_ghosts(self, tick_time, hardcore=True):  # FIXME revision
        self.counter_ai_tick_time += tick_time
        if self.counter_ai_tick_time > DESIRED_AI_TICK_TIME:
            start_time = time.time()
            pacman_coord = get_sector_coord(self.pacman.x + self.pacman.width / 2,
                                            self.pacman.y + self.pacman.height / 2)
            used_sectors = []

            for i in range(len(self.ghosts)):
                target = self.ghosts[i].target_coord

                if get_sector_coord(self.ghosts[i].x + SECTOR_SIZE / 2,
                                    self.ghosts[i].y + SECTOR_SIZE / 2) in self.teleports:
                    if target in self.teleports:
                        self.ghosts[i].target_coord = None
                    continue

                if get_sector_coord(self.ghosts[i].x + SECTOR_SIZE / 2, self.ghosts[i].y + SECTOR_SIZE / 2) == target:
                    target = None

                if len(self.ghosts) >= len(self.mega_pellets) and target is None:
                    target = get_sector_coord(*self.get_random_coord(self.ghosts[i].coord, SECTOR_SIZE * 12))

                if self.pacman_in_radius(self.ghosts[i], radius=5):
                    target = pacman_coord

                if i >= len(self.mega_pellets) and target is None:
                    target = get_sector_coord(*self.get_random_coord(self.ghosts[i].coord, SECTOR_SIZE * 12))

                else:
                    if target is None:
                        target = self.mp_finder(self.ghosts[i])

                self.ghosts[i].target_coord = target
                self.ghosts[i].previous_target_coord = target
                path = self.resolve_ghost_direction(self.ghosts[i], target, used_sectors, 4)  # Hardcore heuristics

                if hardcore and path is not None:
                    used_sectors.extend(path)
            end_time = time.time()
            self.ghost_update_exec_time = end_time - start_time
            self.counter_ai_tick_time = 0

    def move_ghosts(self, counter_physics_tick_time):
        for ghost in self.ghosts:
            ghost.velocity = int(self.current_level.GHOST_PX_PER_SECOND * counter_physics_tick_time)
            self.move_creature(ghost)

    def check_pacman_ghost_collision(self):
        for ghost in self.ghosts:
            if pygame.sprite.collide_mask(self.pacman.creature_hitbox, ghost.creature_hitbox) and ghost.is_alive:
                if self.pacman.form == ghost.form:
                    self.pacman.score += self.current_level.ghost_value
                    ghost_died(ghost)
                elif ghost.is_alive:
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

    def revive_pacman(self):
        self.pacman.is_alive = True
        (self.pacman.x, self.pacman.y) = self.current_level.level_map.pacman_initial_coord

    def pacman_die(self):
        if self.pacman.is_alive:
            if self.pacman.lives > 1:
                self.pacman.lives -= 1
                self.revive_pacman()
            else:
                self.pacman.lives -= 1
                self.player_score = 0
                self.pacman.animation_count = 0
                self.pacman.is_alive = False

        self.deactivate_active_ability()

    def physics_update(self, tick_time):
        if self.pacman.is_alive:
            if tick_time >= DESIRED_PHYSICS_TICK_TIME:
                self.counter_physics_tick_time = tick_time
            else:
                self.counter_physics_tick_time += tick_time

            if self.counter_physics_tick_time >= DESIRED_PHYSICS_TICK_TIME:
                start_time = time.time()
                self.update_pacman(self.counter_physics_tick_time)
                self.move_ghosts(self.counter_physics_tick_time)
                self.counter_physics_tick_time = 0
                end_time = time.time()
                self.physics_update_exec_time = end_time - start_time
        elif self.pacman.animation_count >= 8:
            self.render_update(0.1)
            self.renderer.render_label("WASTED", "Press \"F\" to try again.", bg_full_opacity=True)
            self.pacman.is_alive = False
            self.game_restart()

    def time_convert(self, sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))

    def render_update(self, tick_time, skip_screen_update=False):

        self.counter_render_tick_time += tick_time
        if self.counter_render_tick_time > DESIRED_RENDER_TICK_TIME:
            start_time = time.time()
            self.renderer.render([self.pellets, self.mega_pellets, self.walls, self.current_level.level_map.floors,
                                  [], [self.pacman], self.ghosts],
                                 [self.speed_ability, self.transform_ability], self.cooldown_timer,
                                 self.current_level, tick_time, showgrid=False, show_hitboxes=False,
                                 render_mode=RenderModes.PartialRedraw_A,
                                 skip_screen_update=skip_screen_update)
            end_time = time.time()
            self.counter_render_tick_time = 0
            self.render_update_exec_time = end_time - start_time

    def abilities_update(self, tick_time):
        if self.speed_ability:
            self.speed_ability.update(tick_time)
        if self.transform_ability:
            self.transform_ability.update(tick_time)
        if self.cooldown_timer:
            self.cooldown_timer.update(tick_time)

    def run(self):
        self.is_playing = False
        self.is_game_complete = False

        self.renderer.play_splash_screen()

        self.render_update(1 / GLOBAL_TICK_RATE, skip_screen_update=True)
        self.renderer.render_label("READY?", "Press \"F\" to start!", bg_full_opacity=True)
        self.renderer.restart()

        clock = pygame.time.Clock()
        # DEBUG:
        # self.ticktime_debugger.run()
        run = True
        while run:

            miliseconds = clock.tick(GLOBAL_TICK_RATE)
            self.tick_time = miliseconds / 1000.0  # seconds
            true_tick_time = self.tick_time

            if self.is_playing and not self.is_game_complete:

                if self.tick_time > 0.1:
                    self.tick_time = 1 / GLOBAL_TICK_RATE

                self.handle_events()
                self.physics_update(self.tick_time)
                if self.pacman.is_alive:
                    self.update_ghosts(self.tick_time, hardcore=True)
                self.abilities_update(self.tick_time)

                self.update_level()
                if not self.is_game_restart and not self.is_game_complete:
                    self.render_update(self.tick_time)

            elif not self.is_playing and not self.is_game_complete:

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == K_f:
                            self.is_playing = True
                            if self.is_game_restart:
                                self.is_game_restart = False
                                self.renderer.restart()

            elif self.is_game_complete:

                self.renderer.render_label("You win!", "Great job! Your score is " + str(self.player_score) +
                                           " points. Press \"F\" to play again",
                                           bg_full_opacity=True)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == K_f:
                            self.is_game_complete = False
                            self.player_score = 0
                            self.pacman.score = 0
                            self.renderer.fade_out()
                            self.renderer.restart()

        pygame.quit()
