"""Using tkinter Canvas to display rgba  and hsv colour gradients:-

* Added an hsv colour wheel with ring cursor to show hue and saturation.
* All linked together using numpy arrays to draw gradients and chequers
    with alpha (opacity).
* Resulting arrays are imported into tkinter as PPM images.
* The themed Scale has been changed so that the trough is transparent and
    the slider changed to an upward arrow.
"""

from tkinter import Tk, Canvas, IntVar, Frame, PhotoImage, StringVar
from tkinter.ttk import LabelFrame, Scale, Style, Entry, Spinbox, Label
from PIL import Image, ImageDraw, ImageTk
from colour_tools import rgb2hash,circle,hsv_to_rgb,rgb_to_hsv,\
draw_gradient,draw_agradient,\
vdraw_gradient,is_okay,sb_okay,hash2rgb,polar2cart,cart2polar,hue_gradient


class  TtkScale(Scale):
    """Class to draw themed Scale widget.

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

    def __init__(self, parent, length, from_=0, to=255, orient='horizontal',
                 variable=0, digits=None, tickinterval=None, sliderlength=16,
                 command=None, enlargement=1):
        self.from_=from_
        self.to=to
        self.variable=variable

        super().__init__(parent, length=length+sliderlength, orient=orient,
                         variable=variable, from_=from_, to=to, command=command)

        self.digits=digits
        self.length=length
        self.e = enlargement

        self.build(parent, from_, to, sliderlength, tickinterval, length)

    def build(self, parent, from_, to, sliderlength, tickinterval, length):
        """Create ticks, as the themed Scale has no option.

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
                item = Label(parent, text=i)
                item.place(in_=self, bordermode='outside',
                           relx=sliderlength / length / 2 +
                           i / sc_range * (1 - sliderlength / length),
                           rely=1, anchor='n')

