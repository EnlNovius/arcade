from typing import List

from arcade.experimental.gui_v2.events import UIEvent, UIOnClickEvent, UIMousePressEvent, UIMouseReleaseEvent
from arcade.experimental.gui_v2.widgets import Dummy
from tests.test_gui_v2 import record_ui_events


def test_hover_on_widget(uimanager):
    # GIVEN
    widget = Dummy()
    uimanager.add(widget)

    # WHEN
    uimanager.move_mouse(widget.center_x, widget.center_y)

    # THEN
    assert widget.hover is True


def test_overlapping_hover_on_widget(uimanager):
    # GIVEN
    widget1 = Dummy()
    widget2 = Dummy()
    uimanager.add(widget1)
    uimanager.add(widget2)

    # WHEN
    uimanager.move_mouse(widget1.center_x, widget1.center_y)

    # THEN
    assert widget1.hover is True
    assert widget2.hover is True


def test_click_on_widget(uimanager):
    # GIVEN
    widget1 = Dummy()
    uimanager.add(widget1)

    # WHEN
    with record_ui_events(widget1, "on_event") as records:
        uimanager.click(widget1.center_x, widget1.center_y)

    # THEN
    records: List[UIEvent]
    assert len(records) == 3
    assert isinstance(records[0], UIMousePressEvent)
    assert isinstance(records[1], UIMouseReleaseEvent)

    click_event = records[2]
    assert isinstance(click_event, UIOnClickEvent)
    assert click_event.source == widget1
    assert click_event.x == widget1.center_x
    assert click_event.y == widget1.center_y


def test_click_on_overlay_widget_consumes_events(uimanager):
    # GIVEN
    widget1 = Dummy()
    widget2 = Dummy()
    uimanager.add(widget1)
    uimanager.add(widget2)

    # WHEN
    with record_ui_events(widget1, "on_event") as w1_records:
        with record_ui_events(widget2, "on_event") as w2_records:
            uimanager.click(widget1.center_x, widget1.center_y)

    # THEN
    # events are consumed before they get to underlying widget
    w1_records: List[UIEvent]
    assert len(w1_records) == 0

    # events are dispatched on widget2
    w2_records: List[UIEvent]
    assert len(w2_records) == 3
    click_event = w2_records[2]
    assert isinstance(click_event, UIOnClickEvent)
    assert click_event.source == widget2
    assert click_event.x == widget2.center_x
    assert click_event.y == widget2.center_y
