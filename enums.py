from enum import Enum

from point import Point


class Neighbors(Enum):
    NW = Point(-1, 1)
    N = Point(0, 1)
    NE = Point(1, 1)
    W = Point(-1, 0)
    E = Point(1, 0)
    SW = Point(-1, -1)
    S = Point(0, -1)
    SE = Point(1, -1)

    @classmethod
    def cardinal(cls):
        """
        Gets neighbors in the cardinal directions
        :return: generator object of Point for each cardinal directions
        """
        for direction in [cls.N, cls.E, cls.S, cls.W]:
            yield direction.value

    @classmethod
    def every(cls):
        every = [n for n in cls]
        for direction in cls:
            yield direction.value

    def __call__(self):
        return self.value


class TileType(Enum):
    WALL = (.39, .8, .39, 1)
    FLOOR = (.5, .5, .5, 1)
    DOOR = (1, .5, .5, 1)
    EMPTY = (1, 1, 1, 1)

    def __call__(self):
        return self.value

    def __str__(self):
        return str(self.name)
