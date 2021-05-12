""" Tools for colourpickers

* rgb, hsv and yiq colour systems
"""

from tkinter import PhotoImage
from PIL import Image, ImageDraw, ImageTk
import numpy as np
from math import pi, atan2, degrees, hypot, cos, sin

def  cart2polar(x, y, outer_w, inner_w):
    """Conversion cartesian to polar coordinates
        output hue, ssaturation of hsv; s adjusted

    Parameters
    ----------
    x : int
        horiz coord
    y : int
        vert coord
    outer_w : int
        outside width of colour wheelimage
    inner_w : int
        inner width of colour wheelimage

    Returns
    -------
    degc, sc : float
        degrees, length
    """

    centre = outer_w//2, outer_w//2
    inner = inner_w, inner_w
    radius = min(inner)//2

    dx = x - centre[0]
    dy = y - centre[1]
    deg = int(0.5+degrees(atan2(dy, dx)))
    if deg < 0: deg = 360 + deg
    ray = int(0.5 + hypot(dx, dy) * 100 / radius)
    ray = min(max(ray, 0), 100)
    deg = min(max(deg, 0), 360)

    return deg, ray

def  check(width, height, square_size=4):
    """Draw chequers in numpy as array
        chequer value to grey or white depends on x position

    Parameters
    ----------
    width : int
        canvas width
    height : int
        canvas height
    square_size : int
        size each square

    Returns
    -------
    array : int
        array of integers
    """

    array = np.zeros([height, width, 3], dtype=np.uint8)
    for x in range(width):
        for y in range(height):
            if (x % square_size * 2) // square_size ==\
               (y % square_size * 2) // square_size:
                array[y, x] = 127 - int(0.5 + 127 / width * x)
    return array

def  circle(canvas, x, y, radius, width=None, tags=None, outline=None,
            activeoutline=None):
    """Returns Canvas circle using centre and radius

    Parameters
    ----------
    canvas : str
        handle to canvas
    x : int
        x coord centre
    y : int
        y coord centre
    radius : int
        radius
    width : int
        outside ring
    tags : str
        tags
    outline : str
        colour outside ring
    activeoutline : str
        colour outside ring when mouse on ring
    """

    return canvas.create_oval(x + radius, y + radius, x - radius, y - radius,
                              width=width, tags=tags,
                              activeoutline=activeoutline, outline=outline)

def  draw_agradient(canvas, colour1, colour2, width, height=26):
    """Calls generate_gradient and check, then imports alpha gradient
        into tkinter

    Parameters
    ----------
    canvas : str
        parent widget
    colour1 : tuple of int
        start colour
    colour2 : tuple of int
        end colour
    steps : int
        number steps in gradient
    width : int
        canvas width
    height : int
        canvas height
    """

    arr = generate_gradient(colour1, colour2, height, width)
    arr1 = check(width, height)
    xdata = 'P6 {} {} 255 '.format(
        width, height).encode() + (arr + arr1).tobytes()
    gradient = PhotoImage(width=width, height=height, data=xdata, format='PPM')
    canvas.create_image(0, 0, anchor="nw", image=gradient)
    canvas.image = gradient

def  draw_gradient(canvas, colour1, colour2, width, height=26):
    """Calls generate_gradient, then imports gradient into tkinter

    Parameters
    ----------
    canvas : str
        parent widget
    colour1 : tuple of int
        start colour
    colour2 : tuple of int
        end colour
    steps : int
        number steps in gradient
    width : int
        canvas width
    height : int
        canvas height

    Returns
    -------
    None
    """

    arr = generate_gradient(colour1, colour2, height, width)
    xdata = 'P6 {} {} 255 '.format(width, height).encode() + arr.tobytes()
    gradient = PhotoImage(width=width, height=height, data=xdata, format='PPM')
    canvas.create_image(0, 0, anchor="nw", image=gradient)
    canvas.image = gradient

def  generate_gradient(from_colour, to_colour, height, width):
    """Draw gradient in numpy as array

    Parameters
    ----------
    from_colour : tuple of int
        start colour
    to_colour : tuple of int
        end colour
    height : int
        canvas height
    width : int
        canvas width

    Returns
    -------
    array : int
        array of integers
    """

    new_ch = [np.tile(np.linspace(from_colour[i], to_colour[i], width,
                                  dtype=np.uint8),
                      [height, 1]) for i in range(len(from_colour))]
    return np.dstack(new_ch)

