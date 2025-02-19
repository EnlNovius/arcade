:orphan:

.. _release_notes:

Release Notes
=============

Keep up-to-date with the latest changes to the Arcade library by the release notes.

Version 2.6.0 (UNRELEASED)
--------------------------

Version 2.6.0 is a major update to Arcade. It is not 100% backwards compatible with the 2.5 API.
Updates were made to text rendering, tiled map support, sprites, shaders, textures, GUI system,
and the documentation.

* `Tiled Map Editor <https://www.mapeditor.org/>`_ support has been overhauled.

  * Arcade now uses the .json file format for maps created by the Tiled Map Editor rather than the TMX format.
    Tile sets and other supporting files need to all be saved in .json format. The XML based formats are no longer
    supported by Arcade.
  * Feature-support for Tiles items has been improved.
  * See :ref:`platformer_tutorial` for a how-to.
  * See the `Community RPG <https://github.com/pythonarcade/community-rpg>`_ for a more complex example program.

  .. image:: https://raw.githubusercontent.com/pythonarcade/community-rpg/main/screenshot.png
     :width: 50%
     :alt: Screenshot of tile map

* Texture atlases have been introduced, texture management has been improved.

  * A sprite list will create and use its own texture atlas.
  * This introduces a new :class:`arcade.TextureAtlas` class that is used internally by SpriteList.
  * Sprites with new textures can be added to a sprite list without the delay. Arcade 2.5 had a delay caused by rebuilding
    its internal sprite sheet.
  * As a side effect, sprites can only belong to one sprite list that renders.
  * The texture atlas portion of a sprite can be drawn to, and quickly updated on the GPU side.

    * To demonstrate, there is a new :ref:`minimap` example that creates a sprite that has a dynamic minimap
      projected onto it.

    .. image:: ../examples/minimap.png
       :width: 50%
       :alt: Screenshot of minimap

* Revamped text rendering done by :func:`arcade.draw_text`.
  Rather than use Pillow to render onto an image, Arcade uses Pyglet's
  text drawing system.
  Text drawing is faster, higher resolution, and not prone to memory leaks. Fonts are now specifed by the
  font name, rather than the file name of the font.

  * Fonts can be dynamically loaded with :func:`arcade.load_font`.
  * Kenney.nl's TTF are now included as build-in resources.
  * See the :ref:`drawing_text` example.

  .. image:: ../examples/drawing_text.png
     :width: 50%
     :alt: Screenshot of drawing text


* SpriteList optimizations.

  * Sprites now draw even faster than before. On an Intel i7 with nVidia 980 Ti graphics card,
    8,000+ moving sprites can be drawn while maintaining 60 FPS. The same machine can only
    do 2,000 sprites with Pygame before FPS drops.

* Shadertoy support.

  * `Shadertoy.com <https://www.shadertoy.com/>`_ is a website that makes it easier to write OpenGL shaders.
  * The new :class:`arcade.Shadertoy` class makes it easy to run and interact with these shaders in Arcade.
  * See :ref:`shader_toy_tutorial` and `Asteroids <https://github.com/pythonarcade/asteroids>`_.

    .. image:: ../tutorials/shader_toy/cyber_fuji_2020.png
       :width: 40%

    .. image:: ../tutorials/shader_toy/star_nest.png
       :width: 40%

* Reworked GUI

  * UIEvents are replaced by Widgets
  * Option to relative pin Widgets on screen to center or border (supports resizing)
  * Widgets can be placed on top of each other
  * Overlapping Widgets properly handle mouse interaction
  * Fully typed event classes
  * Events contain source Widget *(planned)*
  * ScrollableText Widgets (more to come)
  * Support for Sprites within Widgets
  * Declarative coding style for borders and padding `widget.with_border(...)`
  * Automatically place Widgets vertically or horizontally (`ListGroup`)
  * Dropped support for YAML style files
  * Better performance and limited memory usage
  * More documentation *(planned)*

* Camera support

  * Easy scrolling with :class:`arcade.Camera`
  * For an example of this see the example: :ref:`sprite_move_scrolling`.
  * Automatic camera shake can be added in, see the example: :ref:`sprite_move_scrolling_shake`.

* Documentation

  * Lots of individual documentation updates for commands.
  * The :ref:`quick_index` has been reorganized to be easier to find commands, and
    the individual API documentation pages have been broken into parts, so it isn't one large monolithic page.
  * New tutorial for :ref:`user-interface-tutorial`.
  * New tutorial for :ref:`raycasting_tutorial`.

    .. image:: ../tutorials/raycasting/example.png
       :width: 50%

  * New tutorial for :ref:`shader_toy_tutorial`.
  * Revamped tutorial: :ref:`platformer_tutorial`.
  * Revamped minimap example: :ref:`minimap`.
  * Moved from AWS hosting to read-the-docs hosting so we can support multiple versions of docs.

* API commands

   * :func:`arcade.get_pixel` supports getting RGB and RGBA color value
   * :func:`arcade.get_three_color_float` Returns colors as RGB float with numbers 0.0-1.1 for each color
   * :func:`arcade.get_four_color_float`  Returns colors as RGBA float with numbers 0.0-1.1 for each color

Special thanks to:

* `einarf <https://github.com/einarf>`_ for performance improvements, texture atlas support, shader toy support,
  text drawing support, advice on GUI, and more.
* `Cleptomania <https://github.com/Cleptomania>`_ for Tiled Map support, sound support, and more.
* `eruvanos <https://github.com/eruvanos>`_ for the original GUI and all the GUI updates.

Version 2.5.7
-------------

Fixes
~~~~~

* The arcade gui should now respect the current viewport
* Fixed an issue with UILabel allocating large amounts of
  textures over time consuming a lot of memory
* Fixed an issue with the initial viewport sometimes being
  1 pixel too small causing some artifacts
* Fixed a race condition in ``Sound.stop()`` sometimes
  causing a crash
* Fixed an issue in requirements causing issues for poetry
* Fixed an error reporting issue when reaching maximum
  texture size

New Features
~~~~~~~~~~~~

**replit.com**

Arcade should now work out of the box on replit.com. We detect
when arcade runs in replit tweaking various settings. One important
setting we disable is antialiasing since this doesn't work
well with software rendering.

**Alternative Garbage Collection of OpenGL Resources**

``arcade.gl.Context`` now supports an alternative garbage collection mode more
compatible with threaded applications and garbage collection of OpenGL resources.
OpenGL resources can only be accessed or destroyed from the same thread the
window was created. In threaded applications the python garbage collector
can in some cases try to destroy OpenGL objects possibly causing a hard crash.

This can be configured when creating the ``arcade.Window`` passing in a new
``gc_mode`` parameter. By default his parameter is ``"auto"`` providing
the default garbage collection we have in python.

Passing in ``"context_gc"`` on the other hand will move all "dead" OpenGL
objects into ``Context.objects``. These can be garbage collected manually
by calling ``Context.gc()`` in a more controlled way in the the right thread.

