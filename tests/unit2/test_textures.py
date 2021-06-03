import os
import arcade
from arcade import Texture

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LINE_HEIGHT = 20
CHARACTER_SCALING = 0.5


def test_main(window: arcade.Window):
    arcade.set_background_color(arcade.color.AMAZON)

    texture = arcade.load_texture(":resources:images/space_shooter/playerShip1_orange.png")
    assert texture.width == 99
    assert texture.height == 75

    circle_texture = arcade.make_circle_texture(10, arcade.color.RED)
    soft_circle_texture = arcade.make_soft_circle_texture(10, arcade.color.RED, 255, 0)
    soft_square_texture = arcade.make_soft_square_texture(10, arcade.color.RED, 255, 0)

    columns = 16
    count = 60
    sprite_width = 256
    sprite_height = 256
    file_name = ":resources:images/spritesheets/explosion.png"

    # Load the explosions from a sprite sheet
    explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

    def on_draw():
        arcade.start_render()
        texture.draw_scaled(50, 50, 1)
        texture.draw_sized(150, 50, 99, 75)

    window.on_draw = on_draw
    window.test()
    arcade.cleanup_texture_cache()


def test_texture_constructor_allows_none_and_none_string():
    """
    Test constructor accepting both None and the old style 'None'
    """
    Texture(
        name="allowsnonehitbox",
        hit_box_algorithm=None
    )

    Texture(
        name="old_behavior_preserved",
        hit_box_algorithm="None"
    )
    arcade.cleanup_texture_cache()