def  hash2rgb(hash_):
    """Conversion hash colour to rgb

    Parameters
    ----------
    hash_ : str
        colour as hash

    Returns
    -------
    rgb : int
        tuple of integers
    """

    hash_ = hash_.strip('#')
    return tuple(int(hash_[i:i+2], 16) for i in (0, 2, 4))

def  hsv_to_rgb(h, s, v):
    """Conversion hsv to rgb
        h 0-360, s & v 0-100

    Parameters
    ----------
    h : int
        hue
    s : int
        saturation
    v : int
        value

    Returns
    -------
    rgb : int
        tuple integers
    """

    h = min(max(h, 0), 360)
    s = min(max(s, 0), 100)
    v = min(max(v, 0), 100)
    h, s, v = h/360.0, s/100.0, v/100.0
    # calculate all 0 รท 1.0
    if s == 0.0:
        v*= 255
        v = int(v)
        return (v, v, v)
    i = int(h*6.)  # XXX assume int() truncates!
    f = (h*6.)-i
    p, q, t = int(255*(v*(1.-s))),\
              int(255*(v*(1.-s*f))),\
              int(255*(v*(1.-s*(1.-f))))
    v*= 255; i%= 6
    v = int(v)
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

def  hue_gradient(canvas, width=300, height=26, steps=360):
    """Returns hue gradient in tkinter canvas

    Parameters
    ----------
    canvas : str
        parent widget
    width : int
        canvas width
    height : int
        canvas height
    steps : int
        steps

    Returns
    -------
    image : int
        array of integers
    """

    image = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(image)

    for i in range(steps):
        x0 = int(float(width * i)/steps)
        x1 = int(float(width * (i+1))/steps)
        draw.rectangle((x0, 0, x1, height), fill=hsv_to_rgb(i, 100, 100))
    gradient = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=gradient)
    canvas.image = gradient

def  is_okay(index, text, input_):  # '%i','%P','%S'
    """Validation for hash, which cannot be removed,
        hex check on input after hash

    Parameters
    ----------
    index : str
        index
    text : str
        text if accepted
    input_ : str
        current input

    Returns
    -------
    various : bool
    """

    index = int(index)  # index is string!
    if index == 0 and text == '#':
        return True
    try:
        int(input_, 16)
        return bool(0 < index < 7)
    except ValueError:  # not a hex
        return False

def  polar2cart(phi, ray, outer_w, inner_w):
    """Conversion polar to cartesian coordinates
        original image 317x317 using inner 299x299 working area,
        ring can be on outer edge wheel, so allow a space around image
        image size used in calculating phi, t from x,y
        phi,t is h,s of hsv, t adjusted

    Parameters
    ----------
    phi : float
        angle
    ray : float
        distance to centre angle
    outer_w : int
        outside width of colour wheelimage
    inner_w : int
        inner width of colour wheelimage

    Returns
    -------
    cartesian : int
        tuple of integers
    """

    centre = outer_w // 2, outer_w // 2
    inner = inner_w, inner_w
    radius = min(inner) // 2
    ray = ray * radius / 100

    dx = ray * cos(phi * pi / 180)
    dy = ray * sin(phi * pi / 180)
    x = centre[0] + dx
    y = centre[1] + dy

    return int(x+0.5), int(y+0.5)

def  rgb2hash(red, green, blue):
    """Convert rgb to hexadecimal

    Parameters
    ----------
    red : int
        red component
    green : int
        green component
    blue : int
        blue component

    Returns
    -------
    hash : str
        hexadecimal colour
    """

    rgb = (red, green, blue)
    return '#%02x%02x%02x' % rgb

def  rgb_to_hsv(red, green, blue):
    """convert rgb to hsv

    Parameters
    ----------
    red : int
        red
    green : int
        Green
    blue : int
        blue

    Returns
    -------
    hsv : int
        tuple of integers
    """

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

def  rgb_to_yiq(red, green, blue):
    """Converts rgb to yiq

    Parameters
    ----------
    red : int
        red
    green : int
        green
    blue : int
        blue

    Returns
    -------
    yiq : float
        tuple of floats
    """

    red = red/255
    green = green/255
    blue = blue/255
    y = 0.30*red + 0.59*green + 0.11*blue
    i = 0.74*(red-y) - 0.27*(blue-y)
    q = 0.48*(red-y) + 0.41*(blue-y)
    i = i/0.599
    q = q/0.5251
    return (y*100, i*100, q*100)

