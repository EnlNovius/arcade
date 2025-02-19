from abc import ABCMeta, abstractmethod
from typing import Optional, Dict, cast

from pyglet.event import EventDispatcher
from pyglet.window import Window

import arcade
from arcade import SpriteList, TextureAtlas
from arcade.gui import (
    UIElement,
    UIEvent,
)
from arcade.gui.events import (
    MOUSE_DRAG,
    MOUSE_PRESS,
    MOUSE_RELEASE,
    MOUSE_SCROLL,
    KEY_PRESS,
    KEY_RELEASE,
    TEXT_INPUT,
    TEXT_MOTION,
    TEXT_MOTION_SELECTION,
    RESIZE,
    MOUSE_MOTION,
)
from arcade.gui.exceptions import UIException


class UIAbstractManager(EventDispatcher, metaclass=ABCMeta):
    window: Window

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.register_event_type("on_ui_event")

        self._focused_element: Optional[UIElement] = None
        self._hovered_element: Optional[UIElement] = None

    @abstractmethod
    def on_ui_event(self, event):
        """
        Processes UIEvents, forward events to added elements and manages focused and hovered elements
        """
        pass

    @abstractmethod
    def on_draw(self):
        """
        Draws all added :py:class:`arcade.gui.UIElement`.
        """
        pass

    def enable(self):
        """
        Registers handler functions (`on_...`) to :py:attr:`arcade.gui.UIElement`

        on_draw is not registered, to provide full control about draw order,
        so it has to be called by the devs themselves.
        """
        self.window.push_handlers(
            self.on_resize,
            self.on_update,
            self.on_mouse_drag,
            self.on_mouse_motion,
            self.on_mouse_press,
            self.on_mouse_release,
            self.on_mouse_scroll,
            self.on_key_press,
            self.on_key_release,
            self.on_text,
            self.on_text_motion,
            self.on_text_motion_select,
        )

    def disable(self):
        """
        Remove handler functions (`on_...`) from :py:attr:`arcade.Window`

        If every :py:class:`arcade.View` uses its own :py:class:`arcade.gui.UIManager`,
        this method should be called in :py:meth:`arcade.View.on_hide_view()`.
        """
        self.window.remove_handlers(
            self.on_resize,
            self.on_update,
            self.on_mouse_drag,
            self.on_mouse_motion,
            self.on_mouse_press,
            self.on_mouse_release,
            self.on_mouse_scroll,
            self.on_key_press,
            self.on_key_release,
            self.on_text,
            self.on_text_motion,
            self.on_text_motion_select,
        )

    def adjust_mouse_coordinates(self, x, y):
        """
        This method is used, to translate mouse coordinates to coordinates
        respecting the viewport and projection of cameras.
        The implementation should work in most common cases.

        If you use scrolling in the :py:class:`arcade.Camera` you have to reset scrolling
        or overwrite this method using the camera conversion: `ui_manager.adjust_mouse_coordinates = camera.mouse_coordinates_to_world`
        """
        vx, vy, vw, vh = self.window.ctx.viewport
        pl, pr, pb, pt = self.window.ctx.projection_2d
        proj_width, proj_height = pr - pl, pt - pb
        dx, dy = proj_width / vw, proj_height / vh
        return (x - vx) * dx, (y - vy) * dy

    def dispatch_ui_event(self, event: UIEvent):
        """
        Dispatches a :py:class:`arcade.gui.UIEvent` to all added :py:class:`arcade.gui.UIElement`.

        :param UIEvent event: event to dispatch
        :return:
        """
        self.dispatch_event("on_ui_event", event)

    # Listener
    def on_resize(self, width, height):
        """
        Callback triggered on window resize
        """
        self.dispatch_ui_event(UIEvent(RESIZE, width=width, height=height))

    def on_update(self, dt):
        """
        Callback triggered on update
        """
        pass
        # TODO pass updates, check performance

    def on_key_press(self, symbol: int, modifiers: int):
        """
        Dispatches :py:meth:`arcade.View.on_key_press()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.events.KEY_PRESS`
        """
        self.dispatch_ui_event(UIEvent(KEY_PRESS, symbol=symbol, modifiers=modifiers))

    def on_key_release(self, symbol: int, modifiers: int):
        """
        Dispatches :py:meth:`arcade.View.on_key_release()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.events.KEY_RELEASE`
        """
        self.dispatch_ui_event(UIEvent(KEY_RELEASE, symbol=symbol, modifiers=modifiers))

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Dispatches :py:meth:`arcade.View.on_mouse_press()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.events.MOUSE_PRESS`
        """
        x, y = self.adjust_mouse_coordinates(x, y)
        self.dispatch_ui_event(
            UIEvent(MOUSE_PRESS, x=x, y=y, button=button, modifiers=modifiers)
        )

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """
        Dispatches :py:meth:`arcade.View.on_mouse_release()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.events.MOUSE_RELEASE`
        """
        x, y = self.adjust_mouse_coordinates(x, y)
        self.dispatch_ui_event(
            UIEvent(MOUSE_RELEASE, x=x, y=y, button=button, modifiers=modifiers)
        )

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        Dispatches :py:meth:`arcade.View.on_mouse_motion()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.events.MOUSE_MOTION`
        """
        x, y = self.adjust_mouse_coordinates(x, y)
        self.dispatch_ui_event(
            UIEvent(
                MOUSE_MOTION,
                x=x,
                y=y,
                dx=dx,
                dy=dy,
            )
        )

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """
        Dispatches :py:meth:`arcade.View.on_mouse_drag()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.events.MOUSE_DRAG`
        """
        x, y = self.adjust_mouse_coordinates(x, y)
        self.dispatch_ui_event(
            UIEvent(
                MOUSE_DRAG, x=x, y=y, dx=dx, dy=dy, buttons=buttons, modifiers=modifiers
            )
        )

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """
        Dispatches :py:meth:`arcade.View.on_mouse_scroll()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.events.MOUSE_SCROLL`
        """
        x, y = self.adjust_mouse_coordinates(x, y)
        self.dispatch_ui_event(
            UIEvent(
                MOUSE_SCROLL,
                x=x,
                y=y,
                scroll_x=scroll_x,
                scroll_y=scroll_y,
            )
        )

    def on_text(self, text):
        """
        Dispatches :py:meth:`arcade.View.on_text()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.events.TEXT_INPUT`
        """
        self.dispatch_ui_event(
            UIEvent(
                TEXT_INPUT,
                text=text,
            )
        )

    def on_text_motion(self, motion):
        """
        Dispatches :py:meth:`arcade.View.on_text_motion()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.events.TEXT_MOTION`
        """
        self.dispatch_ui_event(
            UIEvent(
                TEXT_MOTION,
                motion=motion,
            )
        )

    def on_text_motion_select(self, selection):
        """
        Dispatches :py:meth:`arcade.View.on_text_motion_select()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.events.TEXT_MOTION_SELECT`
        """
        self.dispatch_ui_event(
            UIEvent(
                TEXT_MOTION_SELECTION,
                selection=selection,
            )
        )

    # Define hover and focus elements
    @property
    def focused_element(self) -> Optional[UIElement]:
        """
        :return: focused UIElement, only one UIElement can be focused at a time
        """
        return self._focused_element

    @focused_element.setter
    def focused_element(self, new_focus: UIElement):
        if self._focused_element and hasattr(self._focused_element, "on_focus"):
            self._focused_element.on_unfocus()
        self._focused_element = None

        if hasattr(new_focus, "on_focus"):
            new_focus.on_focus()

        self._focused_element = new_focus

    @property
    def hovered_element(self) -> Optional[UIElement]:
        """
        :return: hovered UIElement, only one UIElement can be focused at a time
        """
        return self._hovered_element

    @hovered_element.setter
    def hovered_element(self, new_hover: UIElement):
        if self._hovered_element and hasattr(self._hovered_element, "on_unhover"):
            self._hovered_element.on_unhover()
        self._hovered_element = None

        if hasattr(new_hover, "on_hover"):
            new_hover.on_hover()

        self._hovered_element = new_hover


