from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scatterlayout import ScatterLayout

from enums import Neighbors
from generator import DungeonGenerator

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MIN_ROOM_SIZE = 5
MAX_ROOM_SIZE = 11
DATA_PATH = "data"
TILE_SIZE = 6
LEVEL_SIZE = 100
ROOM_MARGIN = 1

COLORS = {
    "WALL": (0.39, 0.8, 0.39, 1),
    "FLOOR": (0.5, 0.5, 0.5, 1),
    "DOOR": (1, 0.5, 0.5, 1),
    "EMPTY": (1, 1, 1, 1),
}


class GeneratorScreen(BoxLayout):
    def draw_dungeon(self, dungeon):
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


class DungeonMap(ScatterLayout):
    # map_label = MapLabel()
    map_width = NumericProperty(0)
    map_height = NumericProperty(0)

    def __init__(self, **kwargs):
        super(DungeonMap, self).__init__(**kwargs)
        self.map_settings = {
            "map_height": LEVEL_SIZE,
            "map_width": LEVEL_SIZE + 1,
            "min_room_size": MIN_ROOM_SIZE,
            "max_room_size": MAX_ROOM_SIZE,
            "room_margin": ROOM_MARGIN
        }
        self.generator = DungeonGenerator(self.map_settings["map_height"], self.map_settings["map_width"])
        self.map_width = self.map_settings["map_width"]
        self.map_height = self.map_settings["map_height"]

    def build_dungeon(
        self, map_height, map_width, min_room_size, max_room_size, room_margin=1
    ):
        generator = DungeonGenerator(map_height, map_width)
        generator.place_random_rooms(min_room_size, max_room_size, margin=room_margin)

        self.generator = generator
        self.map_width = self.generator.width
        self.map_height = self.generator.height

    def clear_dungeon(self):
        print("clear dungeon")
        # print(f"{self.children}")
        child = self.children[0]
        child.canvas.before.clear()
        child.canvas.clear()
        child.canvas.after.clear()
        # child.canvas.ask_update()

        self.generator.clear_map()

    def generate_map(self, buttons: InputArea = None):
        # initialize map settings
        map_height = LEVEL_SIZE
        map_width = LEVEL_SIZE + 1
        min_room_size = MIN_ROOM_SIZE
        max_room_size = MAX_ROOM_SIZE
        room_margin = ROOM_MARGIN

        # checks for int values in input boxes
        try:
            map_height = int(buttons.map_height_input.text)
            map_width = int(buttons.map_width_input.text)
            min_room_size = int(buttons.min_room_size_input.text)
            max_room_size = int(buttons.max_room_size_input.text)
            room_margin = int(buttons.room_margin_input.text)
        except ValueError:
            pass

        self.clear_dungeon()
        self.build_dungeon(
            map_height=map_height,
            map_width=map_width,
            min_room_size=min_room_size,
            max_room_size=max_room_size,
            room_margin=room_margin,
        )
        self.display_dungeon()

    def display_dungeon(self):
        map_label = self.children[0]
        for row, col, tile in self.generator:
            # r, g, b, a = COLORS[tile.label]
            r, g, b, a = tile.label()
            with map_label.canvas:
                # draw background square to create grid illusion
                # Color(0, 0, 0, 1)
                # Rectangle(pos=(row*TILE_SIZE, col*TILE_SIZE), size=(TILE_SIZE, TILE_SIZE))
                # draw tile on top
                Color(r, g, b, a)
                Rectangle(
                    pos=(row * TILE_SIZE - 1, col * TILE_SIZE - 1),
                    size=(TILE_SIZE - 1, TILE_SIZE - 1),
                )


class TileButton(Button):
    tile_color = ObjectProperty([1, 1, 1, 1])