def  sb_okay(action, text, input_, lower, upper):  # '%P','%S'
    """Validation for colour components

    Parameters
    ----------
    action : str
        insertion or deletion
    text : str
        text if accepted
    input_ : str
        current input
    lower : str
        lower limit
    upper : int
        upper limit

    Returns
    -------
    various : bool
    """

    if action == "1":
        if input_.isdigit():
            return bool(int(lower) <= int(text) <= int(upper))
        return False
    return True

def  vcheck(width, height, alpha, square_size=4):
    """Draw vertical chequers in numpy as array
        chequer value to grey or white depends on y position

    Parameters
    ----------
    width : int
        canvas width
    height : int
        canvas height
    alpha : int
        opacity
    square_size : int
        size each square

    Returns
    -------
    array : int
        array of integers
    """

    al0 = 127 - alpha // 2
    ah0 = al0 / height
    array = np.zeros([height, width, 3], dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            if (x % square_size * 2) // square_size == (y % square_size * 2) \
                    // square_size:
                array[y, x] = int(0.5 + ah0 * y)
    return array

def  vdraw_gradient(canvas, colour1, alpha=255, width=30, height=30):
    """Either background fill
        or call vgenerate_gradient then vcheck, import vertical gradient
        into tkinter

    Parameters
    ----------
    canvas : str
        parent widget
    colour1 : tuple of int
        start colour
    alpha : int
        opacity
    width : int
        canvas width
    height : int
        canvas height
    """

    if alpha > 240:
        hash_value = rgb2hash(colour1[0], colour1[1], colour1[2])
        canvas['background'] = hash_value
        canvas.background = hash_value
    else:
        arr = vgenerate_gradient(colour1, alpha, height, width)
        arr1 = vcheck(width, height, alpha)
        xdata = 'P6 {} {} 255 '.format(
            width, height).encode() + (arr + arr1).tobytes()
        gradient = PhotoImage(
            width=width,
            height=height,
            data=xdata,
            format='PPM')
        canvas.create_image(0, 0, anchor="nw", image=gradient)
        canvas.image = gradient

def  vgenerate_gradient(to_colour, alpha, height, width):
    """Draw vertical gradient in numpy as array

    Parameters
    ----------
    to_colour : tuple of int
        end colour
    alpha : int
        opacity
    height : int
        canvas height
    width : int
        canvas width

    Returns
    -------
    array : int
        array of integers
    """

    al0 = alpha / 255
    res0 = 1 - al0
    from_colour = (int(to_colour[0] * al0 + 127 * res0),
                   int(to_colour[1] * al0 + 127 * res0),
                   int(to_colour[2] * al0 + 127 * res0))  # changing from_colour
    new_ch = [np.tile(np.linspace(to_colour[i], from_colour[i], height,
                                  dtype=np.uint8),
                      [width, 1]).T for i in range(3)]
    return np.dstack(new_ch)

def  yiq_okay(action, text, input_, lower, upper):
    """Validation for yiq colour components

    Parameters
    ----------
    action : str
        action
    text : str
        text if accepted
    input_ : str
        current input
    lower, upper : str
        lower and upper limits

    Returns
    -------
    various : bool
    """

    # action=1 -> insert
    if action == "1":
        if input_ in '0123456789.-+':
            return bool(float(lower) <= float(text) <= float(upper))
        return False
    return True

def  yiq_to_rgb(y, i, q):
    """Conversion yiq to rgb
        incoming y 0 to 100, i, q ±100

    Parameters
    ----------
    y : str
        luma
    i, q : str
        chrominance

    Returns
    -------
    rgb : int
        tuple of integers
    """

    # assume I and Q between ±100, correct for coloursys ±1
    y = min(max(y, 0), 100)
    i = min(max(i, -100), 100)
    q = min(max(q, -100), 100)
    y = y/100
    i = 0.599*i/100
    q = 0.5251*q/100

    red = y + 0.9468822170900693*i + 0.6235565819861433*q
    green = y - 0.27478764629897834*i - 0.6356910791873801*q
    blue = y - 1.1085450346420322*i + 1.7090069284064666*q
    red = min(max(red, 0), 1)
    green = min(max(green, 0), 1)
    blue = min(max(blue, 0), 1)

    return (int(red*255+0.5), int(green*255+0.5), int(blue*255+0.5))
