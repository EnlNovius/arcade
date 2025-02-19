import arcade


def test_ui_manager_respects_camera(mock_mng, window):
    # GIVEN
    mock_mng.use_super_mouse_adjustment = True
    camera = arcade.Camera(window, window.width, window.height)

    # WHEN
    window.set_size(width=400, height=300)
    camera.viewport = 0, 0, window.width, window.height
    camera.use()

    mock_mng.click(100, 100)

    # THEN
    assert mock_mng.last_event.get("x") == 200
    assert mock_mng.last_event.get("y") == 200
