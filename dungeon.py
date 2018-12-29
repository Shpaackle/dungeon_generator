import numpy

from enums import TileType
from point import Point
from tile import Tile


class Dungeon:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.rooms = []
        # self.current_region = -1

        self.grid_shape = (height, width)
        self.tile_grid = numpy.full(shape=self.grid_shape, fill_value=Tile.empty())
        self.region_grid = numpy.full(shape=self.grid_shape, fill_value=-1, dtype=int)

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield Point(x, y), self.tile_grid[y, x]

    def carve(self, pos: Point, label: TileType = None):
        if label is None:
            label = TileType.FLOOR

        self.tile_grid[pos.in_grid()] = label
        self.region_grid[pos.in_grid()] = self.current_region

    def new_region(self, pos: Point):
        current = self.current_region
        self.region_grid[pos.in_grid()] = current

    @property
    def current_region(self) -> int:
        return self.region_grid.max()

    def clear_dungeon(self):
        self.tile_grid = numpy.full(shape=self.grid_shape, fill_value=Tile.empty())
        self.region_grid = numpy.full(shape=self.grid_shape, fill_value=-1, dtype=int)