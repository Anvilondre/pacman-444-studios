from src.model.MapObjects import Wall


class Node:
    def __init__(self, position: (), parent: ()):
        self.position = position
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    def is_optimal(self, nodes):
        """" If node is not present in list or has lower cost """
        for node in nodes:
            if self == node and self.f >= node.f:
                return False
        else:
            return True

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return '({0},{1})'.format(self.position, self.f)


class PathFinder:

    def __init__(self, hash_map):
        self.hash_map = hash_map

    def get_direction(self, start, end):
        """" Returns direction of the first move """
        path = self.get_path(start, end)
        if path is not None:

            move = path[0]

            if move[0] > start[0]:
                return 'right'

            elif move[0] < start[0]:
                return 'left'

            elif move[1] > start[1]:
                return 'down'

            elif move[1] < start[1]:
                return 'up'

            else:
                raise Exception('Illegal move')
        else:
            return None

    def get_path(self, start, end):

        """" A* search """

        open_nodes = []
        closed_nodes = []

        start_node = Node(start, None)
        goal_node = Node(end, None)

        open_nodes.append(start_node)

        while len(open_nodes) > 0:

            open_nodes.sort()  # Sort nodes by cost

            current_node = open_nodes.pop(0)  # Node with the lowest cost

            closed_nodes.append(current_node)

            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent

                return path[::-1]  # Return reversed path

            (x, y) = current_node.position  # Current x and y
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

            for item in neighbors:

                map_value = self.hash_map.get(item)

                # Skip walls
                if isinstance(map_value, Wall):
                    continue

                neighbor = Node(item, current_node)

                # Skip closed neighbors
                if neighbor in closed_nodes:
                    continue

                ''' Calculating heuristics (L1 norm) '''

                # Distance from neighbor to goal node
                neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(
                    neighbor.position[1] - start_node.position[1])

                # Distance from neighbor to goal node
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(
                    neighbor.position[1] - goal_node.position[1])

                # Evaluate the cost
                neighbor.f = neighbor.g + neighbor.h

                # Add node to open list if it's not already present or has lower cost
                if neighbor.is_optimal(open_nodes):
                    open_nodes.append(neighbor)

        return None  # No path found
