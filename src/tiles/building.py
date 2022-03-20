import arcade
import arcade.gui

MAIN_PATH = "../assets/buildings/"


class AdvancedUiManager(arcade.gui.UIManager):
    def __init__(self, *args):
        super(AdvancedUiManager, self).__init__(*args)

    def clear(self):
        for widget in self.walk_widgets():
            self.remove(widget)


# class AdvancedUiInputText(arcade.gui.UIInputText):
#     def __init__(self, *args):
#         super(AdvancedUiInputText, self).__init__(*args)
#
#     def do_render(self, surface: arcade.gui.surface.Surface):
#         super(AdvancedUiInputText, self).do_render(surface)


class Building(arcade.Sprite):

    def __init__(self, x, y, type_of_build):
        super(Building, self).__init__(f"{MAIN_PATH}{type_of_build}.png", center_x=x, center_y=y)


class Office(Building):
    def __init__(self, x, y, type_of_build):
        super(Office, self).__init__(x=x, y=y, type_of_build=type_of_build)
        self.triggered = False
        self.text = "Info:"
        self.text_x = 910
        # a UIManager to handle the UI.
        self.manager = AdvancedUiManager()
        self.manager.enable()

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

    def display_info(self):
        arcade.draw_text(
            self.text,
            start_x=self.text_x,
            start_y=563,
            font_size=16
        )
        self.manager.draw()

    @staticmethod
    def _on_click_manage_building(event):
        print("called", event.pos, event.source)

    def _on_click_manage_population(self, event):
        self.text = "Manage Population:"
        self.text_x = 840

        self.manager.clear()
        farmers = arcade.gui.UIInputText(text="0", width=250, height=25, font_size=16)
        farmer_border = arcade.gui.UIBorder(child=farmers)
        self.v_box = arcade.gui.UIBoxLayout(space_between=40)

        self.v_box.add(farmers)
        self.v_box.add(farmer_border)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=810,
                align_y=250,
                child=self.v_box
            )
        )

    @staticmethod
    def _on_click_capital_info(event):
        print("called", event.pos, event.source)
