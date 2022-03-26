import arcade
import arcade.gui

from config import PATH
from misc.misc_classes import LabelList
from tiles.tile import Tile

MAIN_PATH = f"{PATH}/../assets/units/"
SUB_MAIN_PATH = f"{PATH}/../assets/misc/"
NUMBER_CORRESPONDENCE = {1: "swordsman.png", 2: "bowman.png", 3: "cavalry.png", 4: "pikeman.png", 5: "cannon.png"}


class Battle(arcade.View):
    def __init__(self, main_window, main_view):
        super(Battle, self).__init__()
        self.manager = None
        self.h_box = None

        self.main_view = main_view
        self.main_window = main_window
        self.army = None

        self.tile_list = None
        self.border_list = None
        self.text_list = None

        self.unit_list = None

        self.tool_bar = None
        self.assign_bar = None

        self.army_supplied_list = None

        arcade.set_background_color((127, 201, 255))

    def setup(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        self.army = self.main_view.player.army

        self.tile_list = arcade.SpriteList()
        self.border_list = arcade.SpriteList()
        self.unit_list = arcade.SpriteList()
        self.text_list = LabelList()

        self.tool_bar = arcade.Sprite(f"{SUB_MAIN_PATH}info_box_h.png", center_x=940, center_y=400)
        self.assign_bar = arcade.Sprite(f"{SUB_MAIN_PATH}dialog_box.png", center_x=540, center_y=50)

        eval(f"self.setup_battle_{self.army.battles_won}()")

    def setup_battle_0(self):
        for x in range(25, 800, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "desert")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for i, unit in enumerate(self.army_supplied_list, start=1):
            self.unit_list.append(arcade.Sprite(f"{MAIN_PATH}{NUMBER_CORRESPONDENCE.get(i)}",
                                                center_x=50 + (i * 75), center_y=40))
            self.text_list.append(arcade.Text(text=f"{unit.text} unit", start_x=50 + (i * 75),
                                              start_y=25, color=(0, 0, 0)))

    def on_draw(self):
        self.clear()

        self.tile_list.draw()
        self.border_list.draw()

        self.assign_bar.draw()
        self.unit_list.draw()
        self.text_list.draw()

        self.tool_bar.draw()
