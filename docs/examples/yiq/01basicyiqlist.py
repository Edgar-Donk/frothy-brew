""" Construction three gradients in yiq using PPM image
    spinbox validation, working with modified Scale
"""

from tkinter import Tk, Canvas, Label, Frame, PhotoImage, StringVar
from tkinter.ttk import LabelFrame, Scale, Style, Spinbox
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

    Returns
    -------
    hash : str
        hexadecimal colour
    """

    rgb = (red, green, blue)
    return '#%02x%02x%02x' % rgb


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
    """

    arr = generate_gradient(colour1, colour2, height, width)
    xdata = 'P6 {} {} 255 '.format(width, height).encode() + arr.tobytes()
    gradient = PhotoImage(width=width, height=height, data=xdata, format='PPM')
    canvas.create_image(0, 0, anchor="nw", image=gradient)
    canvas.image = gradient


def yiq_okay(action, text, input_, lower, upper):
    """Validation for colour components

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
                 command=None, resolution=0.0001):
        self.from_ = from_
        self.to = to
        self.variable = variable

        super().__init__(parent, length=length + sliderlength, orient=orient,
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
                j = (i if from_ > 0 else i - from_)
                item.place(in_=self, bordermode='outside',
                           relx=sliderlength / length / 2 +
                           j / sc_range * (1 - sliderlength / length),
                           rely=1, anchor='n')


class YiqSelect:
    """Class to construct yiq gradients

    Parameters
    ----------
    fr0 : str
        parent widget
    """

    def __init__(self, fr0):
        self.fr0 = fr0

        self.yvar = StringVar()
        self.ivar = StringVar()
        self.qvar = StringVar()

        self.scale_l = 300
        self.canvas_w = self.scale_l
        self.canvas_h = 26
        self.cursor_w = 16

        self.build()

        self.yvar.set(30)
        self.ivar.set(100)
        self.qvar.set(40.56)

    def yiqhandle(self, evt=None):
        """command callback for y, i or q"""

        y = float(self.yvar.get())
        i = float(self.ivar.get())
        q = float(self.qvar.get())
        from_colour = yiq_to_rgb(*(0, i, q))
        to_colour = yiq_to_rgb(*(100, i, q))
        draw_gradient(self.cans[0], from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, -100, q))
        to_colour = yiq_to_rgb(*(y, 100, q))
        draw_gradient(self.cans[1], from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, i, -100))
        to_colour = yiq_to_rgb(*(y, i, 100))
        draw_gradient(self.cans[2], from_colour, to_colour, width=self.canvas_w)

    def build(self):
        """widget construction"""

        fr4 = LabelFrame(self.fr0, text='yiq')
        fr4.grid(column=2, row=0)
        vcmdyiq = root.register(yiq_okay)

        self.cans = []
        sboxes = []
        comps = ['y', 'i', 'q']
        names = ['luma', 'i hue', 'q hue']
        tkvars = [self.yvar, self.ivar, self.qvar]
        froms = [0, -100, -100]
        ticks = [10, 20, 20]

        for ix, comp in enumerate(comps):
            Label(fr4, text=names[ix]).grid(row=3*ix, column=0)
            Label(fr4, height=1).grid(row=2+3*ix, column=2)
            self.cans.append(Canvas(fr4, width=self.canvas_w, height=self.canvas_h,
                bd=0, highlightthickness=0))
            self.cans[ix].grid(row=3*ix, column=1)
            TtkScale(fr4, from_=froms[ix], to=100, variable=tkvars[ix],
                orient='horizontal', length=self.scale_l, command=self.yiqhandle,
                tickinterval=ticks[ix]).grid(row=1+3*ix, column=1, sticky='nw')
            sboxes.append(Spinbox(fr4, from_=froms[ix], to=100, textvariable=tkvars[ix],
                validatecommand=(vcmdyiq, '%d', '%P', '%S', froms[ix], 100),
                validate='key', command=self.yiqhandle, width=5,
                increment=1))
            sboxes[ix].grid(row=1+3*ix, column=2, sticky='nw')
            sboxes[ix].bind('<KeyRelease>', self.checksyiq)


        # assume initial setting 0,100,100 hsv
        to_colour = yiq_to_rgb(*(30, 100.0, 40.56))
        # print(self.canvas_w)
        draw_gradient(self.cans[0], yiq_to_rgb(0.0, 100.0, 40.56),
                      yiq_to_rgb(100, 100, 40.56), width=self.canvas_w)
        draw_gradient(self.cans[1], yiq_to_rgb(30, -100.0, 40.56), to_colour,
                      width=self.canvas_w)
        draw_gradient(self.cans[2], yiq_to_rgb(30, 100, -100),
                      yiq_to_rgb(30, 100, 100), width=self.canvas_w)

    def checksyiq(self, evt):
        """Procedure called by yiq spinboxes

        Parameters
        ----------
        evt : str
            bind handles
        """

        y = float(self.yvar.get())
        i = float(self.ivar.get())
        q = float(self.qvar.get())
        from_colour = yiq_to_rgb(*(0, i, q))
        to_colour = yiq_to_rgb(*(100, i, q))
        draw_gradient(self.cans[0], from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, -100, q))
        to_colour = yiq_to_rgb(*(y, 100, q))
        draw_gradient(self.cans[1], from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, i, -100))
        to_colour = yiq_to_rgb(*(y, i, 100))
        draw_gradient(self.cans[2], from_colour, to_colour, width=self.canvas_w)


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

    fr = Frame(root)
    fr.grid(row=0, column=0, sticky='nsew')
    YiqSelect(fr)
    root.mainloop()