class UIManager(UIAbstractManager):
    """
    The UIManager is the central component of Arcade's GUI library :py:mod:`arcade.gui`.
    UIManager holds and managers all :py:class:`arcade.gui.UIElement` classes and their children.
    It connects them with :py:class:`arcade.Window` callbacks to handle mouse events.

    For more information see the :ref:`user-interface-tutorial`.

    """

    def __init__(self, window=None, auto_enable=False, **kwargs):
        """
        Creates a new :py:class:`arcade.gui.UIManager` and
        registers the corresponding handlers to the current window.

        The UIManager has to be created, before
        :py:meth:`arcade.Window.show_view()`
        has been called.

        To support multiple views a singleton UIManager should be passed to all views.
        As an alternative you can remove all registered handlers of a UIManager by calling
        :py:meth:`arcade.gui.UIManager.unregister_handlers()` within :py:meth:`arcade.View.on_hide_view()`.

        :param arcade.Window window: Window to register handlers to, defaults to :py:meth:`arcade.get_window()`
        :param kwargs: catches unsupported named parameters
        """
        super().__init__()
        self.window: Window = window or arcade.get_window()

        self._ui_elements: SpriteList = SpriteList(atlas=TextureAtlas(size=(1024, 1024)))
        self._id_cache: Dict[str, UIElement] = {}

        if auto_enable:
            # TODO maybe push to ABC
            self.enable()

    def purge_ui_elements(self):
        """
        Removes all UIElements which where added to the :py:class:`arcade.gui.UIManager`.
        """
        self._ui_elements = SpriteList(atlas=TextureAtlas(size=(1024, 1024)))
        self._id_cache = {}

    def add_ui_element(self, ui_element: UIElement):
        """
        Adds a :py:class:`arcade.gui.UIElement` to the :py:class:`arcade.gui.UIManager`.
        :py:attr:`arcade.gui.UIElement.id` has to be unique.

        The :py:class:`arcade.gui.UIElement` will be drawn by the :py:class:`arcade.gui.UIManager`.
        :param UIElement ui_element: element to add.
        """
        if not hasattr(ui_element, "id"):
            raise UIException(
                "UIElement seems not to be properly setup, please check if you"
                ' overwrite the constructor and forgot "super().__init__(**kwargs)"'
            )

        ui_element.render()
        self._ui_elements.append(ui_element)
        ui_element.mng = self

        # Add elements with id to lookup
        if ui_element.id is not None:
            if ui_element.id in self._id_cache:
                raise UIException(f'duplicate id "{ui_element.id}"')

            self._id_cache[ui_element.id] = ui_element

    def find_by_id(self, ui_element_id: str) -> Optional[UIElement]:
        """
        Finds an :py:class:`arcade.gui.UIElement` by its ID.

        :param str ui_element_id: id of the :py:class:`arcade.gui.UIElement`
        :return: :py:class:`arcade.gui.UIElement` if available else None
        """
        return self._id_cache.get(ui_element_id)

    def on_draw(self):
        """
        Draws all added :py:class:`arcade.gui.UIElement`.
        """
        self._ui_elements.draw()

    def on_ui_event(self, event: UIEvent):
        """
        Processes UIEvents, forward events to added elements and manages focused and hovered elements
        """
        for ui_element in list(self._ui_elements):
            ui_element = cast(UIElement, ui_element)

            if event.type == MOUSE_PRESS:
                if ui_element.collides_with_point((event.get("x"), event.get("y"))):
                    self.focused_element = ui_element

                elif ui_element is self.focused_element:
                    # TODO does this work like expected?
                    self.focused_element = None

            if event.type == MOUSE_MOTION:
                if ui_element.collides_with_point((event.get("x"), event.get("y"))):
                    self.hovered_element = ui_element

                elif ui_element is self.hovered_element:
                    self.hovered_element = None

            ui_element.on_ui_event(event)
