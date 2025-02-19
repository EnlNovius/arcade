from abc import abstractmethod
from contextlib import contextmanager
from typing import List

import arcade
from arcade.experimental.gui_v2.events import UIEvent


class InteractionMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_history: List[UIEvent] = []

    def move_mouse(self, x: int, y: int):
        self.on_mouse_motion(x, y, 0, 0)

    def click_and_hold(self, x: int, y: int, button=arcade.MOUSE_BUTTON_LEFT):
        self.on_mouse_press(
            x=x, y=y, button=button, modifiers=0
        )

    def release(self, x: int, y: int, button=arcade.MOUSE_BUTTON_LEFT):
        self.on_mouse_release(
            x=x, y=y, button=button, modifiers=0
        )

    def click(self, x: int, y: int):
        self.click_and_hold(x, y)
        self.release(x, y)

    def right_click(self, x: int, y: int):
        self.click_and_hold(x, y, button=arcade.MOUSE_BUTTON_RIGHT)
        self.release(x, y, button=arcade.MOUSE_BUTTON_RIGHT)

    def _on_ui_event(self, event: UIEvent):
        self.event_history.append(event)

    @property
    def last_event(self):
        return self.event_history[-1] if self.event_history else None

    @abstractmethod
    def dispatch_ui_event(self, event):
        pass


@contextmanager
def record_ui_events(widget, *names) -> List[UIEvent]:
    events = []

    def record(event):
        events.append(event)

    widget.push_handlers(**{name: record for name in names})

    yield events

    widget.remove_handlers(**{name: record for name in names})
