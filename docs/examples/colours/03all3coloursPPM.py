""" Construction three gradients in rgb using PPM image"""

from tkinter import Tk, Canvas, Spinbox, Scale, Label, IntVar, Frame, PhotoImage
import numpy as np


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
    new_ch = [
        np.tile(
            np.linspace(
                from_colour[i], to_colour[i], width, dtype=np.uint8), [
                    height, 1]) for i in range(
                        len(from_colour))]
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
    enlargement : int
        dpi enlargement factor
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


class RgbSelect:
    """Class to construct rgb gradients

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
        self.rvar = IntVar()
        self.gvar = IntVar()
        self.bvar = IntVar()

        self.scale_l = 300 * self.e
        self.canvas_w = self.scale_l - 30 * self.e
        self.canvas_h = 26 * self.e
        self.build()

        self.rvar.set(255)
        self.gvar.set(0)
        self.bvar.set(0)

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
        draw_gradient(self.gcan, (red, 0, blue), (red, 255, blue),
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.bcan, (red, green, 0), (red, green, 255),
                      width=self.canvas_w, height=self.canvas_h)
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
        draw_gradient(self.rcan, (0, green, blue), (255, green, blue),
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.bcan, (red, green, 0), (red, green, 255),
                      width=self.canvas_w, height=self.canvas_h)
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
        draw_gradient(self.rcan, (0, green, blue), (255, green, blue),
                      width=self.canvas_w, height=self.canvas_h)
        draw_gradient(self.gcan, (red, 0, blue), (red, 255, blue),
                      width=self.canvas_w, height=self.canvas_h)
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

        rl1 = Label(self.fr0, text='red  ')
        rl1.grid(column=0, row=0)

        self.rcan = Canvas(self.fr0, width=self.canvas_w, height=self.canvas_h)
        self.rcan.grid(column=1, row=0, sticky='n')

        rsc = Scale(
            self.fr0,
            from_=0,
            to=255,
            variable=self.rvar,
            orient='horizontal',
            length=self.scale_l,
            command=self.rhandle,
            tickinterval=20,
            showvalue=0,
            width=15*self.e,
            sliderlength=30*self.e)
        
        rsc.grid(column=1, row=1, sticky='nw')

        rsb = Spinbox(self.fr0, from_=0, to=255, textvariable=self.rvar,
                      command=self.rhandle, width=5)
        rsb.grid(column=2, row=1, sticky='nw')

        gl1 = Label(self.fr0, text='green')
        gl1.grid(column=0, row=2)

        self.gcan = Canvas(self.fr0, width=self.canvas_w, height=self.canvas_h)
        self.gcan.grid(column=1, row=2, sticky='n')

        gsc = Scale(
            self.fr0,
            from_=0,
            to=255,
            variable=self.gvar,
            orient='horizontal',
            length=self.scale_l,
            command=self.ghandle,
            tickinterval=20,
            showvalue=0,
            width=15*self.e,
            sliderlength=30*self.e)
        
        gsc.grid(column=1, row=3, sticky='nw')

        gsb = Spinbox(self.fr0, from_=0, to=255, textvariable=self.gvar,
                      command=self.ghandle, width=5)
        gsb.grid(column=2, row=3, sticky='nw')

        bl1 = Label(self.fr0, text='blue ')
        bl1.grid(column=0, row=4)

        self.bcan = Canvas(self.fr0, width=self.canvas_w, height=self.canvas_h)
        self.bcan.grid(column=1, row=4, sticky='n')

        bsc = Scale(
            self.fr0,
            from_=0,
            to=255,
            variable=self.bvar,
            orient='horizontal',
            length=self.scale_l,
            command=self.bhandle,
            tickinterval=20,
            showvalue=0,
            width=15*self.e,
            sliderlength=30*self.e)
        
        bsc.grid(column=1, row=5, sticky='nw')

        bsb = Spinbox(self.fr0, from_=0, to=255, textvariable=self.bvar,
                      command=self.bhandle, width=5)
        bsb.grid(column=2, row=5, sticky='nw')

        self.lab = lab = Label(self.fr0, height=4, width=10)
        lab.grid(column=1, row=6)
        lab.grid_propagate(0)
        lab['background'] = self.rgbhash(self.rvar.get(), self.gvar.get(),
                                         self.bvar.get())

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
