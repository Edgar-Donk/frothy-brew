""" Construction three gradients in yiq using PPM image
    spinbox validation, working with modified Scale and
    colour space
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

    Returns
    -------
    None
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
                 command=None):
        self.from_ = from_
        self.to = to
        self.variable = variable

        super().__init__(parent, length=length + sliderlength, orient=orient,
                         variable=variable, from_=from_, to=to, command=command)

        self.digits = digits
        self.length = length

        self.build(parent, from_, to, sliderlength, tickinterval)

    def build(self, parent, from_, to, sliderlength, tickinterval):
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
                           relx=sliderlength / sc_range / 2 +
                           j / sc_range * (1 - sliderlength / sc_range),
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
        self.space = 301
        self.ring_radius = 10
        self.ring_width = 3

        self.yvar.set(30)
        self.ivar.set(100)
        self.qvar.set(40.56)

        self.build()

    def yhandle(self, evt=None):
        """command callback for y"""

        y = float(self.yvar.get())
        i = float(self.ivar.get())
        q = float(self.qvar.get())
        from_colour = yiq_to_rgb(*(0, i, q))
        to_colour = yiq_to_rgb(*(100, i, q))
        draw_gradient(self.ycan, from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, -100, q))
        to_colour = yiq_to_rgb(*(y, 100, q))
        draw_gradient(self.ican, from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, i, -100))
        to_colour = yiq_to_rgb(*(y, i, 100))
        draw_gradient(self.qcan, from_colour, to_colour, width=self.canvas_w)

    def ihandle(self, evt=None):
        """command callback for i"""

        y = float(self.yvar.get())
        i = float(self.ivar.get())
        q = float(self.qvar.get())
        from_colour = yiq_to_rgb(*(0, i, q))
        to_colour = yiq_to_rgb(*(100, i, q))
        draw_gradient(self.ycan, from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, -100, q))
        to_colour = yiq_to_rgb(*(y, 100, q))
        draw_gradient(self.ican, from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, i, -100))
        to_colour = yiq_to_rgb(*(y, i, 100))
        draw_gradient(self.qcan, from_colour, to_colour, width=self.canvas_w)

    def qhandle(self, evt=None):
        """command callback for q"""

        y = float(self.yvar.get())
        i = float(self.ivar.get())
        q = float(self.qvar.get())
        from_colour = yiq_to_rgb(*(0, i, q))
        to_colour = yiq_to_rgb(*(100, i, q))
        draw_gradient(self.ycan, from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, -100, q))
        to_colour = yiq_to_rgb(*(y, 100, q))
        draw_gradient(self.ican, from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, i, -100))
        to_colour = yiq_to_rgb(*(y, i, 100))
        draw_gradient(self.qcan, from_colour, to_colour, width=self.canvas_w)

    def door_bell(self, ring):
        """bind callback from cursor"""

        i, q = ring
        y = float(self.yvar.get())
        # yiq = (y, i, q)
        from_colour = yiq_to_rgb(*(0, i, q))
        to_colour = yiq_to_rgb(*(100, i, q))
        draw_gradient(self.ycan, from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, 0, q))
        to_colour = yiq_to_rgb(*(y, 100, q))
        draw_gradient(self.ican, from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, i, 0))
        to_colour = yiq_to_rgb(*(y, i, 100))
        draw_gradient(self.qcan, from_colour, to_colour, width=self.canvas_w)

    def build(self):
        """widget construction"""

        fr4 = LabelFrame(self.fr0, text='yiq')
        fr4.grid(column=2, row=0)

        yl0 = Label(fr4, text='luma')
        yl0.grid(column=0, row=0, sticky='s')

        self.ycan = Canvas(fr4, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.ycan.grid(column=1, row=0, sticky='s')

        ysc = TtkScale(fr4, from_=0, to=100, variable=self.yvar, orient='horizontal',
                       length=self.scale_l, command=self.yhandle, tickinterval=10)
        ysc.grid(column=1, row=1, sticky='nw')

        vcmdyiq = root.register(yiq_okay)

        ysb = Spinbox(fr4, from_=0, to=100, textvariable=self.yvar, validate='key',
                      validatecommand=(vcmdyiq, '%d', '%P', '%S', 0, 100), command=self.yhandle,
                      width=5, increment=1)
        ysb.grid(column=2, row=1, sticky='nw')
        ysb.bind('<KeyRelease>', self.checksyiq)

        yel = Label(fr4, height=1)
        yel.grid(column=2, row=2)

        il0 = Label(fr4, text='i hue')
        il0.grid(column=0, row=3)

        self.ican = Canvas(fr4, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.ican.grid(column=1, row=3, sticky='s')

        isc = TtkScale(fr4, from_=-100, to=100, variable=self.ivar, orient='horizontal',
                       length=self.scale_l, command=self.ihandle, tickinterval=20)
        isc.grid(column=1, row=4, sticky='nw')

        isb = Spinbox(fr4, from_=-100, to=100, textvariable=self.ivar, validate='key',
                      validatecommand=(vcmdyiq, '%d', '%P', '%S', -100, 100), command=self.ihandle,
                      width=5, increment=1)
        isb.grid(column=2, row=4, sticky='nw')
        isb.bind('<KeyRelease>', self.checksyiq)

        iel = Label(fr4, height=1)
        iel.grid(column=2, row=5)

        ql0 = Label(fr4, text='q hue')
        ql0.grid(column=0, row=6, sticky='s')

        self.qcan = Canvas(fr4, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.qcan.grid(column=1, row=6, sticky='n')

        qsc = TtkScale(fr4, from_=-100, to=100, variable=self.qvar, orient='horizontal',
                       length=self.scale_l, command=self.qhandle, tickinterval=20)
        qsc.grid(column=1, row=7, sticky='nw')

        qsb = Spinbox(fr4, from_=-100, to=100, textvariable=self.qvar, validate='key',
                      validatecommand=(vcmdyiq, '%d', '%P', '%S', -100, 100), command=self.qhandle,
                      width=5, increment=1)
        qsb.grid(column=2, row=7, sticky='nw')
        qsb.bind('<KeyRelease>', self.checksyiq)

        qel = Label(fr4, height=1)
        qel.grid(column=2, row=8)

        # assume initial setting 0,100,100 hsv
        to_colour = yiq_to_rgb(*(30, 100.0, 40.56))
        # print(self.canvas_w)
        draw_gradient(self.ycan, yiq_to_rgb(0.0, 100.0, 40.56),
                      yiq_to_rgb(100, 100, 40.56), width=self.canvas_w)
        draw_gradient(self.ican, yiq_to_rgb(30, -100.0, 40.56), to_colour,
                      width=self.canvas_w)
        draw_gradient(self.qcan, yiq_to_rgb(30, 100, -100),
                      yiq_to_rgb(30, 100, 100), width=self.canvas_w)

        self.can_yiq = can_yiq = Canvas(fr4, width=self.space, height=self.space)
        can_yiq.grid(column=1, row=9, pady=25, sticky='n')
        self.yiqGamut = PhotoImage(file='../../figures/colour_space.png')
        can_yiq.create_image(0, 0, anchor='nw', image=self.yiqGamut)
        self.ring = circle(can_yiq, 300.0, 210.84, self.ring_radius, width=self.ring_width,
                           activeoutline='#555555', tags='ring')  # 240, 181

        can_yiq.bind('<Button-1>', self.click_ring)
        can_yiq.tag_bind('ring', '<B1-Motion>', self.drag_ring)

    def click_ring(self, event):
        """Procedure called when mouse clicks in colour wheel

        Parameters
        ----------
        evt : str
            bind handle

        Returns
        -------
        calls handle for cursor
        """

        X = event.x
        Y = event.y
        ring_radius = self.ring_radius
        space = self.space

        # check whether inside space
        X = min(max(X, 0), space)
        Y = min(max(Y, 0), space)

        for search in self.can_yiq.find_withtag("ring"):
            self.can_yiq.coords(
                search,
                X - ring_radius,
                Y - ring_radius,
                X + ring_radius,
                Y + ring_radius)

        i = (X - space // 2) * 2 / 3
        q = (Y - space // 2) * 2 / 3
        self.ivar.set(i)
        self.qvar.set(q)
        ring = i, q
        self.door_bell(ring)

    def drag_ring(self, event):
        """Procedure called when mouse drags cursor

        Parameters
        ----------
        evt : str
            bind handle

        Returns
        -------
        calls handle for cursor
        """

        X = event.x
        Y = event.y
        ring_radius = self.ring_radius
        space = self.space

        # check whether inside space
        X = min(max(X, 0), space)
        Y = min(max(Y, 0), space)

        for search in self.can_yiq.find_withtag("ring"):
            self.can_yiq.coords(
                search,
                X - ring_radius,
                Y - ring_radius,
                X + ring_radius,
                Y + ring_radius)

        i = (X - space // 2) * 2 / 3
        q = (Y - space // 2) * 2 / 3
        self.ivar.set(i)
        self.qvar.set(q)
        ring = i, q
        self.door_bell(ring)

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
        draw_gradient(self.ycan, from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, -100, q))
        to_colour = yiq_to_rgb(*(y, 100, q))
        draw_gradient(self.ican, from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, i, -100))
        to_colour = yiq_to_rgb(*(y, i, 100))
        draw_gradient(self.qcan, from_colour, to_colour, width=self.canvas_w)


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
