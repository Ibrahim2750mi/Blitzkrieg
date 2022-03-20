import arcade
import arcade.gui

MAIN_PATH = "../assets/buildings/"


class Building(arcade.Sprite):

    def __init__(self, x, y, type_of_build):
        super(Building, self).__init__(f"{MAIN_PATH}{type_of_build}.png", center_x=x, center_y=y)


class Office(Building):
    def __init__(self, x, y, type_of_build, window):
        super(Office, self).__init__(x=x, y=y, type_of_build=type_of_build)
        self.triggered = False

        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout(space_between=20)
        manage_building_button = arcade.gui.UIFlatButton(text="Manage Buildings", width=200, x=400, y=400)
        self.v_box.add(manage_building_button)
        manage_building_button.on_click = self._on_click_manage_building

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def display_info(self):
        arcade.draw_text(
            "Info:",
            start_x=910,
            start_y=562,
            font_size=24
        )
        self.manager.draw()

    @staticmethod
    def _on_click_manage_building(event):
        print("called", event.pos, event.source)
