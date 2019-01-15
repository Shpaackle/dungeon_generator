import time

from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scrollview import ScrollView

from enums import Direction, TileType
from generator import DungeonGenerator
from point import Point

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MIN_ROOM_SIZE = 5
MAX_ROOM_SIZE = 11
DATA_PATH = "data"
TILE_SIZE = 6
LEVEL_SIZE = 100
ROOM_MARGIN = 1
NUM_ROOMS = 100

COLORS = {
    "WALL": (0.39, 0.8, 0.39, 1),
    "FLOOR": (0.5, 0.5, 0.5, 1),
    "DOOR": (1, 0.5, 0.5, 1),
    "EMPTY": (1, 1, 1, 1),
    "BLUE": (0, 0, 1, 1),
    "RED": (1, 0, 0, 1),
    "YELLOW": (1, 1, 0, 1)
}


class GeneratorScreen(BoxLayout):
    pass


class MapLabel(Label):
    pass


class InputArea(BoxLayout):
    map_height_input = ObjectProperty()
    map_width_input = ObjectProperty()
    num_rooms_input = ObjectProperty()
    min_room_size_input = ObjectProperty()
    max_room_size_input = ObjectProperty()
    room_margin_input = ObjectProperty()
    num_attempts_input = ObjectProperty()
    corridors_node_input = ObjectProperty()
    extra_door_input = ObjectProperty()


class DungeonMap(ScrollView):
    # map_width = NumericProperty(0)
    # map_height = NumericProperty(0)

    def __init__(self, **kwargs):
        super(DungeonMap, self).__init__(**kwargs)
        self.map_settings = {
            "map_height": LEVEL_SIZE,
            "map_width": LEVEL_SIZE + 1,
            "min_room_size": MIN_ROOM_SIZE,
            "max_room_size": MAX_ROOM_SIZE,
            "room_margin": ROOM_MARGIN,
            "num_rooms": NUM_ROOMS,
            "tile_size": TILE_SIZE,
        }
        self.generator = DungeonGenerator(self.map_settings)

    @property
    def min_room_size(self):
        return self.map_settings["min_room_size"]

    @min_room_size.setter
    def min_room_size(self, value):
        self.map_settings["min_room_size"] = value

    @property
    def max_rooms_size(self):
        return self.map_settings["max_room_size"]

    @max_rooms_size.setter
    def max_rooms_size(self, value):
        self.map_settings["max_room_size"] = value

    @property
    def num_rooms(self):
        return self.map_settings["num_rooms"]

    @num_rooms.setter
    def num_rooms(self, value):
        self.map_settings["num_rooms"] = value

    @property
    def tile_size(self):
        return self.map_settings["tile_size"]

    @tile_size.setter
    def tile_size(self, value):
        self.map_settings["tile_size"] = value

    @property
    def map_width(self):
        return self.map_settings["map_width"]

    @map_width.setter
    def map_width(self, value):
        self.map_settings["map_width"] = value

    @property
    def map_height(self):
        return self.map_settings["map_height"]

    @map_height.setter
    def map_height(self, value):
        self.map_settings["map_height"] = value

    def create_dungeon(self):
        """
        sets all tiles in dungeon to wall tiles
        places random rooms with current map settings
        """
        self.generator.initialize_map()
        self.generator.place_random_rooms(
            min_room_size=self.map_settings["min_room_size"],
            max_room_size=self.map_settings["max_room_size"],
            margin=self.map_settings["room_margin"],
        )

    def build_dungeon(self):
        """
        sets generator to new instance of Dungeon Generator with current map setting
        Then creates a dungeon with current map settings
        """
        self.generator = DungeonGenerator(self.map_settings)
        self.create_dungeon()

    def clear_dungeon_map(self):
        """
        clears canvas of Map Label and calls clear_map in self.generator
        """
        map_label = self.children[0]
        map_label.canvas.before.clear()
        map_label.canvas.clear()
        map_label.canvas.after.clear()

        self.generator.clear_map()

    def generate_map(self):
        """
        clears dungeon map, then builds new dungeon with current map settings and displays map
        """
        self.clear_dungeon_map()
        self.build_dungeon()
        self.display_dungeon()

    def update_setting_from_input(self, setting: str, value: int):
        if setting not in self.map_settings.keys() or value < 0:
            print(f"User pressed enter in {setting} with value of {value}")
        else:
            self.map_settings[setting] = value

    def update_all_settings(
        self,
        map_height,
        map_width,
        tile_size,
        num_rooms,
        min_room_size,
        max_room_size,
        room_margin,
    ):
        self.map_settings["map_height"] = map_height
        self.map_settings["map_width"] = map_width
        self.map_settings["tile_size"] = tile_size
        self.map_settings["num_rooms"] = num_rooms
        self.map_settings["min_room_size"] = min_room_size
        self.map_settings["max_room_size"] = max_room_size
        self.map_settings["room_margin"] = room_margin

    def display_dungeon(self):
        """
        iterates through every tile in the map and draws a rectangle with color based on tile label
        """
        map_label = self.children[0]
        for row in range(self.map_height):
            for col in range(self.map_width):
                tile = self.generator.tile(col, self.map_height - row - 1)

                r, g, b, a = tile.label()
                with map_label.canvas:
                    Color(r, g, b, a)
                    Rectangle(
                        pos=(col * self.tile_size - 1, row * self.tile_size - 1),
                        size=(self.tile_size - 1, self.tile_size - 1),
                    )

        map_label.width = self.tile_size * self.map_width
        map_label.height = self.tile_size * self.map_height

    def test_dungeon(self):
        self.clear_dungeon_map()
        map_settings = {
            "map_height": 25,
            "map_width": 30,
            "min_room_size": 3,
            "max_room_size": 5,
            "room_margin": 1,
            "num_rooms": 10,
            "tile_size": 10,
        }
        self.generator = DungeonGenerator(map_settings)
        self.generator.initialize_map()
        self.generator.place_random_rooms(
            min_room_size=map_settings["min_room_size"],
            max_room_size=map_settings["max_room_size"],
        )

        self.map_settings = map_settings
        self.display_dungeon()
        time.sleep(1)
        # for y in range(1, self.generator.height, 2):
        #     for x in range(1, self.generator.width, 2):
        #         tile = self.generator.tile(x, y)
        #         if tile.label is not TileType.WALL:
        #             continue
        #         self.generator.grow_maze(Point(x, y))

        self.display_dungeon()

    def build_corridors(self):
        # for y in range(1, self.generator.height, 2):
        #     for x in range(1, self.generator.width, 2):
        #         tile = self.generator.tile(x, y)
        #         if tile.label is not TileType.WALL:
        #             r, g, b, a = tile.label()
        #             with self.children[0].canvas:
        #                 Color(r, g, b, a)
        #                 Rectangle(
        #                     pos=(tile.x * self.tile_size - 1, tile.y * self.tile_size - 1),
        #                     size=(self.tile_size - 1, self.tile_size - 1),
        #                 )
        #             # self.children[0].canvas.ask_update()
        #             # time.sleep(1)
        #             continue
        #         self.generator.grow_maze(Point(x, y))
        self.generator.build_corridors()
        self.display_dungeon()


class DungeonGeneratorApp(App):
    def build(self):
        screen = GeneratorScreen()
        return screen


if __name__ == "__main__":
    # pygame.init()
    # main()
    DungeonGeneratorApp().run()
