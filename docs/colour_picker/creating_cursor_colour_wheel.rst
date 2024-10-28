======================================
Creating a Cursor for the Colour Wheel
======================================

.. figure :: ../figures/wheelhsv.webp
    :width: 469
    :height: 692 
    :alt: hsv colour wheel added to gradients
    :align: center
    
    Colour Wheel imported to basic hsv

The cursor will be a ring that can be moved over the colour wheel either by
using the left mouse button to drag the cursor or clicking to the 
required position with a mouse. It will be constructed from oval which
normally has a transparent fill and a black outline of width 1 pixel. Using 
the assisting function we can create the circle working directly using centre 
and radius::

    def circle(canvas, x, y, radius, width=None, tags=None, outline=None,
               activeoutline=None):
        return canvas.create_oval(x + radius, y + radius, x - radius, y - radius,
                                  width=width, tags=tags,
                                  activeoutline=activeoutline, outline=outline)
        
It will be necessary to enable tags and change the outline colour when the 
user hovers over the cursor.

Bind the cursor to the left
hand mouse button to enable dragging. When clicking use much the same 
code, but include a clause to find the cursor.

If we were to use ``canvas.move`` we need need to know the amount of movement 
meaning that the actual and final positions need to be known. Using 
``canvas.coords`` only the final position is required, which can be readily 
found from the tkinter 
canvas. Sometimes ``coords`` deforms the image when being 
moved, luckily circle does not have this problem. 

The coordinates of the canvas will be in cartesian, whereas the colour wheel
will show the hue and saturation as polar coordinates. Therefore add
conversions between the two systems::

    def polar2cart(phi, ray, outer_w, inner_w):
        # original image 317x317 using inner 299x299 working area, 
        # ring can be on outer edge wheel, so allow a space around image
        image size used in calculating phi, ray from x,y
        phi, ray is h, s of hsv, ray adjusted

        centre = outer_w // 2, outer_w // 2
        inner = inner_w, inner_w
        radius = min(inner) // 2
        ray = ray * radius / 100

        dx = ray * cos(phi * pi / 180)
        dy = ray * sin(phi * pi / 180)
        x = centre[0] + dx
        y = centre[1] + dy

        return int(x+0.5), int(y+0.5)

    def cart2polar(x, y, outer_w, inner_w):
        # output h,s of hsv; s adjusted
        centre = outer_w // 2, outer_w // 2
        inner = inner_w, inner_w
        radius = min(inner) // 2

        dx = x - centre[0]
        dy = y - centre[1]
        deg = int(0.5 + degrees(atan2(dy, dx)))
        if deg < 0:
            deg = 360 + deg
        ray = int(0.5 + hypot(dx, dy) * 100 / radius)
        ray = min(max(ray, 0), 100)
        deg = min(max(deg, 0), 360)

        return deg, ray

Modifying 08basichsv.py add the required polar conversion functions, the
circle drawing function then import the colour wheel image and place the 
cursor at the right-hand edge level with the centre, corresponding to a hsv
of (0,100,100).

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 10wheelhsv.py

    .. literalinclude:: ../examples/colours/10wheelhsv.py

Next make the cursor interact with the mouse actions.


