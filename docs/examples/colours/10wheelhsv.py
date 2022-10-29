""" Construction three gradients in hsv using PPM image
    spinbox validation, working with modified Scale
    adding colour wheel and cursor actions
"""

from tkinter import Tk, Canvas, Label, IntVar, Frame, PhotoImage
from tkinter.ttk import LabelFrame, Scale, Style, Spinbox
from PIL import Image, ImageDraw, ImageTk
from colourTools import draw_gradient, hsv_to_rgb, hue_gradient, circle

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
                 command=None, enlargement=1):
        self.from_ = from_
        self.to = to
        self.variable = variable

        super().__init__(parent, length=length + sliderlength, orient=orient,
                         variable=variable, from_=from_, to=to, command=command)

        self.digits = digits
        self.length = length
        self.e = enlargement

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
                           relx=sliderlength*self.e / length*self.e / 2 +
                           i / sc_range * (1 - sliderlength*self.e / length*self.e),
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

    def __init__(self, fr0, enlargement):
        self.fr0 = fr0

        self.hvar = IntVar()
        self.svar = IntVar()
        self.vvar = IntVar()
        self.e = enlargement

        self.scale_l = 300*self.e
        self.canvas_w = self.scale_l
        self.canvas_h = 26*self.e
        self.cursor_w = 16*self.e
        self.wheel_w = 317*self.e
        self.wheel_iw = 299*self.e
        self.ring_radius = 10*self.e
        self.ring_width = 3*self.e

        self.build()

        self.hvar.set(0)
        self.svar.set(100)
        self.vvar.set(100)

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
        draw_gradient(self.scan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)

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
        draw_gradient(self.scan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)

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
        draw_gradient(self.scan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)

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

        hue_gradient(self.hcan, width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.scan, (255, 255, 255), to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.vcan, (0, 0, 0), to_colour,
                      width=self.canvas_w, height=self.canvas_h)

        can_hsv = Canvas(fr4, width=self.wheel_w,
                         height=self.wheel_w, bg='#d9d9d9')
        can_hsv.grid(column=1, row=9, pady=25, sticky='n')
        self.hsv_gamut = PhotoImage(file='../../figures/colour_wheel'+str(self.e)+'.png')
        can_hsv.create_image(0, 0, anchor='nw', image=self.hsv_gamut)
        self.ring = circle(can_hsv, 307*self.e, 158*self.e, self.ring_radius,
                           width=self.ring_width, tags='ring')

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
        draw_gradient(self.scan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)

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
        draw_gradient(self.scan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)
        from_colour = hsv_to_rgb(*(hue, sat, 0))
        to_colour = hsv_to_rgb(*(hue, sat, 100))
        draw_gradient(self.vcan, from_colour, to_colour,
                      width=self.canvas_w, height=self.canvas_h)


if __name__ == "__main__":
    root = Tk()
    winsys = root.tk.call("tk", "windowingsystem")
    BASELINE = 1.33398982438864281 if winsys != 'aqua' else 1.000492368291482
    scaling = root.tk.call("tk", "scaling")
    enlargement = e = int(scaling / BASELINE + 0.5)

    img = Image.new("RGBA", (16, 10), '#00000000')
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
    #root.geometry("500x600+200+100")
    fra0 = Frame(root)
    fra0.grid(row=0, column=0, sticky='nsew')
    HsvSelect(fra0, enlargement)
    root.mainloop()

root.mainloop()
