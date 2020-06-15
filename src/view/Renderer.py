
import enum
import itertools
import math

import pygame

from src.data import Constants
from src.data.Levels import Level


def distance(a, b):
    try:
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    except:
        raise Exception("a: "+str(a)+"; b: "+str(b))


def _get_near_objects(center_objects_coords, objects, radius=2 * Constants.SECTOR_SIZE):
    """Returns a list of objects in radius <= given radius around center_objects_coords list of coordinates (x,y)"""

    near_objects = []

    for center_object_coord in center_objects_coords:
        for object in objects:
            # Draw if distance between pellet and pacman is smaller than R = 2*SECTOR_SIZE
            if distance(object.coord, center_object_coord) <= radius:
                near_objects.append(object)

    return near_objects


class ResourceManager(object):
    # TODO IMPLEMENT
    animations = dict()
    """{"%animation_owner%": {"%animation_name%": %animation_dict%:, "%animation_name%": %animation_dict%, ...}}"""

    def get_animations_from(animations_paths_dict, icon_size):

        if animations_paths_dict and isinstance(animations_paths_dict, dict):
            animations = dict()

            for animation_type, animation_paths_list in animations_paths_dict.items():

                # Create list of images which are located at given path (at animations_paths)
                animation_images_list = []
                for path in animation_paths_list:
                    animation_images_list.append(ResourceManager.get_image_from(path, icon_size))

                # Insert this list at corresponding key (animation type)
                animations[animation_type] = animation_images_list

            return animations

    def get_image_from(icon_path, icon_size):
        img = pygame.image.load(icon_path)
        img = pygame.transform.scale(img, (icon_size, icon_size))
        img = img.convert_alpha()
        return img


class RenderModes(enum.Enum):
    RedrawAll = 0  # Redraws every single object every tick
    PartialRedraw_A = 1  # Redraws all objects (excluding walls) in given radius


class Icon(object):
    """This class represents an icon. It supports animations."""
    def __init__(self, icon_animations, x=0, y=0, icon_state="default"):
        self.x = x
        self.y = y
        self.animations = icon_animations
        self.icon_size = self.animations["default"][0].get_rect().width
        self.current_state = icon_state
        self.icon_states = list(self.animations.keys())
        self._counter_upper_limit = len(self.animations[self.current_state]) - 1
        self.counter = 0

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
        if value > 0:
            self.rescale_animations(int(value))
            self._icon_size = int(value)
        else:
            raise ValueError("Cannot assign icon_size to " + str(value))

    @property
    def current_state(self):
        return self._icon_state

    @current_state.setter
    def current_state(self, value):
        if value in self.animations.keys():
            self._icon_state = value
            self._counter_cycle = itertools.cycle([0, self.animations[self.current_state]])
        else:
            raise ValueError("Cannot assign icon_state to " + str(value) +
                             ". Unable to find appropriate animation type amongst these: " +
                             str(self.icon_states))

    def rescale_animations(self, size):
        for key, animation in zip(self.animations.keys(), self.animations.values()):
            for frame_i in range(len(animation)):
                self.animations[key][frame_i] = pygame.transform.scale(self.animations[key][frame_i], (size, size))

    def copy(self):
        copy_icon = Icon(self.animations)
        copy_icon.x = self.x
        copy_icon.y = self.y
        copy_icon.icon_size = self.icon_size
        copy_icon.current_state = self.current_state #TODO: COPY
        copy_icon.icon_states = self.icon_states #TODO: COPY
        copy_icon._counter_upper_limit = self._counter_upper_limit
        copy_icon.counter = self.counter

        return copy_icon


class LineOfIconsWidget(object):

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
                delta = (self.boundrect.x + self.boundrect.width/2) - (self.icons[0].x + (self._n * self.box_size)/2)

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

        icon.y = self.boundrect.y + (self.boundrect.height - self.icons_size)/2

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

        # TODO: buggy when n > 10
        # If icons width is greater than width of boundrect..
        icons_width = self._n * self.box_size
        if icons_width > self.boundrect.width:
            # ..then make every icon smaller and change its x position
            correction_ratio = self.boundrect.width / icons_width
            self.icons_size = int(self.icons_size * correction_ratio)
            self.box_size = int(self.box_size * correction_ratio)
            for i, icon in enumerate(self.icons):
                icon.rescale_animations(self.icons_size)
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


