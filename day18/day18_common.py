from enum import Enum
from coord import Coord


class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'
    UNKNOWN = 'X'


class Edge:
    def __init__(self, start: Coord, end: Coord):
        self.start = start
        self.end = end
        self.isVertical = start.x == end.x

    def __str__(self):
        return f"({self.start}, {self.end}, {'V' if self.isVertical else 'H'})"


class Corner:
    def __init__(self, coord: Coord, tail: Direction, head: Direction):
        self.coord = coord
        self.x = coord.x
        self.y = coord.y
        self.tail = tail
        self.head = head

    def __str__(self):
        return f"({self.coord}, {self.tail.value}, {self.head.value})"
