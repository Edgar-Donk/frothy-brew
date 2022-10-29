==================
Joining RGB to HSV
==================

.. figure :: ../figures/combinedrgbhsv.webp
    :width: 509
    :height: 341 
    :alt: combined rgb and hsv
    :align: center

First ensure that the HSV schema fits together with the RGB schema. As none 
of the HSV widgets have a name clash with the RGB widgets it should be 
fairly straightforward. Copy the file 07entryscalemod.py as our start point,
into this file bring in the hsv standalone functions.

Import the math functions. Remove LerpHex, add circle, hue_gradient, 
hsv_to_rgb, polar2cart, cart2polar and replace sb_okay. Modify the Spinboxes 
to include the upper limit 255 and change the handle functions to make the 
tk variable an integer. Test the rgb side.

TtkScale remains the same. Change the class name RgbSeleect to RgbHsvSelect,
add the hsv tk variables, add the wheel constants, add the initial settings 
for hsv tkvariables. Add the hsv handle functions and door_bell. All the
hsv build should be able to be added to the existing build. Add the click 
and drag functions. Add the two check functions. 

Run the program, the rgb side needs to be adjusted to move to the top of
the frame. Change the rgb labelframe to have a sticky 'n', and the opacity 
label frame no longer has self.fr as its parent but the rgb labelframe fr1,
which means it has to be below the blue spacing label and span all 3 
columns.

Join the RGB HSV Output
-----------------------

At present the two sides run independantly, we will have to make an rgb 
change known to hsv and vice versa. We need a supervisory handle that 
receives calls whenever one of the tk variables triggers the
individual handles, or when the hash value is changed. Alpha will not 
trigger a change. Whenever ring is changed we call door_bell which can be
linked to the supervisory handle, overlord. As the hsv side already moves 
the cursor it is only necessary to link the rgb side to the cursor. Remember
that the gradients need to be redrawn by overlord::

        def overlord(self, rgb=None, hsv=None):
        # calls from handles
        if rgb:
            red, green, blue = rgb[0], rgb[1], rgb[2]
            hue, sat, value = rgb_to_hsv(red, green, blue)
            from_colour = hsv_to_rgb(*(hue, 0, value))
            to_colour = hsv_to_rgb(*(hue, 100, value))
            draw_gradient(
                self.scan,
                from_colour,
                to_colour,
                width=self.canvas_w)
            from_colour = hsv_to_rgb(*(hue, sat, 0))
            to_colour = hsv_to_rgb(*(hue, sat, 100))
            draw_gradient(
                self.vcan,
                from_colour,
                to_colour,
                width=self.canvas_w)
            self.hvar.set(hue)
            self.svar.set(sat)
            self.vvar.set(value)
            X, Y = polar2cart(hue, sat, self.wheel_w, self.wheel_iw)
            ring_radius = self.ring_radius
            for i in self.can_hsv.find_withtag("ring"):
                        self.can_hsv.coords(
                        i,
                        X - ring_radius,
                        Y - ring_radius,
                        X + ring_radius,
                        Y + ring_radius)
            
        elif hsv:
            hue, sat, value = hsv[0], hsv[1], hsv[2]
            red, green, blue = hsv_to_rgb(hue, sat, value)
            draw_agradient(self.acan, (127, 127, 127),
                           (red, green, blue), width=self.canvas_w)
            alpha = self.avar.get()
            vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)
            draw_gradient(self.rcan, (0, green, blue),
                          (255, green, blue), width=self.canvas_w)
            draw_gradient(self.gcan, (red, 0, blue),
                          (red, 255, blue), width=self.canvas_w)
            draw_gradient(self.bcan, (red, green, 0),
                          (red, green, 255), width=self.canvas_w)
            self.evar.set(rgb2hash(red, green, blue))
            self.rvar.set(red)
            self.gvar.set(green)
            self.bvar.set(blue)

A typical call to overlord would be::

    self.overlord(hsv=(hue, sat, value))

.. note:: It is important not to have changes creating feedback from 
    one side to the other. Make sure that updating the tk 
    variables does not propagate further changes. 

