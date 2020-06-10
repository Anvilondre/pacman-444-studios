import pygame

from src.data import Constants


class LineOfIconsWidget(object):

    def __init__(self, boundrect, icon_path: str, n: int = 0, box_size: int = 87, icon_margins=0):
        self.icons = []
        self.boundrect = boundrect  # icons bounding rect
        self._n = n  # number of icons
        self.box_size = box_size  # size of box containing single image, px
        self.icon_margins = icon_margins  # px
        self.icon_size = int(box_size - icon_margins)
        self.image = self.get_image_of(icon_path, self.icon_size)

    def get_image_of(self, icon_path, icon_size):
        img = pygame.image.load(icon_path)
        img = pygame.transform.scale(img, (icon_size, icon_size))
        img = img.convert_alpha()
        return img

    def set_n(self, n):
        while self._n > n:
            self.pop()
        while self._n < n:
            self.append()

    def append(self):
        self._n += 1
        self.icons.append([pygame.transform.scale(self.image, (self.icon_size, self.icon_size)),
            self.boundrect.x + (self._n - 1) * self.box_size + self.icon_margins,
            self.boundrect.y])

        # TODO: buggy when n > 10
        # If icons width is greater than width of boundrect..
        icons_width = self._n * self.box_size
        if icons_width > self.boundrect.width:
            # ..then make every icon smaller and change its x position
            correction_ratio = self.boundrect.width / icons_width
            self.icon_size = int(self.icon_size * correction_ratio)
            self.box_size = int(self.box_size * correction_ratio)
            for i, icon in enumerate(self.icons):
                icon[0] = pygame.transform.scale(icon[0], (self.icon_size, self.icon_size))
                icon[1] = self.boundrect.x + i * self.box_size + self.icon_margins
                icon[2] = self.boundrect.y + (self.boundrect.height - self.icon_size)/4


    def pop(self):
        if self._n > 0:
            self._n -= 1
            self.icons.pop()


