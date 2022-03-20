import arcade

import config as cfg
from tiles.building import Building
from tiles.tile import Tile


class Game(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, cfg.SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.land_tile_list = None
        self.border_land_tile_list = None
        self.bar_list = None
        self.buildings_list = None

        # types of tiles
        self.types_of_tiles = None

        # Separate variable that holds the player sprite

        arcade.set_background_color(arcade.color.SMOKY_BLACK)

    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""
        # TODO: resource generation and kingdom class.

        self.land_tile_list = arcade.SpriteList(use_spatial_hash=True)
        self.border_land_tile_list = arcade.SpriteList(use_spatial_hash=True)
        self.bar_list = arcade.SpriteList(use_spatial_hash=True)
        self.buildings_list = arcade.SpriteList(use_spatial_hash=True)

        self.setup_terrain()

        self.buildings_list.append(Building(475, 475, "office"))

        self.bar_list.append(arcade.Sprite("../assets/misc/dialog_box.png", 1, center_x=540, center_y=50))
        self.bar_list.append(arcade.Sprite("../assets/misc/info_box.png", 1, center_x=940, center_y=350))
        self.bar_list.append(arcade.Sprite("../assets/misc/dialog_box.png", 1, center_x=540, center_y=650))

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when keyboard is pressed"""
        pass

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when keyboard is released"""
        pass

    def on_update(self, delta_time: float) -> None:
        """Movement and game logic."""
        pass

    def on_mouse_press(self, x: float, y: float, button: int, key_modifiers: int) -> None:
        pass

    def on_draw(self) -> None:
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here
        self.land_tile_list.draw()
        self.bar_list.draw()
        self.buildings_list.draw()
        self.border_land_tile_list.draw()

    def setup_terrain(self):
        co_ord_list = []
        for x in range(25, 800, 50):
            for y in range(125, 600, 50):
                co_ord_list.append((x, y))

        for x in range(725, 800, 50):
            for y in range(125, 600, 50):
                tile = Tile(x, y, "desert")
                self.land_tile_list.append(tile)
                self.border_land_tile_list.append(tile.border_tile)
                co_ord_list.remove((x, y))

        x_factor = 0
        for i in range(10, 1, -2):
            for y in range(1 + (10 - i) // 2, 11 - (10 - i) // 2):
                tile = Tile(25 + (x_factor * 50), 75 + (y * 50), "forest")
                self.land_tile_list.append(tile)
                self.border_land_tile_list.append(tile.border_tile)
                co_ord_list.remove((25 + (x_factor * 50), 75 + (y * 50)))
            x_factor += 1

        for x in range(625, 700, 50):
            if x == 675:
                for i in range(3):
                    tile = Tile(x, 75 + 50 * (10 - i), "desert")
                    self.land_tile_list.append(tile)
                    self.border_land_tile_list.append(tile.border_tile)
                    tile = Tile(x, 125 + (50 * i), "desert")
                    self.land_tile_list.append(tile)
                    self.border_land_tile_list.append(tile.border_tile)
                    co_ord_list.remove((x, 125 + (50 * i)))
                    co_ord_list.remove((x, 75 + 50 * (10 - i)))
            else:
                tile = Tile(x, 125, "desert")
                self.land_tile_list.append(tile)
                self.border_land_tile_list.append(tile.border_tile)
                tile = Tile(x, 575, "desert")
                self.land_tile_list.append(tile)
                self.border_land_tile_list.append(tile.border_tile)
                co_ord_list.remove((x, 575))
                co_ord_list.remove((x, 125))

        for x in range(1, 6):
            for y in range(10 - x, 10):
                tile = Tile(25 + 50 * x, 125 + 50 * y, "land")
                self.land_tile_list.append(tile)
                self.border_land_tile_list.append(tile.border_tile)
                co_ord_list.remove((25 + 50 * x, 125 + 50 * y))

        y_factor = 0
        for x in range(1, 6):
            y_factor += 1
            for y in range(y_factor):
                tile = Tile(25 + 50 * x, 125 + 50 * y, "land")
                self.land_tile_list.append(tile)
                self.border_land_tile_list.append(tile.border_tile)
                co_ord_list.remove((25 + 50 * x, 125 + 50 * y))

        for x in range(325, 650, 50):
            for y in range(275, 400, 50):
                if x != 325 or y != 275:
                    tile = Tile(x, y, "grass")
                    self.land_tile_list.append(tile)
                    self.border_land_tile_list.append(tile.border_tile)
                    co_ord_list.remove((x, y))

        for x in range(325, 550, 50):
            if x == 325 or x == 525:
                for i in range(2):
                    tile = Tile(x, 575 - 50 * i, "river")
                    self.land_tile_list.append(tile)
                    self.border_land_tile_list.append(tile.border_tile)
                    co_ord_list.remove((x, 575 - 50 * i))
            else:
                tile = Tile(x, 575, "river")
                self.land_tile_list.append(tile)
                self.border_land_tile_list.append(tile.border_tile)
                co_ord_list.remove((x, 575))

        for x in range(325, 550, 50):
            tile = Tile(x, 425, "grass")
            self.land_tile_list.append(tile)
            self.border_land_tile_list.append(tile.border_tile)
            co_ord_list.remove((x, 425))

        for x in range(425, 550, 50):
            for y in range(175, 250, 50):
                if x != 425 or y != 175:
                    tile = Tile(x, y, "grass")
                    self.land_tile_list.append(tile)
                    self.border_land_tile_list.append(tile.border_tile)
                    co_ord_list.remove((x, y))

        for x in range(325, 500, 50):
            for y in range(475, 550, 50):
                if x != 325 or y != 525:
                    if x != 475 or y != 475:
                        tile = Tile(x, y, "mountain")
                        self.land_tile_list.append(tile)
                        self.border_land_tile_list.append(tile.border_tile)
                    else:
                        tile = Tile(x, y, "grass")
                        self.land_tile_list.append(tile)
                        self.border_land_tile_list.append(tile.border_tile)
                        tile = Tile(x + 50, y, "grass")
                        self.land_tile_list.append(tile)
                        self.border_land_tile_list.append(tile.border_tile)
                        co_ord_list.remove((x + 50, y))
                    co_ord_list.remove((x, y))

        for co_ord in co_ord_list:
            tile = Tile(co_ord[0], co_ord[1], "land")
            self.land_tile_list.append(tile)
            self.border_land_tile_list.append(tile.border_tile)

        co_ord_list.clear()


def main():
    """Main function"""
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
