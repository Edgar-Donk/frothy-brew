""" Construction three gradients in hsv using PPM image
    spinbox validation, working with modified Scale
    adding colour wheel and creating cursor
"""

from tkinter import Tk, Canvas, Label, IntVar, Frame, PhotoImage
from tkinter.ttk import LabelFrame, Scale, Style, Spinbox
from math import pi, atan2, degrees, hypot, cos, sin
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


def circle(canvas, x, y, radius, width=None, tags=None, outline=None,
           activeoutline=None):
    """Canvas circle with centre and radius

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

    Returns
    -------
    canvas circle
    """

    return canvas.create_oval(x + radius, y + radius, x - radius, y - radius,
                              width=width, tags=tags,
                              activeoutline=activeoutline, outline=outline)


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


def hue_gradient(canvas, width=300, height=26, steps=360):
    """Draw hue gradient in tkinter canvas

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
    array of integers
    """

    image = Image.new("RGB", (width, height), "#FFFFFF")
    hdraw = ImageDraw.Draw(image)

    for i in range(steps):
        x0 = int(float(width * i) / steps)
        x1 = int(float(width * (i + 1)) / steps)
        hdraw.rectangle((x0, 0, x1, height), fill=hsv_to_rgb(i, 100, 100))
    gradient = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=gradient)
    canvas.image = gradient


def sb_okay(text, input_, upper):  # '%P','%S'
    """Validation for colour components

    Parameters
    ----------
    text : str
        text if accepted
    input_ : str
        current input
    upper : int
        upper limit

    Returns
    -------
    boolean
    """

    if input_.isdigit():
        if 0 < len(text) < 4:
            return bool(0 <= int(text) <= int(upper))
        return False
    return False


