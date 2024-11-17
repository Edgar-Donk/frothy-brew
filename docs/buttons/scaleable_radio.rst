======================
Scaleable Radiobuttons
======================

.. tabularcolumns:: |>{\centering\arraybackslash}\X{1}{5}|>{\centering\arraybackslash}\X{1}{5}

.. list-table::
    :header-rows: 1

    * - Pyscripter unscaled altflex theme
      - Spyder scaled altflex theme

    * - .. figure:: ../figures/buttons/pyscripter_testaltflex.png
                    :width: 243
                    :height: 196

      - .. figure:: ../figures/buttons/Spyder_testaltflex.png
                    :width: 116
                    :height: 171


Drawing the Radiobutton
=======================

Almost everything stated about check buttons can be directly related to 
radiobuttons. How the states interreact is similar except that radiobuttons
have usually only one selection in a group at once, all other radiobuttons
are not selected. Normally it makes sense to enable/disable all the 
radiobutton group at once. 

Drawing the widget is easier as all the borders are curved and can be made 
with pieslices, so
scaling is easier. The theme background is used as the image background,
requiring one more dictionary. Even though the line/pie colours are largely
similar to the checkbutton make a separate dictionary.

As with the check buttons test with an added checkbox to disable/enable one 
of the radiobuttons. When testing without the states (active, selected) and 
active the radiobuttons refused to change state from unselected to selected,
therfore remember to include these states.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* create_radiobuttons.py

    .. literalinclude:: ../examples/buttons/create_radiobuttons.py

.. sidebar:: Creating States by Radiobuttons
    
    As opposed to a dynamic state created using the mouse, click on the
    radiobuttons with the selected states. This method keeps the widget
    static even though in normal usage the state may be transitory, which 
    assists in screenshots.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* RunStatettk.py

    .. literalinclude:: ../examples/buttons/RunStatettk.py

Prove the radiobuttons with a similar script to that with checkbuttons. When
everything works as required almalgamate the check and radiobutton scripts.
So far we have proved the concept, now to change the almalgamated script
into a standalone module. Use one main function ``install``, with a 
subsidiary function ``_load_images``, place the dictionaries **checkimg**, 
**radioimg** in the global space before the two functions, add two more 
dictionaries checkimage and radioimage into the global space. Bring the 
scaling part from the main to the install function. The drawings will now
store the PIL information into checkimage and radioimage dictionaries, then
just before the altflex theme is created, call up _load_images, this will 
convert the PIL information to tkinter readable images and store in checkimg
and radioimg.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* altflex.py

    .. literalinclude:: ../examples/buttons/altflex.py

To test the altflex theme one needs to **import altflex**, run **altflex.install()**
then run **Style.theme_use('altflex')**. The altered widgets can then be tested.
Additional alt widgets are automatically included when using the altflex 
theme and are sized separately as required for dpi awareness.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* test_altflex.py

    .. literalinclude:: ../examples/buttons/test_altflex.py

As can be seen from the test script results (figures at the top of the page)
:ref:`Scaleable Radiobuttons` the check and radiobuttons match in size just 
by scaling.