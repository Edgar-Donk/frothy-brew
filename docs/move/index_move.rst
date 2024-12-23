﻿.. _move:

=====================
Moving Canvas Objects
=====================

.. sidebar:: TagOrID

    Objects on a canvas can be referred to either by their ``Tag`` or the ``ID`` 
    generated by tkinter. Tag is the easiest reference method within a script.
    ``TagOrID`` is the nomenclature used in section 8.6
    `"Tkinter 8.5 reference a GUI for Python" <https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/tkinter.pdf>`_


Objects can be moved on a tkinter Canvas. There are two main methods we can
apply based on move and coords. ``move`` identifies the object with the 
``TagOrId`` and requires an
amount that the object is to be moved, whereas ``coords`` uses TagOrId and
its bounding box to a new set of coordinates.

.. toctree::
   :caption: Moving Objects...
   :maxdepth: 1
   
   canvas_coords
   canvas_move