import base64
import json

import arcade
import arcade.gui

from army.army import Army
from config import PATH
from misc import views
from misc.misc_classes import AdvancedUiFileDialogOpen, AdvancedUiManager, LabelList
from tiles.building import CustomsOffice, DefenceOffice, Hospital, Office
from tiles.tile import Tile

MAIN_PATH = f"{PATH}/../assets/resource/"


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

        self.resource_label_list = LabelList()

        self.world = arcade.Scene()
        self.world.add_sprite_list(name="tiles", use_spatial_hash=True, sprite_list=tile_list)
        self.world.add_sprite_list(name="toolbars", use_spatial_hash=True, sprite_list=bar_list)
        self.world.add_sprite_list(name="buildings", use_spatial_hash=True, sprite_list=arcade.SpriteList())

        self.office = Office(475, 475, "office", self)
        self.world.add_sprite(name="buildings", sprite=self.office)

        self.hospital = None
        self.finance_office = None
        self.defence_office = None

        self.world.add_sprite(sprite=arcade.Sprite(f"{MAIN_PATH}food.png", 1, center_x=80, center_y=635), name="food")
        self.world.add_sprite(sprite=arcade.Sprite(f"{MAIN_PATH}gold.png", 1, center_x=230, center_y=635), name="gold")
        self.world.add_sprite(sprite=arcade.Sprite(f"{MAIN_PATH}happiness.png", 1, center_x=380, center_y=635),
                              name="happiness")
        self.world.add_sprite(sprite=arcade.Sprite(f"{MAIN_PATH}population.png", 1, center_x=570, center_y=635),
                              name="population")

        self.world.add_sprite_list(name="border", use_spatial_hash=True, sprite_list=border_list)
        self.add_labels()

        self.manager = AdvancedUiManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout(space_between=10)
        self.h_box = arcade.gui.UIBoxLayout(space_between=800, vertical=False)

        self.setup_menu()

        self.main_window = main_window
        self.main_view = main_view

        self.army = Army(self)
        self.map = views.Map(self.main_window, self.main_view)
        self.battle = views.Battle(self.main_window, self.main_view)

    def draw(self):
        self.world.draw()

        # labelling resources
        self.resource_label_list.draw()

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

        self.world.get_sprite_list("toolbars").append(
            arcade.Sprite(f"{PATH}/../assets/misc/dialog_box.png", 1, center_x=540,
                          center_y=50))
        self.world.get_sprite_list("toolbars").append(
            arcade.Sprite(f"{PATH}/../assets/misc/info_box.png", 1, center_x=940,
                          center_y=350))
        self.world.get_sprite_list("toolbars").append(
            arcade.Sprite(f"{PATH}/../assets/misc/dialog_box.png", 1, center_x=540,
                          center_y=650))

        map_button = arcade.gui.UIFlatButton(text="Map", width=100, height=25, x=980, y=25)
        map_button.on_click = self._on_click_map_button
        self.manager.add(map_button)

    def add_labels(self):
        self.resource_label_list.append(arcade.Text(
            f"Food(f): {self._food}",
            start_x=100,
            start_y=627.5,
            font_size=12
        ))

        self.resource_label_list.append(arcade.Text(
            f"Gold(g): {self._gold}",
            start_x=250,
            start_y=627.5,
            font_size=12
        ))

        self.resource_label_list.append(arcade.Text(
            f"Happiness(h): {self._happiness}",
            start_x=400,
            start_y=627.5,
            font_size=12
        ))

        self.resource_label_list.append(arcade.Text(
            f"Population(p): {self._population}",
            start_x=590,
            start_y=627.5,
            font_size=12
        ))

    def switched_view(self, file_name):
        with open(f"{PATH}/../data/{file_name}", "rb") as f:
            enc = f.read()
        decoded_data = json.loads(base64.b64decode(enc))

        self._turn_number = decoded_data.get("turn_number", 1)

        self._food = decoded_data.get("food", 0)
        self._gold = decoded_data.get("gold", 0)
        self._happiness = decoded_data.get("happiness", 0)
        self._population = decoded_data.get("population", 0)
        self._farmers = decoded_data.get("farmers", 0)
        self._soldiers = decoded_data.get("soldiers", 0)
        self._workers = decoded_data.get("workers", 0)

        self.army.swords_man = decoded_data.get("swords_man", 0)
        self.army.bow_man = decoded_data.get("bow_man", 0)
        self.army.cavalry = decoded_data.get("cavalry", 0)
        self.army.pike_man = decoded_data.get("pike_man", 0)
        self.army.canons = decoded_data.get("canons", 0)
        self.army.battles = decoded_data.get("battles", 0)
        self.army.battles_won = decoded_data.get("battles_won", 0)
        self.army.morale = decoded_data.get("morale", 100)
        # fixes a bug where the buttons weren't working

        building_sprite_list = self.world.get_sprite_list(name="buildings")
        building_sprite_list.clear()

        self.office = Office(475, 475, "office", self)
        building_sprite_list.append(self.office)

        self.world.remove_sprite_list_by_name(name="buildings")
        self.world.add_sprite_list(name="buildings", sprite_list=building_sprite_list)
        self.world.move_sprite_list_before(name="buildings", before="border")

        if decoded_data.get("hospital"):
            self.build_hospital(True)
        if decoded_data.get("finance_office"):
            self.build_finance_office(True)
        if decoded_data.get("defence_office"):
            self.build_defence_office(True)

        self._setup_map()

        self.resource_label_list.clear()
        self.add_labels()

    def build_hospital(self, ignore_condition=False) -> bool:
        if (self._gold >= 1200 and self._food >= 200) or ignore_condition:
            self.hospital = Hospital(425, 425, "hospital", self)
            self.world.add_sprite(name="buildings", sprite=self.hospital)
            if not ignore_condition:
                self._gold -= 1200
                self._food -= 200
            self.resource_label_list.clear()
            self.add_labels()
        else:
            return False
        return True

    def build_finance_office(self, ignore_condition=False) -> bool:
        if (self._gold >= 1200 and self._food >= 200) or ignore_condition:
            self.finance_office = CustomsOffice(425, 325, "finance_office", self)
            self.world.add_sprite(name="buildings", sprite=self.finance_office)
            if not ignore_condition:
                self._gold -= 1200
                self._food -= 200
            self.resource_label_list.clear()
            self.add_labels()
        else:
            print("called")
            return False
        return True

    def build_defence_office(self, ignore_condition=False) -> bool:
        if (self._gold >= 1000 and self._food >= 500) or ignore_condition:
            self.defence_office = DefenceOffice(525, 375, "defence_office", self)
            self.world.add_sprite(name="buildings", sprite=self.defence_office)
            if not ignore_condition:
                self._gold -= 1000
                self._food -= 500
            self.resource_label_list.clear()
            self.add_labels()
        else:
            return False
        return True

    def setup_menu(self):
        menu_button = arcade.gui.UIFlatButton(text="⚙", width=25, font_size=12, style={"bg_color": (0, 0, 0),
                                                                                       "font_color": (
                                                                                           255, 255, 255)},
                                              height=20)
        menu_button.on_click = self._on_click_menu_button

        next_turn_button = arcade.gui.UIFlatButton(text="Next Turn", width=150, height=25)
        next_turn_button.on_click = self._on_click_next_turn_button

        self.h_box.add(menu_button)
        self.h_box.add(next_turn_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=10,
                align_y=623,
                child=self.h_box
            )
        )

    def _on_click_next_turn_button(self, _: arcade.gui.UIOnClickEvent):
        self._turn_number += 1

        extra_gold_deduction = 0
        extra_food_deduction = 0
        if self.finance_office:
            extra_food_deduction += 20
        if self.hospital:
            extra_gold_deduction += 20
        if self.defence_office:
            extra_gold_deduction += 20
            extra_food_deduction += 20

        self._food += 3 * self._farmers - self._workers - 2 * self._soldiers - extra_food_deduction
        self._gold += - self._farmers + 3 * self._workers - 2 * self._soldiers - extra_gold_deduction

        if self._happiness <= 100:
            if self.unhappiness > 0:
                self._happiness -= self.unhappiness
            elif self.unhappiness == 0:
                self._happiness += 3
        if self._happiness > 100:
            self._happiness = 100
        if self._happiness > 80:
            self._population += (3 * self._farmers - self._workers - 2 * self._soldiers) // 10

        self.resource_label_list.clear()
        self.add_labels()

    def _on_click_map_button(self, _: arcade.gui.UIOnClickEvent):
        self.map.setup()

        self.main_window.show_view(self.map)

    def _on_click_menu_button(self, _: arcade.gui.UIOnClickEvent):
        save_button = arcade.gui.UIFlatButton(text="Save Game", width=250, font_size=24)
        save_button.on_click = self._on_click_save_button

        load_button = arcade.gui.UIFlatButton(text="Load Game", width=250, font_size=24)
        load_button.on_click = self._on_click_load_button

        back_button = arcade.gui.UIFlatButton(text="Back to Game", width=250, font_size=24)
        back_button.on_click = self._on_click_back_button

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=250, font_size=24)
        quit_button.on_click = self._on_click_quit_button

        self.v_box.add(save_button)
        self.v_box.add(load_button)
        self.v_box.add(back_button)
        self.v_box.add(quit_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="center",
                child=self.v_box
            )
        )

    def _on_click_back_button(self, _: arcade.gui.UIOnClickEvent):
        self.manager.clear()
        self.v_box.clear()
        self._setup_map()
        self.setup_menu()

    def _on_click_save_button(self, _: arcade.gui.UIOnClickEvent):
        save_data = {
            "turn_number": self._turn_number,
            "food": self._food,
            "gold": self._gold,
            "happiness": self._happiness,
            "population": self._population,
            "farmers": self._farmers,
            "soldiers": self._soldiers,
            "workers": self._workers,
            "hospital": bool(self.hospital),
            "finance_office": bool(self.finance_office),
            "defence_office": bool(self.defence_office),
            "swords_man": self.army.swords_man,
            "bow_man": self.army.bow_man,
            "cavalry": self.army.cavalry,
            "pike_man": self.army.pike_man,
            "canons": self.army.canons,
            "battles": self.army.battles,
            "battles_won": self.army.battles_won,
            "morale": self.army.morale
        }

        encoded_data = base64.b64encode(json.dumps(save_data).encode("utf-8"))
        print(f"{PATH}/../data/Turn_{self._turn_number}")
        with open(f"{PATH}/../data/Turn_{self._turn_number}", "wb") as f:
            f.write(encoded_data)

    def _setup_map(self):
        map_button = arcade.gui.UIFlatButton(text="Map", width=100, height=25, x=980, y=25)
        map_button.on_click = self._on_click_map_button
        self.manager.add(map_button)

    @staticmethod
    def _on_click_quit_button(_: arcade.gui.UIOnClickEvent):
        arcade.exit()

    def _on_click_load_button(self, _: arcade.gui.UIOnClickEvent):
        file_dialog = AdvancedUiFileDialogOpen(self.main_window, self.main_view)
        file_dialog.setup()
        self.main_window.show_view(file_dialog)

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

    @population.setter
    def population(self, number):
        self._population = number

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
        return int(self.unemployed / 100 + n)
