import arcade

MAIN_PATH = "../assets/buildings/"


class Building(arcade.Sprite):
    def __init__(self, x, y, type_of_build):
        super(Building, self).__init__(f"{MAIN_PATH}{type_of_build}.png", center_x=x, center_y=y)