Version 2.5.6
-------------

Version 2.5.6 was released 2021-03-28

* Fix issue with PyInstaller and Pymunk not allowing Arcade to work with bundling
* `Fix some PyMunk examples <https://github.com/pythonarcade/arcade/issues/835>`_
* Update some example code. Highlight PyInstaller instructions

Version 2.5.5
-------------

Version 2.5.5 was released 2021-02-23

* `Fix setting an individual sprite list location to a new sprite not working <https://github.com/pythonarcade/arcade/issues/824>`_

Version 2.5.4
-------------

Version 2.5.4 was released 2021-02-19

* `Fix for soloud installer hook <https://github.com/pythonarcade/arcade/issues/816>`_
* Add fishy game on example page
* Fix but around framebuffer creation not properly restoring active frame buffer
* Fix for but where TextureRenderTarget creates FBO twice
* Updated pinned version numbers for dependent libraries
* MyPy fixes
* Minor improvements around SpriteList list operations
* `Fix for physics engine getting stuck on a corner <https://github.com/pythonarcade/arcade/issues/820>`_


Version 2.5.3
-------------

Version 2.5.3 was released 2021-01-27

* `Fix memory leak when removing sprites from sprite list <https://github.com/pythonarcade/arcade/issues/815>`_
* `Fix solitaire example using old hitbox parameter <https://github.com/pythonarcade/arcade/issues/814>`_
* Fix/improve tetris example
* Fix for camera2d.scroll_x

Version 2.5.2
-------------

Version 2.5.2 was released 2020-12-27

* Improve schedule/unschedule docstrings
* Fix Sound.get_length
* Raise error if there are multiple instances of a streaming source
* Fix background music example to match new sound API
* Update main landing page for docs
* Split sprite platformer tutorial into multiple pages
* Add 'related projects' page
* Add 'adventure' sample game link
* Add resources for top-down tank images
* Add turn-and-move example
* Fix name of sandCorner_left.png
* Update tilemap to error out instead of continuing if we can't find a tile
* Improve view tutorial
* Generate error rather than warning if we can't find image or sound file
* Specify timer resolution in Windows

Version 2.5.1
-------------

Version 2.5.1 was released 2020-12-14

* Fix bug with sound where panning wasn't working on Windows machines.
* `Fix for create_lines_with_colors <https://github.com/pythonarcade/arcade/issues/804>`_
* `Fix for pegboard example, coin image too small <https://github.com/pythonarcade/arcade/issues/779>`_
* `Fix for create_ellipse dimensions being too big. <https://github.com/pythonarcade/arcade/issues/756>`_
* `Add visible kwarg to window constructor <https://github.com/pythonarcade/arcade/pull/802>`_
* Fix some type-checking errors found by mypy.
* Update API docs

Version 2.5
-----------

Version 2.5 was released 2020-12-09

(Note, libraries Arcade depends on do not work yet with Python 3.9 on Mac. Mac
users will need to use Python 3.6, 3.7 or 3.8.)

* `Changing to Pyglet from Soloud for Sound <https://github.com/pythonarcade/arcade/pull/746>`_
* `Optimize has_line_of_sight using shapely <https://github.com/pythonarcade/arcade/pull/783>`_
* `Update setuptools configuration to align with PEP 517/518 <https://github.com/pythonarcade/arcade/pull/780>`_
* `Changed algorithm for checking for polygon collisions <https://github.com/pythonarcade/arcade/issues/771>`_
* `Fix incorrect PyInstaller data file path handling docs <https://github.com/pythonarcade/arcade/pull/774>`_
* `Fix for hitbox not scaling <https://github.com/pythonarcade/arcade/issues/752>`_
* `Add support for pyinstaller on Linux <https://github.com/pythonarcade/arcade/issues/800>`_

General

* `SpriteList.draw now supports a blend_function parameter. <https://github.com/pythonarcade/arcade/pull/770>`_
  This opens up for drawing sprites with different blend modes.
* Bugfix: Sprite hit box didn't properly update when changing width or height
* GUI improvements (eruvanos needs to elaborate)
* Several examples was improved
* Improvements to the pyinstaller tutorial
* Better pin versions of depended libraries
* Fix issues with simple and platformer physics engines.

Advanced

* Added support for tessellation shaders
* ``arcade.Window`` now takes a ``gl_version`` parameter
  so users can request a higher OpenGL version than the
  default ``(3, 3)`` version. This only be used to advanced users.
* Bugfix: Geometry's internal vertex count was incorrect when using an index buffer
* We now support 8, 16 and 32 bit index buffers
* Optimized several draw methods by omitting ``tobytes()`` letting
  the buffer protocol do the work
* More advanced examples was added to ``arcade/experimental/examples``

Documentation

* Add :ref:`conway_alpha` example showing how to use alpha to control display
  of sprites in a grid.
* Improve documentation around sound API.
* Improve documentation with FPS and timing stats example :ref:`sprite_collect_coins_with_stats`.
* Improve moving platform docs a bit in :ref:`platformer_tutorial` tutorial.

Version 2.4.3
-------------

Version 2.4.3 was released 2020-09-30

General

* Added PyInstalled hook and tutorial
* ShapeLists should no longer share position between instances
* GUI improvements: new UIImageToggle

Low level rendering api (arcade.gl):

* ArcadeContext now has a load_texture method for creating opengl textures using Pillow.
* Bug: Fixed an issue related to drawing indexed geometry with offset
* Bug: Scissor box not updating when using framebuffer
* Bug: Fixed an issue with pack/unpack alignment for textures
* Bug: Transforming geometry into a target buffer should now work with byte offset
* Bug: Duplicate sprites in 'check_for_collision_with_list' `Issue #763 <https://github.com/pythonarcade/arcade/issues/763>`_
* Improved docstrings in arcade.gl

Version 2.4.2
-------------

Version 2.4.2 was released 2020-09-08

* Enhancement: ``draw_hit_boxes`` new method in ``SpriteList``.
* Enhancement: ``draw_points`` now significantly faster
* Added UIToggle, on/off switch
* Add example showing how to do GPU transformations with the mouse
* Create buttons with default size/position so size can be set after creation.
* Allow checking if a sound is done playing `Issue 728 <https://github.com/pvcraven/arcade/issues/728>`_
* Add an early camera mock-up
* Add ``finish`` method to ``arcade.gl.context``.
* New example arcade.experimental.examples.3d_cube (experimental)
* New example arcade.examples.camera_example
* Improved UIManager.unregister_handlers(), improves multi view setup

