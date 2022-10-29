""" Construction three gradients in rgb"""

from tkinter import Tk, Canvas, Spinbox, Scale, Label, IntVar, Frame


def lerp_hex(colour1, colour2, fraction):
    """linear gradient

    Parameters
    ----------
    colour1 : tuple of int
        start colour
    colour2 : tuple of int
        end colour
    fraction : float
        normalised colour fraction

    Results
    -------
    string
        hexadecimal colour
    """

    return '#%02x%02x%02x' % (int(colour1[0] + (colour2[0] - colour1[0]) * fraction),
                              int(colour1[1] + (colour2[1] -
                                                colour1[1]) * fraction),
                              int(colour1[2] + (colour2[2] - colour1[2]) * fraction))


def draw_gradient(canvas, colour1, colour2, steps=256, width=300, height=26):
    """Draw gradient in tkinter

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

    for i in range(steps):
        x0 = int((width * i) / steps)
        x1 = int((width * (i + 1)) / steps)

        canvas.create_rectangle((x0, 0, x1, height), fill=lerp_hex(
            colour1, colour2, i / (steps - 1)), outline='')


class RgbSelect:
    """Class to construct rgb gradients

    Parameters
    ----------
    parent : str
        parent widget
    Returns
    -------
    None
    """

    def __init__(self, parent, enlargement):
        self.parent = parent
        self.e = enlargement

        self.rvar = IntVar()
        self.gvar = IntVar()
        self.bvar = IntVar()

        self.red = self.rvar.get()
        self.green = self.gvar.get()
        self.blue = self.bvar.get()

        self.build()

    def rhandle(self, evt=None):
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
        draw_gradient(self.gcan, (red, 0, blue), (red, 255, blue), width=300*self.e,
                      height=26*self.e)
        draw_gradient(self.bcan, (red, green, 0), (red, green, 255), width=300*self.e,
                      height=26*self.e)
        self.lab['background'] = self.rgbhash(red, green, blue)

    def ghandle(self, evt=None):
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
        draw_gradient(self.rcan, (0, green, blue),
                      (255, green, blue), width=300*self.e, height=26*self.e)
        draw_gradient(self.bcan, (red, green, 0), (red, green, 255),
                        width=300*self.e, height=26*self.e)
        self.lab['background'] = self.rgbhash(red, green, blue)

    def bhandle(self, evt=None):
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
        draw_gradient(self.rcan, (0, green, blue),
                      (255, green, blue), width=300*self.e, height=26*self.e)
        draw_gradient(self.gcan, (red, 0, blue), (red, 255, blue),
                        width=300*self.e, height=26*self.e)
        self.lab['background'] = self.rgbhash(red, green, blue)

    def build(self):
        """widget construction

        Parameters
        ----------
        None

        Results
        -------
        None
        """

        rl1 = Label(self.parent, text='red  ')
        rl1.grid(column=0, row=0)

        self.rcan = Canvas(self.parent, width=300*self.e, height=26*self.e)
        self.rcan.grid(column=1, row=0, sticky='n')

        rsc = Scale(
            self.parent,
            from_=0,
            to=255,
            variable=self.rvar,
            orient='horizontal',
            length=300*self.e,
            command=self.rhandle,
            tickinterval=20,
            showvalue=0,
            width=15*self.e,
            sliderlength=30*self.e)
        
        rsc.grid(column=1, row=1, sticky='nw')

        rsb = Spinbox(self.parent, from_=0, to=255, textvariable=self.rvar,
                      command=self.rhandle, width=5*self.e)
        rsb.grid(column=2, row=0, sticky='nw')

        gl1 = Label(self.parent, text='green')
        gl1.grid(column=0, row=2)

        self.gcan = Canvas(self.parent, width=300*self.e, height=26*self.e)
        self.gcan.grid(column=1, row=2, sticky='n')

        gsc = Scale(
            self.parent,
            from_=0,
            to=255,
            variable=self.gvar,
            orient='horizontal',
            length=300*self.e,
            command=self.ghandle,
            tickinterval=20,
            showvalue=0,
            width=15*self.e,
            sliderlength=30*self.e)
        
        gsc.grid(column=1, row=3, sticky='nw')

        gsb = Spinbox(self.parent, from_=0, to=255, textvariable=self.gvar,
                      command=self.ghandle, width=5*self.e)
        gsb.grid(column=2, row=2, sticky='nw')

        bl1 = Label(self.parent, text='blue ')
        bl1.grid(column=0, row=4)

        self.bcan = Canvas(self.parent, width=300*self.e, height=26*self.e)
        self.bcan.grid(column=1, row=4, sticky='n')

        bsc = Scale(
            self.parent,
            from_=0,
            to=255,
            variable=self.bvar,
            orient='horizontal',
            length=300*self.e,
            command=self.bhandle,
            tickinterval=20,
            showvalue=0,
            width=15*self.e,
            sliderlength=30*self.e)
        
        bsc.grid(column=1, row=5, sticky='nw')

        bsb = Spinbox(self.parent, from_=0, to=255, textvariable=self.bvar,
                      command=self.bhandle, width=5*self.e)
        bsb.grid(column=2, row=4, sticky='nw')

        self.lab = lab = Label(self.parent, height=4, width=10)
        lab.grid(column=1, row=6)
        lab.grid_propagate(0)
        lab['background'] = self.rgbhash(self.red, self.green, self.blue)

    def rgbhash(self, red, green, blue):
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


if __name__ == "__main__":
    root = Tk()
    winsys = root.tk.call("tk", "windowingsystem")
    BASELINE = 1.33398982438864281 if winsys != 'aqua' else 1.000492368291482
    scaling = root.tk.call("tk", "scaling")
    enlargement = int(scaling / BASELINE + 0.5)
    fra1 = Frame(root)
    fra1.grid(row=0, column=0)
    RgbSelect(fra1, enlargement)
    root.mainloop()