def hsv_to_rgb(h, s, v):
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
    tuple integers for rgb
    """

    h = min(max(h, 0), 360)
    s = min(max(s, 0), 100)
    v = min(max(v, 0), 100)
    h, s, v = h / 360.0, s / 100.0, v / 100.0
    # calculate all 0 รท 1.0
    if s == 0.0:
        v *= 255
        v = int(v)
        return (v, v, v)
    i = int(h * 6.)  # assume int() truncates!
    f = (h * 6.) - i
    p, q, t = int(255 * (v * (1. - s))),\
        int(255 * (v * (1. - s * f))),\
        int(255 * (v * (1. - s * (1. - f))))
    v *= 255
    i %= 6
    v = int(v)
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)


def polar2cart(phi, ray, outer_w, inner_w):
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

    return int(x + 0.5), int(y + 0.5)


def cart2polar(x, y, outer_w, inner_w):
    """Conversion cartesian to polar coordinates
        output h,s of hsv; s adjusted

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
    tuple of floats
    """

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
                           relx=sliderlength / length / 2 +
                           i / sc_range * (1 - sliderlength / length),
                           rely=1, anchor='n')


class HsvSelect:
    """Class to construct hsv gradients and colour wheel

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

        self.hvar = IntVar()
        self.svar = IntVar()
        self.vvar = IntVar()

        self.scale_l = 300
        self.canvas_w = self.scale_l
        self.canvas_h = 26
        self.cursor_w = 16
        self.wheel_w = 317
        self.wheel_iw = 299
        self.ring_radius = 10
        self.ring_width = 3

        self.hvar.set(0)
        self.svar.set(100)
        self.vvar.set(100)

        self.build()

    def hhandle(self, evt=None):
        """command callback for hue

        Parameters
        ----------
        None

        Results
        -------
        None
        """

        hue = self.hvar.get()
        self.hvar.set(int(0.5 + hue))
        sat = self.svar.get()
        value = self.vvar.get()
        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour, width=self.canvas_w)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour, width=self.canvas_w)
        X, Y = polar2cart(hue, sat, self.wheel_w, self.wheel_iw)
        ring_radius = self.ring_radius
        for i in self.can_hsv.find_withtag("ring"):
            self.can_hsv.coords(
                i,
                X - ring_radius,
                Y - ring_radius,
                X + ring_radius,
                Y + ring_radius)

    def shandle(self, evt=None):
        """command callback for saturation

        Parameters
        ----------
        None

        Results
        -------
        None
        """

        hue = self.hvar.get()
        sat = self.svar.get()
        self.svar.set(int(0.5 + sat))
        value = self.vvar.get()
        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour, width=self.canvas_w)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour, width=self.canvas_w)
        X, Y = polar2cart(hue, sat, self.wheel_w, self.wheel_iw)
        ring_radius = self.ring_radius
        for i in self.can_hsv.find_withtag("ring"):
            self.can_hsv.coords(
                i,
                X - ring_radius,
                Y - ring_radius,
                X + ring_radius,
                Y + ring_radius)

    def vhandle(self, evt=None):
        """command callback for value

        Parameters
        ----------
        None

        Results
        -------
        None
        """

        hue = self.hvar.get()
        sat = self.svar.get()
        value = self.vvar.get()
        self.vvar.set(int(0.5 + value))
        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour, width=self.canvas_w)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour, width=self.canvas_w)

    def door_bell(self, ring):
        """Calling procedure from cursor binds

        Parameters
        ----------
        ring : tuple of int
            hue, saturation values
        """

        # calls from bind
        hue, sat = ring
        value = self.vvar.get()
        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour, width=self.canvas_w)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour, width=self.canvas_w)

    def build(self):
        """widget construction

        Parameters
        ----------
        None

        Results
        -------
        None
        """

        fr4 = LabelFrame(self.fr0, text='hsv')
        fr4.grid(column=2, row=0, sticky='ns')

        hl0 = Label(fr4, text='hue  ')
        hl0.grid(column=0, row=0, sticky='s')

        self.hcan = Canvas(fr4, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.hcan.grid(column=1, row=0, sticky='s')

        hsc = TtkScale(fr4, from_=0, to=360, variable=self.hvar, orient='horizontal',
                       length=self.scale_l, command=self.hhandle, tickinterval=30)
        hsc.grid(column=1, row=1, sticky='nw')

        vcmdsb = root.register(sb_okay)

        hsb = Spinbox(fr4, from_=0, to=360, textvariable=self.hvar, validate='key',
                      validatecommand=(vcmdsb, '%P', '%S', 360), command=self.hhandle, width=5)
        hsb.grid(column=2, row=1, sticky='nw')
        hsb.bind('<KeyRelease>', self.checksbh)

        hel = Label(fr4, height=1)
        hel.grid(column=2, row=2)

        sl0 = Label(fr4, text='sat  ')
        sl0.grid(column=0, row=3)

        self.scan = Canvas(fr4, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.scan.grid(column=1, row=3, sticky='s')

        ssc = TtkScale(fr4, from_=0, to=100, variable=self.svar, orient='horizontal',
                       length=self.scale_l, command=self.shandle, tickinterval=10)
        ssc.grid(column=1, row=4, sticky='nw')

        ssb = Spinbox(fr4, from_=0, to=100, textvariable=self.svar, validate='key',
                      validatecommand=(vcmdsb, '%P', '%S', 100), command=self.shandle, width=5)
        ssb.grid(column=2, row=4, sticky='nw')
        ssb.bind('<KeyRelease>', self.checksb100)

        sel = Label(fr4, height=1)
        sel.grid(column=2, row=5)

        vl0 = Label(fr4, text='value')
        vl0.grid(column=0, row=6, sticky='s')

        self.vcan = Canvas(fr4, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.vcan.grid(column=1, row=6, sticky='n')

        vsc = TtkScale(fr4, from_=0, to=100, variable=self.vvar, orient='horizontal',
                       length=self.scale_l, command=self.vhandle, tickinterval=10)
        vsc.grid(column=1, row=7, sticky='nw')

        vsb = Spinbox(fr4, from_=0, to=100, textvariable=self.vvar, validate='key',
                      validatecommand=(vcmdsb, '%P', '%S', 100), command=self.vhandle, width=5)
        vsb.grid(column=2, row=7, sticky='nw')
        vsb.bind('<KeyRelease>', self.checksb100)

        vel = Label(fr4, height=1)
        vel.grid(column=2, row=8)

        # assume initial setting 0,100,100 hsv
        to_colour = hsv_to_rgb(*(0, 100, 100))

        hue_gradient(self.hcan, width=self.canvas_w)
        draw_gradient(self.scan, (255, 255, 255),
                      to_colour, width=self.canvas_w)
        draw_gradient(self.vcan, (0, 0, 0), to_colour, width=self.canvas_w)

        self.can_hsv = can_hsv = Canvas(fr4, width=self.wheel_w,
                                         height=self.wheel_w, bg='#d9d9d9')
        can_hsv.grid(column=1, row=9, pady=25, sticky='n')
        self.hsv_gamut = PhotoImage(file='../../figures/colour_wheel.png')
        can_hsv.create_image(0, 0, anchor='nw', image=self.hsv_gamut)
        self.ring = circle(can_hsv, 307, 158, self.ring_radius, width=self.ring_width,
                           activeoutline='#555555', tags='ring')

        can_hsv.bind('<Button-1>', self.click_ring)
        can_hsv.tag_bind('ring', '<B1-Motion>', self.drag_ring)

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

        cx = self.wheel_w // 2
        dx, dy = X - cx, Y - cx
        rad = self.wheel_iw // 2
        if (dx)**2 + (dy)**2 < rad**2:
            for search in self.can_hsv.find_withtag("ring"):
                self.can_hsv.coords(search, X - ring_radius, Y - ring_radius,
                                    X + ring_radius, Y + ring_radius)

        hue, sat = cart2polar(X, Y, self.wheel_w, self.wheel_iw)
        self.hvar.set(hue)
        self.svar.set(sat)
        ring = hue, sat
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

        cx = self.wheel_w // 2
        dx, dy = X - cx, Y - cx
        rad = self.wheel_iw // 2

        if (dx)**2 + (dy)**2 < rad**2:
            self.can_hsv.coords(self.ring, X - ring_radius, Y - ring_radius,
                                X + ring_radius, Y + ring_radius)

        hue, sat = cart2polar(X, Y, self.wheel_w, self.wheel_iw)
        self.hvar.set(hue)
        self.svar.set(sat)
        ring = hue, sat
        self.door_bell(ring)

    def checksbh(self, evt):
        """Procedure called by hue spinbox

        Parameters
        ----------
        evt : str
            bind handles

        Results
        -------
        None
        """

        hue = self.hvar.get()
        sat = self.svar.get()
        value = self.vvar.get()
        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour, width=self.canvas_w)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour, width=self.canvas_w)

    def checksb100(self, evt):
        """Procedure called by s,v spinboxes

        Parameters
        ----------
        evt : str
            bind handles

        Results
        -------
        None
        """

        hue = self.hvar.get()
        sat = self.svar.get()
        value = self.vvar.get()
        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour, width=self.canvas_w)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour, width=self.canvas_w)


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

    root.geometry("500x600+200+100")
    fr = Frame(root)
    fr.grid(row=0, column=0, sticky='nsew')
    HsvSelect(fr)
    root.mainloop()