We require a function to convert rgb to hsv, this is also copied from 
colorsys with a normalised input and a denormalised output::

    rgb_to_hsv(red, green, blue):
        red = min(max(red, 0), 255) / 255
        green = min(max(green, 0), 255) / 255
        blue = min(max(blue, 0), 255) / 255
        maxc = max(red, green, blue)
        minc = min(red, green, blue)
        value = maxc
        if minc == maxc:
            return 0.0, 0.0, value
        sat = int(((maxc - minc) / maxc) * 100 + 0.5)
        rc = (maxc - red) / (maxc - minc)
        gc = (maxc - green) / (maxc - minc)
        bc = (maxc - blue) / (maxc - minc)
        if red == maxc:
            hue = bc - gc
        elif green == maxc:
            hue = 2.0 + rc - bc
        else:
            hue = 4.0 + gc - rc
        hue = (hue / 6.0) % 1.0
        
        return int(hue * 360 + 0.5), sat, int(value * 100 + 0.5)

Next we wish to change labels from tkinter to a themed type, so that they 
blend in with the background. 

Run this and you should see the cursor move when either the hsv side or rgb
side is altered. Any change to the rgb or hsv scales should result in 
gradient and final colour changes on both sides - quite fun really.

Related RGB HSV Colours
-----------------------

When picking colours it often is useful to have related colours. Just using 
RGB this would be a problem, with HSV we can use a constant hue, then adjust
saturation and/or value to find colours within the same colour scheme. For
simplicity choose 4 equidistant values for saturation and value. Do not select 
the zero values as it produces either white or black for most colours. Leave 
the one component at its actual value, which should give a better 
approximation to the original selection's family of colours. In addition add
the complementary colour, derived from RGB by subtracting each component from
255, (when a colour is added to its complement it produces white).

Create the nine additional canvases with declarative labels and hash value
for each related colour. Place these additional widgets between the two colour
parts, directly below the final colour. The canvasses are filled with the 
calculated colours.

Whenever the final colour changes the related colours are redrawn. Use the 
function overlord to trigger the related function. 

Resizing the Widgets
--------------------

.. sidebar:: Vertical Adjustment

    Similar to horizontal, all we need are ``sticky 'ns'`` and ``rowconfigure``.

If we had been using pack then all the container widgets would need the fill
and expand options suitably filled in, but as we are using the grid management
system, it is a bit more complicated. The horizontal expansion will be 
required. All widgets that will adjust horizontally require a ``sticky 'ew'``
option, so if it has a ``'n'`` it becomes ``'new'``, existing ``'ew'`` stay.
All container widgets also require ``sticky 'ew'``, this does not apply to 
root. We now have to inform all container widgets which columns are required
to expand. In our case the columns containing the gradients and scales for
the colour components need to expand. Columns containing labels or the final
colour and its related colour can stay a constant width. 

.. sidebar:: Resizing Normal Images

    Normal images can be treated in a similar way to our gradients, just that
    the image is read in PIL, the result is resized using LANCZOS 
    resampling whilst the new sizes are determined at the bind function. The
    resized image is reimported into tkinter. 

Use **w.columnconfigure(0, weight=1)** where 0 is the relevant column for the
widget w and weight is the proportionality of expansion for each column. If 
this is omitted the columns cannot adjust when the window is changed in size.
For simple widgets this is all that is needed, but if the widget contains an
image then the image must change at the same rate as the column is being 
changed. The easiest method is to add a bind to the relevant widget, in our
case the Canvas. We require a function to be triggered whenever the 
configuration alters ``w.bind("<Configure>", self.function)``. 

Within 12rgbandhsv.py we can use separate functions for each canvas, so that 
only the relevant gradient is redrawn for each canvas. As each canvas is being 
adjusted sequentially this makes sense. Within the bind function we can 
discover the new width of the canvas, then use this to redraw the gradient.
At the same time remember to change the default canvas width's value. The 
redrawn gradient is then imported as normal into canvas. Ensure that none
of the default widths are reactivated, To prevent the colour wheel being 
changed alter its grid layout, start it from column 0 (the label column), 
centralise it on column 1 by using **columnspan=3**.

As we have changed from fixed sizes to widgets that can expand horizontally
the relative sizes of the canvas and scale alters. Unless corrected
the canvas expands to the size of the scale, 
so add horizontal padding, half the slider length, to the canvas.

.. figure :: ../figures/hsv_related.webp
    :width: 516
    :height: 342 
    :alt: combined rgb and hsv with related colours
    :align: center
    
    Combined RGB and HSV with Related Colours

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 12rgbandhsv.py

    .. literalinclude:: ../examples/colours/12rgbandhsv.py

.. figure :: ../figures/hsv_related_adjusted.webp
    :width: 516
    :height: 342 
    :alt: combined rgb and hsv with related colours after adjustment
    :align: center
    
    Combined RGB and HSV with Related Colours with Adjustment
