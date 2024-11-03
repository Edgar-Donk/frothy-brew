""" Construction four gradients in rgba using PPM image
    added final colour
    working with modified Scale
"""

from tkinter import Tk, Canvas, Label, IntVar, Frame, StringVar
from tkinter.ttk import LabelFrame, Scale, Style, Entry, Spinbox
from PIL import Image, ImageDraw, ImageTk
from colourTools import rgb2hash, draw_gradient, \
    draw_agradient, vdraw_gradient


class TtkScale(Scale):
    """Class to draw themed Scale widget

    Parameters
    ----------
    parent : str
        parent widget
    enlargement : int
        dpi enlargement factor
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
                 command=None, enlargement=1):

        self.from_ = from_
        self.to = to
        self.variable = variable

        super().__init__(parent, length=length + sliderlength,
                         variable=variable, from_=from_, to=to, command=command)
        self.e = enlargement
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
                           relx=sliderlength*self.e / length*self.e / 2 + i /
                           sc_range * (1 - sliderlength*self.e / length*self.e),
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

    def __init__(self, fr0, enlargement):
        self.fr0 = fr0
        self.e = enlargement

        self.cursor_w = 16 * self.e

        self.rvar = IntVar()
        self.gvar = IntVar()
        self.bvar = IntVar()
        self.avar = IntVar()
        self.evar = StringVar()

        self.scale_l = 300 * self.e
        self.canvas_w = self.scale_l
        self.canvas_h = 26 * self.e
        self.canvas_b = 30 * self.e
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
        draw_gradient(self.gcan, (red, 0, blue), (red, 255, blue),
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.bcan, (red, green, 0), (red, green, 255),
                      width=self.canvas_w, height=self.canvas_h)
        draw_agradient(self.acan, (127, 127, 127), (red, green, blue),
                       self.e, width=self.canvas_w, height=self.canvas_h)
        vdraw_gradient(self.cmcan, (red, green, blue), self.e, alpha=alpha,
                        width=self.canvas_b, height=self.canvas_b)
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
        draw_gradient(self.rcan, (0, green, blue), (255, green, blue),
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.bcan, (red, green, 0), (red, green, 255),
                      width=self.canvas_w, height=self.canvas_h)
        draw_agradient(self.acan, (127, 127, 127), (red, green, blue), self.e,
                       width=self.canvas_w, height=self.canvas_h)
        vdraw_gradient(self.cmcan, (red, green, blue), self.e, alpha=alpha,
                        width=self.canvas_b, height=self.canvas_b)
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

        red = self.rvar.get() #round(self.rvar.get(),0)
        green = self.gvar.get()
        blue = self.bvar.get()
        alpha = self.avar.get()
        draw_gradient(self.rcan, (0, green, blue), (255, green, blue),
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.gcan, (red, 0, blue), (red, 255, blue),
                      width=self.canvas_w, height=self.canvas_h)
        draw_agradient(self.acan, (127, 127, 127), (red, green, blue),
                       self.e, width=self.canvas_w, height=self.canvas_h)
        vdraw_gradient(self.cmcan, (red, green, blue), self.e, alpha=alpha,
                        width=self.canvas_b, height=self.canvas_b)
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
        vdraw_gradient(self.cmcan, (red, green, blue), self.e, alpha=alpha,
                        width=self.canvas_b, height=self.canvas_b)

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
                       length=self.scale_l, command=self.rhandle, tickinterval=20,
                       enlargement=self.e)
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
                       length=self.scale_l, command=self.ghandle, tickinterval=20,
                       enlargement=self.e)
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
                       length=self.scale_l, command=self.bhandle, tickinterval=20,
                       enlargement=self.e)
        bsc.grid(column=1, row=7, sticky='news')

        bsb = Spinbox(fr1, from_=0, to=255, textvariable=self.bvar,
                      command=self.bhandle, width=5)
        bsb.grid(column=2, row=7, sticky='nw')

        bel = Label(fr1, height=1)
        bel.grid(column=2, row=8)

        fr3 = LabelFrame(self.fr0, text='colour mix')
        fr3.grid(column=1, row=0, sticky='nw')

        self.cmcan = cmcan = Canvas(fr3, width=30*self.e, height=30*self.e, bd=0,
                                    highlightthickness=0)
        cmcan.grid(column=0, row=0, sticky='n', columnspan=2)
        cmcan.grid_propagate(0)
        vdraw_gradient(self.cmcan, (255, 0, 0), self.e, alpha=255)

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
                       length=self.scale_l, command=self.ahandle, tickinterval=20,
                       enlargement=self.e)
        asc.grid(column=1, row=1, sticky='news')

        asb = Spinbox(fr2, from_=0, to=255, textvariable=self.avar,
                      command=self.ahandle, width=5)
        asb.grid(column=2, row=1, sticky='nw')

        ael = Label(fr2, text=' ', height=1)
        ael.grid(column=2, row=2, sticky='s')

        draw_gradient(self.rcan, (0, 0, 0), (255, 0, 0),
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.gcan, (255, 0, 0), (255, 255, 0),
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.bcan, (255, 0, 0), (255, 0, 255),
                      width=self.canvas_w, height=self.canvas_h)
        draw_agradient(self.acan, (127, 127, 127), (255, 0, 0),
                       self.e, width=self.canvas_w, height=self.canvas_h)


if __name__ == "__main__":
    root = Tk()
    winsys = root.tk.call("tk", "windowingsystem")
    BASELINE = 1.33398982438864281 if winsys != 'aqua' else 1.000492368291482
    scaling = root.tk.call("tk", "scaling")
    enlargement = e = int(scaling / BASELINE + 0.5)

    img = Image.new("RGBA", (16*e, 10*e), '#00000000')
    trough = ImageTk.PhotoImage(img)

    # constants for creating upward pointing arrow
    WIDTH = 17*e
    HEIGHT = 17*e
    OFFSET = 5*e
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
    style.configure('TSpinbox', arrowsize=10*e)
    fra0 = Frame(root)
    root.columnconfigure(0, weight=1)
    fra0.grid(row=0, column=0, sticky='nsew')
    fra0.columnconfigure(0, weight=1)
    RgbSelect(fra0, enlargement)
    root.mainloop()
