import pygame

from src.data import Constants


class Renderer(object):
    def __init__(self, map_dimensions, is_fullscreen=Constants.IS_FULLSCREEN,
                 windowed_screen_width=Constants.WINDOWED_SCREEN_WIDTH,
                 windowed_screen_height=Constants.WINDOWED_SCREEN_HEIGHT):

        self.map_dimensions = map_dimensions
        self.animation_period = Constants.ANIMATION_PERIOD # seconds
        self.time_elapsed_from_prev_animation_frame = 0

        # Set window mode
        if is_fullscreen is True:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((windowed_screen_width, windowed_screen_height))

        # Get actual window size
        self.canvas_width = pygame.display.get_surface().get_width()
        self.canvas_height = pygame.display.get_surface().get_height()

        # Init UI surfaces and calculate their coordinate and size
        self.background_surf = pygame.Surface((self.canvas_width, self.canvas_height))
        self.background_surf_x = 0
        self.background_surf_y = 0
        self.background_surf.fill((0, 0, 0))

        top_bar_width = Constants.TOP_BAR_WIDTH_RATIO * self.canvas_width
        top_bar_height = Constants.TOP_BAR_HEIGHT_RATIO * self.canvas_height
        self.bottom_bar_width = Constants.BOTTOM_BAR_WIDTH_RATIO * self.canvas_width
        self.bottom_bar_height = Constants.BOTTOM_BAR_HEIGHT_RATIO * self.canvas_height

        self.lives_bar_surf_width = int(Constants.LIVES_BAR_WIDTH * self.bottom_bar_width)
        self.lives_bar_surf_height = int(self.bottom_bar_height)
        self.lives_bar_surf = pygame.Surface((self.lives_bar_surf_width, self.lives_bar_surf_height))
        self.lives_bar_surf_x = Constants.BOTTOM_BAR_X_RATIO * self.canvas_width
        self.lives_bar_surf_y = Constants.BOTTOM_BAR_Y_RATIO * self.canvas_height
        self.lives_bar_surf.fill((203, 124, 30))

        self.abilities_bar_surf_width = int(Constants.ABILITIES_BAR_WIDTH * self.bottom_bar_width)
        self.abilities_bar_surf_height = int(self.bottom_bar_height)
        self.abilities_bar_surf = pygame.Surface((self.abilities_bar_surf_width, self.abilities_bar_surf_height))
        self.abilities_bar_surf_x = self.lives_bar_surf_x + self.lives_bar_surf_width
        self.abilities_bar_surf_y = self.lives_bar_surf_y
        self.abilities_bar_surf.fill((65, 204, 186))

        self.fruits_bar_surf_width = int(Constants.FRUITS_BAR_WIDTH * self.bottom_bar_width)
        self.fruits_bar_surf_height = int(self.bottom_bar_height)
        self.fruits_bar_surf = pygame.Surface((self.fruits_bar_surf_width, self.fruits_bar_surf_height))
        self.fruits_bar_surf_x = self.abilities_bar_surf_x + self.abilities_bar_surf_width
        self.fruits_bar_surf_y = self.abilities_bar_surf_y
        self.fruits_bar_surf.fill((204, 65, 107))

        self.gamescreen_boundbox_surf_width = int(Constants.GAMESCREEN_BOUNDBOX_SURF_WIDTH_RATIO * self.canvas_width)
        self.gamescreen_boundbox_surf_height = int(Constants.GAMESCREEN_BOUNDBOX_SURF_HEIGHT_RATIO * self.canvas_height)
        self.gamescreen_boundbox_surf = pygame.Surface((self.gamescreen_boundbox_surf_width, self.gamescreen_boundbox_surf_height))
        self.gamescreen_boundbox_surf_x = self.canvas_width / 2 - self.gamescreen_boundbox_surf.get_width() / 2
        self.gamescreen_boundbox_surf_y = self.canvas_height / 2 - self.gamescreen_boundbox_surf.get_height() / 2
        self.gamescreen_boundbox_surf.fill((80, 0, 0))

        self.gamescreen_cell_size = int(Constants.GAMESCREEN_CELL_SIZE_RATIO * self.canvas_width)
        print("CELL SIZE:", self.gamescreen_cell_size)
        self.gamescreen_surf_width = map_dimensions[0] * self.gamescreen_cell_size
        self.gamescreen_surf_height = map_dimensions[1] * self.gamescreen_cell_size

        # Rescale gamescreen if
        if self.gamescreen_surf_width > self.gamescreen_boundbox_surf_width and \
           self.gamescreen_surf_height > self.gamescreen_boundbox_surf_height:
            self.gamescreen_cell_size = int(self.gamescreen_cell_size * min(self.gamescreen_boundbox_surf_width/self.gamescreen_surf_width,
                                                                            self.gamescreen_boundbox_surf_height/self.gamescreen_surf_height))
        # Recalculate width and height
        self.gamescreen_surf_width = map_dimensions[0] * self.gamescreen_cell_size
        self.gamescreen_surf_height = map_dimensions[1] * self.gamescreen_cell_size

        if self.gamescreen_surf_width > self.gamescreen_boundbox_surf_width:
            self.gamescreen_cell_size = int(self.gamescreen_cell_size * self.gamescreen_boundbox_surf_width/self.gamescreen_surf_width)

            # Recalculate width and height
            self.gamescreen_surf_width = map_dimensions[0] * self.gamescreen_cell_size
            self.gamescreen_surf_height = map_dimensions[1] * self.gamescreen_cell_size

        if self.gamescreen_surf_height > self.gamescreen_boundbox_surf_height:
            self.gamescreen_cell_size = int(self.gamescreen_cell_size * self.gamescreen_boundbox_surf_height / self.gamescreen_surf_height)

            # Recalculate width and height
            self.gamescreen_surf_width = map_dimensions[0] * self.gamescreen_cell_size
            self.gamescreen_surf_height = map_dimensions[1] * self.gamescreen_cell_size



        self.gamescreen_surf = pygame.Surface((self.gamescreen_surf_width, self.gamescreen_surf_height))
        self.gamescreen_surf_x = self.canvas_width / 2 - self.gamescreen_surf.get_width() / 2
        self.gamescreen_surf_y = self.canvas_height / 2 - self.gamescreen_surf.get_height() / 2
        self.gamescreen_surf.fill((255, 100, 100))


        # (map_width, map_height)

        # Create a list of all ui elements and their absolute positions on the canvas
        self.ui_elements = []
        self.ui_elements.append([self.background_surf, self.background_surf_x, self.background_surf_y])
        self.ui_elements.append([self.gamescreen_boundbox_surf, self.gamescreen_boundbox_surf_x, self.gamescreen_boundbox_surf_y])
        self.ui_elements.append([self.gamescreen_surf, self.gamescreen_surf_x, self.gamescreen_surf_y])

        self.ui_elements.append([self.lives_bar_surf, self.lives_bar_surf_x, self.lives_bar_surf_y])
        self.ui_elements.append([self.abilities_bar_surf, self.abilities_bar_surf_x, self.abilities_bar_surf_y])
        self.ui_elements.append([self.fruits_bar_surf, self.fruits_bar_surf_x, self.fruits_bar_surf_y])

    def render(self, entities_list, elapsed_time):
        """entities_list: (pellets, mega_pellets, walls, cherry, pacman, ghosts)"""
        # Init surfaces

        # Unpack entities_list
        pellets, mega_pellets, walls, cherry, pacman, ghosts = entities_list
        # Unpack map_dimensions (unit: cells)
        map_width, map_height = self.map_dimensions

        # Draw GUI
        for element in self.ui_elements:
            self.window.blit(element[0], (element[1], element[2]))

        # Draw entities. Every texture is resized accordingly to sector size
        self.time_elapsed_from_prev_animation_frame += elapsed_time

        for pellet in pellets:
            surface = pellet.texture
            rescaled_img = pygame.transform.scale(surface, (self.gamescreen_cell_size, self.gamescreen_cell_size))
            self.window.blit(rescaled_img, (pellet.x, pellet.y))

        for mega_pellet in mega_pellets:
            surface = mega_pellet.texture
            rescaled_img = pygame.transform.scale(surface, (self.gamescreen_cell_size, self.gamescreen_cell_size))
            self.window.blit(rescaled_img, (mega_pellet.x, mega_pellet.y))

        for wall in walls:
            surface = wall.texture
            rescaled_img = pygame.transform.scale(surface, (self.gamescreen_cell_size, self.gamescreen_cell_size))
            self.window.blit(rescaled_img, (wall.x, wall.y))

        for cher in cherry:
            surface = cher.texture
            rescaled_img = pygame.transform.scale(surface, (self.gamescreen_cell_size, self.gamescreen_cell_size))
            self.window.blit(rescaled_img, (cher.x, cher.y))

        for pac in pacman:
            if pac.is_alive is True and pac.direction == "left":
                surface = pac.animations["move_left"][pac.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    pac.animation_count += 1
                    if pac.animation_count >= 4:
                        pac.animation_count = 0

            elif pac.is_alive is True and pac.direction == "up":
                surface = pac.animations["move_up"][pac.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    pac.animation_count += 1
                    if pac.animation_count >= 4:
                        pac.animation_count = 0

            elif pac.is_alive is True and pac.direction == "right":
                surface = pac.animations["move_right"][pac.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    pac.animation_count += 1
                    if pac.animation_count >= 4:
                        pac.animation_count = 0

            elif pac.is_alive is True and pac.direction == "down":
                surface = pac.animations["move_down"][pac.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    pac.animation_count += 1
                    if pac.animation_count >= 4:
                        pac.animation_count = 0
            elif pac.is_alive is False:
                surface = pac.animations["dead"][pac.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    pac.animation_count += 1
                    if pac.animation_count >= 9:
                        pac.animation_count = 0
            else:
                raise Exception("Unable to identify pacman's state", pac)
            rescaled_img = pygame.transform.scale(surface, (self.gamescreen_cell_size, self.gamescreen_cell_size))
            self.window.blit(rescaled_img, (pac.x, pac.y))

        for ghost in ghosts:
            if ghost.is_alive is True and ghost.direction == "left":
                surface = ghost.animations["move_left"][ghost.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    ghost.animation_count += 1
                    if ghost.animation_count >= 4:
                        ghost.animation_count = 0

            elif ghost.is_alive is True and ghost.direction == "up":
                surface = ghost.animations["move_up"][ghost.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    ghost.animation_count += 1
                    if ghost.animation_count >= 4:
                        ghost.animation_count = 0

            elif ghost.is_alive is True and ghost.direction == "right":
                surface = ghost.animations["move_right"][ghost.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    ghost.animation_count += 1
                    if ghost.animation_count >= 4:
                        ghost.animation_count = 0

            elif ghost.is_alive is True and ghost.direction == "down":
                surface = ghost.animations["move_down"][ghost.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    ghost.animation_count += 1
                    if ghost.animation_count >= 4:
                        ghost.animation_count = 0
            elif ghost.is_alive is False:
                surface = ghost.animations["dead"][ghost.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    ghost.animation_count += 1
                    if ghost.animation_count >= 9:
                        ghost.animation_count = 0
            else:
                raise Exception("Unable to identify ghost's state:", ghost)

            rescaled_img = pygame.transform.scale(surface, (self.gamescreen_cell_size, self.gamescreen_cell_size))
            self.window.blit(rescaled_img, (ghost.x, ghost.y))

        if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
            self.time_elapsed_from_prev_animation_frame = 0
        # self.window.blit(pacman[1].animations["move_left"][0], (pacman[1].x, pacman[1].y))
        # self.window.blit(self.gamescreen_surf, (200, 200))