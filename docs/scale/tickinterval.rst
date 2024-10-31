==================
Scale Tickinterval
==================

Tickinterval is a bit of a misnomer, since we are dealing with
range values and not small straight lines, ``tickinterval`` is normally 
larger than the ``resolution``.

.. sidebar:: Number of Ticks

    As the range is equally divided the number of ticks will be the answer 
    the difference between ``from_`` and ``to`` divided by the ``tickinterval`` 
    plus one. So if from_=0.0, to=1.0, and tickinterval=0.25 there are
    :math:`(1.0 - 0.0) / 0.25 + 1 = 4 + 1 = 5` ticks.

When a scale is correctly set up the user should see that the centre of the 
slider corresponds to the attributes ``from_`` and ``to`` when the slider is 
pushed to the extreme ends of the trough and the displayed value shows these 
two values. The positioning of the ``ticks`` (value range) should be such 
that the centre of the lowest range value corresponds to the centre of the
slider at its minimum and the highest corresponds to the position of the 
slider centre at its maximum. 

The range values start from the left hand side on the horizontal scale and
from the top on a vertical scale.

.. warning:: Do not be tempted to start the vertical range from the bottom, 
    as any linkages such as with a tkinter variable will want to work as 
    though the scale started from the top.

Placing Range Values
====================

Values of Scale Elements
------------------------

Before we can accurately place the range values we need to know the position
of the slider's halfway line (half the slider length).
The class name for the horizontal scale is 'Horizontal.TSlider', 
the component names are 'trough' and 'slider', and the relevant element names 
are 'borderwidth' and 'sliderlength'. For instance we can query the trough
borderwidth element directly::



    >>> Style.lookup('Horizontal.Scale.trough','borderwidth')
    ## --> 1

while::

    >>> Style.lookup('Horizontal.Scale.slider', 'sliderlength')
    ## --> ''

the last was not particularly useful. In fact these results using the default
theme are better than most, usually even the standard themes return no value
for these two items. Later on we shall be calibrating the range values and 
the location of the current value by finding out the 'borderwidth' and 
'sliderlength'.

If we specify the values using a ``Style.configure()`` method then be aware
that the changes relate to the actual pixel size, even in dpi unaware IDEs. 
When confirming the option ``length`` using ``cget()`` then the length
corresponds to the length in pixels but the display size is for a dpi unaware
situation in Idle and PyScripter.

Horizontal and Vertical Ranges
------------------------------

Allowances should be made for the value lengths, so **-1.00** will be longer 
than **1.00** in a horizontal Scale. If there is a set of negative range 
values then this set will be longer than the corresponding positive set. 
Vertical Scales will not have this problem, but the distances between lines 
and their height must be known. On the face of it the vertical Scale should 
be easier to set up. In earlier scripts a scale length will be guessed at, 
in later scripts this problem will be addressed.

Ranges 
------

.. sidebar:: Standard Ranges

    Note when using ColourPicker and YIQColourPicker they have 
    standard ranges 0 to 100 for HSV and YIQ, 0 to 255 for RGB and 0 to 360 
    for HSV. Special cases are not encountered. 

The range values are made of Labels, that 
use the ``place()`` layout manager, which are incorporated into the Scale 
widget by the layout manager. The placement is made easier as the text is 
placed centrally over each "tick", therefore provided the ticks have been
positioned correctly the range values should look properly positioned, 
irrespective of size. 

Some special ranges should be checked against the tkinter Scale and the 
script adjusted as necessary. 

The slider can only travel a reduced amount compared to the trough length.
The range labels will be placed outside the scale using a relative position. 
As a starting point assume that the tickinterval includes the lowest and 
highest values together with the intermediate values spaced out evenly. Use 
a ``for`` loop with ``range`` to set the range positions::

    for i in range(from_val, to_val + 1, tick_val):
        print('tick', i)

now display the range values::

        item = ttk.Label(root, text=i)
        item.place(in_=scth, bordermode='outside',
                    relx=slider_val / len_val / 2 +
                    i / sc_range * (1 - slider_val / len_val),
                    rely=1, anchor='n')

This gives a reasonably good correlation, but may be slightly innaccurate at
the lowest values. A better estimate would account for the sizes of the 
cursor at the two extremes and the trough border thickness. The travel of the 
slider is from the border thickness plus half the slider length to the length
of the trough minus the border thickness minus half the slider length. This
reduced length is what is available for the range values starting from halfway
along the ``to`` text and halfway along the ``from_`` text.

The number of ticks remains the same - so no change to the ``for`` loop.
However the first tick starts at a slightly different position::

    ((slider_val - from_size) / 2 + bw_val) / len_val

similarly the last value should be modified::

    1 - (slider_val / 2 + bw_val) / len_val

provided the range is large enough to have a tickinterval equal to or larger
than one unit, then this script should be good enough and the only slight
problem is the setting of the slider length value. The problem is exasperated
by how tkinter/ttk work with dpi aware and unaware environments, the length
might be set in one environment but used elsewhere.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 05ttk_tkinter_get.py

    .. literalinclude:: ../examples/scale/05ttk_tkinter_get.py
        :emphasize-lines: 4-14, 25, 29-34, 39, 41, 43-50
