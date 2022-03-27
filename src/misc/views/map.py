import time

import arcade
import arcade.gui

from army.army import Army
from config import PATH
from misc.misc_classes import AdvanceUiInputText

MAIN_PATH = f"{PATH}/../assets/maps/map_"
SUB_MAIN_PATH = f"{PATH}/../assets/misc/"


class Map(arcade.View):
    def __init__(self, main_window, main_view):
        super(Map, self).__init__()

        self.map = None
        self.dialog_sprite = None
        self.info_box = None

        self.sprite_container = None

        self.manager = None
        self.v_box = None
        self.v_box_1 = None

        self.main_window = main_window
        self.main_view = main_view
        self.army: Army = None

        self.heading_text = self.heading_text = arcade.Text(
            "Assign Army:",
            start_x=875,
            start_y=610,
            font_size=16
        )

        self.manage_army_input_box_list = None
        self.battle_list = None

        arcade.set_background_color((127, 201, 255))

    def setup(self):
        self.army = self.main_view.player.army

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.sprite_container = arcade.SpriteList()

        self.manage_army_input_box_list = []
        self.battle_list = []

        self.v_box = arcade.gui.UIBoxLayout(space_between=10)
        self.v_box_1 = arcade.gui.UIBoxLayout(space_between=15)

        self.map = arcade.Sprite(f"{MAIN_PATH}{self.army.battles_won + 1}.png", center_x=400,
                                 center_y=400)
        self.info_box = arcade.Sprite(f"{SUB_MAIN_PATH}info_box_h.png", center_x=940, center_y=450)
        self.label_info_box()
        self.dialog_sprite = arcade.Sprite(f"{SUB_MAIN_PATH}dialog_box.png", center_y=50, center_x=450)

        self.sprite_container.append(self.map)
        self.sprite_container.append(self.info_box)
        self.sprite_container.append(self.dialog_sprite)

        battle_button = arcade.gui.UIFlatButton(text="Battle", width=100, height=25)
        battle_button.on_click = self._on_click_battle_button

        back_button = arcade.gui.UIFlatButton(text="Back", width=100, height=25)
        back_button.on_click = self._on_click_back_button

        self.v_box_1.add(battle_button)
        self.v_box_1.add(back_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=980,
                align_y=5,
                child=self.v_box_1
            )
        )

    def on_draw(self):
        self.clear()

        self.sprite_container.draw()

        self.manager.draw()
        self.heading_text.draw()
        if self.army.battles_won == 10:
            time.sleep(1)
            arcade.exit()

    def label_info_box(self):
        swords_man_label = arcade.gui.UILabel(text="Assign swords man unit:", font_size=11, width=250,
                                              text_color=(0, 0, 0))
        swords_man_input_box = AdvanceUiInputText(text=str(self.army.swords_man), width=250, height=20,
                                                  font_size=12, only_numeric_values=True)
        swords_man_input_box_border = arcade.gui.UIBorder(swords_man_input_box)

        self.v_box.add(swords_man_label)
        self.v_box.add(swords_man_input_box_border)
        self.manage_army_input_box_list.append(swords_man_input_box)

        bow_man_label = arcade.gui.UILabel(text="Assign bow man unit:", font_size=11, width=250,
                                           text_color=(0, 0, 0))
        bow_man_input_box = AdvanceUiInputText(text=str(self.army.bow_man), width=250, height=20,
                                               font_size=12, only_numeric_values=True)
        bow_man_input_box_border = arcade.gui.UIBorder(bow_man_input_box)

        self.v_box.add(bow_man_label)
        self.v_box.add(bow_man_input_box_border)
        self.manage_army_input_box_list.append(bow_man_input_box)

        cavalry_label = arcade.gui.UILabel(text="Assign cavalry unit:", font_size=11, width=250,
                                           text_color=(0, 0, 0))
        cavalry_input_box = AdvanceUiInputText(text=str(self.army.cavalry), width=250, height=20,
                                               font_size=12, only_numeric_values=True)
        cavalry_input_box_border = arcade.gui.UIBorder(cavalry_input_box)

        self.v_box.add(cavalry_label)
        self.v_box.add(cavalry_input_box_border)
        self.manage_army_input_box_list.append(cavalry_input_box)

        pike_man_label = arcade.gui.UILabel(text="Assign pike man unit:", font_size=11, width=250,
                                            text_color=(0, 0, 0))
        pike_man_input_box = AdvanceUiInputText(text=str(self.army.pike_man), width=250, height=20,
                                                font_size=12, only_numeric_values=True)
        pike_man_input_box_border = arcade.gui.UIBorder(pike_man_input_box)

        self.v_box.add(pike_man_label)
        self.v_box.add(pike_man_input_box_border)
        self.manage_army_input_box_list.append(pike_man_input_box)

        canons_label = arcade.gui.UILabel(text="Assign canons:", font_size=11, width=250,
                                          text_color=(0, 0, 0))
        canons_input_box = AdvanceUiInputText(text=str(self.army.canons), width=250, height=20,
                                              font_size=12, only_numeric_values=True)
        canons_input_box_border = arcade.gui.UIBorder(canons_input_box)

        self.v_box.add(canons_label)
        self.v_box.add(canons_input_box_border)
        self.manage_army_input_box_list.append(canons_input_box)

        save_button = arcade.gui.UIFlatButton(text="SAVE and CONTINUE", width=250)
        save_button.on_click = self._on_click_save_button_manage_army

        self.v_box.add(save_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=810,
                align_y=200,
                child=self.v_box
            )
        )

    def _on_click_battle_button(self, _: arcade.gui.UIOnClickEvent):
        self.main_view.player.battle.army_supplied_list = self.battle_list
        self.main_view.player.battle.setup()
        self.main_view.music.stop(self.main_view.music_player)
        self.main_window.show_view(self.main_view.player.battle)

    def _on_click_back_button(self, _: arcade.gui.UIOnClickEvent):
        self.main_window.hide_view()
        self.main_window.show_view(self.main_view)

    def _on_click_save_button_manage_army(self, _: arcade.gui.UIOnClickEvent):
        if self.manage_army_input_box_list[-1].text > self.army.canons:
            self.manage_army_input_box_list[-1].text = self.army.canons
        if self.manage_army_input_box_list[-2].text > self.army.pike_man:
            self.manage_army_input_box_list[-2].text = self.army.pike_man
        if self.manage_army_input_box_list[-3].text > self.army.cavalry:
            self.manage_army_input_box_list[-3].text = self.army.cavalry
        if self.manage_army_input_box_list[-2].text > self.army.bow_man:
            self.manage_army_input_box_list[-2].text = self.army.bow_man
        if self.manage_army_input_box_list[-1].text > self.army.swords_man:
            self.manage_army_input_box_list[-1].text = self.army.swords_man

        self.battle_list.append(self.manage_army_input_box_list[-5])
        self.battle_list.append(self.manage_army_input_box_list[-4])
        self.battle_list.append(self.manage_army_input_box_list[-3])
        self.battle_list.append(self.manage_army_input_box_list[-2])
        self.battle_list.append(self.manage_army_input_box_list[-1])
