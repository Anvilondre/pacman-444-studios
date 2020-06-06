import pygame

from src.data import Constants


class Renderer(object):
    def __init__(self, map_dimensions, is_fullscreen=Constants.IS_FULLSCREEN,
                 windowed_screen_width=Constants.WINDOWED_SCREEN_WIDTH,
                 windowed_screen_height=Constants.WINDOWED_SCREEN_HEIGHT):

        self.map_dimensions = map_dimensions

        # Set window mode
        if is_fullscreen is True:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((windowed_screen_width, windowed_screen_height))

        # Get actual window size
        self.canvas_width = pygame.display.get_surface().get_width()
        self.canvas_height = pygame.display.get_surface().get_height()

        # Init UI Surfaces
        self.background_surf = pygame.Surface((self.canvas_width, self.canvas_height))#Constants.SCREEN_BACKGROUND_IMAGE
        self.background_surf_x = 0
        self.background_surf_y = 0
        self.background_surf.fill((0, 0, 0))

        top_bar_width = Constants.TOP_BAR_WIDTH_RATIO * self.canvas_width
        top_bar_height = Constants.TOP_BAR_HEIGHT_RATIO * self.canvas_height
        self.bottom_bar_width = Constants.BOTTOM_BAR_WIDTH_RATIO * self.canvas_width
        self.bottom_bar_height = Constants.BOTTOM_BAR_HEIGHT_RATIO * self.canvas_height

        self.lives_bar_surf_width = int(Constants.LIVES_BAR_WIDTH * self.bottom_bar_width)
        self.lives_bar_surf_height =int(self.bottom_bar_height)
        self.lives_bar_surf = pygame.Surface((self.lives_bar_surf_width, self.lives_bar_surf_height))
        self.lives_bar_surf_x = Constants.BOTTOM_BAR_X_RATIO*self.canvas_width
        self.lives_bar_surf_y = Constants.BOTTOM_BAR_Y_RATIO*self.canvas_height
        self.lives_bar_surf.fill((210, 100, 0))

        self.abilities_bar_surf_width = int(Constants.ABILITIES_BAR_WIDTH * self.bottom_bar_width)
        self.abilities_bar_surf_height = int(self.bottom_bar_height)
        self.abilities_bar_surf = pygame.Surface((self.abilities_bar_surf_width, self.abilities_bar_surf_height))
        self.abilities_bar_surf_x = self.lives_bar_surf_x+self.lives_bar_surf_width
        self.abilities_bar_surf_y = self.lives_bar_surf_y
        self.abilities_bar_surf.fill((89, 10, 200))

        self.fruits_bar_surf_width = int(Constants.FRUITS_BAR_WIDTH * self.bottom_bar_width)
        self.fruits_bar_surf_height = int(self.bottom_bar_height)
        self.fruits_bar_surf = pygame.Surface((self.fruits_bar_surf_width, self.fruits_bar_surf_height))
        self.fruits_bar_surf_x = self.abilities_bar_surf_x+self.abilities_bar_surf_height
        self.fruits_bar_surf_y = self.abilities_bar_surf_y
        self.fruits_bar_surf.fill((80, 100, 120))


        self.gamescreen_boundbox_surf = pygame.Surface((int(Constants.GAMESCREEN_BOUNDBOX_SURF_WIDTH_RATIO * self.canvas_width),
                                                        int(Constants.GAMESCREEN_BOUNDBOX_SURF_HEIGHT_RATIO * self.canvas_height)))
        self.gamescreen_boundbox_surf_x = self.canvas_width/2 - self.gamescreen_boundbox_surf.get_width()/2
        self.gamescreen_boundbox_surf_y = self.canvas_height/2 - self.gamescreen_boundbox_surf.get_height()/2
        self.gamescreen_boundbox_surf.fill((80, 0, 0))

        self.gamescreen_cell_size = Constants.GAMESCREEN_CELL_SIZE_RATIO * self.canvas_width
        self.gamescreen_surf = pygame.Surface((map_dimensions[0] * self.gamescreen_cell_size,
                                               map_dimensions[1] * self.gamescreen_cell_size))
        self.gamescreen_surf_x = self.canvas_width/2 - self.gamescreen_surf.get_width()/2
        self.gamescreen_surf_y = self.canvas_height/2 - self.gamescreen_surf.get_height()/2
        self.gamescreen_surf.fill((255, 255, 0))

        # TODO RESCALE IF GAMESCREEN.RECT > BOUNDBOX.RECT
        #(map_width, map_height)

        self.ui_elements = []
        self.ui_elements.append([self.background_surf, self.background_surf_x, self.background_surf_y])
        self.ui_elements.append([self.gamescreen_boundbox_surf, self.gamescreen_boundbox_surf_x, self.gamescreen_boundbox_surf_y])
        self.ui_elements.append([self.gamescreen_surf, self.gamescreen_surf_x, self.gamescreen_surf_y])

        self.ui_elements.append([self.lives_bar_surf, self.lives_bar_surf_x, self.lives_bar_surf_y])
        self.ui_elements.append([self.abilities_bar_surf, self.abilities_bar_surf_x, self.abilities_bar_surf_y])
        self.ui_elements.append([self.fruits_bar_surf, self.fruits_bar_surf_x, self.fruits_bar_surf_y])

    def render(self, entities_list):
        pass