class DungeonGeneratorApp(App):

    dungeon_map = DungeonMap()
    input_area = InputArea()
    screen = None

    def display_dungeon(self, dungeon_map=None):
        map_label = MapLabel()
        with map_label.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=(0, 0), size=self.parent.size)
        for row, col, tile in self.dungeon_map.generator:
            # r, g, b, a = COLORS[tile.label]
            r, g, b, a = tile.label()
            with map_label.canvas.after:
                # draw background square to create grid illusion
                # Color(0, 0, 0, 1)
                # Rectangle(pos=(row*TILE_SIZE, col*TILE_SIZE), size=(TILE_SIZE, TILE_SIZE))
                # draw tile on top
                Color(r, g, b, a)
                Rectangle(
                    pos=(row * TILE_SIZE - 1, col * TILE_SIZE - 1),
                    size=(TILE_SIZE - 1, TILE_SIZE - 1),
                )

        self.dungeon_map.map_label = map_label
        self.dungeon_map.add_widget(map_label)

    def clear_map(self, *args):
        self.dungeon_map.clear_dungeon()

    def generate_map(self, *args):
        print(f"generate map {self.dungeon_map.height}")
        self.clear_map()
        self.dungeon_map.build_dungeon(
            map_height=self.button_bar.map_height_input,
            map_width=self.button_bar.map_width_input,
            min_room_size=self.button_bar.min_room_size_input,
            max_room_size=self.button_bar.max_room_size_input,
        )
        self.display_dungeon()

    def build(self):
        # button_bar = ButtonBar()
        # dungeon_map = DungeonMap()
        # self.button_bar = button_bar
        # self.dungeon_map = DungeonMap()
        # self.dungeon_map.build_dungeon(map_height=LEVEL_SIZE,
        #                                map_width=LEVEL_SIZE + 1,
        #                                min_room_size=MIN_ROOM_SIZE,
        #                                max_room_size=MAX_ROOM_SIZE)

        # for row, col, tile in self.dungeon_map.dungeon:
        #     r, g, b, a = COLORS[tile.label]
        #     with self.dungeon_map.map_label.canvas.before:
        #         # draw background square to create grid illusion
        #         Color(0, 0, 0, 1)
        #         Rectangle(pos=(row*TILE_SIZE, col*TILE_SIZE), size=(TILE_SIZE, TILE_SIZE))
        #         # draw tile on top
        #         Color(r, g, b, a)
        #         Rectangle(pos=(row*TILE_SIZE-1, col*TILE_SIZE-1), size=(TILE_SIZE-1, TILE_SIZE-1))

        # self.dungeon_map.add_widget(self.dungeon_map.map_label)

        # button = Button()
        # button.text = "Generate New Map"
        # button.bind(on_press=self.generate_map)
        # self.dungeon_map.add_widget(button)
        #
        # button2 = Button()
        # button2.text = "Clear Map"
        # button2.bind(on_press=self.clear_map)
        # self.dungeon_map.add_widget(button2)

        # self.screen.add_widget(self.dungeon_map)
        # self.screen.add_widget(self.button_bar)

        # self.display_dungeon()
        self.screen = GeneratorScreen()
        return self.screen


"""
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dungeon Generator")

    '''
    d = dungeonGenerator.dungeonGenerator(levelSize, levelSize)
    d.placeRandomRooms(5, 11, 2, 4, 500)
    d.generateCorridors()
    d.connectAllRooms(30)
    d.pruneDeadends(20)
    d.placeWalls()
    '''

    d = DungeonGenerator(LEVEL_SIZE, LEVEL_SIZE + 1)
    d.place_random_rooms(3, 7)

    dungeon_surface = draw_dungeon1(d)
    dungeon_surface.convert(dungeon_surface)
    screen.blit(dungeon_surface, (10, 10))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_q
            ):
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                d.clear_map()
                d.place_random_rooms(5, 11, 2, 1, 500)

        dungeon_surface = draw_dungeon1(d)
        dungeon_surface.convert(dungeon_surface)

        screen.blit(dungeon_surface, (10, 10))
        pygame.display.flip()
"""

if __name__ == "__main__":
    # pygame.init()
    # main()
    DungeonGeneratorApp().run()
