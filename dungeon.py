import numpy

from enums import TileType
from point import Point
from tile import Tile


class Dungeon:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.rooms = []

        self.grid_shape = (height, width)
        self.tile_grid = numpy.full(shape=self.grid_shape, fill_value=Tile.empty())
        self.region_grid = numpy.full(shape=self.grid_shape, fill_value=-1, dtype=int)

    @property
    def rows(self):
        return self.height

    @property
    def columns(self):
        return self.width

    def __iter__(self):
        for j in range(self.rows):
            for i in range(self.columns):
                yield Point(i, j), self.tile_grid[j, i]

    def clear_dungeon(self):
        self.tile_grid = numpy.full(shape=self.grid_shape, fill_value=Tile.empty())
        self.region_grid = numpy.full(shape=self.grid_shape, fill_value=-1, dtype=int)

    def tile(self, point: Point,) -> Tile:
        return self.tile_grid[point.y, point.x]

    def set_tile(self, point: Point, label: TileType):
        self.tile_grid[point.y, point.x] = Tile.from_label(point, label)

    def region(self, point: Point) -> int:
        return self.region_grid[point.y, point.x]

    def set_region(self, point: Point, region: int) -> None:
        self.region_grid[point.y, point.x] = region
