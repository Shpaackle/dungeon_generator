from collections import OrderedDict
from random import randrange, randint

from dungeon import Dungeon
from enums import Neighbors, TileType
from point import Point
from tile import Tile


class Room:
    """

    """

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.region: int = None
        self.connections = []

    def __iter__(self):
        for i in range(self.height):
            for j in range(self.width):
                yield Point(x=self.x + j, y=self.y + i)

    def collides_with(self, other_room):
        for point in other_room:
            if point in self:
                return True

        return False


class DungeonGenerator:
    def __init__(self, height: int, width: int):
        self.height = abs(height)
        self.width = abs(width)
        self.dungeon = Dungeon(height, width)
        self.grid = [
            [Tile.empty(Point(x, y)) for y in range(self.height)] for x in range(self.width)
        ]

        self.rooms = []
        self.regions = OrderedDict({"count": 0})

    def __iter__(self):
        for j in range(self.height):
            for i in range(self.width):
                yield i, j, self.grid[i][j]

    def tile(self, x: int, y: int) -> Tile:
        tile = self.grid[x][y]
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
        room = Room(start_x, start_y, room_width, room_height)
        if self.room_fits(room, margin) or ignore_overlap:
            room.region = "Room" + str(len(self.rooms))
            for point in room:
                self.grid[point.x][point.y] = Tile.floor(point)
                self.regions[point] = room.region
            self.rooms.append(room)

    def place_random_rooms(
        self,
        min_room_size: int,
        max_room_size: int,
        room_step: int = 1,
        margin: int = 1,
        attempts: int = 500,
    ):
        for _ in range(attempts):
            room_width = randrange(min_room_size, max_room_size, room_step)
            room_height = randrange(min_room_size, max_room_size, room_step)
            start_x = randint(0, self.width)
            start_y = randint(0, self.height)
            self.place_room(start_x, start_y, room_width, room_height, margin)

    def room_fits(self, room: Room, margin: int) -> bool:
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
                if tile.label is not TileType.EMPTY:
                    return False

            return True
        return False

    def find_neighbors(self, point, neighbors=Neighbors.every()):
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

    def find_neighbors_direct(self, point):
        return self.find_neighbors(point, neighbors=Neighbors.cardinal())

    def clear_map(self):
        self.grid = [
            [Tile.empty(Point(x, y)) for y in range(self.height)] for x in range(self.width)
        ]

        self.rooms = []
