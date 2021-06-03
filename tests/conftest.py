import pytest
import arcade

# Reduce the atlas size
arcade.ArcadeContext.atlas_size = (2048, 2048)

WINDOW = None

def create_window():
    global WINDOW
    if not WINDOW:
        print("CREATING WINDOW")
        WINDOW = arcade.Window(title="Testing", vsync=False)
    return WINDOW


def prepare_window(window: arcade.Window):
    # Check if someone has been naughty
    if window.has_exit:
        raise RuntimeError("Please do not close the global test window :D")

    window.switch_to()
    ctx = window.ctx
    ctx._default_atlas = None  # Clear the global atlas
    window.hide_view()  # Disable views if any is active

    # Reset context (various states)
    ctx.reset()
    window.flip()
    window.clear()

    # Ensure no old functions are lingering
    window.on_draw = lambda: None
    window.on_update = lambda dt: None
    window.update = lambda dt: None


def pytest_addoption(parser):
    parser.addoption("--twm", action="store_true", default=False, help="Disable window geometry tests when using a tiling window manager" )


@pytest.fixture(scope="function")
def twm(pytestconfig):
    if pytestconfig.getoption("twm"):
        return True
    return False


@pytest.fixture(scope="function")
def ctx():
    window = create_window()
    arcade.set_window(window)
    try:
        prepare_window(window)
        yield window.ctx
    finally:
        window.flip()


@pytest.fixture(scope="function")
def window():
    window = create_window()
    arcade.set_window(window)
    try:
        prepare_window(window)
        yield window
    finally:
        window.flip()
