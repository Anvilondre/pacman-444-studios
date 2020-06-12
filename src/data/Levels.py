from src.model.Map import Map
from abc import ABC, abstractmethod


class Level(ABC):

    @property
    @abstractmethod
    def level_map(self):
        pass

    @property
    @abstractmethod
    def pacman_velocity(self):
        pass

    @property
    @abstractmethod
    def pacman_boost(self):
        pass

    @property
    @abstractmethod
    def pacman_cooldown(self):
        pass

    @property
    @abstractmethod
    def ghosts_velocity(self):
        pass

    @property
    @abstractmethod
    def ghosts_slowdown(self):
        pass

    @property
    @abstractmethod
    def speed_ability_duration(self):
        pass

    @property
    @abstractmethod
    def transform_ability_duration(self):
        pass


class Level1(Level):
    PACMAN_PX_PER_SECOND = 36 * 5
    PACMAN_BOOST_PX_PER_SECOND = 36 * 3.5
    GHOST_PX_PER_SECOND = 36 * 5
    pacman_velocity = 6
    pacman_boost = 20
    pacman_cooldown = 10
    speed_ability_duration = 5
    transform_ability_duration = 5
    ghosts_velocity = 6
    ghosts_slowdown = 0

    level_map = Map(["###################",
                     "#........#........#",
                     "#.##.###.#.###.##.#",
                     "#..o...........o..#",
                     "#.##.#.#####.#.##.#",
                     "#....#...#...#....#",
                     "####.###.#.###.####",
                     "####.#.......#.####",
                     "####.#.## ##.#.####",
                     ".......#  $#.......",
                     "####.#.#####.#.####",
                     "####.#.......#.####",
                     "####.#.#####.#.####",
                     "#..#.....@.....#..#",
                     "##.#.#.#####.#.#.##",
                     "#.o..#...#...#.o..#",
                     "#.######.#.######.#",
                     "#.................#",
                     "###################"])


class Level2(Level):
    PACMAN_PX_PER_SECOND = 36 * 5
    PACMAN_BOOST_PX_PER_SECOND = 36 * 3.5
    GHOST_PX_PER_SECOND = 36 * 5
    pacman_velocity = 6
    pacman_boost = 6
    pacman_cooldown = 12
    speed_ability_duration = 5
    transform_ability_duration = 5
    ghosts_velocity = 5
    ghosts_slowdown = 2

    level_map = Map(["######### #########",
                     "#........ ........#",
                     "#.##.###.#.###.##.#",
                     "#..o...........o..#",
                     "#.##.#.#####.#.##.#",
                     "#....#...#...#....#",
                     "####.###.#.###.####",
                     "####.#.......#.####",
                     "####.#.## ##.#.####",
                     ".......#$$$#.......",
                     "####.#.#####.#.####",
                     "####.#.......#.####",
                     "####.#.#####.#.####",
                     "#..#.....@.....#..#",
                     "##.#.#.#####.#.#.##",
                     "#.o..#...#...#.o..#",
                     "#.######.#.######.#",
                     "#.................#",
                     "######### #########"])

class Level3(Level):
    PACMAN_PX_PER_SECOND = 36 * 5
    PACMAN_BOOST_PX_PER_SECOND = 36 * 3.5
    GHOST_PX_PER_SECOND = 36 * 5
    pacman_velocity = 8
    pacman_boost = 3
    pacman_cooldown = 15
    speed_ability_duration = 5
    transform_ability_duration = 5
    ghosts_velocity = 7
    ghosts_slowdown = 3

    level_map = Map(["#############.#####",
                     "#........#........#",
                     "#.##.###.#.###.##.#",
                     "#..o...........o..#",
                     "#.##.#.#####.#.##.#",
                     "#....#...#...#....#",
                     "####.###.#.###.####",
                     "####.#.......#.####",
                     "####.#.## ##.#.####",
                     "#......#$$$#......#",
                     "####.#.#####.#.####",
                     "####.#.......#.####",
                     "####.#.#####.#.####",
                     "#........#........#",
                     "#.##.###.#.###.##.#",
                     "#..#.....@.....#..#",
                     "##.#.#.#####.#.#.##",
                     "#.o..#...#...#.o..#",
                     "#.######.#.######.#",
                     "#.................#",
                     "#############.#####"])
