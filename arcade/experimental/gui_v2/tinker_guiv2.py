from random import choice

import arcade
from arcade import load_texture
from arcade.examples.perf_test.stress_test_draw_shapes import FPSCounter
from arcade.experimental.gui_v2 import UIManager
from arcade.experimental.gui_v2.widgets import Dummy, SpriteWidget, TextArea, InputText, TexturePane, FlatButton

LOREM_IPSUM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent eget pellentesque velit. Nam eu rhoncus nulla. Fusce ornare libero eget ex vulputate, vitae mattis orci eleifend. Donec quis volutpat arcu. Proin lacinia velit id imperdiet ultrices. Fusce porta magna leo, non maximus justo facilisis vel. Duis pretium sem ut eros scelerisque, a dignissim ante pellentesque. Cras rutrum aliquam fermentum. Donec id mollis mi.

Nullam vitae nunc aliquet, lobortis purus eget, porttitor purus. Curabitur feugiat purus sit amet finibus accumsan. Proin varius, enim in pretium pulvinar, augue erat pellentesque ipsum, sit amet varius leo risus quis tellus. Donec posuere ligula risus, et scelerisque nibh cursus ac. Mauris feugiat tortor turpis, vitae imperdiet mi euismod aliquam. Fusce vel ligula volutpat, finibus sapien in, lacinia lorem. Proin tincidunt gravida nisl in pellentesque. Aenean sed arcu ipsum. Vivamus quam arcu, elementum nec auctor non, convallis non elit. Maecenas id scelerisque lectus. Vivamus eget sem tristique, dictum lorem eget, maximus leo. Mauris lorem tellus, molestie eu orci ut, porta aliquam est. Nullam lobortis tempor magna, egestas lacinia lectus.
"""


class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """

    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.current_texture = 0
            self.set_texture(self.current_texture)


class UIMockup(arcade.Window):
    def load_explosion(self):
        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"

        # Load the explosions from a sprite sheet
        explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)
        return Explosion(explosion_texture_list)

    def __init__(self):
        super().__init__(800, 600, "UI Mockup", resizable=True)
        self.manager = UIManager()
        self.fps = FPSCounter()

        # size = 40
        # for y in range(0, self.height, size):
        #     for x in range(0, self.width, size):
        #         button = Button(x, y, size, size)
        #         self.change_color(button)
        #         button.on_click = self.change_color
        #         self.manager.add(button)

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        tex = load_texture(":resources:gui_basic_assets/red_button_normal.png")
        tex_hov = load_texture(":resources:gui_basic_assets/red_button_hover.png")
        tex_press = load_texture(":resources:gui_basic_assets/red_button_press.png")

        # for y in range(0, self.height, 40):
        #     for x in range(0, self.width, 90):
        #         self.manager.add(
        # FlatButton(x, y, 80, 30, text="Hello", style={"font_size": 10})
        # ImageButton(x, y, 80, 30, tex, tex_hov, tex_press, text="Hallo")
        # SpriteWidget(x=x, y=y, width=80, height=30, sprite=Sprite(":resources:gui_basic_assets/red_button_normal.png"))
        # ).on_click = self.on_button_click

        self.manager.add(
            SpriteWidget(x=500, y=300, width=256, height=256, sprite=self.load_explosion())
        )

        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        self.manager.add(
            TexturePane(
                TextArea(x=100, y=200, width=200, height=300, text=LOREM_IPSUM, text_color=(0, 0, 0, 255)).with_padding(
                    right=20),
                tex=bg_tex,
                pad=(10, 10, 10, 10)
            )
        )

        self.manager.add(
            TexturePane(
                InputText(x=340, y=200, width=200, height=50, text="Hello"),
                tex=bg_tex,
                pad=(10, 10, 10, 10)
            ))
        self.manager.add(
                InputText(x=340, y=110, width=200, height=50, text="Hello"),
            )

        self.manager.add(
            FlatButton(x=500, y=50, width=200, height=200, text="Hello 1")
        )
        self.manager.add(
            FlatButton(x=500, y=50, width=100, height=100, text="Hello 2"), layer=1
        )

        print(f"Render {len(self.manager._children)} widgets")

    def on_button_click(self, button, *args):
        print(button)

    def change_color(self, button: Dummy, *args):
        colors = [arcade.color.RED,
                  arcade.color.BLACK,
                  arcade.color.GREEN,
                  arcade.color.BLUE,
                  arcade.color.YELLOW,
                  arcade.color.BAZAAR]
        colors.remove(button.color)
        button.color = choice(colors)

    def on_draw(self):
        self.fps.tick()
        # print("window size", self.get_size())
        # print("proj", self.ctx.projection_2d)
        # print("vp", self.ctx.viewport)
        arcade.start_render()
        self.manager.draw()
        arcade.draw_text(f"{self.fps.get_fps():.0f}", self.width // 2, self.height // 2, color=arcade.color.RED,
                         font_size=20)

    def on_update(self, time_delta):
        self.manager.on_update(time_delta)

    # TODO These can be registered by UIManager
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.manager.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        self.manager.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.manager.on_mouse_release(x, y, button, modifiers)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.manager.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_text(self, text):
        self.manager.on_text(text)

    def on_text_motion(self, motion):
        self.manager.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        self.manager.on_text_motion_select(motion)

    def on_resize(self, width: float, height: float):
        # TODO: Tell Widgets they need to re-draw because surface was cleared
        super().on_resize(width, height)
        self.manager.resize(width, height)


window = UIMockup()
arcade.run()
