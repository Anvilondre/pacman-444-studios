from src.model.Map import Map
from abc import ABC, abstractmethod


class Level(ABC):
    @property
    @abstractmethod
    def level_name(self):
        pass

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
    level_name = "1. Boringly easy"
    PACMAN_PX_PER_SECOND = 36 * 5
    PACMAN_BOOST_PX_PER_SECOND = 36 * 3.5
    GHOST_PX_PER_SECOND = 36 * 5
    pacman_velocity = 6
    pacman_boost = 20
    pacman_cooldown = 10
    speed_ability_duration = 5
    transform_ability_duration = 5
    ghosts_velocity = 6
    ghost_value = 100

    level_map = Map(["####.#########.####",
                     "#........#........#",
                     "#.##.###.#.###.##.#",
                     "#..o...........o..#",
                     "#.##.#.#####.#.##.#",
                     "#....#...#...#....#",
                     "####.###.#.###.####",
                     "####.#.......#.####",
                     "####.#.## ##.#.####",
                     ".......#$ $#.......",
                     "####.#.#####.#.####",
                     "####.#.......#.####",
                     "####.#.#####.#.####",
                     "...#.....@.....#...",
                     "##.#.#.#####.#.#.##",
                     "#.o..#...#...#.o..#",
                     "#.##.###.#.###.##.#",
                     "#.................#",
                     "####.#########.####"])


class Level2(Level):
    level_name = "2. A little harder.."
    PACMAN_PX_PER_SECOND = 36 * 6
    PACMAN_BOOST_PX_PER_SECOND = 36 * 3.5
    GHOST_PX_PER_SECOND = 36 * 6
    pacman_velocity = 6
    pacman_boost = 20
    ghost_value = 200
    pacman_cooldown = 10
    speed_ability_duration = 3
    transform_ability_duration = 3
    ghosts_velocity = 6
    ghost_value = 200

    level_map = Map(["##############.####",
                     "#........#........#",
                     "#.##.###.#.###.##.#",
                     "#..o...........o..#",
                     "#.##.#.#####.#.##.#",
                     "#....#...#...#....#",
                     "####.###.#.###.####",
                     "####.#.......#.####",
                     "####.#.## ##.#.####",
                     ".......#$ $#.......",
                     "####.#.#####.#.####",
                     "####.#.......#.####",
                     "####.#.#####.#.####",
                     "...#.....@.....#...",
                     "##.#.#.#####.#.#.##",
                     "#.o..#...#...#.o..#",
                     "#.##.###.#.###.##.#",
                     "#.................#",
                     "##############.####"])


class Level3(Level):
    level_name = "3. In the middle"
    PACMAN_PX_PER_SECOND = 36 * 6
    PACMAN_BOOST_PX_PER_SECOND = 36 * 3.5
    GHOST_PX_PER_SECOND = 36 * 6
    pacman_velocity = 6
    pacman_boost = 20
    pacman_cooldown = 10
    speed_ability_duration = 3
    transform_ability_duration = 3
    ghosts_velocity = 6
    ghost_value = 300

    level_map = Map(["###################",
                     "#........#........#",
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
                     "...#.....@.....#...",
                     "##.#.#.#####.#.#.##",
                     "#.o..#...#...#.o..#",
                     "#.##.###.#.###.##.#",
                     "#.................#",
                     "###################"])


class Level4(Level):
    level_name = "4. Trolley"
    PACMAN_PX_PER_SECOND = 36 * 7
    PACMAN_BOOST_PX_PER_SECOND = 36 * 3.5
    GHOST_PX_PER_SECOND = 36 * 7
    pacman_velocity = 100
    pacman_boost = 20
    pacman_cooldown = 10
    speed_ability_duration = 2.5
    transform_ability_duration = 2.5
    ghosts_velocity = 6
    ghost_value = 400

    level_map = Map(["###################",
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
                     "...#.....@.....#...",
                     "##.#.#.#####.#.#.##",
                     "#.o..#...#...#.o..#",
                     "#.##.###.#.###.##.#",
                     "#.................#",
                     "###################"])


class Level5(Level):
    level_name = "5. Final boss!"
    PACMAN_PX_PER_SECOND = 36 * 7
    PACMAN_BOOST_PX_PER_SECOND = 36 * 3.5
    GHOST_PX_PER_SECOND = 36 * 7
    pacman_velocity = 6
    pacman_boost = 20
    pacman_cooldown = 10
    speed_ability_duration = 2
    transform_ability_duration = 2
    ghosts_velocity = 6
    ghost_value = 500

    level_map = Map(["###################",
                     "#........#........#",
                     "#.##.###.#.###.##.#",
                     "#..o...........o..#",
                     "#.##.#.#####.#.##.#",
                     "#....#...#...#....#",
                     "####.###.#.###.####",
                     "####.#.......#.####",
                     "####.#.##$##.#.####",
                     "#......#$$$#......#",
                     "####.#.#####.#.####",
                     "####.#.......#.####",
                     "####.#.#####.#.####",
                     "#..#.....@.....#..#",
                     "##.#.#.#####.#.#.##",
                     "#.o..#...#...#.o..#",
                     "#.##.###.#.###.##.#",
                     "#.................#",
                     "###################"])
