import base64
import json

import arcade

from config import PATH
from misc.misc_classes import AdvancedUiFileDialogOpen, AdvancedUiManager, LabelList
from tiles.building import Office
from tiles.tile import Tile

MAIN_PATH = f"{PATH}/../../assets/resource/"


class Kingdom:
    def __init__(self, tile_list, border_list, bar_list, main_window, main_view):

        self._food = 750
        self._gold = 1000
        self._happiness = 100
        self._population = 500

        self._farmers = 0
        self._soldiers = 0
        self._workers = 0

        self._turn_number = 1

        self.label_list = LabelList()

        self.world = arcade.Scene()
        self.world.add_sprite_list(name="tiles", use_spatial_hash=True, sprite_list=tile_list)
        self.world.add_sprite_list(name="toolbars", use_spatial_hash=True, sprite_list=bar_list)

        self.office = Office(475, 475, "office", self)
        self.world.add_sprite(name="office", sprite=self.office)

        self.world.add_sprite(sprite=arcade.Sprite(f"{MAIN_PATH}food.png", 1, center_x=80, center_y=635), name="food")
        self.world.add_sprite(sprite=arcade.Sprite(f"{MAIN_PATH}gold.png", 1, center_x=305, center_y=635), name="gold")
        self.world.add_sprite(sprite=arcade.Sprite(f"{MAIN_PATH}happiness.png", 1, center_x=530, center_y=635),
                              name="happiness")
        self.world.add_sprite(sprite=arcade.Sprite(f"{MAIN_PATH}population.png", 1, center_x=805, center_y=635),
                              name="population")

        self.world.add_sprite_list(name="border", use_spatial_hash=True, sprite_list=border_list)
        self.add_labels()

        self.manager = AdvancedUiManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        self.setup_menu()

        self.main_window = main_window
        self.main_view = main_view

    def draw(self):
        self.world.draw()

        # labelling resources
        self.label_list.draw()

        # menu
        self.manager.draw()

    def setup_terrain(self):
        co_ord_list = []
        for x in range(25, 800, 50):
            for y in range(125, 600, 50):
                co_ord_list.append((x, y))

        for x in range(725, 800, 50):
            for y in range(125, 600, 50):
                tile = Tile(x, y, "desert")
                self.world.get_sprite_list("tiles").append(tile)
                self.world.get_sprite_list('border').append(tile.border_tile)
                co_ord_list.remove((x, y))

        x_factor = 0
        for i in range(10, 1, -2):
            for y in range(1 + (10 - i) // 2, 11 - (10 - i) // 2):
                tile = Tile(25 + (x_factor * 50), 75 + (y * 50), "forest")
                self.world.get_sprite_list("tiles").append(tile)
                self.world.get_sprite_list('border').append(tile.border_tile)
                co_ord_list.remove((25 + (x_factor * 50), 75 + (y * 50)))
            x_factor += 1

        for x in range(625, 700, 50):
            if x == 675:
                for i in range(3):
                    tile = Tile(x, 75 + 50 * (10 - i), "desert")
                    self.world.get_sprite_list("tiles").append(tile)
                    self.world.get_sprite_list('border').append(tile.border_tile)
                    tile = Tile(x, 125 + (50 * i), "desert")
                    self.world.get_sprite_list("tiles").append(tile)
                    self.world.get_sprite_list('border').append(tile.border_tile)
                    co_ord_list.remove((x, 125 + (50 * i)))
                    co_ord_list.remove((x, 75 + 50 * (10 - i)))
            else:
                tile = Tile(x, 125, "desert")
                self.world.get_sprite_list("tiles").append(tile)
                self.world.get_sprite_list('border').append(tile.border_tile)
                tile = Tile(x, 575, "desert")
                self.world.get_sprite_list("tiles").append(tile)
                self.world.get_sprite_list('border').append(tile.border_tile)
                co_ord_list.remove((x, 575))
                co_ord_list.remove((x, 125))

        for x in range(1, 6):
            for y in range(10 - x, 10):
                tile = Tile(25 + 50 * x, 125 + 50 * y, "land")
                self.world.get_sprite_list("tiles").append(tile)
                self.world.get_sprite_list('border').append(tile.border_tile)
                co_ord_list.remove((25 + 50 * x, 125 + 50 * y))

        y_factor = 0
        for x in range(1, 6):
            y_factor += 1
            for y in range(y_factor):
                tile = Tile(25 + 50 * x, 125 + 50 * y, "land")
                self.world.get_sprite_list("tiles").append(tile)
                self.world.get_sprite_list('border').append(tile.border_tile)
                co_ord_list.remove((25 + 50 * x, 125 + 50 * y))

        for x in range(325, 650, 50):
            for y in range(275, 400, 50):
                if x != 325 or y != 275:
                    tile = Tile(x, y, "grass")
                    self.world.get_sprite_list("tiles").append(tile)
                    self.world.get_sprite_list('border').append(tile.border_tile)
                    co_ord_list.remove((x, y))

        for x in range(325, 550, 50):
            if x == 325 or x == 525:
                for i in range(2):
                    tile = Tile(x, 575 - 50 * i, "river")
                    self.world.get_sprite_list("tiles").append(tile)
                    self.world.get_sprite_list('border').append(tile.border_tile)
                    co_ord_list.remove((x, 575 - 50 * i))
            else:
                tile = Tile(x, 575, "river")
                self.world.get_sprite_list("tiles").append(tile)
                self.world.get_sprite_list('border').append(tile.border_tile)
                co_ord_list.remove((x, 575))

        for x in range(325, 550, 50):
            tile = Tile(x, 425, "grass")
            self.world.get_sprite_list("tiles").append(tile)
            self.world.get_sprite_list('border').append(tile.border_tile)
            co_ord_list.remove((x, 425))

        for x in range(425, 550, 50):
            for y in range(175, 250, 50):
                if x != 425 or y != 175:
                    tile = Tile(x, y, "grass")
                    self.world.get_sprite_list("tiles").append(tile)
                    self.world.get_sprite_list('border').append(tile.border_tile)
                    co_ord_list.remove((x, y))

        for x in range(325, 500, 50):
            for y in range(475, 550, 50):
                if x != 325 or y != 525:
                    if x != 475 or y != 475:
                        tile = Tile(x, y, "mountain")
                        self.world.get_sprite_list("tiles").append(tile)
                        self.world.get_sprite_list('border').append(tile.border_tile)
                    else:
                        tile = Tile(x, y, "grass")
                        self.world.get_sprite_list("tiles").append(tile)
                        self.world.get_sprite_list('border').append(tile.border_tile)
                        tile = Tile(x + 50, y, "grass")
                        self.world.get_sprite_list("tiles").append(tile)
                        self.world.get_sprite_list('border').append(tile.border_tile)
                        co_ord_list.remove((x + 50, y))
                    co_ord_list.remove((x, y))

        for co_ord in co_ord_list:
            tile = Tile(co_ord[0], co_ord[1], "land")
            self.world.get_sprite_list("tiles").append(tile)
            self.world.get_sprite_list('border').append(tile.border_tile)

        co_ord_list.clear()

        self.world.get_sprite_list("toolbars").append(arcade.Sprite(f"{PATH}/../../assets/misc/dialog_box.png", 1, center_x=540,
                                                                    center_y=50))
        self.world.get_sprite_list("toolbars").append(arcade.Sprite(f"{PATH}/../../assets/misc/info_box.png", 1, center_x=940,
                                                                    center_y=350))
        self.world.get_sprite_list("toolbars").append(arcade.Sprite(f"{PATH}/../../assets/misc/dialog_box.png", 1, center_x=540,
                                                                    center_y=650))

    def add_labels(self):
        self.label_list.append(arcade.Text(
            f"Food(f): {self._food}",
            start_x=100,
            start_y=627.5,
            font_size=16
        ))

        self.label_list.append(arcade.Text(
            f"Gold(g): {self._gold}",
            start_x=325,
            start_y=627.5,
            font_size=16
        ))

        self.label_list.append(arcade.Text(
            f"Happiness(h): {self._happiness}",
            start_x=550,
            start_y=627.5,
            font_size=16
        ))

        self.label_list.append(arcade.Text(
            f"Population(p): {self._population}",
            start_x=825,
            start_y=627.5,
            font_size=16
        ))

    def setup_menu(self):
        menu_button = arcade.gui.UIFlatButton(text="⚙", width=25, font_size=16, style={"bg_color": (127, 201, 255)}, height=20)
        menu_button.on_click = self._on_click_menu_button
        self.v_box.add(menu_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=10,
                align_y=627.5,
                child=self.v_box
            )
        )

    def _on_click_menu_button(self, event: arcade.gui.UIOnClickEvent):

        save_button = arcade.gui.UIFlatButton(text="Save Game", width=250, font_size=24)
        save_button.on_click = self._on_click_save_button

        load_button = arcade.gui.UIFlatButton(text="Load Game", width=250, font_size=24)
        load_button.on_click = self._on_click_load_button

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=250, font_size=24)
        quit_button.on_click = self._on_click_quit_button

        self.v_box.add(save_button)
        self.v_box.add(load_button)
        self.v_box.add(quit_button)
        

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="center",
                child=self.v_box
            )
        )

    def _on_click_save_button(self, event: arcade.gui.UIOnClickEvent):
        save_data = {
            "food": self._food,
            "gold": self._gold,
            "happiness": self._happiness,
            "population": self._population,
            "farmers": self._farmers,
            "soldiers": self._soldiers,
            "workers": self._workers,
        }
        encoded_data = base64.b64encode(json.dumps(save_data).encode("utf-8"))
        with open(f"{PATH}/../../data/Turn_{self._turn_number}", "wb") as f:
            f.write(encoded_data)

        

    def _on_click_quit_button(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()

    def _on_click_load_button(self, _: arcade.gui.UIOnClickEvent):
        file_dialog = AdvancedUiFileDialogOpen(self.main_window, self.main_view)
        file_dialog.setup()
        self.main_window.show_view(file_dialog)
        print("first")

    def switched_view(self, file_name):
        with open(f"{PATH}/../../data/{file_name}", "rb") as f:
            enc = f.read()
        decoded_data = json.loads(base64.b64.decode(enc))
        decoded_data.get("food", 0) = self._food
        decoded_data.get("gold", 0) = self._gold
        decoded_data.get("happiness", 0) = self._happiness
        decoded_data.get("population", 0) = self._population
        decoded_data.get("farmers", 0) = self._farmers
        decoded_data.get("soldiers",0) = self._soldiers
        decoded_data.get("workers",0) = self._workers

    @property
    def farmers(self):
        return self._farmers

    @property
    def workers(self):
        return self._workers

    @property
    def soldiers(self):
        return self._soldiers

    @farmers.setter
    def farmers(self, number):
        self._farmers = number

    @workers.setter
    def workers(self, number):
        self._workers = number

    @soldiers.setter
    def soldiers(self, number):
        self._soldiers = number

    @property
    def population(self):
        return self._population

    @property
    def unemployed(self):
        return self.population - self.farmers - self.workers - self.soldiers

    @property
    def unhappiness(self):
        n = 0
        if self._food != abs(self._food):
            n += abs(self._food) / 10
        if self._gold != abs(self._gold):
            n += abs(self._gold) / 10
        return self.unemployed / 100 + n