class Renderer(object):

    def __init__(self, map_dimensions, is_fullscreen=Constants.IS_FULLSCREEN,
                 windowed_screen_width=Constants.WINDOWED_SCREEN_WIDTH,
                 windowed_screen_height=Constants.WINDOWED_SCREEN_HEIGHT):

        self.initial_map_render = True

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
        self._init_boundsurfs()
        self._init_gamescreen(map_dimensions)
        self._init_guisurfs()
        self._init_gui_icons()
        self._init_teleport_covers()

        # Init element lists
        self._init_boundsurf_list()
        self._init_gui_list()
        self._init_teleport_covers_list()

    def set_map_dimensions(self, map_dimensions):
        self.map_dimensions = map_dimensions  # cells
        self.map_size = [map_dimensions[0] * Constants.SECTOR_SIZE, map_dimensions[1] * Constants.SECTOR_SIZE, ]  # px

        # Because map dimensions have changed, we have to update our gamescreen surf, cell size and
        # update all elements dependant on latter
        self._init_gamescreen(map_dimensions)
        self._init_boundsurf_list()
        self._init_guisurfs()
        self._init_gui_icons()
        self._init_gui_list()
        self._init_teleport_covers()
        self._init_teleport_covers_list()

    def _init_boundsurfs(self):
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
        self.gamescreen_boundbox_surf.fill((0, 255, 0))

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
        """Rescale gamescreen if it's bigger than gamescreen bounds"""
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

    def _init_guisurfs(self):
        self.top_bar_width = Constants.TOP_BAR_WIDTH_RATIO * self.canvas_width
        self.top_bar_height = Constants.TOP_BAR_HEIGHT_RATIO * self.canvas_height
        self.bottom_bar_width = self.gamescreen_surf_width #Constants.BOTTOM_BAR_WIDTH_RATIO * self.canvas_width
        self.bottom_bar_height = Constants.BOTTOM_BAR_HEIGHT_RATIO * self.canvas_height
        self.bottom_bar_x = self.canvas_width/2 - self.bottom_bar_width/2
        self.bottom_bar_y = self.gamescreen_surf_y + self.gamescreen_surf_height + self.gamescreen_cell_size/4

        self.lives_bar_surf_width = int(Constants.LIVES_BAR_WIDTH * self.bottom_bar_width)
        self.lives_bar_surf_height = int(self.bottom_bar_height)
        self.lives_bar_surf = pygame.Surface((self.lives_bar_surf_width, self.lives_bar_surf_height))
        self.lives_bar_surf_x = self.bottom_bar_x
        self.lives_bar_surf_y = self.bottom_bar_y
        self.lives_bar_surf.fill((203, 124, 30))

        self.abilities_bar_surf_width = int(Constants.ABILITIES_BAR_WIDTH * self.bottom_bar_width)
        self.abilities_bar_surf_height = int(self.bottom_bar_height)
        self.abilities_bar_surf = pygame.Surface((self.abilities_bar_surf_width, self.abilities_bar_surf_height))
        self.abilities_bar_surf_x = self.lives_bar_surf_x + self.lives_bar_surf_width
        self.abilities_bar_surf_y = self.bottom_bar_y
        self.abilities_bar_surf.fill((63, 67, 88))

        self.mana_bar_surf_width = int(Constants.MANA_BAR_WIDTH * self.bottom_bar_width)
        self.mana_bar_surf_height = int(self.bottom_bar_height)
        self.mana_bar_surf = pygame.Surface((self.mana_bar_surf_width, self.mana_bar_surf_height))
        self.mana_bar_surf_x = self.abilities_bar_surf_x + self.abilities_bar_surf_width
        self.mana_bar_surf_y = self.bottom_bar_y
        self.mana_bar_surf.fill((204, 65, 107))

    def _init_gui_icons(self):
        # Lives Icons
        boundrect = pygame.Rect(self.lives_bar_surf_x, self.lives_bar_surf_y,
                                self.lives_bar_surf_width, self.lives_bar_surf_height)
        self.lives_icons = LineOfIconsWidget(boundrect, box_size=self.gamescreen_cell_size)

        animations = ResourceManager.get_animations_from(Constants.LIVES_ICON_ANIMATIONS_PATH, icon_size=int(self.gamescreen_cell_size))
        self.lives_icons.append(Icon(animations))

        # Abilities Icons
        boundrect = pygame.Rect(self.abilities_bar_surf_x, self.abilities_bar_surf_y,
                                self.abilities_bar_surf_width, self.abilities_bar_surf_height)
        self.abilities_icons = LineOfIconsWidget(boundrect, box_size=int(self.gamescreen_cell_size*1.25), # TODO: CONSTANT
                                                 align=LineOfIconsWidget.Align.Center)

        animations = ResourceManager.get_animations_from(Constants.BOOST_ICON_ANIMATIONS_PATH, icon_size=int(self.gamescreen_cell_size*1.25))
        self.abilities_icons.append(Icon(animations))

        animations = ResourceManager.get_animations_from(Constants.MORPH_ICON_ANIMATIONS_PATH, icon_size=int(self.gamescreen_cell_size*1.25))
        self.abilities_icons.append(Icon(animations))

        # Mana Icons
        boundrect = pygame.Rect(self.mana_bar_surf_x, self.mana_bar_surf_y,
                                self.mana_bar_surf_width, self.mana_bar_surf_height)
        self.mana_icons = LineOfIconsWidget(boundrect, box_size=self.gamescreen_cell_size,
                                            align=LineOfIconsWidget.Align.Right,
                                            pop_append_order=LineOfIconsWidget.Order.PopLeftAppendLeft)

        animations = ResourceManager.get_animations_from(Constants.MANA_ICON_ANIMATIONS_PATH, icon_size=int(self.gamescreen_cell_size))
        self.mana_icons.append(Icon(animations))

    def _init_teleport_covers(self):
        self.left_teleport_cover_surf = pygame.Surface((self.gamescreen_surf_x, self.gamescreen_surf_height))
        self.left_teleport_cover_surf_x = 0
        self.left_teleport_cover_surf_y = self.gamescreen_surf_y
        self.left_teleport_cover_surf.fill(Constants.SCREEN_BACKGROUND_COLOR)

        self.up_teleport_cover_surf = pygame.Surface((self.gamescreen_boundbox_surf_width, self.gamescreen_surf_y))
        self.up_teleport_cover_surf_x = 0
        self.up_teleport_cover_surf_y = 0
        self.up_teleport_cover_surf.fill(Constants.SCREEN_BACKGROUND_COLOR)

        self.right_teleport_cover_surf = pygame.Surface((self.gamescreen_boundbox_surf_width -
                                                         (self.gamescreen_surf_x + self.gamescreen_surf_width),
                                                         self.gamescreen_surf_height))
        self.right_teleport_cover_surf_x = self.gamescreen_surf_x + self.gamescreen_surf_width
        self.right_teleport_cover_surf_y = self.gamescreen_surf_y
        self.right_teleport_cover_surf.fill(Constants.SCREEN_BACKGROUND_COLOR)
        self.down_teleport_cover_surf = pygame.Surface((self.gamescreen_boundbox_surf_width,
                                                        self.canvas_height -
                                                        (self.gamescreen_surf_y + self.gamescreen_surf_height)))
        self.down_teleport_cover_surf_x = 0
        self.down_teleport_cover_surf_y = self.gamescreen_surf_y + self.gamescreen_surf_height
        self.down_teleport_cover_surf.fill(Constants.SCREEN_BACKGROUND_COLOR)

    def _init_boundsurf_list(self):
        """Creates a list of filled background surfaces and their absolute positions on the canvas"""
        self.boundsurfs = []

        #self.bg_elements.append([self.background_surf, self.background_surf_x, self.background_surf_y])
        #self.boundsurfs.append([self.gamescreen_boundbox_surf, self.gamescreen_boundbox_surf_x, self.gamescreen_boundbox_surf_y])
        #self.bg_elements.append([self.gamescreen_surf, self.gamescreen_surf_x, self.gamescreen_surf_y])

    def _init_gui_list(self):
        """Creates a list of all gui elements and their absolute positions on the canvas"""
        self.guisurfs = []

        self.guisurfs.append([self.lives_bar_surf, self.lives_bar_surf_x, self.lives_bar_surf_y])
        self.guisurfs.append([self.abilities_bar_surf, self.abilities_bar_surf_x, self.abilities_bar_surf_y])
        self.guisurfs.append([self.mana_bar_surf, self.mana_bar_surf_x, self.mana_bar_surf_y])

        self.icon_lines = []
        self.icon_lines.append(self.lives_icons)
        self.icon_lines.append(self.abilities_icons)
        self.icon_lines.append(self.mana_icons)

    def _init_teleport_covers_list(self):
        """Creates a list of all teleport covers and their absolute positions on the canvas"""
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

    def _draw_text(self, pacman, current_level):
        # TODO OPTIMIZE
        font = pygame.font.Font(Constants.FRANKLIN_FONT_PATH, int(self.canvas_height*Constants.FONT_SIZE_RATIO))
        score_text = font.render("Score: " + str(pacman.score), 1, Constants.FONT_COLOR)
        place = score_text.get_rect(topleft=(self.gamescreen_surf_x, self.top_bar_height/2))
        self.window.blit(score_text, place)

        level_text = font.render("Level: " + current_level.level_name, 1, Constants.FONT_COLOR)
        place = level_text.get_rect(topleft=(self.gamescreen_surf_x + self.gamescreen_surf_width
                                             - level_text.get_rect().width,
                                             self.top_bar_height/2))
        self.window.blit(level_text, place)

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

    def _redraw_all_mapobjects(self, entities_list, show_hitboxes=False):
        pellets, mega_pellets, walls, floors, cherry, pacmans, ghosts = entities_list

        self._draw_mapobjects(walls, show_hitboxes=show_hitboxes)
        self._draw_mapobjects(floors, show_hitboxes=show_hitboxes)
        self._draw_mapobjects(pellets, show_hitboxes=show_hitboxes)
        self._draw_mapobjects(mega_pellets, show_hitboxes=show_hitboxes)
        self._draw_mapobjects(cherry, show_hitboxes=show_hitboxes)

    def restart(self):
        self.initial_map_render = True

    def render(self, entities_list: [], current_level: Level, elapsed_time: float, showgrid: bool=False, show_hitboxes: bool=True,
               render_mode: RenderModes=RenderModes.RedrawAll):
        """entities_list: (pellets, mega_pellets, walls, cherry, pacmans, ghosts)"""

        # Unpack entities_list
        pellets, mega_pellets, walls, floors, cherry, pacmans, ghosts = entities_list

        if self.initial_map_render:
            self.prev_pacmans_coords = [pacman.coord for pacman in pacmans]
            self.prev_ghosts_coords = [ghost.coord for ghost in ghosts]

        # This variable is needed for proper animation speed independent of FPS
        self.time_elapsed_from_prev_animation_frame += elapsed_time

        if render_mode == RenderModes.RedrawAll:
            self._redraw_all_mapobjects(entities_list, show_hitboxes)

        elif render_mode == RenderModes.PartialRedraw_A:
            # Draw all mapobjects if map has been just changed
            if self.initial_map_render:
                self._redraw_all_mapobjects(entities_list, show_hitboxes)
                self.initial_map_render = False

            # Else only redraw objects in given radius
            else:
                radius = 2 * Constants.SECTOR_SIZE

                def _draw_mapobjects_around_coords(coords):
                    self._draw_mapobjects(_get_near_objects(coords, floors, radius), show_hitboxes)
                    self._draw_mapobjects(_get_near_objects(coords, pellets, radius), show_hitboxes)
                    self._draw_mapobjects(_get_near_objects(coords, mega_pellets, radius), show_hitboxes)
                    self._draw_mapobjects(_get_near_objects(coords, cherry, radius), show_hitboxes)

                # Redraw all when pacman teleports (because of low/inconsistent tickrate or pacman's death)
                for pacman, prev_pacman_coord in zip(pacmans, self.prev_pacmans_coords):
                    if distance(pacman.coord, prev_pacman_coord) >= radius:
                        _draw_mapobjects_around_coords([prev_pacman_coord])

                # Redraw all when ghost teleports (because of low/inconsistent tickrate)
                for ghost, prev_ghost_coord in zip(ghosts, self.prev_ghosts_coords):
                    if distance(ghost.coord, prev_ghost_coord) >= radius:
                        _draw_mapobjects_around_coords([prev_ghost_coord])

                _draw_mapobjects_around_coords([creature.coord for creature in (pacmans + ghosts)])

        # Draw creatures
        self._draw_pacmans(pacmans, show_hitboxes=show_hitboxes)
        self._draw_ghosts(ghosts, show_hitboxes=show_hitboxes)

        # pygame.display.set_caption("Elapsed time: " + str(elapsed_time))

        # Draw covers
        for cover in self.covers:
           self.window.blit(cover[0], (cover[1], cover[2]))

        # Draw boundsurfs
        for surf in self.boundsurfs:
            self.window.blit(surf[0], (surf[1], surf[2]))

        # Draw GUI
        # TODO STORE ANIMATIONS IN RESOURCE MANAGER
        animations = ResourceManager.get_animations_from(Constants.LIVES_ICON_ANIMATIONS_PATH, icon_size=int(self.gamescreen_cell_size))
        self.lives_icons.duplicate(pacmans[0].lives, duplicated_icon=Icon(animations))

        # TODO STORE ANIMATIONS IN RESOURCE MANAGER
        animations = ResourceManager.get_animations_from(Constants.MANA_ICON_ANIMATIONS_PATH, icon_size=int(self.gamescreen_cell_size))
        self.mana_icons.duplicate(pacmans[0].mana, duplicated_icon=Icon(animations))
        self._draw_text(pacmans[0], current_level)

        # ...
        #self._init_gui_list()
        for element in self.guisurfs:
            pass
            #self.window.blit(element[0], (element[1], element[2]))

        for icon_line in self.icon_lines:
            for icon in icon_line.icons:
                self.window.blit(icon.animations[icon.current_state][icon.counter],
                                 (icon.x, icon.y))
                icon.counter += 1
        # Draw Grid
        if showgrid:
            self._draw_grid()

        if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
            self.time_elapsed_from_prev_animation_frame = 0

        if not self.initial_map_render:
            # Update prev entities list
            #self.prev_entites = entities_list.copy()
            self.prev_pacmans_coords = [pacman.coord for pacman in pacmans]
            self.prev_ghosts_coords = [ghost.coord for ghost in ghosts]

        pygame.display.update()

    def _draw_mapobjects(self, mapobjects, show_hitboxes=False):
        for obj in mapobjects:
            surface = obj.texture
            rescaled_img = pygame.transform.scale(surface, (self.gamescreen_cell_size, self.gamescreen_cell_size))
            self.window.blit(rescaled_img, self._mapscreen_coords_to_gamescreen_coords(obj.coord))

            if show_hitboxes:
                self._show_hitbox(obj)

    def _draw_pacmans(self, pacmans, show_hitboxes=False):
        for pac in pacmans:
            if pac.is_alive is True and pac.direction == "left":
                if pac.animation_count >= 4:
                    pac.animation_count = 0
                surface = pac.animations["move_left"][pac.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    pac.animation_count += 1
                    if pac.animation_count >= 4:
                        pac.animation_count = 0

            elif pac.is_alive is True and pac.direction == "up":
                if pac.animation_count >= 4:
                    pac.animation_count = 0
                surface = pac.animations["move_up"][pac.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    pac.animation_count += 1
                    if pac.animation_count >= 4:
                        pac.animation_count = 0

            elif pac.is_alive is True and pac.direction == "right":
                if pac.animation_count >= 4:
                    pac.animation_count = 0
                surface = pac.animations["move_right"][pac.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    pac.animation_count += 1
                    if pac.animation_count >= 4:
                        pac.animation_count = 0

            elif pac.is_alive is True and pac.direction == "down":
                if pac.animation_count >= 4:
                    pac.animation_count = 0
                surface = pac.animations["move_down"][pac.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    pac.animation_count += 1
                    if pac.animation_count >= 4:
                        pac.animation_count = 0

            elif pac.is_alive is False:
                if pac.animation_count >= 9:
                    pac.animation_count = 0
                surface = pac.animations["dead"][pac.animation_count]
                if self.time_elapsed_from_prev_animation_frame >= Constants.ANIMATION_PERIOD:
                    pac.animation_count += 1
                    if pac.animation_count >= 9:
                        pac.animation_count = 0
            else:
                raise Exception("Unable to identify pacman's state: " + str(pac))

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
                if ghost.direction == "up":
                    surface = ghost.animations["dead"][0]
                elif ghost.direction == "left":
                    surface = ghost.animations["dead"][1]
                elif ghost.direction == "down":
                    surface = ghost.animations["dead"][2]
                elif ghost.direction == "right":
                    surface = ghost.animations["dead"][3]

            else:
                raise Exception("Unable to identify ghost's state:", ghost)

            rescaled_img = pygame.transform.scale(surface, (self.gamescreen_cell_size, self.gamescreen_cell_size))
            self.window.blit(rescaled_img, self._mapscreen_coords_to_gamescreen_coords((ghost.x, ghost.y)))

            if show_hitboxes:
                self._show_hitbox(ghost)
