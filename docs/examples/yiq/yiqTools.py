"""
Standard yiq tools 
rgb2hash
circle
yiq_to_rgb
rgb_to_yiq
generate_gradient
draw_gradient
check
draw_agradient
vcheck
vgenerate_gradient
vdraw_gradient
hash2rgb
yiq_okay
is_okay
sb_okay

"""
from tkinter import PhotoImage
import numpy as np

def rgb2hash(red, green, blue):
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

def circle(canvas, x, y, radius, width=None, tags=None, outline=None,
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

def yiq_to_rgb(y, i, q):
    """Conversion yiq to rgb
        incoming y 0 to 100, i, q ±100

    Parameters
    ----------
    y : str
        luma
    i : str
        chrominance
    q : str
        chrominance

    Returns
    -------
    tuple of integers
    """

    # assume I and Q between ±1, correct for coloursys
    y = min(max(y, 0), 100)
    i = min(max(i, -100), 100)
    q = min(max(q, -100), 100)
    y = y / 100
    i = 0.599 * i / 100
    q = 0.5251 * q / 100

    red = y + 0.9468822170900693 * i + 0.6235565819861433 * q
    green = y - 0.27478764629897834 * i - 0.6356910791873801 * q
    blue = y - 1.1085450346420322 * i + 1.7090069284064666 * q
    red = min(max(red, 0), 1)
    green = min(max(green, 0), 1)
    blue = min(max(blue, 0), 1)

    return (int(red * 255 + 0.5), int(green * 255 + 0.5), int(blue * 255 + 0.5))

def rgb_to_yiq(red, green, blue):
    """Converts rgb to yiq
        incoming and outgoing denormalised, y 0 to 100, i, q ±100

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

    red = red / 255
    green = green / 255
    blue = blue / 255
    y = 0.30 * red + 0.59 * green + 0.11 * blue
    i = 0.74 * (red - y) - 0.27 * (blue - y)
    q = 0.48 * (red - y) + 0.41 * (blue - y)
    i = i / 0.599
    q = q / 0.5251
    return (y * 100, i * 100, q * 100)

def generate_gradient(from_colour, to_colour, height, width):
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
    array of integers
    """

    new_ch = [np.tile(np.linspace(from_colour[i], to_colour[i], width,
                                  dtype=np.uint8),
                      [height, 1]) for i in range(len(from_colour))]
    return np.dstack(new_ch)

def draw_gradient(canvas, colour1, colour2, width, height=26):
    """Import gradient into tkinter

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
    xdata = 'P6 {} {} 255 '.format(width, height).encode() + arr.tobytes()
    gradient = PhotoImage(width=width, height=height, data=xdata, format='PPM')
    canvas.create_image(0, 0, anchor="nw", image=gradient)
    canvas.image = gradient

def check(width, height, enlargement, square_size=4):
    """Draw chequers in numpy as array
        chequer value to grey or white depends on x position

    Parameters
    ----------
    width : int
        canvas width
    height : int
        canvas height
    enlargement : int
        dpi enlargement factor
    square_size : int
        size each square

    Returns
    -------
    array of integers
    """
    
    sqe = square_size * enlargement
    array = np.zeros([height, width, 3], dtype=np.uint8)
    for x in range(width):
        for y in range(height):
            if (x %
                sqe * 2) // sqe == (y %
                    sqe * 2) // sqe:
                        array[y, x] = 127 - int(0.5 + 127 / width * x)
    return array

def draw_agradient(canvas, colour1, colour2, enlargement, width=300, height=26):
    """Import alpha gradient into tkinter

    Parameters
    ----------
    canvas : str
        parent widget
    colour1 : tuple of int
        start colour
    colour2 : tuple of int
        end colour
    enlargement : int
        dpi enlargement factor
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
    arr1 = check(width, height, enlargement)
    xdata = 'P6 {} {} 255 '.format(
        width, height).encode() + (arr + arr1).tobytes()
    gradient = PhotoImage(width=width, height=height, data=xdata, format='PPM')
    canvas.create_image(0, 0, anchor="nw", image=gradient)
    canvas.image = gradient

def vcheck(width, height, enlargement, alpha, square_size=4):
    """Draw vertical chequers in numpy as array
        chequer value to grey or white depends on y position

    Parameters
    ----------
    width : int
        canvas width
    height : int
        canvas height
    enlargement : int
        dpi enlargement factor
    alpha : int
        opacity
    square_size : int
        size each square

    Returns
    -------
    array of integers
    """
    sqe = square_size * enlargement
    al0 = 127 - alpha // 2
    ah0 = al0 / height
    array = np.zeros([height, width, 3], dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            if (x % sqe * 2) // sqe == (y % sqe * 2) \
                    // sqe:
                array[y, x] = int(0.5 + ah0 * y)
    return array

def vgenerate_gradient(to_colour, alpha, height, width):
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
    array of integers
    """

    al0 = alpha / 255
    res0 = 1 - al0
    from_colour = (int(to_colour[0] * al0 + 127 * res0),
                  int(to_colour[1] * al0 + 127 * res0),
                  int(to_colour[2] * al0 + 127 * res0))  # changing from_colour
    new_ch = [np.tile(np.linspace(to_colour[i], from_colour[i], height,
                                  dtype=np.uint8), [width, 1]).T for i in range(3)]
    return np.dstack(new_ch)

def vdraw_gradient(canvas, colour1, enlargement, alpha=255, width=30, height=30):
    """Either fill in background
        or import vertical gradient into tkinter

    Parameters
    ----------
    canvas : str
        parent widget
    colour1 : tuple of int
        start colour
    enlargement : int
        dpi enlargement factor
    alpha : int
        opacity
    width : int
        canvas width
    height : int
        canvas height

    Returns
    -------
    None
    """

    if alpha > 240:
        hash_value = rgb2hash(colour1[0], colour1[1], colour1[2])
        canvas['background'] = hash_value
        canvas.background = hash_value
    else:
        arr = vgenerate_gradient(colour1, alpha, height, width)
        arr1 = vcheck(width, height, enlargement, alpha)
        xdata = 'P6 {} {} 255 '.format(
            width, height).encode() + (arr + arr1).tobytes()
        gradient = PhotoImage(
            width=width,
            height=height,
            data=xdata,
            format='PPM')
        canvas.create_image(0, 0, anchor="nw", image=gradient)
        canvas.image = gradient

def hash2rgb(hash_):
    """Conversion hash colour to rgb

    Parameters
    ----------
    hash_ : str
        colour as hash

    Returns
    -------
    tuple of integers
    """

    hash_ = hash_.strip('#')
    return tuple(int(hash_[i:i + 2], 16) for i in (0, 2, 4))

def yiq_okay(action, text, input_, lower, upper):
    """Validation for yiq colour components

    Parameters
    ----------
    action : str
        action
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
    boolean
    """

    # action=1 -> insert
    if action == "1":
        if input_ in '0123456789.-+':
            return bool(float(lower) <= float(text) <= float(upper))
        return False
    return True


def is_okay(index, text, input_):  # '%i','%P','%S'
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
    boolean
    """

    index = int(index)  # index is string!
    if index == 0 and text == '#':
        return True
    try:
        int(input_, 16)
        return bool(0 < index < 7)
    except ValueError:  # not a hex
        return False


def sb_okay(action, text, input_, lower, upper):  # '%d', '%P','%S'
    """Validation for rgba colour components

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
    boolean
    """

    if action == "1":
        if input_.isdigit():
            return bool(int(lower) <= int(text) <= int(upper))
        return False
    return True
