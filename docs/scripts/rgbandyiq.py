"""Construction four gradients in rgba three gradients in yiq.

    using PPM image spinbox validation, working with modified Scale
    and colour space
"""

from tkinter import Tk,Canvas,IntVar,Frame,PhotoImage,StringVar
from tkinter.ttk import LabelFrame,Scale,Style,Entry,Spinbox,Label
from PIL import Image,ImageDraw,ImageTk
from functools import partial
from colour_tools import rgb2hash,circle,yiq_to_rgb,rgb_to_yiq,\
draw_gradient,draw_agradient,\
vdraw_gradient,yiq_okay,is_okay,sb_okay,hash2rgb

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
                 command=None, resolution=0.0001):
        self.from_ = from_
        self.to = to
        self.variable = variable

        super().__init__(parent, length=length, from_=from_,
                         variable=variable, to=to, command=command)

        self.digits = digits
        self.length = length

        self.build(parent, from_, to, sliderlength, tickinterval)

    def build(self, parent, from_, to, sliderlength, tickinterval):
        """Create ttk Scale ticks.

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

        scRange = to - from_
        if tickinterval:

            for i in range(from_, to+2, tickinterval):
                item = Label(parent, text=i)
                j = (i if from_ > 0 else i - from_)
                item.place(in_=self, bordermode='outside',
                    relx=sliderlength/scRange/4+j/scRange*(1-sliderlength/scRange/2),
                    rely=1, anchor='n')

class RgbYiqSelect:
    """Class to construct rgba, yiq gradients and yiq colour space.

    Parameters
    ----------
    fr : str
        parent widget

    """

    def __init__(self, fr0):
        self.fr0 = fr0

        self.yvar = StringVar()
        self.ivar = StringVar()
        self.qvar = StringVar()
        self.rvar = IntVar()
        self.gvar = IntVar()
        self.bvar = IntVar()
        self.avar = IntVar()
        self.evar = StringVar()

        self.scale_l = 300
        self.sliderlength = 16
        self.canvas_w = self.scale_l - self.sliderlength
        self.canvas_h = 26

        self.space = 301
        self.ring_radius = 10
        self.ring_width = 3

        self.build()

        self.yvar.set(30)
        self.ivar.set(100)
        self.qvar.set(40.56)
        self.rvar.set(255)
        self.gvar.set(0)
        self.bvar.set(0)
        self.avar.set(255)
        self.evar.set('#ff0000')

    def yhandle(self, *evt):
        """Command callback for y.

        Parameters
        ----------
        evt : str
            command handle

        """

        y=float(self.yvar.get())
        i=float(self.ivar.get())
        q=float(self.qvar.get())
        from_colour = yiq_to_rgb(*(0, i, q))
        to_colour = yiq_to_rgb(*(100, i, q))
        draw_gradient(self.cans[0], from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, -100, q))
        to_colour = yiq_to_rgb(*(y, 100, q))
        draw_gradient(self.cans[1], from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, i, -100))
        to_colour = yiq_to_rgb(*(y, i, 100))
        draw_gradient(self.cans[2], from_colour, to_colour, width=self.canvas_w)
        self.overlord(yiq=(y, i, q))

    def iqhandle(self, *evt):
        """Command callback for i.

        Parameters
        ----------
        evt : str
            command handle

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
        X = i*3/2+150
        Y = q*3/2+150
        ring_radius = self.ring_radius
        for s in self.canYiq.find_withtag("ring"):
            self.canYiq.coords(s, X-ring_radius, Y-ring_radius, X+ring_radius, Y+ring_radius)
        self.overlord(yiq=(y, i, q))

    def door_bell(self, ring):
        """Bind callback from cursor.

        Parameters
        ----------
        ring : tuple of int
            y, i, q values

        """

        # calls from bind
        i, q = ring
        y = float(self.yvar.get())

        from_colour = yiq_to_rgb(*(0, i, q))
        to_colour = yiq_to_rgb(*(100, i, q))
        draw_gradient(self.cans[0], from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, 0, q))
        to_colour = yiq_to_rgb(*(y, 100, q))
        draw_gradient(self.cans[1], from_colour, to_colour, width=self.canvas_w)
        from_colour = yiq_to_rgb(*(y, i, 0))
        to_colour = yiq_to_rgb(*(y, i, 100))
        draw_gradient(self.cans[2], from_colour, to_colour, width=self.canvas_w)
        self.overlord(yiq=(y, i, q))

    def related(self, y, i, q):
        lumas = [0, 20, 40, 60, 80, 100]

        for ix, luma in enumerate(lumas):
            relcol = rgb2hash(*yiq_to_rgb(luma, i, q))
            self.rccans[ix]['background'] = relcol
            self.rccans[ix].background = relcol
            self.rcls[ix]['text'] = relcol

        comp_col = rgb2hash(*yiq_to_rgb(100-y, -i, -q))
        self.cccan['background'] = comp_col
        self.cccan.background = comp_col
        self.ccl['text'] = comp_col

    def rgbhandle(self, evt=None):
        """command callback for red, green, blue"""

        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        alpha = self.avar.get()
        draw_gradient(self.rgbcans[0], (0, green, blue),
                      (255, green, blue), width=self.canvas_w)
        draw_gradient(self.rgbcans[1], (red, 0, blue),
                      (red, 255, blue), width=self.canvas_w)
        draw_gradient(self.rgbcans[2], (red, green, 0),
                      (red, green, 255), width=self.canvas_w)
        draw_agradient(self.rgbcans[3], (127, 127, 127),
                       (red, green, blue), width=self.canvas_w)
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)
        self.evar.set(rgb2hash(red, green, blue))
        self.overlord(rgb=(red, green, blue))

    def ahandle(self, *evt):
        """Command callback for alpha,

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
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)

    def overlord(self, rgb=None, yiq=None):
        """Supervisory procedure to control calls from handles.

        Parameters
        ----------
        rgb : tuple of integers
            rgb
        yiq : tuple of integers
            yiq

        Returns
        -------
        draws gradients and sets other colour system
        """

        if rgb:
            red, green, blue = rgb[0], rgb[1], rgb[2]
            y, i, q = rgb_to_yiq(red, green, blue)
            from_colour = yiq_to_rgb(*(0, i, q))
            to_colour = yiq_to_rgb(*(100, i, q))
            draw_gradient(
                self.cans[0],
                from_colour,
                to_colour,
                width=self.canvas_w)
            from_colour = yiq_to_rgb(*(y, -100, q))
            to_colour = yiq_to_rgb(*(y, 100, q))
            draw_gradient(
                self.cans[1],
                from_colour,
                to_colour,
                width=self.canvas_w)
            from_colour = yiq_to_rgb(*(y, i, -100))
            to_colour = yiq_to_rgb(*(y, i, 100))
            draw_gradient(
                self.cans[2],
                from_colour,
                to_colour,
                width=self.canvas_w)
            self.yvar.set(y)
            self.ivar.set(i)
            self.qvar.set(q)
            X = i * 3 / 2 + 150
            Y = q * 3 / 2 + 150
            ring_radius = self.ring_radius
            for s in self.canYiq.find_withtag("ring"):
                self.canYiq.coords(
                    s,
                    X - ring_radius,
                    Y - ring_radius,
                    X + ring_radius,
                    Y + ring_radius)
            self.related(y, i, q)

        if yiq:
            y, i, q = yiq[0], yiq[1], yiq[2]
            red, green, blue = yiq_to_rgb(y, i, q)
            draw_agradient(self.rgbcans[3], (127, 127, 127),
                           (red, green, blue), width=self.canvas_w)
            alpha = self.avar.get()
            vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)
            draw_gradient(self.rgbcans[0], (0, green, blue),
                          (255, green, blue), width=self.canvas_w)
            draw_gradient(self.rgbcans[1], (red, 0, blue),
                          (red, 255, blue), width=self.canvas_w)
            draw_gradient(self.rgbcans[2], (red, green, 0),
                          (red, green, 255), width=self.canvas_w)
            self.evar.set(rgb2hash(red, green, blue))
            self.rvar.set(red)
            self.gvar.set(green)
            self.bvar.set(blue)
            self.related(y, i, q)

    def resize(self, event, can=''):
        W = event.width
        self.canvas_w = W
        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        if can == self.rgbcans[3]:
            draw_agradient(self.rgbcans[3], (127, 127, 127),
                (red, green, blue), width=W)
        if can == self.rgbcans[0]:
            draw_gradient(self.rgbcans[0], (0, green, blue),
                (255, green, blue), width=W)
        if can == self.rgbcans[1]:
            draw_gradient(self.rgbcans[1], (red, 0, blue),
                (red, 255, blue), width=W)
        if can == self.rgbcans[2]:
            draw_gradient(self.rgbcans[2], (red, green, 0),
                (red, green, 255), width=W)

    def resize_yiq(self, event, can=''):
        W = event.width
        self.canvas_w = W
        y = float(self.yvar.get())
        i = float(self.ivar.get())
        q = float(self.qvar.get())

        if can == self.cans[0]:
            from_colour = yiq_to_rgb(*(0, i, q))
            to_colour = yiq_to_rgb(*(100, i, q))
            draw_gradient(self.cans[0], from_colour, to_colour, width=W)
        if can == self.cans[1]:
            from_colour = yiq_to_rgb(*(y, -100, q))
            to_colour = yiq_to_rgb(*(y, 100, q))
            draw_gradient(self.cans[1], from_colour, to_colour, width=W)
        if can == self.cans[2]:
            from_colour = yiq_to_rgb(*(y, i, -100))
            to_colour = yiq_to_rgb(*(y, i, 100))
            draw_gradient(self.cans[2], from_colour, to_colour, width=W)

    def build(self):
        """Widget construction."""

        lf1 = LabelFrame(self.fr0,text='rgb')
        lf1.grid(column=0, row=0, sticky='new')
        lf1.columnconfigure(1, weight=1)
        vcmdsb = root.register(sb_okay)

        self.rgbcans = []
        rgbsboxes = []
        rgbcomps = ['r', 'g', 'b', 'a']
        rgbnames = ['red  ', 'green', 'blue ', 'alpha']
        rgbvars = [self.rvar, self.gvar, self.bvar, self.avar]
        rgbhandles = [self.rgbhandle, self.rgbhandle, self.rgbhandle, self.ahandle]
        binds = [self.checksb, self.checksb, self.checksb, self.checksba]

        for ix, comp in enumerate(rgbcomps):
            Label(lf1, text=rgbnames[ix]).grid(row=3*ix, column=0)
            Label(lf1).grid(row=2+3*ix, column=2)
            self.rgbcans.append(Canvas(lf1, height=self.canvas_h, width=self.canvas_w,
                bd=0, highlightthickness=0))
            self.rgbcans[ix].grid(row=3*ix, column=1, sticky='ew', padx=self.sliderlength//2)
            self.rgbcans[ix].bind("<Configure>", partial(self.resize,
                can= self.rgbcans[ix]))

            TtkScale(lf1, self.scale_l, from_=0, to=255, variable=rgbvars[ix],
                orient='horizontal', command=rgbhandles[ix],
                tickinterval=20).grid(row=1+3*ix, column=1, sticky='new')
            rgbsboxes.append(Spinbox(lf1, from_=0, to=255, textvariable=rgbvars[ix], validate='key',
                validatecommand=(vcmdsb, '%d', '%P', '%S', 0, 255), command=rgbhandles[ix], width=5))
            rgbsboxes[ix].grid(row=1+3*ix, column=2, sticky='nw')
            rgbsboxes[ix].bind('<KeyRelease>', binds[ix])

        lf3 = LabelFrame(self.fr0, text='colour mix')
        lf3.grid(column=1, row=0, sticky='nw')

        self.cmcan = cmcan = Canvas(lf3, width=30, height=30, bd=0,
            highlightthickness=0)
        cmcan.grid(column=0, row=0, sticky='n', columnspan=2)
        cmcan.grid_propagate(0)
        vdraw_gradient(self.cmcan, (255, 0, 0), alpha=255)

        cml = Label(lf3, text='hash\nvalue')
        cml.grid(column=0, row=1)

        vcmd = root.register(is_okay)
        self.en = en = Entry(lf3, width=8, validate='key', textvariable=self.evar,
                             validatecommand=(vcmd, '%i', '%P', '%S'))
        en.grid(column=1, row=1)
        en.bind('<KeyRelease>', self.checkhash)

        lf5 = LabelFrame(lf3, text='related colours')
        lf5.grid(column=0, row=2, sticky='nw', columnspan=2)

        self.rcls = []
        self.rccans = []
        relateds = [0, 20, 40, 60, 80, 100]
        rtexts = ['0% Y', '20% Y', '40% Y', '60% Y', '80% Y', '100% Y']

        for ix, rel in enumerate(relateds):
            Label(lf5, text=rtexts[ix]).grid(row=1+2*ix, column=0, sticky='n')
            self.rcls.append(Label(lf5))
            self.rcls[ix].grid(row=1+2*ix, column=1, sticky='n')
            self.rccans.append(Canvas(lf5, width=30, height=30, bd=0,
                             highlightthickness=0))
            self.rccans[ix].grid(row=2*ix, column=0, sticky='n', columnspan=2)

        self.cccan = Canvas(lf5, width=30, height=30, bd=0,
                             highlightthickness=0)
        self.cccan.grid(column=0, row=12, sticky='n', columnspan=2)

        self.ccla = Label(lf5, text = "comp'y")
        self.ccla.grid(column=0, row=13, sticky='n')

        self.ccl = Label(lf5, text = "")
        self.ccl.grid(column=1, row=13, sticky='n')

        draw_gradient(self.rgbcans[0], (0, 0, 0), (255, 0, 0), width=self.canvas_w)
        draw_gradient(self.rgbcans[1], (255, 0, 0),
                      (255, 255, 0), width=self.canvas_w)
        draw_gradient(self.rgbcans[2], (255, 0, 0),
                      (255, 0, 255), width=self.canvas_w)
        draw_agradient(self.rgbcans[3], (127, 127, 127),
                       (255, 0, 0), width=self.canvas_w)

        lf4 = LabelFrame(self.fr0, text='yiq')
        lf4.grid(column=2, row=0, sticky='ew')
        lf4.columnconfigure(1, weight=1)
        vcmdyiq = root.register(yiq_okay)

        self.cans = []
        sboxes = []
        comps = ['y', 'i', 'q']
        names = ['luma', 'i hue', 'q hue']
        tkvars = [self.yvar, self.ivar, self.qvar]
        handles = [self.yhandle, self.iqhandle, self.iqhandle]
        froms = [0, -100, -100]
        ticks = [10, 20, 20]

        for ix, comp in enumerate(comps):
            Label(lf4, text=names[ix]).grid(row=3*ix, column=0)
            Label(lf4).grid(row=2+3*ix, column=2)
            self.cans.append(Canvas(lf4, width=self.canvas_w, height=self.canvas_h,
                bd=0, highlightthickness=0))
            self.cans[ix].grid(row=3*ix, column=1, sticky='ew', padx=self.sliderlength//2)
            self.cans[ix].bind("<Configure>", partial(self.resize_yiq,
                can=self.cans[ix]))
            TtkScale(lf4, from_=froms[ix], to=100, variable=tkvars[ix],
                orient='horizontal', length=self.scale_l, command=handles[ix],
                tickinterval=ticks[ix]).grid(row=1+3*ix, column=1, sticky='new')
            sboxes.append(Spinbox(lf4, from_=froms[ix], to=100, textvariable=tkvars[ix],
                validatecommand=(vcmdyiq, '%d', '%P', '%S', froms[ix], 100),
                validate='key', command=handles[ix], width=5,
                increment=1))
            sboxes[ix].grid(row=1+3*ix, column=2, sticky='nw')
            sboxes[ix].bind('<KeyRelease>', self.checksyiq)

        # assume initial setting 30,100.0,40.56 yiq
        to_colour = yiq_to_rgb(*(30, 100.0, 40.56))
        draw_gradient(self.cans[0], yiq_to_rgb(0.0, 100.0, 40.56),
                      yiq_to_rgb(100, 100, 40.56), width=self.canvas_w)
        draw_gradient(self.cans[1], yiq_to_rgb(30, -100.0, 40.56), to_colour,
                      width=self.canvas_w)
        draw_gradient(self.cans[2], yiq_to_rgb(30, 100, -100),
                      yiq_to_rgb(30, 100, 100), width=self.canvas_w)

        self.related(30, 100.0, 40.56)

        self.canYiq = canYiq = Canvas(lf4, width=self.space, height=self.space)
        canYiq.grid(column=0, row=9, columnspan=3, pady=25, sticky='n')
        self.yiqGamut = PhotoImage(file='../figures/colour_space.png')
        canYiq.create_image(0, 0, anchor='nw', image = self.yiqGamut)
        self.ring = circle(canYiq, 300.0, 210.84, self.ring_radius, width=self.ring_width,
                           activeoutline='#555555', tags='ring')

        canYiq.bind('<Button-1>', self.move_ring)
        canYiq.tag_bind('ring', '<B1-Motion>',self.move_ring)

    def move_ring(self, event):
        """Procedure called when mouse clicked or dragged in colour space

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
        X = min(max(X,0),space)
        Y = min(max(Y,0),space)

        for s in self.canYiq.find_withtag("ring"):
            self.canYiq.coords(s, X-ring_radius, Y-ring_radius, X+ring_radius, Y+ring_radius)

        i = (X-space//2)*2/3
        q = (Y-space//2)*2/3
        self.ivar.set(i)
        self.qvar.set(q)
        ring=i,q
        self.door_bell(ring)

    def checksyiq(self, evt):
        """Procedure called by yiq spinboxes.

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

    def checkhash(self, evt):
        """Procedure called by entry for hash.

        Parameters
        ----------
        evt : str
            bind handles

        """

        h = self.en.get()
        if len(h) == 7:
            red, green, blue = hash2rgb(h)
            alpha = self.avar.get()
            self.rvar.set(red)
            self.gvar.set(green)
            self.bvar.set(blue)
            draw_agradient(self.rgbcans[3], (127, 127, 127),
                           (red, green, blue), width=self.canvas_w)
            draw_gradient(self.rgbcans[0], (0, green, blue),
                          (255, green, blue), width=self.canvas_w)
            draw_gradient(self.rgbcans[1], (red, 0, blue),
                          (red, 255, blue), width=self.canvas_w)
            draw_gradient(self.rgbcans[2], (red, green, 0),
                          (red, green, 255), width=self.canvas_w)
            vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)
            self.overlord(rgb=(red, green, blue))

    def checksba(self, evt):
        """Procedure called by alpha spinbox.

        Parameters
        ----------
        evt : str
            bind handles

        """

        alpha = self.avar.get()
        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)

    def checksb(self, evt):
        """Procedure called by rgb colour spinboxes.

        Parameters
        ----------
        evt : str
            bind handles

        """

        alpha = self.avar.get()
        red = self.rvar.get()
        green = self.gvar.get()
        blue = self.bvar.get()
        draw_agradient(self.rgbcans[3], (127, 127, 127),
                       (red, green, blue), width=self.canvas_w)
        draw_gradient(self.rgbcans[0], (0, green, blue),
                      (255, green, blue), width=self.canvas_w)
        draw_gradient(self.rgbcans[1], (red, 0, blue),
                      (red, 255, blue), width=self.canvas_w)
        draw_gradient(self.rgbcans[2], (red, green, 0),
                      (red, green, 255), width=self.canvas_w)
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)
        self.evar.set(rgb2hash(red, green, blue))

if __name__ == "__main__":
    root = Tk()

    img = Image.new("RGBA",(16,10),'#00000000')
    trough = ImageTk.PhotoImage(img)

    # constants for creating upward pointing arrow
    width = 17
    height = 17
    offset = 5
    st = width//2, height-1-offset
    light = 'GreenYellow'
    med = 'LawnGreen'
    dark = '#5D9B90'

    # normal state
    im=Image.new("RGBA", (width, height), '#00000000')
    rdraw = ImageDraw.Draw(im)
    rdraw.polygon([st[0], st[1], 0, height-1, width-1, height-1], fill=light)
    rdraw.polygon([st[0], st[1], st[0], 0, 0, height-1], fill=med)
    rdraw.polygon([st[0], st[1], width-1, height-1, st[0], 0], fill=dark)
    slider = ImageTk.PhotoImage(im)

    #pressed state
    imp = Image.new("RGBA", (width, height), '#00000000')
    draw = ImageDraw.Draw(imp)
    draw.polygon([st[0], st[1], 0, height-1, width-1, height-1], fill=light)
    draw.polygon([st[0], st[1], st[0], 0, 0, height-1], fill=dark)
    draw.polygon([st[0],st[1], width-1, height-1, st[0], 0], fill=med)
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

    root.columnconfigure(0, weight=1)
    fr = Frame(root)
    fr.grid(row=0, column=0, sticky='nsew')
    fr.columnconfigure(0, weight=1)
    fr.columnconfigure(2, weight=1)
    RgbYiqSelect(fr)
    root.mainloop()