* Update ``preload_textures`` method of ``SpriteList`` to actually pre-load textures
* GUI code clean-up `Issue 723 <https://github.com/pvcraven/arcade/issues/723>`_
* Update downloadable .zip for for platformer example code to match current code in documentation.
* Bug Fix: ``draw_point`` calculates wrong point size
* Fixed draw_points calculates wrong point size
* Fixed create_line_loop for thickness !=
* Fixed pixel scale for offscreen framebuffers and read()
* Fixed SpriteList iterator is stateful
* Fix for pixel scale in offscreen framebuffers
* Fix for UI tests
* Fix issues with FBO binding
* Cleanup Remove old examples and code


Version 2.4
-----------

Arcade 2.4.1 was released 2020-07-13.

Arcade version 2.4 is a major enhancement release to Arcade.

.. image:: ../examples/light_demo.png
    :width: 30%
    :class: inline-image
    :target: examples/light_demo.html

.. image:: ../examples/astar_pathfinding.png
    :width: 30%
    :class: inline-image
    :target: examples/astar_pathfinding.html

.. image:: ../examples/bloom_defender.png
    :width: 30%
    :class: inline-image
    :target: examples/bloom_defender.html

.. image:: ../examples/gui_elements.png
    :width: 30%
    :class: inline-image
    :target: examples/gui_elements.html

.. image:: ../tutorials/pymunk_platformer/title_animated_gif.gif
    :width: 30%
    :class: inline-image
    :target: tutorials/pymunk_platformer/index.html

.. image:: ../tutorials/gpu_particle_burst/explosions.gif
    :width: 30%
    :class: inline-image
    :target: tutorials/gpu_particle_burst/index.html

.. image:: ../tutorials/card_game/animated.gif
    :width: 30%
    :class: inline-image
    :target: tutorials/card_game/index.html

.. image:: ../examples/transform_feedback.png
    :width: 30%
    :class: inline-image
    :target: examples/transform_feedback.html

Version 2.4 Major Features
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Support for defining your own frame buffers, shaders, and more
  advanced OpenGL programming. New API in Arcade Open GL.

    * Support to render to frame buffer, then re-render.
    * Use frame buffers to create a 'glow' or 'bloom' effect: :ref:`bloom_defender`.
    * Use frame-buffers to support lights: :ref:`light_demo`.

* New support for style-able GUI elements. New API in :ref:`arcade-api-gui`.

    * Example: :ref:`gui_elements`
    * Example: :ref:`gui_custom_style`

* PyMunk engine for platformers. See tutorial: :ref:`pymunk_platformer_tutorial`.
* AStar algorithm for finding paths. See
  :data:`~arcade.astar_calculate_path` and :data:`~arcade.AStarBarrierList`.

  * For an example of using the A-Star algorithm, see :ref:`astar_pathfinding`.


Version 2.4 Minor Features
~~~~~~~~~~~~~~~~~~~~~~~~~~

**New functions/classes:**

* Added `get_display_size() <arcade.html#arcade.get_display_size>`_ to get
  resolution of the monitor
* Added `Window.center_window() <arcade.html#arcade.Window.center_window>`_ to
  center the window on the monitor.
* Added `has_line_of_sight() <arcade.html#arcade.has_line_of_sight>`_ to
  calculate if there is line-of-sight between two points.
* Added `SpriteSolidColor <arcade.html#arcade.SpriteSolidColor>`_
  class that makes a solid-color rectangular sprite.
* Added `SpriteCircle <arcade.html#arcade.SpriteCircle>`_
  class that makes a circular sprite, either solid or with a fading gradient.
* Added :data:`~arcade.get_distance` function to get the distance between two points.

**New functionality:**

* Support for logging. See :ref:`logging`.
* Support volume and pan arguments in `play_sound <arcade.html#arcade.play_sound>`_
* Add ability to directly assign items in a sprite list. This is particularly
  useful when re-ordering sprites for drawing.
* Support left/right/rotated sprites in tmx maps generated by the Tiled Map Editor.
* Support getting tmx layer by path, making it less likely reading in a tmx file
  will have directory confusion issues.
* Add in font searching code if we can't find default font when drawing text.
* Added :data:`arcade.Sprite.draw_hit_box` method to draw a hit box outline.
* The :data:`arcade.Texture` class, :data:`arcade.Sprite` class, and
  :data:`arcade.tilemap.process_layer` take in ``hit_box_algorithm`` and
  ``hit_box_detail`` parameters for hit box calculation.

.. figure:: ../images/hit_box_algorithm_none.png
   :width: 40%

   hit_box_algorithm = "None"

.. figure:: ../images/hit_box_algorithm_simple.png
   :width: 55%

   hit_box_algorithm = "Simple"

.. figure:: ../images/hit_box_algorithm_detailed.png
   :width: 75%

   hit_box_algorithm = "Detailed"


Version 2.4 Under-the-hood improvements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**General**

* Simple Physics engine is less likely to 'glitch' out.
* Anti-aliasing should now work on windows if ``antialiasing=True``
  is passed in the window constructor.
* Major speed improvements to drawing of shape primitives, such as lines, squares,
  and circles by moving more of the work to the graphics processor.
