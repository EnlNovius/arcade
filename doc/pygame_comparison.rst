.. _pygame-comparison:

Pygame Comparison
=================

The Python Arcade Library has the same target audience as the well-known
Pygame library. So how do they differ?

Features that the Arcade Library has:

* Licensed under the `MIT License`_, which is more generous than Pygame's LGPL_.
* Draws stationary sprites much faster. See :ref:`drawing_stationary_performance`
* Supports Python 3 `type hinting`_.
* Thick ellipses, arcs, and circles do not have a `moiré pattern`_.
* Ellipses, arcs, and other shapes can be easily rotated.
* Uses standard coordinate system you learned about in math. (0, 0) is in
  the lower left, and not upper left. Y-coordinates are not reversed.
* Has built-in physics engine for platformers.
* Supports animated sprites.
* API documentation for the commands is better.
* Command names are consistent. For example, to add to a sprite list you use the
  ``append()`` method, like any other list in Python. Pygame uses ``add()``.
* Parameter and command names are clearer. For example, open_window instead of
  set_mode.
* Less boiler-plate code than Pygame.
* Basic drawing does not require knowledge on how to define functions or
  classes or how to do loops.
* Encourages separation of logic and display code. Pygame tends to put both into
  the same game loop.
* With the use of sprite lists, uses the acceleration of the graphics card to
  improve performance.
* Easily scale and rotate sprites and graphics.
* Images with transparency are transparent by default. No extra code needed.
* Lots of :ref:`example-code`.


Features that Pygame has that the Arcade Library does not:

* Has better performance for moving sprites
* Python 2 support
* Does not require OpenGL, so works on Raspberry Pis
* Has better support for pixel manipulation in a memory buffer that isn't
  displayed on screen.

Things that are just different:

* Pygame supports SDL2 library from 2.0_. Arcade runs on top of OpenGL 3+ and
  Pyglet. 
* Sound support: Pygame uses the old, unsupported Avbin library.
  Arcade uses SoLoud. Supports panning and volume.

:ref:`performance`.


.. _MIT License: https://github.com/pythonarcade/arcade/blob/development/license.rst
.. _LGPL: https://github.com/pygame/pygame/blob/main/docs/LGPL.txt
.. _type hinting: https://docs.python.org/3/library/typing.html
.. _moiré pattern: http://stackoverflow.com/questions/10148479/artifacts-when-drawing-primitives-with-pygame
.. _2.0: https://github.com/pygame/pygame/releases/tag/2.0.0
