"""
Low level tests for OpenGL 3.3 wrappers.
"""
import pytest


def test_ctx(ctx):
    assert ctx.gl_version >= (3, 3)
    assert ctx.limits.MAX_TEXTURE_SIZE > 4096
    assert ctx.limits.MAX_ARRAY_TEXTURE_LAYERS >= 256

    assert ctx.blend_func == ctx.BLEND_DEFAULT
    ctx.blend_func = ctx.BLEND_PREMULTIPLIED_ALPHA
    assert ctx.blend_func == ctx.BLEND_PREMULTIPLIED_ALPHA


def test_viewport(ctx):
    vp = 0, 0, 100, 100
    ctx.viewport = vp
    assert ctx.viewport == vp


def test_projection(window):
    ctx = window.ctx
    assert ctx.projection_2d == (0, window.width, 0, window.height)
    ctx.projection_2d = (1, 10, 2, 11)
    assert ctx.projection_2d == (1, 10, 2, 11)

    with pytest.raises(ValueError):
        ctx.projection_2d = "moo"

    with pytest.raises(ValueError):
        ctx.projection_2d = 1, 2, 3, 4, 5

    # ctx.projection_2d = 0, window.width, 0, window.height


def test_point_size(ctx):
    assert ctx.point_size == 1.0
    ctx.point_size = 2.0
    assert ctx.point_size == 2.0


def test_primitive_restart(ctx):
    assert ctx.primitive_restart_index == -1
    ctx.primitive_restart_index = -2
    assert ctx.primitive_restart_index == -2


def test_enable_disable(ctx):
    # Blend is enabled by default
    assert ctx.is_enabled(ctx.BLEND)
    ctx.enable_only() 
    assert len(ctx._flags) == 0

    ctx.enable(ctx.BLEND)
    ctx.enable(ctx.BLEND, ctx.DEPTH_TEST, ctx.CULL_FACE)
    assert ctx.is_enabled(ctx.BLEND)
    assert ctx.is_enabled(ctx.DEPTH_TEST)
    assert ctx.is_enabled(ctx.CULL_FACE)

    ctx.disable(ctx.BLEND)
    assert ctx.is_enabled(ctx.BLEND) is False
    assert len(ctx._flags) == 2

    ctx.enable_only(ctx.BLEND, ctx.CULL_FACE, ctx.DEPTH_TEST, ctx.PROGRAM_POINT_SIZE)
