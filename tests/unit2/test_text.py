import pytest
import arcade


def test_text(window):
    arcade.set_background_color(arcade.color.AMAZON)

    SCREEN_WIDTH = window.width
    SCREEN_HEIGHT = window.height
    LINE_HEIGHT = 20

    arcade.start_render()
    current_x = 20

    # First line
    current_y = SCREEN_HEIGHT - LINE_HEIGHT
    arcade.draw_text("Test Text", current_x, current_y, arcade.color.BLACK, 12)

    # Again to test caching
    current_y -= LINE_HEIGHT
    arcade.draw_text("Test Text", current_x, current_y, arcade.color.BLACK, 12)

    current_y -= LINE_HEIGHT
    arcade.draw_text("Test Text Anchor Left", SCREEN_WIDTH // 2, current_y,
                        arcade.color.BLACK, 12, anchor_x="left")
    arcade.draw_point(SCREEN_WIDTH // 2, current_y, arcade.color.RED, 5)

    current_y -= LINE_HEIGHT
    arcade.draw_text("Test Text Anchor Center", SCREEN_WIDTH // 2, current_y,
                        arcade.color.BLACK, 12, anchor_x="center")
    arcade.draw_point(SCREEN_WIDTH // 2, current_y, arcade.color.RED, 5)

    current_y -= LINE_HEIGHT
    arcade.draw_text("Test Text Anchor Right", SCREEN_WIDTH // 2, current_y,
                        arcade.color.BLACK, 12, anchor_x="right")
    arcade.draw_point(SCREEN_WIDTH // 2, current_y, arcade.color.RED, 5)

    current_y -= LINE_HEIGHT
    arcade.draw_text("Test Text Anchor Top", SCREEN_WIDTH // 2, current_y,
                        arcade.color.BLACK, 12, anchor_y="top")
    arcade.draw_point(SCREEN_WIDTH // 2, current_y, arcade.color.RED, 5)

    current_y -= LINE_HEIGHT
    arcade.draw_text("Test Text Anchor Center", SCREEN_WIDTH // 2, current_y,
                        arcade.color.BLACK, 12, anchor_y="center")
    arcade.draw_point(SCREEN_WIDTH // 2, current_y, arcade.color.RED, 5)

    current_y -= LINE_HEIGHT
    arcade.draw_text("Test Text Anchor Bottom", SCREEN_WIDTH // 2, current_y,
                        arcade.color.BLACK, 12, anchor_y="bottom")
    arcade.draw_point(SCREEN_WIDTH // 2, current_y, arcade.color.RED, 5)

    field_width = SCREEN_WIDTH
    current_y -= LINE_HEIGHT
    arcade.draw_text(f"Test Text Field Width {field_width}", current_x, current_y,
                        arcade.color.BLACK, 12, font_name="arial", width=field_width)

    current_y -= LINE_HEIGHT
    arcade.draw_text(f"Centered Test Text Field Width {field_width}", current_x, current_y,
                        arcade.color.BLACK, 12, font_name="arial", width=field_width, align="center")

    current_y -= LINE_HEIGHT
    font_name = "comic"
    arcade.draw_text("Different font", current_x, current_y, arcade.color.BLACK, 12, font_name=font_name)

    current_y -= LINE_HEIGHT

    window.flip()


def test_create_text_image(window):
    pass


def test_create_text(window):
    pass


def test_create_text_sprite(window):
    pass

