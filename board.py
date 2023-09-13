from coordinate import Coordinate
from direction import Direction

L = Direction(Coordinate(-1, 0), 'l')
R = Direction(Coordinate(1, 0), 'r')
U = Direction(Coordinate(0, -1), 'u')
D = Direction(Coordinate(0, 1), 'd')
directions = [U, D, L, R]

class Board:
    def __init__(self, dir_list):
        self.dir_list = dir_list  # List of directions for solution
        self.walls = set()
        self.goals = set()
        self.diamonds = set()
        self.fdiamonds = frozenset()  # Since set() is not hashable
        self.player = None

    def __eq__(self, other):
        # Check if diamonds are a subset of other.diamonds and player positions match
        if self.diamonds.issubset(other.diamonds) and self.player == other.player:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.fdiamonds, self.player))

    def add_wall(self, x, y):
        self.walls.add(Coordinate(x, y))

    def add_goal(self, x, y):
        self.goals.add(Coordinate(x, y))

    def add_diamond(self, x, y):
        self.diamonds.add(Coordinate(x, y))

    def set_player(self, x, y):
        self.player = Coordinate(x, y)

    def moves_available(self):
        available_moves = []
        for direction in directions:
            if self.player + direction.coordinate not in self.walls:
                if self.player + direction.coordinate in self.diamonds:
                    if self.player + direction.coordinate.double() not in self.diamonds.union(self.walls):
                        available_moves.append(direction)
                else:
                    available_moves.append(direction)
        return available_moves

    def move(self, direction):
        new_position = self.player + direction.coordinate
        if new_position in self.diamonds:
            self.diamonds.remove(new_position)
            self.diamonds.add(new_position + direction.coordinate)
        self.player = new_position
        self.dir_list.append(direction)

    def is_win(self):
        if self.goals.issubset(self.diamonds):
            return True
        else:
            return False

    def getDirections(self):
        direction_chars = ''
        for direction in self.dir_list:
            direction_chars += direction.char
            direction_chars += ', '
        return direction_chars
