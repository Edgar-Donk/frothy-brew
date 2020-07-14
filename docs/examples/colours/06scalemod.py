""" Construction four gradients in rgba using PPM image
    added final colour
    working with modified Scale
"""

from tkinter import Tk, Canvas, Label, IntVar, Frame, PhotoImage, StringVar
from tkinter.ttk import LabelFrame, Scale, Style, Entry, Spinbox
from PIL import Image, ImageDraw, ImageTk
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
    Results
    -------
    string
        hexadecimal colour
    """

    rgb = (red, green, blue)
    return '#%02x%02x%02x' % rgb


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


def check(width, height, square_size=4):
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
    array of integers
    """

    # Set check value to grey or white depending on x position
    array = np.zeros([height, width, 3], dtype=np.uint8)  # ,dtype=np.uint8
    for x in range(width):
        for y in range(height):
            if (x % square_size * 2) // square_size ==\
                    (y % square_size * 2) // square_size:
                array[y, x] = 127 - int(0.5 + 127 / width * x)
    return array


def draw_gradient(canvas, colour1, colour2, width=300, height=26):
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

    Returns
    -------
    None
    """

    arr = generate_gradient(colour1, colour2, height, width)
    xdata = 'P6 {} {} 255 '.format(width, height).encode() + arr.tobytes()
    gradient = PhotoImage(width=width, height=height, data=xdata, format='PPM')
    canvas.create_image(0, 0, anchor="nw", image=gradient)
    canvas.image = gradient


def draw_agradient(canvas, colour1, colour2, width=300, height=26):
    """Import alpha gradient into tkinter

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
    arr1 = check(width, height)
    xdata = 'P6 {} {} 255 '.format(
        width, height).encode() + (arr + arr1).tobytes()
    gradient = PhotoImage(width=width, height=height, data=xdata, format='PPM')
    canvas.create_image(width//2, height//2, anchor='center', image=gradient)  #"nw" 0, 0,
    canvas.image = gradient


def vcheck(width, height, alpha, square_size=4):
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


def vdraw_gradient(canvas, colour1, alpha=255, width=30, height=30):
    """Either fill in background
        or import vertical gradient into tkinter

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


class TtkScale(Scale):
    """Class to draw themed Scale widget

    Parameters
    ----------
    parent : str
        parent widget
    from_ : int
        start of scale
    to : int
        end of scale
    length : int
        length in pixels
    orient : str
        orientation
    variable : str
        tk variable
    digits : int
        length variable when converted to string
    tickinterval : float or int
        how many digits show up in tick interval
    sliderlength : int
        what it says
    command : str
        procedure called when slider moves
    """

    def __init__(self, parent, from_=0, to=255, length=300, orient='horizontal',
                 variable=0, digits=None, tickinterval=None, sliderlength=16,
                 command=None):
        self.from_ = from_
        self.to = to
        self.variable = variable

        super().__init__(parent, length=length + sliderlength,
                         variable=variable, from_=from_, to=to, command=command)

        self.digits = digits
        self.length = length

        self.build(parent, from_, to, sliderlength, tickinterval, length)

    def build(self, parent, from_, to, sliderlength, tickinterval, length):
        """Create ticks

        Parameters
        ----------
        parent : str
            parent widget
        from_ : int
            start of scale
        to : int
            end of scale
        length : int
            length in pixels
        tickinterval : float or int

        """

        sc_range = to - from_

        if tickinterval:
            for i in range(from_, to + 2, tickinterval):
                item = Label(parent, text=i, bg='#EFFEFF')
                item.place(in_=self, bordermode='outside',
                           relx=sliderlength / length / 2 + i /
                           sc_range * (1 - sliderlength / length),
                           rely=1, anchor='n')


class RgbSelect:
    """Class to construct rgba gradients and final colour

    Parameters
    ----------
    fr0 : str
        parent widget

    Returns
    -------
    None
    """

    def __init__(self, fr0):
        self.fr0 = fr0

        self.cursor_w = 16

        self.rvar = IntVar()
        self.gvar = IntVar()
        self.bvar = IntVar()
        self.avar = IntVar()
        self.evar = StringVar()

        self.scale_l = 300
        self.canvas_w = self.scale_l
        self.canvas_h = 26
        self.build()

        self.rvar.set(255)
        self.gvar.set(0)
        self.bvar.set(0)
        self.avar.set(255)
        self.evar.set('#ff0000')

    def rhandle(self, *args):
        """command callback for red

        Parameters
        ----------
        None

        Results
        -------
        None
        """

        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        alpha = self.avar.get()
        draw_gradient(self.gcan, (red, 0, blue),
                      (red, 255, blue), width=self.canvas_w)
        draw_gradient(self.bcan, (red, green, 0),
                      (red, green, 255), width=self.canvas_w)
        draw_agradient(self.acan, (127, 127, 127),
                       (red, green, blue), width=self.canvas_w)
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)
        self.evar.set(rgb2hash(red, green, blue))

    def ghandle(self, *args):
        """command callback for green

        Parameters
        ----------
        None

        Results
        -------
        None
        """

        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        alpha = self.avar.get()
        draw_gradient(self.rcan, (0, green, blue),
                      (255, green, blue), width=self.canvas_w)
        draw_gradient(self.bcan, (red, green, 0),
                      (red, green, 255), width=self.canvas_w)
        draw_agradient(self.acan, (127, 127, 127),
                       (red, green, blue), width=self.canvas_w)
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)
        self.evar.set(rgb2hash(red, green, blue))

    def bhandle(self, *args):
        """command callback for blue

        Parameters
        ----------
        None

        Results
        -------
        None
        """

        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        alpha = self.avar.get()
        draw_gradient(self.rcan, (0, green, blue),
                      (255, green, blue), width=self.canvas_w)
        draw_gradient(self.gcan, (red, 0, blue),
                      (red, 255, blue), width=self.canvas_w)
        draw_agradient(self.acan, (127, 127, 127),
                       (red, green, blue), width=self.canvas_w)
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)
        self.evar.set(rgb2hash(red, green, blue))

    def ahandle(self, *args):
        """command callback for alpha

        Parameters
        ----------
        None

        Results
        -------
        None
        """

        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        alpha = self.avar.get()
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)

    def build(self):
        """widget construction

        Parameters
        ----------
        None

        Results
        -------
        None
        """

        fr1 = LabelFrame(self.fr0, text='rgb')
        fr1.grid(column=0, row=0, sticky='news')

        rl0 = Label(fr1, text='red  ')
        rl0.grid(column=0, row=0, sticky='s')

        self.rcan = Canvas(fr1, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.rcan.grid(column=1, row=0, sticky='s')

        rsc = TtkScale(fr1, from_=0, to=255, variable=self.rvar, orient='horizontal',
                       length=self.scale_l, command=self.rhandle, tickinterval=20)
        rsc.grid(column=1, row=1, sticky='news')

        rsb = Spinbox(fr1, from_=0, to=255, textvariable=self.rvar,
                      command=self.rhandle, width=5)
        rsb.grid(column=2, row=1, sticky='nw')

        rel = Label(fr1, height=1)
        rel.grid(column=2, row=2)

        gl0 = Label(fr1, text='green')
        gl0.grid(column=0, row=3)

        self.gcan = Canvas(fr1, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.gcan.grid(column=1, row=3, sticky='s')

        gsc = TtkScale(fr1, from_=0, to=255, variable=self.gvar, orient='horizontal',
                       length=self.scale_l, command=self.ghandle, tickinterval=20)
        gsc.grid(column=1, row=4, sticky='news')

        gsb = Spinbox(fr1, from_=0, to=255, textvariable=self.gvar,
                      command=self.ghandle, width=5)
        gsb.grid(column=2, row=4, sticky='nw')

        gel = Label(fr1, height=1)
        gel.grid(column=2, row=5)

        bl0 = Label(fr1, text='blue ')
        bl0.grid(column=0, row=6, sticky='s')

        self.bcan = Canvas(fr1, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.bcan.grid(column=1, row=6, sticky='n')

        bsc = TtkScale(fr1, from_=0, to=255, variable=self.bvar, orient='horizontal',
                       length=self.scale_l, command=self.bhandle, tickinterval=20)
        bsc.grid(column=1, row=7, sticky='news')

        bsb = Spinbox(fr1, from_=0, to=255, textvariable=self.bvar,
                      command=self.bhandle, width=5)
        bsb.grid(column=2, row=7, sticky='nw')

        bel = Label(fr1, height=1)
        bel.grid(column=2, row=8)

        fr3 = LabelFrame(self.fr0, text='colour mix')
        fr3.grid(column=1, row=0, sticky='nw')

        self.cmcan = cmcan = Canvas(fr3, width=30, height=30, bd=0,
                                    highlightthickness=0)
        cmcan.grid(column=0, row=0, sticky='n', columnspan=2)
        cmcan.grid_propagate(0)
        vdraw_gradient(self.cmcan, (255, 0, 0), alpha=255)

        cml = Label(fr3, text='hash\nvalue')
        cml.grid(column=0, row=1)

        ent0 = Entry(fr3, width=8, textvariable=self.evar)
        ent0.grid(column=1, row=1)

        fr2 = LabelFrame(self.fr0, text='opacity')
        fr2.grid(column=0, row=1, sticky='news')

        al0 = Label(fr2, text='alpha')
        al0.grid(column=0, row=0, sticky='s')

        self.acan = Canvas(fr2, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.acan.grid(column=1, row=0, sticky='n')

        asc = TtkScale(fr2, from_=0, to=255, variable=self.avar, orient='horizontal',
                       length=self.scale_l, command=self.ahandle, tickinterval=20)
        asc.grid(column=1, row=1, sticky='news')

        asb = Spinbox(fr2, from_=0, to=255, textvariable=self.avar,
                      command=self.ahandle, width=5)
        asb.grid(column=2, row=1, sticky='nw')

        ael = Label(fr2, text=' ', height=1)
        ael.grid(column=2, row=2, sticky='s')

        draw_gradient(self.rcan, (0, 0, 0), (255, 0, 0), width=self.canvas_w)
        draw_gradient(self.gcan, (255, 0, 0),
                      (255, 255, 0), width=self.canvas_w)
        draw_gradient(self.bcan, (255, 0, 0),
                      (255, 0, 255), width=self.canvas_w)
        draw_agradient(self.acan, (127, 127, 127),
                       (255, 0, 0), width=self.canvas_w)


if __name__ == "__main__":
    root = Tk()

    img = Image.new("RGBA", (16, 10), '#00000000')
    trough = ImageTk.PhotoImage(img)

    # constants for creating upward pointing arrow
    WIDTH = 17
    HEIGHT = 17
    OFFSET = 5
    ST0 = WIDTH // 2, HEIGHT - 1 - OFFSET
    LIGHT = 'GreenYellow'
    MEDIUM = 'LawnGreen'
    DARK = '#5D9B90'

    # normal state
    im = Image.new("RGBA", (WIDTH, HEIGHT), '#00000000')
    rdraw = ImageDraw.Draw(im)
    rdraw.polygon([ST0[0], ST0[1], 0, HEIGHT - 1,
                   WIDTH - 1, HEIGHT - 1], fill=LIGHT)
    rdraw.polygon([ST0[0], ST0[1], ST0[0], 0, 0, HEIGHT - 1], fill=MEDIUM)
    rdraw.polygon([ST0[0], ST0[1], WIDTH - 1,
                   HEIGHT - 1, ST0[0], 0], fill=DARK)
    slider = ImageTk.PhotoImage(im)

    # pressed state
    imp = Image.new("RGBA", (WIDTH, HEIGHT), '#00000000')
    draw = ImageDraw.Draw(imp)
    draw.polygon([ST0[0], ST0[1], 0, HEIGHT - 1,
                  WIDTH - 1, HEIGHT - 1], fill=LIGHT)
    draw.polygon([ST0[0], ST0[1], ST0[0], 0, 0, HEIGHT - 1], fill=DARK)
    draw.polygon([ST0[0], ST0[1], WIDTH - 1,
                  HEIGHT - 1, ST0[0], 0], fill=MEDIUM)
    sliderp = ImageTk.PhotoImage(imp)

    style = Style()
    style.theme_settings('default', {
        'Horizontal.Scale.trough': {"element create":
                                    ('image', trough,
                                     {'border': 0, 'sticky': 'wes'})},
        'Horizontal.Scale.slider': {"element create":
                                    ('image', slider,
                                     ('pressed', sliderp),
                                     {'border': 3, 'sticky': 'n'})}})

    style.theme_use('default')

    fra0 = Frame(root)
    root.columnconfigure(0, weight=1)
    fra0.grid(row=0, column=0, sticky='nsew')
    fra0.columnconfigure(0, weight=1)
    RgbSelect(fra0)
    root.mainloop()
