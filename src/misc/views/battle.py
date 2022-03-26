import arcade
import arcade.gui

from army.army import Unit
from config import PATH
from misc.misc_classes import LabelList
from tiles.tile import Tile

MAIN_PATH = f"{PATH}/../assets/units/"
SUB_MAIN_PATH = f"{PATH}/../assets/misc/"
NUMBER_CORRESPONDENCE_FOR_UNITS = {1: (10, 0.33), 2: (10, 0.1), 3: (15, 0.05), 4: (10, 0.1), 5: (25, 0)}


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

        self.loaded_textures = []

    def setup(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout(space_between=10)

        self.army = self.main_view.player.army

        self.tile_list = arcade.SpriteList()
        self.border_list = arcade.SpriteList()
        self.unit_icon_list = arcade.SpriteList()
        self.text_list = LabelList()
        self.friendly_unit_list = arcade.SpriteList()
        self.enemy_unit_list = arcade.SpriteList()

        self.loaded_textures = []
        self.load_textures()

        self.tool_bar = arcade.Sprite(f"{SUB_MAIN_PATH}info_box_h.png", center_x=940, center_y=400)
        self.assign_bar = arcade.Sprite(f"{SUB_MAIN_PATH}dialog_box.png", center_x=540, center_y=50)
        self.text_list.append(arcade.Text(text="Unit Info:", start_x=880, start_y=663))

        self.mouse_point = arcade.Sprite(f"{SUB_MAIN_PATH}mouse_point.png")

        eval(f"self.setup_battle_{self.army.battles_won}()")

    def general_setup(self):
        for i, unit in enumerate(self.army_supplied_list, start=1):
            sprite_unit = Unit(texture=self.loaded_textures[i - 1], center_x=50 + (i * 75), center_y=40, index=i - 1)
            sprite_unit.attack = NUMBER_CORRESPONDENCE_FOR_UNITS[i][0]
            sprite_unit.defence_percent = NUMBER_CORRESPONDENCE_FOR_UNITS[i][1]
            self.unit_icon_list.append(sprite_unit)
            self.text_list.append(arcade.Text(text=f"{unit.text}", start_x=50 + (i * 75),
                                              start_y=25, color=(0, 0, 0)))

    def setup_battle_0(self):
        for x in range(25, 800, 50):
            for y in range(125, 700, 50):
                tile = Tile(x, y, "desert")
                self.tile_list.append(tile)
                self.border_list.append(tile.border_tile)

        for x in [625, 675, 725]:
            for y in [425, 475, 525]:
                sprite_unit = Unit(texture=self.loaded_textures[10], center_x=x,
                                   center_y=y, index=0, enemy=True)
                self.enemy_unit_list.append(sprite_unit)

        self.general_setup()

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

                if int(self.text_list[i + 1].text[0]) > 0:
                    sprite_unit = Unit(texture=self.loaded_textures[i + 5],
                                       center_x=center_x,
                                       center_y=center_y, index=i)

                    sprite_unit.attack = self.selected_unit.attack
                    sprite_unit.defence = self.selected_unit.defence_percent

                    self.friendly_unit_list.append(sprite_unit)

                    self.text_list[i + 1].text = f"{int(self.text_list[i + 1].text[0]) - 1}"

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

    def _on_click_move_button(self, _: arcade.gui.UIOnClickEvent):
        pass

    def _on_click_attack_button(self, _: arcade.gui.UIOnClickEvent):
        pass

    def _on_click_next_turn_button(self, _: arcade.gui.UIOnClickEvent):
        pass
