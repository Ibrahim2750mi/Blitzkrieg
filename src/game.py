import arcade
from arcade import MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT

import config as cfg
from kingdoms import playerKingdom


class Game(arcade.View):
    """
    Main application class.
    """

    def __init__(self, window):
        # Call the parent class and set up the window
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.land_tile_list = None
        self.border_land_tile_list = None
        self.bar_list = None

        # player
        self.player = None
        self.window = window

        self.loaded_sounds = None
        self.music = None
        self.music_player = None
        # Separate variable that holds the player sprite

        arcade.set_background_color(arcade.color.SMOKY_BLACK)

    def setup(self) -> None:
        """Set up the game here. Call this function to restart the game."""
        self.music = arcade.Sound(f"{cfg.PATH}/../assets/background_music/Call_to_Adventure_Ambient.wav")

        self.land_tile_list = arcade.SpriteList(use_spatial_hash=True)
        self.border_land_tile_list = arcade.SpriteList(use_spatial_hash=True)
        self.bar_list = arcade.SpriteList(use_spatial_hash=True)

        self.player = playerKingdom.Kingdom(self.land_tile_list, self.border_land_tile_list, self.bar_list, self.window,
                                            self)

        self.player.setup_terrain()

        self.music_player = self.music.play(loop=True, volume=0.1)

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
        second_iter = False
        building_which_triggered = None
        if button == MOUSE_BUTTON_LEFT:
            for building in self.player.world.get_sprite_list(name="buildings"):
                if building.collides_with_point((x, y)):
                    building.triggered = True
                    second_iter = True
                    building_which_triggered = building
                    break
            if second_iter:
                for building in self.player.world.get_sprite_list(name="buildings"):
                    if building != building_which_triggered and building.triggered:
                        building.triggered = False
                        break
        elif button == MOUSE_BUTTON_RIGHT:
            for building in self.player.world.get_sprite_list(name="buildings"):
                if building.triggered:
                    building.triggered = False

    def on_draw(self) -> None:
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here
        self.player.draw()

        for building in self.player.world.get_sprite_list(name="buildings"):
            if building.triggered:
                building.display_info()


def main():
    """Main function"""
    window = arcade.Window(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, cfg.SCREEN_TITLE)
    player_kingdom_view = Game(window)
    player_kingdom_view.setup()
    window.show_view(player_kingdom_view)
    arcade.run()


if __name__ == "__main__":
    main()
