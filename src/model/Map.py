from src.model.MapObjects import Wall, Pellet, MegaPellet, Floor
from src.data.Constants import SECTOR_SIZE


class Map:
    def __init__(self, string_map):
        self.string_map = string_map
        self.width = len(string_map[0])
        self.height = len(string_map)
        self.dims = (self.width, self.height)
        self.pellets = \
            self.mega_pellets = \
            self.walls = \
            self.floors = \
            self.hash_map = \
            self.pacman_initial_coord = \
            self.ghosts_initial_coords = \
            self.linked_list = None

    def pre_process(self):
        pellets = []
        mega_pellets = []
        walls = []
        floors = []
        hash_map = {}
        linked_list = {}
        pacman_initial_coord = (0, 0)
        ghosts_initial_coords = []
        for x in range(self.width):
            for y in range(self.height):
                ch = self.string_map[y][x]
                coord = (x * SECTOR_SIZE, y * SECTOR_SIZE)
                str_coord = (x, y)
                if ch == '#':
                    obj = Wall(coord)
                    walls.append(obj)

                elif ch == '.':
                    obj = Pellet(coord)
                    pellets.append(obj)

                elif ch == 'o':
                    obj = MegaPellet(coord)
                    mega_pellets.append(obj)

                elif ch == '@':
                    obj = None
                    pacman_initial_coord = coord

                elif ch == '$':
                    obj = None
                    ghosts_initial_coords.append(coord)

                else:
                    obj = None

                if ch != '#':
                    floors.append(Floor(coord))

                hash_map[str_coord] = obj

        self.hash_map = hash_map
        self.pellets = pellets
        self.mega_pellets = mega_pellets
        self.walls = walls
        self.floors = floors
        self.hash_map = hash_map
        self.pacman_initial_coord = pacman_initial_coord
        self.ghosts_initial_coords = ghosts_initial_coords
        self.linked_list = linked_list

    def get_object_from_coord(self, x, y):
        return self.hash_map[(x, y)]

    def __str__(self):
        return '\n'.join(self.string_map)
