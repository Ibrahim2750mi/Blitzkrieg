import arcade
import arcade.gui

from misc.misc_classes import AdvanceUiInputText, AdvancedUiManager

MAIN_PATH = "../assets/buildings/"


class Building(arcade.Sprite):

    def __init__(self, x, y, type_of_build, kingdom):
        super(Building, self).__init__(f"{MAIN_PATH}{type_of_build}.png", center_x=x, center_y=y)
        self.kingdom = kingdom


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
        # a UIManager to handle the UI.
        self.manager = AdvancedUiManager()
        self.manager.enable()

        self.v_child_box = arcade.gui.UIBoxLayout(space_between=20)

        self.v_box = arcade.gui.UIBoxLayout(space_between=40)

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

        self.manage_population_widget_list = []

    def display_info(self):
        self.heading_text.draw()
        self.manager.draw()

    @staticmethod
    def _on_click_manage_building(event):
        print("called", event.pos, event.source)

    def _on_click_manage_population(self, event):
        self.heading_text.text = "Manage Population:"
        self.heading_text.x = 840

        self.manager.clear()
        farmer_label = arcade.gui.UILabel(text="Assign farmer(+3f, -1g, -1p)", font_size=11, width=250,
                                          text_color=(0, 0, 0))
        farmers = AdvanceUiInputText(text=str(self.kingdom.farmers), width=250, height=25, font_size=16,
                                     only_numeric_value=True)
        farmer_border = arcade.gui.UIBorder(child=farmers)

        worker_label = arcade.gui.UILabel(text="Assign worker(+3g, -1f, -1p)", font_size=11, width=250,
                                          text_color=(0, 0, 0))
        workers = AdvanceUiInputText(text=str(self.kingdom.workers), width=250, height=25, font_size=16,
                                     only_numeric_value=True)
        worker_border = arcade.gui.UIBorder(child=workers)

        soldier_label = arcade.gui.UILabel(text="Assign soldier(-2g, -2f, -1p, +1a)", font_size=11, width=250,
                                           text_color=(0, 0, 0))
        soldiers = AdvanceUiInputText(text=str(self.kingdom.soldiers), width=250, height=25, font_size=16,
                                      only_numeric_value=True)
        soldier_border = arcade.gui.UIBorder(child=soldiers)

        save_button = arcade.gui.UIFlatButton(text="SAVE", width=250)
        save_button.on_click = self._on_click_save_button

        self.v_box = arcade.gui.UIBoxLayout(space_between=10)

        # self.v_box.add(farmers)
        self.v_box.add(farmer_label)
        self.v_box.add(farmer_border)
        self.v_box.add(worker_label)
        self.v_box.add(worker_border)
        self.v_box.add(soldier_label)
        self.v_box.add(soldier_border)
        self.v_box.add(save_button)

        self.manage_population_widget_list.append(farmers)
        self.manage_population_widget_list.append(workers)
        self.manage_population_widget_list.append(soldiers)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=810,
                align_y=240,
                child=self.v_box
            )
        )

    @staticmethod
    def _on_click_capital_info(event):
        print("called", event.pos, event.source)

    def _on_click_save_button(self, event):
        self.kingdom.farmers = self.manage_population_widget_list[0].text
        self.kingdom.workers = self.manage_population_widget_list[1].text
        self.kingdom.soldiers = self.manage_population_widget_list[2].text
