from functools import partial

import arcade
import arcade.gui

from config import PATH
from misc.misc_classes import AdvanceUiInputText, AdvancedUiManager

MAIN_PATH = f"{PATH}/../assets/buildings/"


class Building(arcade.Sprite):

    def __init__(self, x, y, type_of_build, kingdom):
        super(Building, self).__init__(f"{MAIN_PATH}{type_of_build}.png", center_x=x, center_y=y)
        self.kingdom = kingdom
        self.manager = AdvancedUiManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout(space_between=18)


class CustomsOffice(Building):
    def __init__(self, x, y, type_of_build, kingdom):
        super(CustomsOffice, self).__init__(x=x, y=y, type_of_build=type_of_build, kingdom=kingdom)


class DefenceOffice(Building):
    def __init__(self, x, y, type_of_build, kingdom):
        super(DefenceOffice, self).__init__(x=x, y=y, type_of_build=type_of_build, kingdom=kingdom)


class Hospital(Building):
    def __init__(self, x, y, type_of_build, kingdom):
        super(Hospital, self).__init__(x=x, y=y, type_of_build=type_of_build, kingdom=kingdom)


class Office(Building):
    def __init__(self, x, y, type_of_build, kingdom):
        super(Office, self).__init__(x=x, y=y, type_of_build=type_of_build, kingdom=kingdom)
        self.triggered = False

        self.heading_text = arcade.Text(
            "Info:",
            start_x=912,
            start_y=563,
            font_size=16
        )

        self.setup_default_menu()

        self.manage_population_widget_list = []

        self.error_squiggle_save_manage_population = False
        self.error_squiggle_building_resource = False

        self.back_button = arcade.gui.UIFlatButton(text="BACK", width=250)
        self.back_button.on_click = self._on_click_back_button

    def display_info(self):
        self.heading_text.draw()
        self.manager.draw()

    def setup_default_menu(self):
        manage_building_button = arcade.gui.UIFlatButton(text="Manage Buildings", width=250)
        manage_population_button = arcade.gui.UIFlatButton(text="Manage Population", width=250)
        capital_info_button = arcade.gui.UIFlatButton(text="Capital Info", width=250)

        self.v_box.add(manage_building_button)
        self.v_box.add(manage_population_button)
        self.v_box.add(capital_info_button)

        manage_building_button.on_click = self._on_click_manage_building
        manage_population_button.on_click = self._on_click_manage_population
        capital_info_button.on_click = self._on_click_capital_info

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=810,
                align_y=250,
                child=self.v_box)
        )

    def _on_click_manage_building(self, _: arcade.gui.UIOnClickEvent = None):
        self.heading_text.text = "Manage Buildings:"
        self.heading_text.x = 840

        self.manager.clear()
        self.v_box.clear()

        build_label = arcade.gui.UILabel(text="Build:", font_size=16, text_color=(0, 0, 0))
        self.v_box.add(build_label)

        if not self.kingdom.hospital:
            self.h_box_hospital = arcade.gui.UIBoxLayout(space_between=10, vertical=False)
            hospital = arcade.gui.UIFlatButton(text="Hospital", font_size=8, width=200)
            hospital.on_click = self._on_click_hospital_button
            hospital_info_button = arcade.gui.UIFlatButton(text="?", width=20)
            hospital_info_button.on_click = partial(self._on_click_building_info_button,
                                                    text="Used to admit injured soldiers to save them.\nCapacity: "
                                                         "200\nResource consumption per turn: 20g\nInitial build "
                                                         "cost: 1200g, 200f")

            self.h_box_hospital.add(hospital)
            self.h_box_hospital.add(hospital_info_button)

            self.v_box.add(self.h_box_hospital)

        if not self.kingdom.finance_office:
            self.h_box_finance_office = arcade.gui.UIBoxLayout(space_between=10, vertical=False)
            finance_office = arcade.gui.UIFlatButton(text="Finance Office", font_size=8, width=200)
            finance_office.on_click = self._on_click_finance_office_button
            finance_office_info_button = arcade.gui.UIFlatButton(text="?", width=20)
            finance_office_info_button.on_click = partial(self._on_click_building_info_button,
                                                          text="Used to manage finances.\nResource consumption per "
                                                               "turn: 20f\nInitial build cost: 1200g, 200f")

            self.h_box_finance_office.add(finance_office)
            self.h_box_finance_office.add(finance_office_info_button)

            self.v_box.add(self.h_box_finance_office)

        if not self.kingdom.defence_office:
            self.h_box_defence_office = arcade.gui.UIBoxLayout(space_between=10, vertical=False)
            defence_office = arcade.gui.UIFlatButton(text="Defence Office", font_size=8, width=200)
            defence_office.on_click = self._on_click_defence_office_button
            defence_office_info_button = arcade.gui.UIFlatButton(text="?", width=20)
            defence_office_info_button.on_click = partial(self._on_click_building_info_button,
                                                          text="Used to manage army(important).\nResource consumption "
                                                               "per turn: 20f 20g\nInitial build cost: 1000g, 500f")

            self.h_box_defence_office.add(defence_office)
            self.h_box_defence_office.add(defence_office_info_button)

            self.v_box.add(self.h_box_defence_office)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=810,
                align_y=300,
                child=self.v_box
            )
        )

    def _on_click_building_info_button(self, _: arcade.gui.UIOnClickEvent, text: str):
        self.manager.clear()
        self.v_box.clear()

        message_box = arcade.gui.UIMessageBox(
            width=350,
            height=200,
            message_text=(
                text
            ),
            callback=self._on_click_manage_building,
            buttons=["ok"]
        )

        self.v_box.add(message_box)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="center",
                child=self.v_box
            )
        )

    def _on_click_hospital_button(self, _: arcade.gui.UIOnClickEvent):
        ret = self.kingdom.build_hospital()
        self._on_click_manage_building()
        if not ret and self.error_squiggle_building_resource:
            self._raise_manage_building_resource_error()
            self.error_squiggle_building_resource = True
        else:
            self.error_squiggle_building_resource = False

    def _on_click_finance_office_button(self, _: arcade.gui.UIOnClickEvent):
        ret = self.kingdom.build_finance_office()
        self._on_click_manage_building()
        if not ret and self.error_squiggle_building_resource:
            self._raise_manage_building_resource_error()
            self.error_squiggle_building_resource = True
        else:
            self.error_squiggle_building_resource = False

    def _on_click_defence_office_button(self, _: arcade.gui.UIOnClickEvent):
        ret = self.kingdom.build_defence_office()
        self._on_click_manage_building()
        if not ret and self.error_squiggle_building_resource:
            self._raise_manage_building_resource_error()
            self.error_squiggle_building_resource = True
        else:
            self.error_squiggle_building_resource = False

    def _on_click_manage_population(self, _: arcade.gui.UIOnClickEvent):
        self.heading_text.text = "Manage Population:"
        self.heading_text.x = 840

        self.manager.clear()
        farmer_label = arcade.gui.UILabel(text="Assign farmer(+3f, -1g, -1p)", font_size=11, width=250,
                                          text_color=(0, 0, 0))
        farmers = AdvanceUiInputText(text=str(self.kingdom.farmers), width=250, height=25, font_size=16,
                                     only_numeric_values=True)
        farmer_border = arcade.gui.UIBorder(child=farmers)

        worker_label = arcade.gui.UILabel(text="Assign worker(+3g, -1f, -1p)", font_size=11, width=250,
                                          text_color=(0, 0, 0))
        workers = AdvanceUiInputText(text=str(self.kingdom.workers), width=250, height=25, font_size=16,
                                     only_numeric_values=True)
        worker_border = arcade.gui.UIBorder(child=workers)

        soldier_label = arcade.gui.UILabel(text="Assign soldier(-2g, -2f, -1p, +1a)", font_size=11, width=250,
                                           text_color=(0, 0, 0))
        soldiers = AdvanceUiInputText(text=str(self.kingdom.soldiers), width=250, height=25, font_size=16,
                                      only_numeric_values=True)
        soldier_border = arcade.gui.UIBorder(child=soldiers)

        save_button = arcade.gui.UIFlatButton(text="SAVE", width=250)
        save_button.on_click = self._on_click_save_button_manage_population

        self.v_box.clear()

        # self.v_box.add(farmers)
        self.v_box.add(farmer_label)
        self.v_box.add(farmer_border)
        self.v_box.add(worker_label)
        self.v_box.add(worker_border)
        self.v_box.add(soldier_label)
        self.v_box.add(soldier_border)
        self.v_box.add(save_button)
        self.v_box.add(self.back_button)

        self.manage_population_widget_list.append(farmers)
        self.manage_population_widget_list.append(workers)
        self.manage_population_widget_list.append(soldiers)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=810,
                align_y=150,
                child=self.v_box
            )
        )

    def _on_click_capital_info(self, _: arcade.gui.UIOnClickEvent):
        self.heading_text.text = "Capital Info:"
        self.heading_text.x = 875

        self.manager.clear()

        self.v_box.clear()

        net_food = 3 * self.kingdom.farmers - self.kingdom.workers - 2 * self.kingdom.soldiers
        net_gold = 3 * self.kingdom.workers - self.kingdom.farmers - 2 * self.kingdom.soldiers
        unemployed_population = self.kingdom.unemployed

        info_food_label = arcade.gui.UITextArea(text=f"Net food production per turn: {net_food}",
                                                multiline=True, width=250, font_size=11, text_color=(0, 0, 0))
        info_gold_label = arcade.gui.UITextArea(text=f"Net gold production per turn: {net_gold}",
                                                multiline=True, width=250, font_size=11, text_color=(0, 0, 0))
        info_soldiers_label = arcade.gui.UITextArea(text=f"Number of soldiers: {self.kingdom.soldiers}",
                                                    multiline=True, width=250, font_size=11, text_color=(0, 0, 0))
        info_unemployed_population_label = arcade.gui.UITextArea(text=f"Unemployed population: {unemployed_population}",
                                                                 multiline=True, width=250, font_size=11,
                                                                 text_color=(0, 0, 0))
        info_unhappiness_label = arcade.gui.UITextArea(text=f"Unhappiness per turn: {self.kingdom.unhappiness}",
                                                       multiline=True, width=250, font_size=11, text_color=(0, 0, 0))

        self.v_box.add(info_food_label)
        self.v_box.add(info_gold_label)
        self.v_box.add(info_soldiers_label)
        self.v_box.add(info_unemployed_population_label)
        self.v_box.add(info_unhappiness_label)
        self.v_box.add(self.back_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=810,
                align_y=180,
                child=self.v_box
            )
        )

    def _on_click_back_button(self, _: arcade.gui.UIOnClickEvent):
        self.manager.clear()
        self.v_box.clear()
        self.setup_default_menu()

    def _on_click_save_button_manage_population(self, _: arcade.gui.UIOnClickEvent):
        if sum([i.text for i in self.manage_population_widget_list[-3:]]) <= self.kingdom.population:
            self.kingdom.farmers = self.manage_population_widget_list[0].text
            self.kingdom.workers = self.manage_population_widget_list[1].text
            self.kingdom.soldiers = self.manage_population_widget_list[2].text
            self.error_squiggle_save_manage_population = False
        elif not self.error_squiggle_save_manage_population:
            self.manager.clear()

            error_label = arcade.gui.UITextArea(width=250, text="Your assigned population is greater "
                                                                "than your current population".upper(),
                                                multiline=True, text_color=(255, 0, 0), font_size=12, height=60)
            self.error_squiggle_save_manage_population = True
            self.v_box.add(error_label)

            self.manager.add(
                arcade.gui.UIAnchorWidget(
                    anchor_x="left",
                    anchor_y="bottom",
                    align_x=810,
                    align_y=100,
                    child=self.v_box
                )
            )

    def _raise_manage_building_resource_error(self):
        self.manager.clear()

        error_label = arcade.gui.UITextArea(text="You don't have enough resource click on ? for more info",
                                            text_color=(255, 0, 0), width=250, multiline=True)
        self.v_box.add(error_label)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=810,
                align_y=200,
                child=self.v_box
            )
        )
