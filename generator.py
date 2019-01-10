from collections import OrderedDict
from typing import List

import numpy as np
from random import randrange, randint

from dungeon import Dungeon
from enums import Direction, TileType
from point import Point
from tile import Tile


class Room:
    """
    Args:
        x- and y-coordinate of the top left corner of the room
        width and height of the room

    Attributes:
        x, y: top left coordinate in the 2d array
        width: number of tiles the room spans
        height: number of tiles the room spans
        region: number corresponding to region, used for connecting locations
        connections: list of regions room is connected to
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.region: int = None
        self.connections: list = []

    def __iter__(self):
        for i in range(self.height):
            for j in range(self.width):
                yield Point(x=self.x + j, y=self.y + i)

    @property
    def top_left(self) -> Point:
        return Point(self.x, self.y)

    @property
    def top_right(self) -> Point:
        return Point(self.x + self.width - 1, self.y)

    @property
    def bottom_left(self) -> Point:
        return Point(self.x, self.y + self.height - 1)

    @property
    def bottom_right(self) -> Point:
        return Point(self.x + self.width - 1, self.y + self.height - 1)

    @property
    def right(self) -> int:
        return self.x + self.width - 1

    @property
    def bottom(self) -> int:
        return self.y + self.height - 1


class DungeonGenerator:
    def __init__(self, map_settings: dict):
        self.height = abs(map_settings["map_height"])
        self.width = abs(map_settings["map_width"])
        self.dungeon = Dungeon(self.height, self.width)

        self.current_region: int = -1

        self.rooms = []
        self.regions = OrderedDict({"count": 0})

        self.map_settings = OrderedDict(map_settings)
        self.winding_percent = 40

    def __iter__(self):
        # for j in range(self.height):
        #     for i in range(self.width):
        #         yield i, j, self.grid[i][j]
        for x, y, tile in self.dungeon.tile_grid:
            yield x, y, tile

    def new_region(self) -> int:
        self.current_region += 1
        return self.current_region

    def display(self):
        """
        iterator that begins at bottom left of the dungeon to display properly
        :rtype: List[int, int, Point]
        """
        for i in range(self.height - 1, 0, -1):
            for j in range(self.width):
                # yield i, j - 1, self.grid[i][j - 1]
                yield j, i, self.dungeon.tile(Point(j, i))

        """
            def __iter__(self):
        for i in range(self.height):
            for j in range(self.width):
                yield Point(x=self.x + j, y=self.y + i)
        """

    def initialize_map(self):
        for y in range(self.dungeon.rows):
            for x in range(self.dungeon.columns):
                self.dungeon.set_tile(Point(x, y), TileType.WALL)

    def tile(self, x: int, y: int) -> Tile:
        """

        :param x: x-coordinate of tile
        :type x: int
        :param y: y-coordinate of tile
        :type y: int
        :return: Tile at coordinate (x, y)
        :rtype: Tile
        """
        tile = self.dungeon.tile(Point(x, y))
        return tile

    def regenerate_map(self):
        print(f"regenerate map {self.height}")

    def place_room(
        self,
        start_x: int,
        start_y: int,
        room_width: int,
        room_height: int,
        margin: int,
        ignore_overlap: bool = False,
    ):
        """

        :param start_x: 
        :type start_x: int
        :param start_y: 
        :type start_y: int
        :param room_width: 
        :type room_width: int
        :param room_height: 
        :type room_height: int
        :param margin: 
        :type margin: int
        :param ignore_overlap: 
        :type ignore_overlap: bool
        """
        room = Room(start_x, start_y, room_width, room_height)
        if self.room_fits(room, margin) or ignore_overlap:
            room.region = self.new_region
            for point in room:
                # print(point)
                self.dungeon.set_tile(point, TileType.FLOOR)
                self.dungeon.set_region(point, self.current_region)
            self.rooms.append(room)

    def place_random_rooms(
        self,
        min_room_size: int,
        max_room_size: int,
        room_step: int = 1,
        margin: int = 1,
        attempts: int = 500,
    ):
        """

        :param min_room_size: minimum number of tiles
        :type min_room_size: int
        :param max_room_size: 
        :type max_room_size: int
        :param room_step: 
        :type room_step: int
        :param margin: 
        :type margin: int
        :param attempts: number of times 
        :type attempts: int
        """
        for _ in range(attempts):
            if len(self.rooms) >= self.map_settings["num_rooms"]:
                break
            room_width = randrange(min_room_size, max_room_size, room_step)
            room_height = randrange(min_room_size, max_room_size, room_step)
            start_x = randint(0, self.width)
            start_y = randint(0, self.height)
            self.place_room(start_x, start_y, room_width, room_height, margin)

    def room_fits(self, room: Room, margin: int) -> bool:
        """

        :param room: 
        :type room: Room
        :param margin: 
        :type margin: int
        :return: 
        :rtype: bool
        """
        mar_room = Room(
            (room.x - margin),
            (room.y - margin),
            (room.width + margin * 2),
            (room.height + margin * 2),
        )

        if (
            mar_room.x + mar_room.width < self.width
            and mar_room.y + mar_room.height < self.height
            and mar_room.x >= 0
            and mar_room.y >= 0
        ):
            for x, y in mar_room:
                tile = self.tile(x, y)
                if tile.label is not TileType.WALL:
                    return False

            return True
        return False

    def grow_maze(self, start: Point, label: TileType = None):
        """

        :param start:
        :type start: Point
        :param label:
        :type label: TileType
        """

        if label is None:
            label = TileType.CORRIDOR
        tiles = []
        last_direction = Point(0, 0)

        region = self.new_region()
        self.carve(start, region, label)

        tiles.append(start)
        while len(tiles) > 0:
            tile = tiles.pop(-1)  # grab last tile

            # see which neighboring tiles can be carved
            open_tiles = []
            for d in Direction.cardinal():
                if self.can_carve(tile, d):
                    print("True")
                    open_tiles.append(d)
                else:
                    print("False")

            if len(open_tiles) > 0:

                current_direction = None
                if (
                    last_direction in open_tiles
                    and randint(1, 101) > self.winding_percent
                ):
                    current_direction = last_direction
                else:
                    current_direction = open_tiles[randint(0, len(open_tiles) - 1)]

                self.carve(tile + current_direction, region, label)
                self.carve(tile + current_direction * 2, region, label)

                open_tiles.append(tile + current_direction * 2)
                last_direction = current_direction
            else:
                # end current path
                last_direction = None

    def find_neighbors(self, point: Point, neighbors: Direction = None):
        """

        :param point:
        :type point: Point
        :param neighbors:
        :type neighbors: Direction
        """
        if neighbors is None:
            neighbors = Direction.every()
        for direction in neighbors:
            new_point = point + direction
            if (
                new_point.x < 0
                or new_point.y < 0
                or new_point.x >= self.width
                or new_point.y >= self.height
            ):
                continue
            yield new_point

    def find_neighbors_direct(self, point: Point):
        return self.find_neighbors(point, neighbors=Direction.cardinal())

    def clear_map(self):
        # self.grid = [
        #     [Tile.empty(Point(x, y)) for y in range(self.height)]
        #     for x in range(self.width)
        # ]

        self.rooms = []

        self.dungeon.clear_dungeon()

    def can_carve(self, tile: Point, direction: Point) -> bool:
        # if not (0 <= tile.x + direction.x * 3 < self.width and 0 <= tile.y + direction.y * 3 < self.height):
        #     return False
        three_tiles = tile + direction * 3
        two_tiles = tile + direction * 2

        print(f"tile = {tile}, 2 tiles = {two_tiles}, 3 tiles = {three_tiles}")

        if (
            tile.x + direction.x * 3 >= self.width
            or tile.x + direction.x * 3 < 0
            or tile.y + direction.y * 3 >= self.height
            or tile.y + direction.y * 3 < 0
        ):
            print(f"{three_tiles} out of bounds")
            return False

        print(f"{self.tile(two_tiles.x, two_tiles.y)}")
        return (
            self.tile(tile.x + direction.x * 2, tile.y + direction.y * 2).label
            == TileType.WALL
        )

    def carve(self, pos: Point, region: int, label: TileType = None):
        if label is None:
            label = TileType.FLOOR

        self.dungeon.set_tile(pos, label)
        self.dungeon.set_region(pos, region)