class Renderer(object):
    def __init__(self, map_dimensions, is_fullscreen=Constants.IS_FULLSCREEN,
                 windowed_screen_width=Constants.WINDOWED_SCREEN_WIDTH,
                 windowed_screen_height=Constants.WINDOWED_SCREEN_HEIGHT):

        self.first_map_render = True

        self.map_dimensions = map_dimensions  # cells
        self.map_size = [map_dimensions[0] * Constants.SECTOR_SIZE, map_dimensions[1] * Constants.SECTOR_SIZE, ]  # px
        self.animation_period = Constants.ANIMATION_PERIOD  # seconds
        self.time_elapsed_from_prev_animation_frame = 0  # seconds

        # Set window mode
        if is_fullscreen is True:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((windowed_screen_width, windowed_screen_height))

        # Get actual window size
        self.canvas_width = pygame.display.get_surface().get_width()
        self.canvas_height = pygame.display.get_surface().get_height()

        # Init GUI and all required surfaces
        self._init_background()
        self._init_gui()
        self._init_gamescreen(map_dimensions)
        self._init_covers()

        # Init element lists
        self._init_bg_elements_list()
        self._init_gui_elements_list()
        self._init_covers_list()

    def set_map_dimensions(self, map_dimensions):
        self.map_dimensions = map_dimensions  # cells
        self.map_size = [map_dimensions[0] * Constants.SECTOR_SIZE, map_dimensions[1] * Constants.SECTOR_SIZE, ]  # px

        # Because map dimensions have changed, we have to update our gamescreen surf, cell size and
        # update all elements dependant on latter
        self._init_gamescreen(map_dimensions)
        self._init_bg_elements_list()
        self._init_gui_elements_list()
        self._init_covers()
        self._init_covers_list()

    def _init_background(self):
        self.background_surf = pygame.Surface((self.canvas_width, self.canvas_height))
        self.background_surf_x = 0
        self.background_surf_y = 0
        self.background_surf.fill(Constants.SCREEN_BACKGROUND_COLOR)

        self.gamescreen_boundbox_surf_width = int(Constants.GAMESCREEN_BOUNDBOX_SURF_WIDTH_RATIO * self.canvas_width)
        self.gamescreen_boundbox_surf_height = int(Constants.GAMESCREEN_BOUNDBOX_SURF_HEIGHT_RATIO * self.canvas_height)
        self.gamescreen_boundbox_surf = pygame.Surface(
            (self.gamescreen_boundbox_surf_width, self.gamescreen_boundbox_surf_height))
        self.gamescreen_boundbox_surf_x = self.canvas_width / 2 - self.gamescreen_boundbox_surf.get_width() / 2
        self.gamescreen_boundbox_surf_y = self.canvas_height / 2 - self.gamescreen_boundbox_surf.get_height() / 2
        self.gamescreen_boundbox_surf.fill(Constants.SCREEN_BACKGROUND_COLOR)

    def _init_gamescreen(self, map_dimensions):
        self.gamescreen_cell_size = int(Constants.GAMESCREEN_CELL_SIZE_RATIO * self.canvas_width)
        self.gamescreen_surf_width = map_dimensions[0] * self.gamescreen_cell_size
        self.gamescreen_surf_height = map_dimensions[1] * self.gamescreen_cell_size
        self._rescale_gamescreen(map_dimensions)

        self.gamescreen_surf = pygame.Surface((self.gamescreen_surf_width, self.gamescreen_surf_height))
        self.gamescreen_surf_x = self.canvas_width / 2 - self.gamescreen_surf.get_width() / 2
        self.gamescreen_surf_y = self.canvas_height / 2 - self.gamescreen_surf.get_height() / 2
        self.gamescreen_surf.fill(Constants.GAMESCREEN_COLOR)

    def _rescale_gamescreen(self, map_dimensions):
        """Rescale gamescreen if it's bigger, than gamescreen bounds"""
        if self.gamescreen_surf_width > self.gamescreen_boundbox_surf_width and \
                self.gamescreen_surf_height > self.gamescreen_boundbox_surf_height:
            self.gamescreen_cell_size = int(
                self.gamescreen_cell_size * min(self.gamescreen_boundbox_surf_width / self.gamescreen_surf_width,
                                                self.gamescreen_boundbox_surf_height / self.gamescreen_surf_height))
            # Recalculate width and height
            self.gamescreen_surf_width = map_dimensions[0] * self.gamescreen_cell_size
            self.gamescreen_surf_height = map_dimensions[1] * self.gamescreen_cell_size

        if self.gamescreen_surf_width > self.gamescreen_boundbox_surf_width:
            self.gamescreen_cell_size = int(
                self.gamescreen_cell_size * self.gamescreen_boundbox_surf_width / self.gamescreen_surf_width)

            # Recalculate width and height
            self.gamescreen_surf_width = map_dimensions[0] * self.gamescreen_cell_size
            self.gamescreen_surf_height = map_dimensions[1] * self.gamescreen_cell_size

        if self.gamescreen_surf_height > self.gamescreen_boundbox_surf_height:
            self.gamescreen_cell_size = int(
                self.gamescreen_cell_size * self.gamescreen_boundbox_surf_height / self.gamescreen_surf_height)

            # Recalculate width and height
            self.gamescreen_surf_width = map_dimensions[0] * self.gamescreen_cell_size
            self.gamescreen_surf_height = map_dimensions[1] * self.gamescreen_cell_size

    def _init_gui(self):
        self.top_bar_width = Constants.TOP_BAR_WIDTH_RATIO * self.canvas_width
        self.top_bar_height = Constants.TOP_BAR_HEIGHT_RATIO * self.canvas_height
        self.bottom_bar_width = Constants.BOTTOM_BAR_WIDTH_RATIO * self.canvas_width
        self.bottom_bar_height = Constants.BOTTOM_BAR_HEIGHT_RATIO * self.canvas_height

        self.lives_bar_surf_width = int(Constants.LIVES_BAR_WIDTH * self.bottom_bar_width)
        self.lives_bar_surf_height = int(self.bottom_bar_height)
        self.lives_bar_surf = pygame.Surface((self.lives_bar_surf_width, self.lives_bar_surf_height))
        self.lives_bar_surf_x = Constants.BOTTOM_BAR_X_RATIO * self.canvas_width
        self.lives_bar_surf_y = Constants.BOTTOM_BAR_Y_RATIO * self.canvas_height
        self.lives_bar_surf.fill((203, 124, 30))
        self.lives_icons = LineOfIconsWidget(pygame.Rect(self.lives_bar_surf_x, self.lives_bar_surf_y,
                                                         self.lives_bar_surf_width, self.lives_bar_surf_height),
                                             icon_path=Constants.LIVES_ICON_PATH,
                                             box_size=self.bottom_bar_height)

        self.abilities_bar_surf_width = int(Constants.ABILITIES_BAR_WIDTH * self.bottom_bar_width)
        self.abilities_bar_surf_height = int(self.bottom_bar_height)
        self.abilities_bar_surf = pygame.Surface((self.abilities_bar_surf_width, self.abilities_bar_surf_height))
        self.abilities_bar_surf_x = self.lives_bar_surf_x + self.lives_bar_surf_width
        self.abilities_bar_surf_y = self.lives_bar_surf_y
        self.abilities_bar_surf.fill((65, 204, 186))
        # self.lives_icons = LineOfIconsWidget(pygame.Rect(self.abilities_bar_surf_x, self.abilities_bar_surf_y,
        #                                                  self.abilities_bar_surf_width, self.abilities_bar_surf_height),
        #                                      icon_path=Constants.ABILITIES_ICON_PATH,
        #                                      box_size=self.bottom_bar_height)

        self.fruits_bar_surf_width = int(Constants.FRUITS_BAR_WIDTH * self.bottom_bar_width)
        self.fruits_bar_surf_height = int(self.bottom_bar_height)
        self.fruits_bar_surf = pygame.Surface((self.fruits_bar_surf_width, self.fruits_bar_surf_height))
        self.fruits_bar_surf_x = self.abilities_bar_surf_x + self.abilities_bar_surf_width
        self.fruits_bar_surf_y = self.abilities_bar_surf_y
        self.fruits_bar_surf.fill((204, 65, 107))

    def _init_covers(self):
        self.left_teleport_cover_surf = pygame.Surface((self.gamescreen_cell_size, self.gamescreen_surf_height))
        self.left_teleport_cover_surf_x = self.gamescreen_surf_x - self.gamescreen_cell_size
        self.left_teleport_cover_surf_y = self.gamescreen_surf_y
        self.left_teleport_cover_surf.fill(Constants.SCREEN_BACKGROUND_COLOR)

        self.up_teleport_cover_surf = pygame.Surface((self.gamescreen_surf_width, self.gamescreen_cell_size))
        self.up_teleport_cover_surf_x = self.gamescreen_surf_x
        self.up_teleport_cover_surf_y = self.gamescreen_surf_y - self.gamescreen_cell_size
        self.up_teleport_cover_surf.fill(Constants.SCREEN_BACKGROUND_COLOR)

        self.right_teleport_cover_surf = pygame.Surface((self.gamescreen_cell_size, self.gamescreen_surf_height))
        self.right_teleport_cover_surf_x = self.gamescreen_surf_x + self.gamescreen_surf_width
        self.right_teleport_cover_surf_y = self.gamescreen_surf_y
        self.right_teleport_cover_surf.fill(Constants.SCREEN_BACKGROUND_COLOR)

        self.down_teleport_cover_surf = pygame.Surface((self.gamescreen_surf_width, self.gamescreen_cell_size))
        self.down_teleport_cover_surf_x = self.gamescreen_surf_x
        self.down_teleport_cover_surf_y = self.gamescreen_surf_y + self.gamescreen_surf_height
        self.down_teleport_cover_surf.fill(Constants.SCREEN_BACKGROUND_COLOR)

    def _init_bg_elements_list(self):
        """Creates a list of all background elements and their absolute positions on the canvas"""
        self.bg_elements = []

        self.bg_elements.append([self.background_surf, self.background_surf_x, self.background_surf_y])
        self.bg_elements.append(
            [self.gamescreen_boundbox_surf, self.gamescreen_boundbox_surf_x, self.gamescreen_boundbox_surf_y])
        self.bg_elements.append([self.gamescreen_surf, self.gamescreen_surf_x, self.gamescreen_surf_y])

    def _init_gui_elements_list(self):
        """Creates a list of all gui elements and their absolute positions on the canvas"""
        self.gui_elements = []

        self.gui_elements.append([self.lives_bar_surf, self.lives_bar_surf_x, self.lives_bar_surf_y])
        self.gui_elements.append([self.abilities_bar_surf, self.abilities_bar_surf_x, self.abilities_bar_surf_y])
        self.gui_elements.append([self.fruits_bar_surf, self.fruits_bar_surf_x, self.fruits_bar_surf_y])
        for icon in self.lives_icons.icons:
            self.gui_elements.append(icon)

    def _init_covers_list(self):
        """Creates a list of all covers and their absolute positions on the canvas"""
        self.covers = []

        self.covers.append(
            [self.left_teleport_cover_surf, self.left_teleport_cover_surf_x, self.left_teleport_cover_surf_y])
        self.covers.append([self.up_teleport_cover_surf, self.up_teleport_cover_surf_x, self.up_teleport_cover_surf_y])
        self.covers.append(
            [self.right_teleport_cover_surf, self.right_teleport_cover_surf_x, self.right_teleport_cover_surf_y])
        self.covers.append(
            [self.down_teleport_cover_surf, self.down_teleport_cover_surf_x, self.down_teleport_cover_surf_y])

    def _draw_grid(self):
        for x in range(self.gamescreen_surf_width // self.gamescreen_cell_size + 1):
            pygame.draw.line(self.window, (255, 255, 255),
                             (x * self.gamescreen_cell_size + self.gamescreen_surf_x, self.gamescreen_surf_y),
                             (x * self.gamescreen_cell_size + self.gamescreen_surf_x,
                              self.gamescreen_surf_y + self.gamescreen_surf_height))
        for x in range(self.gamescreen_surf_height // self.gamescreen_cell_size + 1):
            pygame.draw.line(self.window, (255, 255, 255),
                             (self.gamescreen_surf_x, x * self.gamescreen_cell_size + self.gamescreen_surf_y),
                             (self.gamescreen_surf_x + self.gamescreen_surf_width,
                              x * self.gamescreen_cell_size + self.gamescreen_surf_y))

    def _draw_text(self, pacman):
        # TODO
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text = font.render("Score: " + str(pacman.score), 1, (255, 255, 255))
        place = text.get_rect(topleft=(self.lives_bar_surf_x, 0))
        self.window.blit(text, place)

    def _mapscreen_coords_to_gamescreen_coords(self, coords):
        x = coords[0] * self.gamescreen_surf_width / self.map_size[0] + self.gamescreen_surf_x
        y = coords[1] * self.gamescreen_surf_height / self.map_size[1] + self.gamescreen_surf_y
        return (x, y)

    def _mapscreen_xy_to_gamescreen_coords(self, x, y):
        x = x * self.gamescreen_surf_width / self.map_size[0]
        y = y * self.gamescreen_surf_height / self.map_size[1]
        return (x, y)

    def _show_hitbox(self, gameObject):
        """This method shows all the hitboxes gameObject has"""
        try:
            hitbox_preview = gameObject.hitbox.image
            self._show_transparent_hitbox(gameObject, hitbox_preview)
        except:
            pass

        try:
            hitbox_preview = gameObject.mapobject_hitbox.image
            self._show_transparent_hitbox(gameObject, hitbox_preview)
        except:
            pass

        try:
            hitbox_preview = gameObject.creature_hitbox.image
            self._show_transparent_hitbox(gameObject, hitbox_preview)
        except:
            pass

    def _show_transparent_hitbox(self, gameObject, hitbox_preview):

        x, y = self._mapscreen_coords_to_gamescreen_coords(gameObject.coord)
        rescaled_hitbox_preview = pygame.transform.scale(hitbox_preview,
                                                         (self.gamescreen_cell_size, self.gamescreen_cell_size))

        temp = pygame.Surface((rescaled_hitbox_preview.get_width(), rescaled_hitbox_preview.get_height())).convert()
        temp.blit(self.window, (-x, -y))
        temp.blit(rescaled_hitbox_preview, (0, 0))
        temp.set_alpha(Constants.HITBOX_OPACITY)
        self.window.blit(temp, (x, y))

    def render(self, entities_list, elapsed_time, showgrid=False, show_hitboxes=True):
        """entities_list: (pellets, mega_pellets, walls, cherry, pacman, ghosts)"""

        # Unpack entities_list
        pellets, mega_pellets, walls, cherry, pacman, ghosts = entities_list

        # Draw background
        for element in self.bg_elements:
            self.window.blit(element[0], (element[1], element[2]))

        # This variable is needed for proper animation speed independent of FPS
        self.time_elapsed_from_prev_animation_frame += elapsed_time

        # Draw mapobjects
        if self.first_map_render:
            self._draw_mapobjects(walls, show_hitboxes=show_hitboxes)
            # TODO
            self.first_map_render = True
        self._draw_mapobjects(pellets, show_hitboxes=show_hitboxes)
        self._draw_mapobjects(mega_pellets, show_hitboxes=show_hitboxes)
        self._draw_mapobjects(cherry, show_hitboxes=show_hitboxes)

        # Draw creatures
        self._draw_pacmans(pacman, show_hitboxes=show_hitboxes)
        self._draw_ghosts(ghosts, show_hitboxes=show_hitboxes)

        # self._draw_text(pacman[0])
        # pygame.display.set_caption("Elapsed time: " + str(elapsed_time))

        # Draw covers
        for cover in self.covers:
            self.window.blit(cover[0], (cover[1], cover[2]))

        # Draw GUI
        self.lives_icons.set_n(pacman[0].lives)
        # ...
        self._init_gui_elements_list()
        for element in self.gui_elements:
            self.window.blit(element[0], (element[1], element[2]))

        # Draw Grid
        if showgrid:
            self._draw_grid()

        if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
            self.time_elapsed_from_prev_animation_frame = 0

        pygame.display.update()

    def _draw_mapobjects(self, mapobjects, show_hitboxes=False):
        for obj in mapobjects:
            surface = obj.texture
            rescaled_img = pygame.transform.scale(surface, (self.gamescreen_cell_size, self.gamescreen_cell_size))
            self.window.blit(rescaled_img, self._mapscreen_coords_to_gamescreen_coords(obj.coord))

            if show_hitboxes:
                self._show_hitbox(obj)

    def _draw_pacmans(self, pacman, show_hitboxes=False):
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
            self.window.blit(rescaled_img, self._mapscreen_coords_to_gamescreen_coords((pac.x, pac.y)))

            if show_hitboxes:
                self._show_hitbox(pac)

    def _draw_ghosts(self, ghosts, show_hitboxes=False):
        for ghost in ghosts:
            if ghost.is_alive is True and ghost.direction == "left":
                if ghost.animation_count >= 2:
                    ghost.animation_count = 0
                surface = ghost.animations["move_left"][ghost.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    ghost.animation_count += 1
                    if ghost.animation_count >= 2:
                        ghost.animation_count = 0

            elif ghost.is_alive is True and ghost.direction == "up":
                if ghost.animation_count >= 2:
                    ghost.animation_count = 0
                surface = ghost.animations["move_up"][ghost.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    ghost.animation_count += 1
                    if ghost.animation_count >= 2:
                        ghost.animation_count = 0

            elif ghost.is_alive is True and ghost.direction == "right":
                if ghost.animation_count >= 2:
                    ghost.animation_count = 0
                surface = ghost.animations["move_right"][ghost.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    ghost.animation_count += 1
                    if ghost.animation_count >= 2:
                        ghost.animation_count = 0

            elif ghost.is_alive is True and ghost.direction == "down":
                if ghost.animation_count >= 2:
                    ghost.animation_count = 0
                surface = ghost.animations["move_down"][ghost.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    ghost.animation_count += 1
                    if ghost.animation_count >= 2:
                        ghost.animation_count = 0

            elif ghost.is_alive is False:
                if ghost.animation_count >= 2:
                    ghost.animation_count = 0
                surface = ghost.animations["dead"][ghost.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    ghost.animation_count += 1
                    if ghost.animation_count >= 9:
                        ghost.animation_count = 0
            else:
                raise Exception("Unable to identify ghost's state:", ghost)

            rescaled_img = pygame.transform.scale(surface, (self.gamescreen_cell_size, self.gamescreen_cell_size))
            self.window.blit(rescaled_img, self._mapscreen_coords_to_gamescreen_coords((ghost.x, ghost.y)))

            if show_hitboxes:
                self._show_hitbox(ghost)