class  RgbHsvSelect:
    """Class to construct rgba, hsv gradients and hsv colour wheel.

    Parameters
    ----------
    fr0 : str
        parent widget

    Returns
    -------
    None
    """

    def __init__(self, fr0, enlargement):
        self.fr0 =fr0
        self.e = enlargement

        self.rvar = IntVar()
        self.gvar = IntVar()
        self.bvar = IntVar()
        self.avar = IntVar()
        self.evar = StringVar()
        self.hvar = IntVar()
        self.svar = IntVar()
        self.vvar = IntVar()

        self.scale_l = 300*self.e
        self.sliderlength = 16*self.e
        self.canvas_w = self.scale_l-self.sliderlength
        self.canvas_h = 26*self.e
        self.canvas_b = 30*self.e

        self.wheel_w = 317*self.e
        self.wheel_iw = 299*self.e
        self.ring_radius = 10*self.e
        self.ring_width = 3*self.e

        self.build()

        self.rvar.set(255)
        self.gvar.set(0)
        self.bvar.set(0)
        self.avar.set(255)
        self.evar.set('#ff0000')
        self.hvar.set(0)
        self.svar.set(100)
        self.vvar.set(100)

    def  rhandle(self, evt=None):
        """Command callback for red.

        Parameters
        ----------
        evt : str
            command handle

        Results
        -------
        None
        """

        red = self.rvar.get()
        self.rvar.set(red)
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
        self.overlord(rgb=(red, green, blue))

    def  ghandle(self, evt=None):
        """Command callback for green.

        Parameters
        ----------
        evt : str
            command handle
        """

        red = self.rvar.get()
        green = self.gvar.get()
        self.gvar.set(green)
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
        self.overlord(rgb=(red, green, blue))

    def  bhandle(self, evt=None):
        """Command callback for blue.

        Parameters
        ----------
        evt : str
            command handle
        """

        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        self.bvar.set(blue)
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
        self.overlord(rgb=(red, green, blue))

    def  ahandle(self, evt=None):
        """Command callback for alpha.

        Parameters
        ----------
        evt : str
            command handle
        """

        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        alpha = self.avar.get()
        self.avar.set(alpha)
        vdraw_gradient(self.cmcan, (red, green, blue), self.e, alpha=alpha,
                        width=self.canvas_b, height=self.canvas_b)

    def  hhandle(self, evt=None):
        """Command callback for hue.

        Parameters
        ----------
        evt : str
            command handle
        """

        hue = self.hvar.get()
        self.hvar.set(int(0.5 + hue))
        sat = self.svar.get()
        value = self.vvar.get()
        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        X, Y = polar2cart(hue, sat, self.wheel_w, self.wheel_iw)
        ring_radius = self.ring_radius
        for i in self.can_hsv.find_withtag("ring"):
            self.can_hsv.coords(
                i,
                X - ring_radius,
                Y - ring_radius,
                X + ring_radius,
                Y + ring_radius)
        self.overlord(hsv=(hue, sat, value))

    def  shandle(self, evt=None):
        """Command callback for saturation.

        Parameters
        ----------
        evt : str
            command handle
        """

        hue = self.hvar.get()
        sat = self.svar.get()
        self.svar.set(int(0.5 + sat))
        value = self.vvar.get()
        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        X, Y = polar2cart(hue, sat, self.wheel_w, self.wheel_iw)
        ring_radius = self.ring_radius
        for i in self.can_hsv.find_withtag("ring"):
            self.can_hsv.coords(
                i,
                X - ring_radius,
                Y - ring_radius,
                X + ring_radius,
                Y + ring_radius)
        self.overlord(hsv=(hue, sat, value))

    def  vhandle(self, evt=None):
        """Command callback for value.

        Parameters
        ----------
        evt : str
            command handle
        """

        hue = self.hvar.get()
        sat = self.svar.get()
        value = self.vvar.get()
        self.vvar.set(int(0.5 + value))
        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        self.overlord(hsv=(hue, sat, value))

    def  door_bell(self,ring):
        """Calling procedure from cursor binds.

        Parameters
        ----------
        ring : tuple of int
            hue, saturation values
        """

        hue, sat = ring
        value = self.vvar.get()
        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        self.overlord(hsv=(hue, sat, value))

    def  overlord(self, rgb=None, hsv=None):
        """Supervisory procedure to control calls from handle functions.

        Parameters
        ----------
        rgb : tuple of integers
            call from rgb
        hsv : tuple of integers
            call from hsv

        Returns
        -------
        draws gradients and sets other colour system
        """

        if rgb:
            red, green, blue = rgb[0], rgb[1], rgb[2]
            hue, sat, value = rgb_to_hsv(red, green, blue)
            from_colour = hsv_to_rgb(*(hue, 0, value))
            to_colour = hsv_to_rgb(*(hue, 100, value))
            draw_gradient(
                self.scan,
                from_colour,
                to_colour,
                width=self.canvas_w, height=self.canvas_h)
            from_colour = hsv_to_rgb(*(hue, sat, 0))
            to_colour = hsv_to_rgb(*(hue, sat, 100))
            draw_gradient(
                self.vcan,
                from_colour,
                to_colour,
                width=self.canvas_w, height=self.canvas_h)
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
            self.related(hue, sat, value, red, green, blue)

        elif hsv:
            hue, sat, value = hsv[0], hsv[1], hsv[2]
            red, green, blue = hsv_to_rgb(hue, sat, value)
            draw_agradient(self.acan, (127, 127, 127), (red, green, blue),
                           self.e, width=self.canvas_w, height=self.canvas_h)
            alpha = self.avar.get()
            vdraw_gradient(self.cmcan, (red, green, blue), self.e, alpha=alpha,
                           width=self.canvas_b, height=self.canvas_b)
            draw_gradient(self.rcan, (0, green, blue), (255, green, blue),
                          width=self.canvas_w, height=self.canvas_h)
            draw_gradient(self.gcan, (red, 0, blue), (red, 255, blue),
                          width=self.canvas_w, height=self.canvas_h)
            draw_gradient(self.bcan, (red, green, 0), (red, green, 255),
                          width=self.canvas_w, height=self.canvas_h)
            self.evar.set(rgb2hash(red, green, blue))
            self.rvar.set(red)
            self.gvar.set(green)
            self.bvar.set(blue)
            self.related(hue, sat, value, red, green, blue)

    def related(self, h, s, v, r, g, b):
        """Creating related Colours, 5 in saturation, 5 for value,
            1 complementary

        Parameters
        ----------
        h : float
            hue
        s : float
            saturation
        v : float
            value
        r : int
            red
        g : int
            green
        b : int
            blue
        """
        sats = [25, 50, 75, 100]
        vals = [25, 50, 75, 100]

        for ix, sat in enumerate(sats):
            srelcol = rgb2hash(*hsv_to_rgb(h, sat, v))
            self.srccans[ix]['background'] = srelcol
            self.srccans[ix].background = srelcol
            self.srcls[ix]['text'] = srelcol
            vrelcol = rgb2hash(*hsv_to_rgb(h, s, sat))
            self.vrccans[ix]['background'] = vrelcol
            self.vrccans[ix].background = vrelcol
            self.vrcls[ix]['text'] = vrelcol

        comp_col = rgb2hash(255-r, 255-g, 255-b)
        self.cccan['background'] = comp_col
        self.cccan.background = comp_col
        self.ccl['text'] = comp_col

    def resize_rcan(self, event):
        """Bind function for red resizing

        Parameters
        ----------
        event : str
        """
        W = event.width
        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        draw_gradient(self.rcan, (0, green, blue), (255, green, blue),
                      width=W, height=self.canvas_h)

    def resize_gcan(self, event):
        """Bind function for green resizing

        Parameters
        ----------
        event : str
        """
        W = event.width
        red = self.rvar.get()
        blue = self.bvar.get()

        draw_gradient(self.gcan, (red, 0, blue), (red, 255, blue),
                      width=W, height=self.canvas_h)

    def resize_bcan(self, event):
        """Bind function for blue resizing

        Parameters
        ----------
        event : str
        """
        W = event.width
        red = self.rvar.get()
        green = self.gvar.get()

        draw_gradient(self.bcan, (red, green, 0), (red, green, 255),
                      width=W, height=self.canvas_h)

    def resize_acan(self, event):
        """Bind function for alpha resizing

        Parameters
        ----------
        event : str
        """
        W = event.width
        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        draw_agradient(self.acan, (127, 127, 127), (red, green, blue),
                       self.e, width=W, height=self.canvas_h)

    def resize_hcan(self, event):
        """Bind function for hue resizing

        Parameters
        ----------
        event : str
        """
        W = event.width
        self.canvas_w = W
        hue_gradient(self.hcan, width=W, height=self.canvas_h, steps=360)

    def resize_scan(self, event):
        """Bind function for saturation resizing

        Parameters
        ----------
        event : str
        """
        W = event.width
        self.canvas_w = W
        hue = self.hvar.get()
        value = self.vvar.get()

        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour,
                      width=W, height=self.canvas_h)

    def resize_vcan(self, event):
        """Bind function for value resizing

        Parameters
        ----------
        event : str
        """
        W = event.width
        self.canvas_w = W
        hue = self.hvar.get()
        sat = self.svar.get()

        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour,
                      width=W, height=self.canvas_h)

    def  build(self):
        """Widget construction."""

        lf1 = LabelFrame(self.fr0, text='rgb')
        lf1.grid(column=0, row=0, sticky='new')
        lf1.columnconfigure(1, weight=1)

        rl0 = Label(lf1, text='red  ')
        rl0.grid(column=0, row=0, sticky='s')

        self.rcan = Canvas(lf1, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.rcan.grid(column=1, row=0, sticky='sew', padx=self.sliderlength//2)
        self.rcan.bind("<Configure>", self.resize_rcan)

        rsc = TtkScale(lf1, self.scale_l, from_=0, to=255, variable=self.rvar,
            orient='horizontal', command=self.rhandle, tickinterval=20)
        rsc.grid(column=1, row=1, sticky='new')

        vcmdsb = root.register(sb_okay)

        rsb = Spinbox(lf1, from_=0, to=255, textvariable=self.rvar, validate='key',
                      validatecommand=(vcmdsb, '%d', '%P', '%S', 255), command=self.rhandle, width=5)
        rsb.grid(column=2, row=1, sticky='nw')
        rsb.bind('<KeyRelease>', self.checksb)

        rel = Label(lf1)
        rel.grid(column=2, row=2)

        gl0 = Label(lf1, text='green')
        gl0.grid(column=0, row=3)

        self.gcan = Canvas(lf1, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.gcan.grid(column=1, row=3, sticky='sew', padx=self.sliderlength//2)
        self.gcan.bind("<Configure>", self.resize_gcan)

        gsc = TtkScale(lf1, self.scale_l, from_=0, to=255, variable=self.gvar,
            orient='horizontal', command=self.ghandle, tickinterval=20)
        gsc.grid(column=1, row=4, sticky='new')


        gsb = Spinbox(lf1, from_=0, to=255, textvariable=self.gvar, validate='key',
                      validatecommand=(vcmdsb, '%d', '%P', '%S', 255), command=self.ghandle, width=5)
        gsb.grid(column=2, row=4, sticky='nw')
        gsb.bind('<KeyRelease>', self.checksb)

        gel = Label(lf1)
        gel.grid(column=2, row=5)

        bl0 = Label(lf1, text='blue ')
        bl0.grid(column=0, row=6, sticky='s')

        self.bcan = Canvas(lf1, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.bcan.grid(column=1, row=6, sticky='new', padx=self.sliderlength//2)
        self.bcan.bind("<Configure>", self.resize_bcan)

        bsc = TtkScale(lf1, self.scale_l, from_=0, to=255, variable=self.bvar,
            orient='horizontal', command=self.bhandle, tickinterval=20)
        bsc.grid(column=1, row=7, sticky='new')

        bsb = Spinbox(lf1, from_=0, to=255, textvariable=self.bvar, validate='key',
                      validatecommand=(vcmdsb, '%d', '%P', '%S', 255), command=self.bhandle, width=5)
        bsb.grid(column=2, row=7, sticky='nw')
        bsb.bind('<KeyRelease>', self.checksb)

        bel = Label(lf1)
        bel.grid(column=2, row=8)

        lf3 = LabelFrame(self.fr0, text='colour mix')
        lf3.grid(column=1, row=0, sticky='nw')

        self.cmcan = cmcan = Canvas(lf3, width=self.canvas_b, height=self.canvas_b,
                                    bd=0, highlightthickness=0)
        cmcan.grid(column=0, row=0, sticky='n', columnspan=2)
        cmcan.grid_propagate(0)
        vdraw_gradient(self.cmcan, (255, 0, 0), self.e, alpha=255,
                       width=self.canvas_b, height=self.canvas_b)

        cml = Label(lf3, text='hash\nvalue')
        cml.grid(column=0, row=1)

        vcmd = root.register(is_okay)
        self.ent0 = ent0 = Entry(lf3, width=8, validate='key',
                                 validatecommand=(vcmd, '%i', '%P', '%S'), textvariable=self.evar)
        ent0.grid(column=1, row=1)
        ent0.bind('<KeyRelease>', self.checkhash)

        lf5 = LabelFrame(lf3, text='related colours', style='Wide.TLabelframe')
        lf5.grid(column=0, row=2, sticky='nw', columnspan=2)

        self.srcls = []
        self.vrcls = []
        self.srccans = []
        self.vrccans = []
        relateds = [25, 50, 75, 100]
        stexts = ['25% sat', '50% sat', '75% sat', '100% sat']
        vtexts = ['25% val', '50% val', '75% val', '100% val']

        for ix, rel in enumerate(relateds):
            Label(lf5, text=stexts[ix]).grid(row=1+2*ix, column=0, sticky='n')
            self.srcls.append(Label(lf5))
            self.srcls[ix].grid(row=1+2*ix, column=1, sticky='n')
            self.srccans.append(Canvas(lf5, width=self.canvas_b,
                            height=self.canvas_b, bd=0, highlightthickness=0))
            self.srccans[ix].grid(row=2*ix, column=0, sticky='n', columnspan=2)
            Label(lf5, text=vtexts[ix]).grid(row=9+2*ix, column=0, sticky='n')
            self.vrcls.append(Label(lf5))
            self.vrcls[ix].grid(row=9+2*ix, column=1, sticky='n')
            self.vrccans.append(Canvas(lf5, width=self.canvas_b,
                                height=self.canvas_b, bd=0, highlightthickness=0))
            self.vrccans[ix].grid(row=8+2*ix, column=0, sticky='n', columnspan=2)

        self.cccan = Canvas(lf5, width=self.canvas_b, height=self.canvas_b, bd=0,
                             highlightthickness=0)
        self.cccan.grid(column=0, row=17, sticky='n', columnspan=2)

        self.ccla = Label(lf5, text = "comp'y")
        self.ccla.grid(column=0, row=18, sticky='n')

        self.ccl = Label(lf5, text = "")
        self.ccl.grid(column=1, row=18, sticky='n')

        al0 = Label(lf1, text='alpha')
        al0.grid(column=0, row=10, sticky='s')

        self.acan = Canvas(lf1, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.acan.grid(column=1, row=10, sticky='new', padx=self.sliderlength//2)
        self.acan.bind("<Configure>", self.resize_acan)

        asc = TtkScale(lf1, self.scale_l, from_=0, to=255, variable=self.avar,
            orient='horizontal', command=self.ahandle, tickinterval=20)
        asc.grid(column=1, row=11, sticky='new')

        asb = Spinbox(lf1, from_=0, to=255, textvariable=self.avar, validate='key',
                      validatecommand=(vcmdsb, '%d', '%P', '%S', 255), command=self.ahandle, width=5)
        asb.grid(column=2, row=11, sticky='nw')
        asb.bind('<KeyRelease>', self.checksba)

        ael = Label(lf1, text=' ')
        ael.grid(column=2, row=12, sticky='s')

        draw_gradient(self.rcan, (0, 0, 0), (255, 0, 0),
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.gcan, (255, 0, 0),
                      (255, 0, 255), width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.bcan, (255, 0, 0),
                      (255, 255, 0), width=self.canvas_w, height=self.canvas_h)
        draw_agradient(self.acan, (127, 127, 127),
                       (255, 0, 0), self.e, width=self.canvas_w, height=self.canvas_h)

        lf4 = LabelFrame(self.fr0, text='hsv')
        lf4.grid(column=2, row=0, sticky='news')
        lf4.columnconfigure(1, weight=1)

        hl0 = Label(lf4, text='hue  ')
        hl0.grid(column=0, row=0, sticky='s')

        self.hcan = Canvas(lf4, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.hcan.grid(column=1, row=0, sticky='sew', padx=self.sliderlength//2)
        self.hcan.bind("<Configure>", self.resize_hcan)

        hsc = TtkScale(lf4, self.scale_l, from_=0, to=360, variable=self.hvar,
            orient='horizontal', command=self.hhandle, tickinterval=30)
        hsc.grid(column=1, row=1, sticky='new')

        vcmdsb = root.register(sb_okay)

        hsb = Spinbox(lf4, from_=0, to=360, textvariable=self.hvar, validate='key',
                      validatecommand=(vcmdsb, '%P', '%S', 360), command=self.hhandle, width=5)
        hsb.grid(column=2, row=1, sticky='nw')
        hsb.bind('<KeyRelease>', self.checksbh)

        hel = Label(lf4)
        hel.grid(column=2, row=2)

        sl0 = Label(lf4, text='sat  ')
        sl0.grid(column=0, row=3)

        self.scan = Canvas(lf4, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.scan.grid(column=1, row=3, sticky='sew', padx=self.sliderlength//2)
        self.scan.bind("<Configure>", self.resize_scan)

        ssc = TtkScale(lf4, self.scale_l, from_=0, to=100, variable=self.svar,
            orient='horizontal', command=self.shandle, tickinterval=10)
        ssc.grid(column=1, row=4, sticky='new')

        ssb = Spinbox(lf4, from_=0, to=100, textvariable=self.svar, validate='key',
                      validatecommand=(vcmdsb, '%P', '%S', 100), command=self.shandle, width=5)
        ssb.grid(column=2, row=4, sticky='nw')
        ssb.bind('<KeyRelease>', self.checksb100)

        sel = Label(lf4)
        sel.grid(column=2, row=5)

        vl0 = Label(lf4, text='value')
        vl0.grid(column=0, row=6, sticky='s')

        self.vcan = Canvas(lf4, width=self.canvas_w, height=self.canvas_h, bd=0,
                           highlightthickness=0)
        self.vcan.grid(column=1, row=6, sticky='new', padx=self.sliderlength//2)
        self.vcan.bind("<Configure>", self.resize_vcan)

        vsc = TtkScale(lf4, self.scale_l,  from_=0, to=100, variable=self.vvar,
            orient='horizontal', command=self.vhandle, tickinterval=10)
        vsc.grid(column=1, row=7, sticky='new')

        vsb = Spinbox(lf4, from_=0, to=100, textvariable=self.vvar, validate='key',
                      validatecommand=(vcmdsb, '%P', '%S', 100), command=self.vhandle, width=5)
        vsb.grid(column=2, row=7, sticky='nw')
        vsb.bind('<KeyRelease>', self.checksb100)

        vel = Label(lf4)
        vel.grid(column=2, row=8)

        # assume initial setting 0,100,100 hsv
        to_colour = hsv_to_rgb(*(0, 100, 100))

        hue_gradient(self.hcan, width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.scan, (255, 255, 255),
                      to_colour, width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.vcan, (0, 0, 0), to_colour,
                      width=self.canvas_w, height=self.canvas_h)

        self.can_hsv = can_hsv = Canvas(lf4, width=self.wheel_w,
                                        height=self.wheel_w, bg='#d9d9d9')
        can_hsv.grid(column=0, row=9, columnspan=3, pady=25, sticky='n')
        self.hsv_gamut = PhotoImage(file='../figures/colour_wheel'+str(self.e)+'.png')
        can_hsv.create_image(0, 0, anchor='nw', image=self.hsv_gamut)
        self.ring = circle(can_hsv, 307*self.e, 158*self.e, self.ring_radius,
                           width=self.ring_width,
                           outline='#555555', activeoutline='black', tags='ring')

        can_hsv.bind('<Button-1>', self.click_ring)
        can_hsv.tag_bind('ring', '<B1-Motion>', self.drag_ring)

        self.related(0, 100, 100, 255, 0, 0)

    def  checkhash(self, evt=None):
        """Procedure called by entry for hash.

        Parameters
        ----------
        evt : str
            bind handles

        Results
        -------
        None
        """

        hash0 = self.ent0.get()
        if len(hash0) == 7:
            red, green, blue = hash2rgb(hash0)
            alpha = self.avar.get()
            self.rvar.set(red)
            self.gvar.set(green)
            self.bvar.set(blue)
            draw_agradient(self.acan, (127, 127, 127), (red, green, blue),
                           self.e, width=self.canvas_w, height=self.canvas_h)
            draw_gradient(self.rcan, (0, green, blue), (255, green, blue),
                          width=self.canvas_w, height=self.canvas_h)
            draw_gradient(self.gcan, (red, 0, blue), (red, 255, blue),
                          width=self.canvas_w, height=self.canvas_h)
            draw_gradient(self.bcan, (red, green, 0), (red, green, 255),
                          width=self.canvas_w, height=self.canvas_h)
            vdraw_gradient(self.cmcan, (red, green, blue), self.e, alpha=alpha,
                           width=self.canvas_b, height=self.canvas_b)
            self.overlord(rgb=(red, green, blue))

    def  click_ring(self, event):
        """Procedure called when mouse clicks in colour wheel.

        Parameters
        ----------
        event : str
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

    def  drag_ring(self, event):
        """Procedure called when mouse drags cursor.

        Parameters
        ----------
        event : str
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

    def  checksba(self, evt=None):
        """Procedure called by alpha spinbox.

        Parameters
        ----------
        evt : str
            bind handles

        Results
        -------
        None
        """

        alpha = self.avar.get()
        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        vdraw_gradient(self.cmcan, (red, green, blue), self.e, alpha=alpha,
                       width=self.canvas_b, height=self.canvas_b)

    def  checksb(self, evt=None):
        """Procedure called by rgb colour spinboxes.

        Parameters
        ----------
        evt : str
            bind handles

        Results
        -------
        None
        """

        alpha = self.avar.get()
        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        draw_agradient(self.acan, (127, 127, 127), (red, green, blue),
                       self.e, width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.rcan, (0, green, blue), (255, green, blue),
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.gcan, (red, 0, blue), (red, 255, blue),
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.bcan, (red, green, 0), (red, green, 255),
                      width=self.canvas_w, height=self.canvas_h)
        vdraw_gradient(self.cmcan, (red, green, blue), self.e, alpha=alpha,
                       width=self.canvas_b, height=self.canvas_b)
        self.evar.set(rgb2hash(red, green, blue))
        self.overlord(rgb=(red, green, blue))

    def  checksbh(self, event=None):
        """Procedure called by hue spinbox.

        Parameters
        ----------
        event : str
            bind handles
        """

        hue = self.hvar.get()
        sat = self.svar.get()
        value = self.vvar.get()
        from_colour = hsv_to_rgb(*(hue, 0, value))
        to_colour = hsv_to_rgb(*(hue, 100, value))
        draw_gradient(self.scan, from_colour, to_colour, width=self.canvas_w,
                      height=self.canvas_h)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour, width=self.canvas_w,
                      height=self.canvas_h)
        self.overlord(hsv=(hue, sat, value))

    def  checksb100(self, event=None):
        """Procedure called by saturation and value spinboxes.

        Parameters
        ----------
        event : str
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
        draw_gradient(self.scan, from_colour, to_colour, width=self.canvas_w,
                      height=self.canvas_h)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour, width=self.canvas_w,
                      height=self.canvas_h)
        self.overlord(hsv=(hue, sat, value))

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

    #pressed state
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
    style.configure('Width.TLabelframe', width=60*e)
    style.configure('TSpinbox', arrowsize=10*e)
    root.columnconfigure(0, weight=1)

    fr = Frame(root)
    fr.grid(row=0, column=0, sticky='nsew')
    fr.columnconfigure(0, weight=1)
    fr.columnconfigure(2, weight=1)
    RgbHsvSelect(fr, enlargement)
    root.mainloop()

