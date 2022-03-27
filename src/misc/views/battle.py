import arcade
import arcade.gui

from army.army import Unit
from config import PATH
from misc.misc_classes import LabelList
from tiles.tile import Tile

MAIN_PATH = f"{PATH}/../assets/units/"
SUB_MAIN_PATH = f"{PATH}/../assets/misc/"
NUMBER_CORRESPONDENCE_FOR_UNITS = {1: (10, 0.33), 2: (10, 0.1), 3: (15, 0.05), 4: (10, 0.1), 5: (30, -0.05)}


class Battle(arcade.View):
    def __init__(self, main_window, main_view):
        super(Battle, self).__init__()
        self.v_box = None
        self.manager = None

        self.main_view = main_view
        self.main_window = main_window
        self.army = None

        self.tile_list = None
        self.border_list = None
        self.text_list = None

        self.unit_icon_list = None
        self.friendly_unit_list = None
        self.enemy_unit_list = None

        self.tool_bar = None
        self.assign_bar = None

        self.army_supplied_list = None
        self.unit_info = None

        arcade.set_background_color((127, 201, 255))

        self.selected_unit = None
        self.selected_friendly_unit = None
        self.selected_enemy_unit = None
        self.selected_tile_pos = None

        self.mouse_point = None

        self.loaded_textures = None
        self.loaded_sounds = None

        self.occupied_places = None

        self.music = None
        self.music_player = None

    def setup(self):
        self.music = arcade.Sound(f"{PATH}/../assets/background_music/Lord_of_the_Land _Ambient.wav")

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.occupied_places = []

        self.v_box = arcade.gui.UIBoxLayout(space_between=10)

        self.army = self.main_view.player.army

        self.tile_list = arcade.SpriteList()
        self.border_list = arcade.SpriteList()
        self.unit_icon_list = arcade.SpriteList()
        self.text_list = LabelList()
        self.friendly_unit_list = arcade.SpriteList()
        self.enemy_unit_list = arcade.SpriteList()

        self.loaded_textures = []
        self.loaded_sounds = []

        self.load_textures()
        self.load_sounds()

        self.tool_bar = arcade.Sprite(f"{SUB_MAIN_PATH}info_box_h.png", center_x=940, center_y=400)
        self.assign_bar = arcade.Sprite(f"{SUB_MAIN_PATH}dialog_box.png", center_x=540, center_y=50)
        self.text_list.append(arcade.Text(text="Unit Info:", start_x=880, start_y=663))

        self.mouse_point = arcade.Sprite(f"{SUB_MAIN_PATH}mouse_point.png")

        next_turn_button = arcade.gui.UIFlatButton(text="Next Turn", width=200, x=840, y=10, height=50)
        next_turn_button.on_click = self._on_click_next_turn_button
        self.manager.add(next_turn_button)
        eval(f"self.setup_battle_{self.army.battles_won}()")

        self.music_player = self.music.play(volume=0.1, loop=True)

    def general_setup(self):
        for i, unit in enumerate(self.army_supplied_list, start=1):
            sprite_unit = Unit(texture=self.loaded_textures[i - 1], center_x=50 + (i * 75), center_y=40, index=i - 1)
            sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[i][0]
            sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[i][1]
            self.unit_icon_list.append(sprite_unit)
            self.text_list.append(arcade.Text(text=f"{unit.text}", start_x=50 + (i * 75),
                                              start_y=25, color=(0, 0, 0)))

    def setup_battle_0(self):
        for x in range(25, 400, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "desert")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)
        for x in range(425, 800, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "forest")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in [625, 675, 725]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[10], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[1][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[1][1]
                self.enemy_unit_list.append(sprite_unit)

        self.general_setup()

    def setup_battle_1(self):
        for x in range(25, 800, 50):
            for y in range(125, 500, 50):
                tile = Tile(x, y, "grass")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)
        for x in range(25, 800, 50):
            for y in range(525, 700, 50):
                tile = Tile(x, y, "desert")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in [625, 675, 725]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[10], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[1][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[1][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [525, 575]:
            for y in [325, 375]:
                sprite_unit = Unit(texture=self.loaded_textures[14], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[5][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[5][1]
                self.enemy_unit_list.append(sprite_unit)

        self.general_setup()

    def setup_battle_2(self):
        for x in range(25, 400, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "grass")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)
        for x in range(425, 800, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "forest")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in [625, 675, 725]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[10], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[1][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[1][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [625, 675, 725]:
            for y in [325, 375]:
                sprite_unit = Unit(texture=self.loaded_textures[14], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[5][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[5][1]
                self.enemy_unit_list.append(sprite_unit)
        for x in [525, 575]:
            for y in [375, 425]:
                sprite_unit = Unit(texture=self.loaded_textures[13], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[4][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[4][1]
                self.enemy_unit_list.append(sprite_unit)

        self.general_setup()

    def setup_battle_3(self):
        for x in range(25, 800, 50):
            for y in range(125, 500, 50):
                tile = Tile(x, y, "grass")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)
        for x in range(25, 800, 50):
            for y in range(525, 700, 50):
                tile = Tile(x, y, "forest")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in [625, 675, 725]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[10], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[1][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[1][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [625, 675, 725]:
            for y in [275, 325, 375]:
                sprite_unit = Unit(texture=self.loaded_textures[14], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[5][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[5][1]
                self.enemy_unit_list.append(sprite_unit)
        for x in [525, 575]:
            for y in [325, 375, 425, 475]:
                sprite_unit = Unit(texture=self.loaded_textures[13], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[4][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[4][1]
                self.enemy_unit_list.append(sprite_unit)

        self.general_setup()

    def setup_battle_4(self):
        for x in range(25, 450, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "mountain")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)
        for x in range(475, 800, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "forest")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in [625, 675, 725]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[10], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[1][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[1][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [625, 675, 725]:
            for y in [275, 325, 375]:
                sprite_unit = Unit(texture=self.loaded_textures[14], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[5][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[5][1]
                self.enemy_unit_list.append(sprite_unit)
        for x in [525, 575]:
            for y in [275, 325, 375, 425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[13], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[4][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[4][1]
                self.enemy_unit_list.append(sprite_unit)

        self.general_setup()

    def setup_battle_5(self):
        for x in range(25, 800, 50):
            for y in range(125, 500, 50):
                tile = Tile(x, y, "mountain")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in range(25, 800, 50):
            for y in range(525, 700, 50):
                tile = Tile(x, y, "grass")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in [625, 675, 725]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[10], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[1][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[1][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [625, 675, 725]:
            for y in [275, 325, 375]:
                sprite_unit = Unit(texture=self.loaded_textures[14], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[5][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[5][1]
                self.enemy_unit_list.append(sprite_unit)
        for x in [525, 575]:
            for y in [275, 325, 375, 425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[13], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[4][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[4][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [225, 275]:
            for y in [425, 475]:
                sprite_unit = Unit(texture=self.loaded_textures[11], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[2][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[2][1]
                self.enemy_unit_list.append(sprite_unit)

        self.general_setup()

    def setup_battle_6(self):
        for x in range(25, 250, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "desert")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in range(275, 800, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "forest")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in [625, 675, 725]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[10], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[1][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[1][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [625, 675, 725]:
            for y in [275, 325, 375]:
                sprite_unit = Unit(texture=self.loaded_textures[14], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[5][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[5][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [525, 575]:
            for y in [275, 325, 375, 425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[13], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[4][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[4][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [225, 275, 325]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[11], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[2][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[2][1]
                self.enemy_unit_list.append(sprite_unit)
        self.general_setup()

    def setup_battle_7(self):
        for x in range(25, 800, 50):
            for y in range(125, 250, 50):
                tile = Tile(x, y, "grass")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in range(25, 800, 50):
            for y in range(275, 700, 50):
                tile = Tile(x, y, "desert")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in [625, 675, 725]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[10], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[1][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[1][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [625, 675, 725]:
            for y in [275, 325, 375]:
                sprite_unit = Unit(texture=self.loaded_textures[14], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[5][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[5][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [525, 575]:
            for y in [275, 325, 375, 425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[13], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[4][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[4][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [225, 275, 325, 375]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[11], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[2][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[2][1]
                self.enemy_unit_list.append(sprite_unit)
        self.general_setup()

    def setup_battle_8(self):
        for x in range(25, 250, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "grass")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in range(275, 800, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "desert")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in [625, 675, 725]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[10], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[1][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[1][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [625, 675, 725]:
            for y in [275, 325, 375]:
                sprite_unit = Unit(texture=self.loaded_textures[14], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[5][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[5][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [525, 575]:
            for y in [275, 325, 375, 425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[13], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[4][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[4][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [225, 275, 325, 375]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[11], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[2][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[2][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [225, 275]:
            for y in [325, 375]:
                sprite_unit = Unit(texture=self.loaded_textures[12], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[3][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[3][1]
                self.enemy_unit_list.append(sprite_unit)
        self.general_setup()

    def setup_battle_9(self):
        for x in range(25, 800, 50):
            for y in range(125, 250, 50):
                tile = Tile(x, y, "mountain")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in range(25, 800, 50):
            for y in range(275, 700, 50):
                tile = Tile(x, y, "river")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in [625, 675, 725]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[10], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[1][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[1][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [625, 675, 725]:
            for y in [275, 325, 375]:
                sprite_unit = Unit(texture=self.loaded_textures[14], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[5][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[5][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [525, 575]:
            for y in [275, 325, 375, 425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[13], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[4][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[4][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [175, 225, 275, 325, 375]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[11], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[2][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[2][1]
                self.enemy_unit_list.append(sprite_unit)

        for x in [175, 225, 275, 325, 375]:
            for y in [275, 325, 375]:
                sprite_unit = Unit(texture=self.loaded_textures[12], center_x=x,
                                   center_y=y, index=0, enemy=True)
                sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[3][0]
                sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[3][1]
                self.enemy_unit_list.append(sprite_unit)

        self.general_setup()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == 119:
            self.enemy_unit_list.clear()
        elif symbol == 120:
            self.friendly_unit_list.clear()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for unit_icon in self.unit_icon_list:
            unit_icon: Unit
            if unit_icon.collides_with_point((x, y)):
                self.selected_unit = unit_icon

        self.mouse_point.pos = [x, y]

        if self.selected_unit:
            i = self.selected_unit.index
            if x <= 800 and y >= 100:
                gif_x_100 = int(x / 100) * 100
                gif_y_100 = int(y / 100) * 100
                if gif_x_100 <= x <= gif_x_100 + 50:
                    center_x = gif_x_100 + 25
                else:
                    center_x = gif_x_100 + 75
                if gif_y_100 <= y <= gif_y_100 + 50:
                    center_y = gif_y_100 + 25
                else:
                    center_y = gif_y_100 + 75

                self.selected_tile_pos = [center_x, center_y]

                if int(self.text_list[i + 1].text[0]) > 0 and (center_x, center_y) not in self.occupied_places:
                    sprite_unit = Unit(texture=self.loaded_textures[i + 5],
                                       center_x=center_x,
                                       center_y=center_y, index=i)
                    sprite_unit.attack = self.selected_unit.attack
                    sprite_unit.defence_percent = self.selected_unit.defence_percent

                    self.friendly_unit_list.append(sprite_unit)

                    self.text_list[i + 1].text = f"{int(self.text_list[i + 1].text[0]) - 1}"
                    self.occupied_places.append((center_x, center_y))

            for unit in self.friendly_unit_list:
                if unit.collides_with_point((x, y)):
                    if self.selected_friendly_unit:
                        self.selected_friendly_unit.center_y -= 5

                    self.selected_friendly_unit = unit
                    self.selected_friendly_unit.center_y += 5

                    self.v_box.clear()
                    self.unit_info = arcade.gui.UITextArea(text=str(unit), multiline=True,
                                                           height=150, text_color=(0, 0, 0))
                    move_button = arcade.gui.UIFlatButton(text="Move")
                    move_button.on_click = self._on_click_move_button
                    self.v_box.add(self.unit_info)
                    self.v_box.add(move_button)
                    self.manager.add(arcade.gui.UIAnchorWidget(
                        anchor_x="left",
                        anchor_y="bottom",
                        align_x=810,
                        align_y=363,
                        child=self.v_box
                    )
                    )
            for unit in self.enemy_unit_list:
                if unit.collides_with_point((x, y)):
                    if self.selected_enemy_unit:
                        self.selected_enemy_unit.center_y -= 5

                    self.selected_enemy_unit = unit
                    self.selected_enemy_unit.center_y += 5

                    self.v_box.clear()
                    self.unit_info = arcade.gui.UITextArea(text=str(unit), multiline=True,
                                                           height=150, text_color=(0, 0, 0))
                    attack_button = arcade.gui.UIFlatButton(text="Attack")
                    attack_button.on_click = self._on_click_attack_button
                    self.v_box.add(self.unit_info)
                    self.v_box.add(attack_button)
                    self.manager.add(arcade.gui.UIAnchorWidget(
                        anchor_x="left",
                        anchor_y="bottom",
                        align_x=810,
                        align_y=363,
                        child=self.v_box
                    )
                    )

    def on_draw(self):
        self.clear()

        self.tile_list.draw()
        self.border_list.draw()

        self.assign_bar.draw()
        self.unit_icon_list.draw()
        self.tool_bar.draw()
        self.manager.draw()

        self.text_list.draw()

        self.friendly_unit_list.draw()
        self.enemy_unit_list.draw()

    def load_textures(self):
        name_list = ["swordsman.png", "bowman.png", "cavalry.png", "pikeman.png", "cannon.png"]
        for name in name_list:
            self.loaded_textures.append(arcade.load_texture(f"{MAIN_PATH}{name}"))
        for name in name_list:
            self.loaded_textures.append(arcade.load_texture(f"{MAIN_PATH}friendly/{name}"))
        for name in name_list:
            self.loaded_textures.append(arcade.load_texture(f"{MAIN_PATH}enemy/{name}"))

    def load_sounds(self):
        sound_list = ["metalhit.mp3", "arrow.mp3", "horse.mp3", "metalhit.mp3", "cannon.mp3"]
        for name in sound_list:
            self.loaded_sounds.append(arcade.Sound(f"{PATH}/../assets/sound_effects/{name}"))

    def _on_click_move_button(self, _: arcade.gui.UIOnClickEvent):
        if self.selected_friendly_unit.played:
            text = arcade.gui.UITextArea(text="Already played with this unit", text_color=(255, 0, 0),
                                         multiline=True)

            if len(self.v_box.children) < 3:
                self.v_box.add(text)
            return False
        if abs(self.selected_tile_pos[0] - self.selected_friendly_unit.center_x) > 100:
            return False
        if abs(self.selected_tile_pos[1] - self.selected_friendly_unit.center_y) > 100:
            return False
        self.selected_friendly_unit.played = True
        self.selected_friendly_unit.center_x = self.selected_tile_pos[0]
        self.selected_friendly_unit.center_y = self.selected_tile_pos[1]

    def _on_click_attack_button(self, _: arcade.gui.UIOnClickEvent):
        if self.selected_friendly_unit.played:
            text = arcade.gui.UITextArea(text="Already played with this unit", text_color=(255, 0, 0),
                                         multiline=True)

            if len(self.v_box.children) < 3:
                self.v_box.add(text)
            return False
        self.selected_enemy_unit.deduct_health(self.selected_friendly_unit.attack, self.selected_friendly_unit.name)
        self.loaded_sounds[self.selected_friendly_unit.index].play(volume=0.7)
        self.selected_friendly_unit.played = True
        self.unit_info.text = str(self.selected_enemy_unit)

    def _on_click_next_turn_button(self, _: arcade.gui.UIOnClickEvent):
        for enemy in self.enemy_unit_list:
            if enemy.health < 0:
                self.enemy_unit_list.remove(enemy)
            if not self.friendly_unit_list:
                break
            adjacent_unit, distance = arcade.get_closest_sprite(enemy, self.friendly_unit_list)
            if distance <= 50 ** (2 ** 0.5):
                adjacent_unit.deduct_health(enemy.attack, enemy.name)
            else:
                move_x = adjacent_unit.center_x - enemy.center_x
                move_y = adjacent_unit.center_y - enemy.center_y
                if move_x > 100:
                    move_x = 100
                elif move_x < -100:
                    move_x = -100
                if move_y > 100:
                    move_y = 100
                elif move_y < -100:
                    move_y = -100
                if (enemy.center_x + move_x, enemy.center_y + move_y) not in self.occupied_places:
                    enemy.center_x += move_x
                    enemy.center_y += move_y

        if len(self.enemy_unit_list) == 0:
            self.army.battles_won += 1
            self.army.battles += 1
            if self.army.morale < 100:
                self.army.morale += 5
            if self.army.morale > 100:
                self.army.morale = 100

            self.manager.clear()
            self.music.stop(self.music_player)
            self.main_view.music.play(loop=True, volume=0.1)
            self.main_window.show_view(self.main_view)

        for friend in self.friendly_unit_list:
            friend.played = False
            if friend.health < 0:
                self.friendly_unit_list.remove(friend)

        if len(self.friendly_unit_list) == 0:
            self.army.battles += 1
            if self.army.morale <= 100:
                self.army.morale -= 5
            self.army.null()
            self.main_view.player.population -= self.army.population_in_army()
            self.main_view.player.soldiers = 0
            self.manager.clear()
            self.music.stop(self.music_player)
            self.main_view.music.play(loop=True, volume=0.1)
            self.main_window.show_view(self.main_view)
