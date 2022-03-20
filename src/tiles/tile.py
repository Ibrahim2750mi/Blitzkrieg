import arcade

COLOR_CORRESPONDENCE = {"desert": (241, 184, 26), "grass": (105, 193, 39), "land": (183, 204, 106),
                        "forest": (39, 130, 25), "mountain": (152, 173, 163), "river": (24, 174, 228)}


class Tile(arcade.SpriteSolidColor):
    def __init__(self, x, y, type_of_block):
        super(Tile, self).__init__(width=50, height=50, color=COLOR_CORRESPONDENCE[type_of_block])
        self.center_x = x
        self.center_y = y
        self.type = type_of_block
        self.border_tile = arcade.Sprite("../assets/misc/border.png", 1, center_x=x, center_y=y)