* Speed improvements for sprites including gpu-based sprite culling (don't draw sprites outside the screen).
* Speed improvements due to shader caching. This should be especially noticeable on Mac OS.
* Speed improvements due to more efficient ways of setting rendering states such as projection.
* Speed improvements due to less memory copying in the lower level rendering API.

**OpenGL API**

A brand new low level rendering API wrapping OpenGL 3.3 core was added in this release.
It's loosely based on the `ModernGL <https://github.com/moderngl/moderngl>`_ API,
so ModernGL users should be able to pick it up fast.
This API is used by arcade for all the higher level drawing functionality, but
can also be used by end users to really take advantage of their GPU. More
guides and tutorials around this is likely to appear in the future.

A simplified list of features in the new API:

* A :py:class:`~arcade.gl.Context` and :py:class:`arcade.ArcadeContext` object was
  introduced and can be found through the ``window.ctx`` property.
  This object offers methods to create opengl resources such as textures,
  programs/shaders, framebuffers, buffers and queries. It also has shortcuts for changing
  various context states. When working with OpenGL in arcade you are encouraged to use
  ``arcade.gl`` instead of ``pyglet.gl``. This is important as the context is doing
  quite a bit of bookkeeping to make our life easier.
* New :py:class:`~arcade.gl.Texture` class supporting a wide variety of formats such as 8/16/32 bit
  integer, unsigned integer and float values. New convenient methods and properties
  was also added to change filtering, repeat mode, read and write data, building mipmaps etc.
* New :py:class:`~arcade.gl.Buffer` class with methods for manipulating data such as
  simple reading/writing and copying data from other buffers. This buffer can also
  now be bound as a uniform buffer object.
* New :py:class:`~arcade.gl.Framebuffer` wrapper class making us able to render any content into
  one more more textures. This opens up for a lot of possibilities.
* The :py:class:`~arcade.gl.Program` has been expanded to support geometry shaders and transform feedback
  (rendering to a buffer instead of a screen). It also exposes a lot of new
  properties due to much more details introspection during creation.
  We also able to assign binding locations for uniform blocks.
* A simple glsl wrapper/parser was introduced to sanity check the glsl code,
  inject preprocessor values and auto detect out attributes (used in transforms).
* A higher level type :py:class:`~arcade.gl.Geometry` was introduced to make working with
  shaders/programs a lot easier. It supports using a subset of attributes
  defined in your buffer description by inspecting the the program's attributes
  generating and caching compatible variants internally.
* A :py:class:`~arcade.gl.Query` class was added for easy access to low level
  measuring of opengl rendering calls. We can get the number samples written,
  number of primitives processed and time elapsed in nanoseconds.
* Added support for the buffer protocol. When ``arcade.gl`` requires byte data
  we can also pass objects like numpy array of pythons ``array.array`` directly
  not having to convert this data to bytes.

Version 2.4 New Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* New Tutorial: :ref:`pymunk_platformer_tutorial`
* New Tutorial: :ref:`view-tutorial`
* New Tutorial: :ref:`solitaire_tutorial`
* New Tutorial: :ref:`gpu_particle_burst`
* Several new and updated examples on :ref:`example-code`
* `New performance testing project <https://craven-performance-testing.s3-us-west-2.amazonaws.com/index.html>`_
* A lot of improvements to https://learn.arcade.academy
* `Instructional videos <https://www.youtube.com/playlist?list=PLUjR0nhln8uaI277eQfKkM8Nhp-xARriu>`_
  added to for https://learn.arcade.academy

Version 2.4 'Experimental'
~~~~~~~~~~~~~~~~~~~~~~~~~~

There is now an ``arcade.experimental`` module that holds code still under
development. Any code in this module might still have API changes.

Special Thanks
~~~~~~~~~~~~~~

Special thanks to `Einar Forselv <https://github.com/einarf>`_ and
`Maic Siemering <https://github.com/eruvanos>`_ for their significant work in helping
put this release together.

Version 2.3.15
--------------

*Release Date: Apr-14-2020*

* Bug Fix: Fix invalid empty text width `Issue 633 <https://github.com/pvcraven/arcade/issues/633>`_
* Bug Fix: Make sure file name is string before checking resources `Issue 636 <https://github.com/pvcraven/arcade/issues/636>`_
* Enhancement: Implement Size and Rotation for Tiled Objects `Issue 638 <https://github.com/pvcraven/arcade/issues/638>`_
* Documentation: Fix incorrect link to 'sprites following player' example

Version 2.3.14
--------------

*Release Date: Apr-9-2020*

* Bug Fix: Another attempt at fixing sprites with different dimensions added to
  same SpriteList didn't display correctly `Issue 630 <https://github.com/pvcraven/arcade/issues/630>`_
* Add lots of unit tests around Sprites and texture loading.

Version 2.3.13
--------------

*Release Date: Apr-8-2020*

* Bug Fix: Sprites with different dimensions added to same SpriteList didn't display correctly `Issue 630 <https://github.com/pvcraven/arcade/issues/630>`_

Version 2.3.12
--------------

*Release Date: Apr-8-2020*

* Enhancement: Support more textures in a SpriteList `Issue 332 <https://github.com/pvcraven/arcade/issues/332>`_

Version 2.3.11
--------------

*Release Date: Apr-5-2020*

* Bug Fix: Fix procedural_caves_bsp.py
* Bug Fix: Improve Windows install docs `Issue 623 <https://github.com/pvcraven/arcade/issues/623>`_


Version 2.3.10
--------------

*Release Date: Mar-31-2020*

* Bug Fix: Remove unused AudioStream and PlaysoundException from __init__
* Remove attempts to load ffmpeg library
* Add background music example
* Bug Fix: Improve Windows install docs `Issue 619 <https://github.com/pvcraven/arcade/issues/619>`_
* Add tutorial on edge artifacts `Issue 418 <https://github.com/pvcraven/arcade/issues/418>`_
* Bug Fix: Can't remove sprite from multiple lists `Issue 621 <https://github.com/pvcraven/arcade/issues/621>`_
* Several documentation updates

Version 2.3.9
-------------

*Release Date: Mar-25-2020*

* Bug Fix: Fix for calling SpriteList.remove `Issue 613 <https://github.com/pvcraven/arcade/issues/613>`_
* Bug Fix: get_image not working correctly on hi-res macs `Issue 594 <https://github.com/pvcraven/arcade/issues/594>`_
* Bug Fix: Fix for "shiver" in simple physics engine `Issue 614 <https://github.com/pvcraven/arcade/issues/614>`_
* Bug Fix: Fix for create_line_strip `Issue 616 <https://github.com/pvcraven/arcade/issues/616>`_
* Bug Fix: Fix for volume control `Issue 610 <https://github.com/pvcraven/arcade/issues/610>`_
* Bug Fix: Fix for loading SoLoud under Win64 `Issue 615 <https://github.com/pvcraven/arcade/issues/615>`_
* Fix jumping/falling texture in platformer example
* Add tests for gui.theme `Issue 605 <https://github.com/pvcraven/arcade/issues/605>`_
* Fix bad link to arcade.color docs

Version 2.3.8
-------------

*Release Date: Mar-09-2020*

* Major enhancement to sound. Uses SoLoud cross-platform library. New features include
  support for sound volume, sound stop, and pan left/right.

Version 2.3.7
-------------

*Release Date: Feb-27-2020*

* Bug Fix: If setting color of sprite with 4 ints, also set alpha
* Enhancement: Add image for code page 437
* Bug Fix: Fixes around hit box calcs `Issue 601 <https://github.com/pvcraven/arcade/issues/601>`_
* Bug Fix: Fixes for animated tiles and loading animated tiles from tile maps `Issue 603 <https://github.com/pvcraven/arcade/issues/603>`_

Version 2.3.6
-------------

*Release Date: Feb-17-2020*

* Enhancement: Add texture transformations `Issue 596 <https://github.com/pvcraven/arcade/issues/596>`_
* Bug Fix: Fix off-by-one issue with default viewport
* Bug Fix: Arcs are drawn double-sized `Issue 598 <https://github.com/pvcraven/arcade/issues/598>`_
* Enhancement: Add ``get_sprites_at_exact_point`` function
* Enhancement: Add code page 437 to default resources

Version 2.3.5
-------------

*Release Date: Feb-12-2020*

* Bug Fix: Calling sprite.draw wasn't drawing the sprite if scale was 1 `Issue 575 <https://github.com/pvcraven/arcade/issues/575>`_
* Add unit test for Issue 575
* Bug Fix: Changing sprite scale didn't cause sprite to redraw in new scale `Issue 588 <https://github.com/pvcraven/arcade/issues/588>`_
* Add unit test for Issue 588
* Enhancement: Simplify using built-in resources `Issue 576 <https://github.com/pvcraven/arcade/issues/576>`_
* Fix for failure on on_resize(), which pyglet was quietly ignoring
* Update ``rotate_point`` function to make it more obvious it takes degrees


Version 2.3.4
-------------

*Release Date: Feb-08-2020*

* Bug Fix: Sprites weren't appearing `Issue 585 <https://github.com/pvcraven/arcade/issues/585>`_


Version 2.3.3
-------------

*Release Date: Feb-08-2020*

* Bug Fix: set_scale checks height rather than scale `Issue 578 <https://github.com/pvcraven/arcade/issues/578>`_
* Bug Fix: Window flickers for drawing when not derived from Window class `Issue 579 <https://github.com/pvcraven/arcade/issues/579>`_
* Enhancement: Allow joystick selection in dual-stick shooter `Issue 571 <https://github.com/pvcraven/arcade/issues/571>`_
* Test coverage reporting now working correctly with TravisCI
* Improved test coverage
* Improved documentation and typing with Texture class
* Improve minimal View example

Version 2.3.2
-------------

*Release Date: Feb-01-2020*

* Remove scale as a parameter to load_textures because it is not unused
* Improve documentation
* Add example for acceleration/friction

Version 2.3.1
-------------

*Release Date: Jan-30-2020*

* Don't auto-update sprite hit box with animated sprite
* Fix issues with sprite.draw
* Improve error message given when trying to do a collision check and there's no
  hit box set on the sprite.

Version 2.3.0
-------------

*Release Date: Jan-30-2020*

* Backwards Incompatability: arcade.Texture no longer has a scale property. This
  property made things confusing as Sprites had their own scale attribute. This
  seemingly small change required a lot of rework around sprites, sprite lists,
  hit boxes, and drawing of textured rectangles.
* Include all the things that were part of 2.2.8, but hopefully working now.
* Bug Fix: Error when calling Sprite.draw() `Issue 570 <https://github.com/pvcraven/arcade/issues/570>`_
* Enhancement: Added Sprite.draw_hit_box to visually draw the hit box. (Kind of slow, but useful for debugging.)

Version 2.2.9
-------------

*Release Date: Jan-28-2020*

* Roll back to 2.2.7 because bug fixes in 2.2.8 messed up scaling

Version 2.2.8
-------------

*Release Date: Jan-27-2020*

* Version number now contained in one file, rather than three.
* Enhancement: Move several GitHub-listed enhancements to the .rst enhancement list
* Bug Fix: Texture scale not accounted for when getting height `Issue 516 <https://github.com/pvcraven/arcade/issues/516>`_
* Bug Fix: Issue with text cut off if it goes below baseline `Issue 515 <https://github.com/pvcraven/arcade/issues/515>`_
* Enhancement: Allow non-cached texture creation, fixing issue with resizing `Issue 506 <https://github.com/pvcraven/arcade/issues/506>`_
* Enhancement: Physics engine supports rotation
* Bug Fix: Need to better resolve collisions so sprite doesn't get hyper-spaces to new weird spot `Issue 569 <https://github.com/pvcraven/arcade/issues/569>`_
* Bug Fix: Hit box not getting properly created when working with multi-texture player sprite. `Issue 568 <https://github.com/pvcraven/arcade/issues/568>`_
* Bug Fix: Issue with text_sprite and anchor y of top `Issue 567 <https://github.com/pvcraven/arcade/issues/567>`_
* Bug Fix: Issues with documentation

Version 2.2.7
-------------

*Release Date: Jan-25-2020*

* Enhancement: Have draw_text return a sprite `Issue 565 <https://github.com/pvcraven/arcade/issues/565>`_
* Enhancement: Improve speed when changing alpha of text `Issue 563 <https://github.com/pvcraven/arcade/issues/563>`_
* Enhancement: Add dual-stick shooter example `Issue 301 <https://github.com/pvcraven/arcade/issues/301>`_
* Bug Fix: Fix for Pyglet 2.0dev incompatability `Issue 560 <https://github.com/pvcraven/arcade/issues/560>`_
* Bug Fix: Fix broken particle_systems.py example `Issue 558 <https://github.com/pvcraven/arcade/issues/558>`_
* Enhancement: Added mypy check to TravisCI build `Issue 557 <https://github.com/pvcraven/arcade/issues/557>`_
* Enhancement: Fix typing issues `Issue 537 <https://github.com/pvcraven/arcade/issues/537>`_
* Enhancement: Optimize load font in draw_text `Issue 525 <https://github.com/pvcraven/arcade/issues/525>`_
* Enhancement: Reorganize examples
* Bug Fix: get_pixel not working on MacOS `Issue 539 <https://github.com/pvcraven/arcade/issues/539>`_


Version 2.2.6
-------------

*Release Date: Jan-20-2020*

* Bug Fix: particle_fireworks example is not running with 2.2.5 `Issue 555 <https://github.com/pvcraven/arcade/issues/555>`_
* Bug Fix: Sprite.pop isn't reliable `Issue 531 <https://github.com/pvcraven/arcade/issues/531>`_
* Enhancement: Raise error if default font not found on system `Issue 432 <https://github.com/pvcraven/arcade/issues/432>`_
* Enhancement: Add space invaders clone to example list `Issue 526 <https://github.com/pvcraven/arcade/issues/526>`_
* Enhancement: Add sitemap to website
* Enhancement: Improve performance, error handling around setting a sprite's color
* Enhancement: Implement optional filtering parameter to SpriteList.draw `Issue 405 <https://github.com/pvcraven/arcade/issues/405>`_
* Enhancement: Return list of items hit during physics engine update `Issue 401 <https://github.com/pvcraven/arcade/issues/401>`_
* Enhancement: Update resources documentation `Issue 549 <https://github.com/pvcraven/arcade/issues/549>`_
* Enhancement: Add on_update to sprites, which includes delta_time `Issue 266 <https://github.com/pvcraven/arcade/issues/266>`_
* Enhancement: Close enhancement-related github issues and reference them in the new :ref:`enhancement_list`.

Version 2.2.5
-------------

*Release Date: Jan-17-2020*

* Enhancement: Improved speed when rendering non-buffered drawing primitives
* Bug fix: Angle working in radians instead of degrees in 2.2.4 `Issue 552 <https://github.com/pvcraven/arcade/issues/552>`_
* Bug fix: Angle and color of sprite not updating in 2.2.4 `Issue 553 <https://github.com/pvcraven/arcade/issues/553>`_


Version 2.2.4
-------------

*Release Date: Jan-15-2020*

* Enhancement: Moving sprites now 20% more efficient.

Version 2.2.3
-------------

*Release Date: Jan-12-2020*

* Bug fix: Hit boxes not getting updated with rotation and scaling. `Issue 548 <https://github.com/pvcraven/arcade/issues/548>`_
  This update depricates Sprite.points and instead uses Sprint.hit_box and Sprint.get_adjusted_hit_box
* Major internal change around not having ``__init__`` do ``import *`` but
  specifically name everything. `Issue 537 <https://github.com/pvcraven/arcade/issues/537>`_
  This rearranded a lot of files and also reworked the quickindex in documentation.


Version 2.2.2
-------------

*Release Date: Jan-09-2020*

* Bug fix: Arcade assumes tiles in tileset are same sized `Issue 550 <https://github.com/pvcraven/arcade/issues/550>`_

Version 2.2.1
-------------

*Release Date: Dec-22-2019*

* Bug fix: Resource folder not included in distribution `Issue 541 <https://github.com/pvcraven/arcade/issues/541>`_

Version 2.2.0
-------------

*Release Date: Dec-19-2019**

* Major Enhancement: Add built-in resources support `Issue 209 <https://github.com/pvcraven/arcade/issues/209>`_
  This also required many changes to the code samples, but they can be run now without
  downloading separate images.
* Major Enhancement: Auto-calculate hit box points by trimming out the transparency
* Major Enhancement: Sprite sheet support for the tiled map editor works now
* Enhancement: Added ``load_spritesheet`` for loading images from a sprite sheet
* Enhancement: Updates to physics engine to better handle non-rectangular sprites
* Enhancement: Add SpriteSolidColor class, for creating a single-color rectangular sprite
* Enhancement: Expose type hints to modules that depend on arcade via PEP 561
  `Issue 533 <https://github.com/pvcraven/arcade/issues/533>`_
  and `Issue 534 <https://github.com/pvcraven/arcade/issues/534>`_
* Enhancement: Add font_color to gui.TextButton init `Issue 521 <https://github.com/pvcraven/arcade/issues/521>`_
* Enhancement: Improve error messages around loading tilemaps
* Bug fix: Turn on vsync as it sometimes was limiting FPS to 30.
* Bug fix: get_tile_by_gid() incorrectly assumes tile GID cannot exceed tileset length `Issue 527 <https://github.com/pvcraven/arcade/issues/527>`_
* Bug fix: Tiles in object layers not placed properly `Issue 536 <https://github.com/pvcraven/arcade/issues/536>`_
* Bug fix: Typo when loading font `Issue 518 <https://github.com/pvcraven/arcade/issues/518>`_
* Updated ``requirements.txt`` file
* Add robots.txt to documentation

Please also update pyglet, pyglet_ffmpeg2, and pytiled_parser libraries.

Special tanks to Jon Fincher, Mr. Gallo, SirGnip, lubie0kasztanki, and EvgeniyKrysanoc
for their contributions to this release.


Version 2.1.7
-------------

* Enhancement: Tile set support. `Issue 511 <https://github.com/pvcraven/arcade/issues/511>`_
* Bug fix, search file tile images relative to tile map. `Issue 480 <https://github.com/pvcraven/arcade/issues/480>`_


Version 2.1.6
-------------

* Fix: Lots of fixes around positioning and hitboxes with tile maps  `Issue 503 <https://github.com/pvcraven/arcade/issues/503>`_
* Documentation updates, particularly using `on_update` instead of `update` and
  `remove_from_sprite_lists` instead of `kill`. `Issue 381 <https://github.com/pvcraven/arcade/issues/381>`_
* Remove/adjust some examples using csvs for maps

Version 2.1.5
-------------

* Fix: Default font sometimes not pulling on mac  `Issue 488 <https://github.com/pvcraven/arcade/issues/488>`_
* Documentation updates, particularly around examples for animated characters on platformers
* Fix to Sprite class to better support character animation around ladders

Version 2.1.4
-------------

* Fix: Error when importing arcade on Raspberry Pi 4  `Issue 485 <https://github.com/pvcraven/arcade/issues/485>`_
* Fix: Transparency not working in draw functions `Issue 489 <https://github.com/pvcraven/arcade/issues/489>`_
* Fix: Order of parameters in draw_ellipse documentation `Issue 490 <https://github.com/pvcraven/arcade/issues/490>`_
* Raise better error on data classes missing
* Lots of code cleanup from SirGnip `Issue 484 <https://github.com/pvcraven/arcade/pull/484>`_
* New code for buttons and dialog boxes from wamiqurrehman093 `Issue 476 <https://github.com/pvcraven/arcade/pull/476>`_

Version 2.1.3
-------------

* Fix: Ellipses drawn to incorrect dimensions `Issue 479 <https://github.com/pvcraven/arcade/issues/467>`_
* Enhancement: Add unit test for debugging `Issue 478 <https://github.com/pvcraven/arcade/issues/478>`_
* Enhancement: Add more descriptive error when file not found `Issue 472 <https://github.com/pvcraven/arcade/issues/472>`_
* Enhancement: Explicitly state delta time is in seconds `Issue 473 <https://github.com/pvcraven/arcade/issues/473>`_
* Fix: Add missing 'draw' function to view `Issue 470 <https://github.com/pvcraven/arcade/issues/470>`_

Version 2.1.2
-------------

* Fix: Linked to wrong version of Pyglet `Issue 467 <https://github.com/pvcraven/arcade/issues/467>`_

Version 2.1.1
-------------

* Added pytiled-parser as a dependency in setup.py

Version 2.1.0
--------------

* New file reader for tmx files http://arcade.academy/arcade.html#module-arcade.tilemap
* Add new view switching framework http://arcade.academy/examples/index.html#view-management
* Fix and Re-enable TravisCI builds https://travis-ci.org/pvcraven/arcade/builds

* New: Collision methods to Sprite `Issue 434 <https://github.com/pvcraven/arcade/issues/434>`_
* Fix: make_circle_texture `Issue 431 <https://github.com/pvcraven/arcade/issues/431>`_
* Fix: Points drawn as triangles rather than rects `Issue 429 <https://github.com/pvcraven/arcade/issues/429>`_
* Fix: Fix screen update rate issue `Issue 424 <https://github.com/pvcraven/arcade/issues/424>`_
* Fix: Typo `Issue 422 <https://github.com/pvcraven/arcade/issues/422>`_
* Put in exampel Kayzee game
* Fix: Add links to PyCon video `Issue 414 <https://github.com/pvcraven/arcade/issues/414>`_
* Fix: Docstring `Issue 409 <https://github.com/pvcraven/arcade/issues/409>`_
* Fix: Typo `Issue 403 <https://github.com/pvcraven/arcade/issues/403>`_

Thanks to SirGnip, Mr. Gallow, and Christian Clauss for their contributions.

Version 2.0.9
-------------

* Fix: Unable to specify path to .tsx file for tiled spritesheet `Issue 360 <https://github.com/pvcraven/arcade/issues/360>`_
* Fix: TypeError: __init__() takes from 3 to 11 positional arguments but 12 were given in text.py `Issue 373 <https://github.com/pvcraven/arcade/issues/373>`_
* Fix: Test create_line_strip `Issue 379 <https://github.com/pvcraven/arcade/issues/379>`_
* Fix: TypeError: draw_rectangle_filled() got an unexpected keyword argument 'border_width' `Issue 385 <https://github.com/pvcraven/arcade/issues/385>`_
* Fix: See about creating a localization/internationalization example `Issue 391 <https://github.com/pvcraven/arcade/issues/391>`_
* Fix: Glitch when you die in the lava in 09_endgame.py `Issue 392 <https://github.com/pvcraven/arcade/issues/392>`_
* Fix: No default font found on ArchLinux and no error message (includes patch)  `Issue 402 <https://github.com/pvcraven/arcade/issues/402>`_
* Fix: Update docs around batch drawing and array_backed_grid.py example  `Issue 403 <https://github.com/pvcraven/arcade/issues/403>`_

Version 2.0.8
-------------

* Add example code from lixingque
* Fix: Drawing primitives example broke in prior release `Issue 365 <https://github.com/pvcraven/arcade/issues/365>`_
* Update: Improve automated testing of all code examples `Issue 326 <https://github.com/pvcraven/arcade/issues/326>`_
* Update: raspberry pi instructions, although it still doesn't work yet
* Fix: Some buffered draw commands not working `Issue 368 <https://github.com/pvcraven/arcade/issues/368>`_
* Remove yml files for build environments that don't work because of OpenGL
* Update requirement.txt files
* Fix mountain examples
* Better error handling when playing sounds
* Remove a few unused example code files


Version 2.0.7
-------------

* Last release improperly required pyglet-ffmpeg, updated to pyglet-ffmpeg2
* Fix: The alpha value seems NOT work with draw_texture_rectangle `Issue 364 <https://github.com/pvcraven/arcade/issues/364>`_
* Fix: draw_xywh_rectangle_textured error `Issue 363 <https://github.com/pvcraven/arcade/issues/363>`_

Version 2.0.6
-------------

* Improve ffmpeg support. Think it works on MacOS and Windows now. `Issue 350 <https://github.com/pvcraven/arcade/issues/350>`_
* Improve buffered drawing command support
* Improve PEP-8 compliance
* Fix for tiled map reader, `Issue 360 <https://github.com/pvcraven/arcade/issues/360>`_
* Fix for animated sprites `Issue 359 <https://github.com/pvcraven/arcade/issues/359>`_
* Remove unused avbin library for mac

Version 2.0.5
-------------

* Issue if scale is set for a sprite that doesn't yet have a texture set. `Issue 354 <https://github.com/pvcraven/arcade/issues/354>`_
* Fix for ``Sprite.set_position`` not working. `Issue 356 <https://github.com/pvcraven/arcade/issues/354>`_

Version 2.0.4
-------------

* Fix for drawing with a border width of 1 `Issue 352 <https://github.com/pvcraven/arcade/issues/352>`_

Version 2.0.3
-------------

Version 2.0.2 was compiled off the wrong branch, so it had a bunch of untested
code. 2.0.3 is what 2.0.2 was supposed to be.

Version 2.0.2
-------------

* Fix for loading a wav file `Issue 344 <https://github.com/pvcraven/arcade/issues/344>`_
* Fix Linux only getting 30 fps `Issue 342 <https://github.com/pvcraven/arcade/issues/342>`_
* Fix error on window creation `Issue 340 <https://github.com/pvcraven/arcade/issues/340>`_
* Fix for graphics cards not supporting multi-sample `Issue 339 <https://github.com/pvcraven/arcade/issues/339>`_
* Fix for set view error on mac `Issue 336 <https://github.com/pvcraven/arcade/issues/336>`_
* Changing scale attribute on Sprite now dynamically changes sprite scale `Issue 331 <https://github.com/pvcraven/arcade/issues/331>`_

Version 2.0.1
-------------

* Turn on multi-sampling so lines could be anti-aliased
  `Issue 325 <https://github.com/pvcraven/arcade/issues/325>`_

Version 2.0.0
-------------

Released 2019-03-10

Lots of improvements in 2.0.0. Too many to list, but the two main improvements:

* Using shaders for sprites, making drawing sprites incredibly fast.
* Using ffmpeg for sound.

Version 1.3.7
-------------

Released 2018-10-28

* Fix for `Issue 275 <https://github.com/pvcraven/arcade/issues/275>`_ where sprites can get blurry.


Version 1.3.6
-------------

Released 2018-10-10

* Bux fix for spatial hashing
* Implement commands for getting a pixel, and image from screen

Version 1.3.5
-------------

Released 08-23-2018

Bug fixes for spatial hashing and sound.

Version 1.3.4
-------------

Released 28-May-2018

New Features
~~~~~~~~~~~~

* `Issue 197 <https://github.com/pvcraven/arcade/issues/197>`_: Add new set of color names that match CSS color names
* `Issue 203 <https://github.com/pvcraven/arcade/issues/203>`_: Add on_update as alternative to update
* Add ability to read .tmx files.

Bug Fixes
~~~~~~~~~

* `Issue 159 <https://github.com/pvcraven/arcade/issues/159>`_: Fix array backed grid buffer example
* `Issue 177 <https://github.com/pvcraven/arcade/issues/177>`_: Kind of fix issue with gi sound library
* `Issue 180 <https://github.com/pvcraven/arcade/issues/180>`_: Fix up API docs with sound
* `Issue 198 <https://github.com/pvcraven/arcade/issues/198>`_: Add start of isometric tile support
* `Issue 210 <https://github.com/pvcraven/arcade/issues/210>`_: Fix bug in MacOS sound handling
* `Issue 213 <https://github.com/pvcraven/arcade/issues/213>`_: Update code with gi streamer
* `Issue 214 <https://github.com/pvcraven/arcade/issues/214>`_: Fix issue with missing images in animated sprites
* `Issue 216 <https://github.com/pvcraven/arcade/issues/216>`_: Fix bug with venv
* `Issue 222 <https://github.com/pvcraven/arcade/issues/222>`_: Fix get_window when using a Window class

Documentation
~~~~~~~~~~~~~

* `Issue 217 <https://github.com/pvcraven/arcade/issues/217>`_: Fix typo in doc string
* `Issue 198 <https://github.com/pvcraven/arcade/issues/198>`_: Add example showing start of isometric tile support


Version 1.3.3
-------------

Released 2018-May-05

New Features
~~~~~~~~~~~~

* `Issue 184 <https://github.com/pvcraven/arcade/issues/184>`_: For sound, wav, mp3, and ogg should work on Linux and Windows. wav and mp3 should work on Mac.

Updated Examples
~~~~~~~~~~~~~~~~

* Add happy face drawing example

Version 1.3.2
-------------

Released 2018-Apr-20

New Features
~~~~~~~~~~~~

* `Issue 189 <https://github.com/pvcraven/arcade/issues/189>`_: Add spatial hashing for faster collision detection
* `Issue 191 <https://github.com/pvcraven/arcade/issues/191>`_: Add function to get the distance between two sprites
* `Issue 192 <https://github.com/pvcraven/arcade/issues/192>`_: Add function to get closest sprite in a list to another sprite
* `Issue 193 <https://github.com/pvcraven/arcade/issues/193>`_: Improve decorator support

Updated Documentation
~~~~~~~~~~~~~~~~~~~~~

* Link the class methods in the quick index to class method documentation
* Add mountain midpoint displacement example
* Improve CSS
* Add "Two Worlds" example game

Updated Examples
~~~~~~~~~~~~~~~~

* Update ``sprite_collect_coints_move_down.py`` to not use ``all_sprites_list``
* Update ``sprite_bullets_aimed.py`` to add a warning about how to manage text on a scrolling screen
* `Issue 194 <https://github.com/pvcraven/arcade/issues/194>`_: Fix for calculating distance traveled in scrolling examples

Version 1.3.1
-------------

Released 2018-Mar-31

New Features
~~~~~~~~~~~~

* Update ``create_rectangle`` code so that it uses color buffers to improve performance
* `Issue 185 <https://github.com/pvcraven/arcade/issues/185>`_: Add support for repeating textures
* `Issue 186 <https://github.com/pvcraven/arcade/issues/186>`_: Add support for repeating textures on Sprites
* `Issue 184 <https://github.com/pvcraven/arcade/issues/184>`_: Improve sound support
* `Issue 180 <https://github.com/pvcraven/arcade/issues/180>`_: Improve sound support
* Work on improving sound support

Updated Documentation
~~~~~~~~~~~~~~~~~~~~~
* Update quick-links on homepage of http://arcade.academy
* Update Sprite class documentation
* Update copyright date to 2018

Updated Examples
~~~~~~~~~~~~~~~~

* Update PyMunk example code to use keyboard constants rather than hard-coded values
* New sample code showing how to avoid placing coins on walls when randomly placing them
* Improve listing/organization of sample code
* Work at improving sample code, specifically try to avoid using ``all_sprites_list``
* Add PyMunk platformer sample code
* Unsuccessful work at getting TravisCI builds to work
* Add new sample for using shape lists
* Create sample code showing difference in speed when using ShapeLists.
* `Issue 182 <https://github.com/pvcraven/arcade/issues/182>`_: Use explicit imports in sample PyMunk code
* Improve sample code for using a graphic background
* Improve collect coins example
* New sample code for creating caves using cellular automata
* New sample code for creating caves using Binary Space Partitioning
* New sample code for explosions

Version 1.3.0
-------------

Released 2018-February-11.

Enhancements
~~~~~~~~~~~~

* `Issue 126 <https://github.com/pvcraven/arcade/issues/126>`_: Initial support for decorators.
* `Issue 167 <https://github.com/pvcraven/arcade/issues/167>`_: Improve audio support.
* `Issue 169 <https://github.com/pvcraven/arcade/issues/169>`_: Code cleanup in SpriteList.move()
* `Issue 174 <https://github.com/pvcraven/arcade/issues/174>`_: Support for gradients.

Version 1.2.5
-------------

Released 2017-December-29.

Bug Fixes
~~~~~~~~~

* `Issue 173 <https://github.com/pvcraven/arcade/issues/173>`_: JPGs not included in examples

Enhancements
~~~~~~~~~~~~

* `Issue 171 <https://github.com/pvcraven/arcade/issues/171>`_: Clean up sprite list code



Version 1.2.4
-------------

Released 2017-December-23.

Bug Fixes
~~~~~~~~~

* `Issue 170 <https://github.com/pvcraven/arcade/issues/170>`_: Unusually high CPU

Version 1.2.3
-------------

Released 2017-December-20.

Bug Fixes
~~~~~~~~~

* `Issue 44 <https://github.com/pvcraven/arcade/issues/44>`_: Improve wildcard imports
* `Issue 150 <https://github.com/pvcraven/arcade/issues/150>`_: "Shapes" example refers to chapter that does not exist
* `Issue 157 <https://github.com/pvcraven/arcade/issues/157>`_: Different levels example documentation hook is messed up.
* `Issue 160 <https://github.com/pvcraven/arcade/issues/160>`_: sprite_collect_coins example fails to run
* `Issue 163 <https://github.com/pvcraven/arcade/issues/163>`_: Some examples aren't loading images

Enhancements
~~~~~~~~~~~~

* `Issue 84 <https://github.com/pvcraven/arcade/issues/84>`_: Allow quick running via -m
* `Issue 149 <https://github.com/pvcraven/arcade/issues/149>`_: Need better error message with check_for_collision
* `Issue 151 <https://github.com/pvcraven/arcade/issues/151>`_: Need example showing how to go between rooms
* `Issue 152 <https://github.com/pvcraven/arcade/issues/152>`_: Standardize name of main class in examples
* `Issue 154 <https://github.com/pvcraven/arcade/issues/154>`_: Improve GitHub compatibility
* `Issue 155 <https://github.com/pvcraven/arcade/issues/155>`_: Improve readme documentation
* `Issue 156 <https://github.com/pvcraven/arcade/issues/156>`_: Clean up root folder
* `Issue 162 <https://github.com/pvcraven/arcade/issues/162>`_: Add documentation with performance tips
* `Issue 164 <https://github.com/pvcraven/arcade/issues/164>`_: Create option for a static sprite list where we don't check to see if things moved.
* `Issue 165 <https://github.com/pvcraven/arcade/issues/165>`_: Improve error message with physics engine

Version 1.2.2
-------------

Released 2017-December-02.

Bug Fixes
~~~~~~~~~

* `Issue 143 <https://github.com/pvcraven/arcade/issues/143>`_: Error thrown when using scroll wheel
* `Issue 128 <https://github.com/pvcraven/arcade/issues/128>`_: Fix infinite loop in physics engine
* `Issue 127 <https://github.com/pvcraven/arcade/issues/127>`_: Fix bug around warning with Python 3.6 when imported
* `Issue 125 <https://github.com/pvcraven/arcade/issues/125>`_: Fix bug when creating window on Linux

Enhancements
~~~~~~~~~~~~
* `Issue 147 <https://github.com/pvcraven/arcade/issues/147>`_: Fix bug building documentation where two image files where specified incorrectly
* `Issue 146 <https://github.com/pvcraven/arcade/issues/146>`_: Add release notes to documentation
* `Issue 144 <https://github.com/pvcraven/arcade/issues/144>`_: Add code to get window and viewport dimensions
* `Issue 139 <https://github.com/pvcraven/arcade/issues/139>`_: Add documentation on what ``collision_radius`` is
* `Issue 131 <https://github.com/pvcraven/arcade/issues/131>`_: Add example code on how to do full-screen games
* `Issue 113 <https://github.com/pvcraven/arcade/issues/113>`_: Add example code showing enemy turning around when hitting a wall
* `Issue 67 <https://github.com/pvcraven/arcade/issues/67>`_: Improved support and documentation for joystick/game controllers

