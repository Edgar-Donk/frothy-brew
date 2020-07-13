""" Construction four gradients in rgba using PPM image"""


from tkinter import Tk, Canvas, Spinbox, Scale, Label, IntVar, Frame, PhotoImage
from tkinter.ttk import LabelFrame
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


def check(width, height, square_size=4):
    """Draw chequers in numpy as array
        chequer value to grey or white depends on x position

    Parameters
    ----------
    height : int
        canvas height
    width : int
        canvas width
    square_size : int
        size each square

    Returns
    -------
    array of integers
    """

    array = np.zeros([height, width, 3], dtype=np.uint8)  # ,dtype=np.uint8
    for x in range(width):
        for y in range(height):
            if (x %
                square_size * 2) // square_size == (y %
                    square_size * 2) // square_size:
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
    canvas.create_image(0, 0, anchor="nw", image=gradient)
    canvas.image = gradient


class RgbSelect:
    """Class to construct rgba gradients

    Parameters
    ----------
    parent : str
        parent widget
    Returns
    -------
    None
    """

    def __init__(self, parent):
        self.parent = parent
        self.rvar = IntVar()
        self.gvar = IntVar()
        self.bvar = IntVar()
        self.avar = IntVar()

        self.scale_l = 300
        self.canvas_w = self.scale_l - 30
        self.canvas_h = 26
        self.build()

        self.rvar.set(255)
        self.gvar.set(0)
        self.bvar.set(0)
        self.avar.set(255)

    def rhandle(self, _evt):
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
        draw_gradient(self.gcan, (red, 0, blue),
                      (red, 255, blue), width=self.canvas_w)
        draw_gradient(self.bcan, (red, green, 0),
                      (red, green, 255), width=self.canvas_w)
        draw_agradient(self.acan, (127, 127, 127),
                       (red, green, blue), width=self.canvas_w)
        self.lab['background'] = self.rgbhash(red, green, blue)

    def ghandle(self, _evt):
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
                      (255, green, blue), width=self.canvas_w)
        draw_gradient(self.bcan, (red, green, 0),
                      (red, green, 255), width=self.canvas_w)
        draw_agradient(self.acan, (127, 127, 127),
                       (red, green, blue), width=self.canvas_w)
        self.lab['background'] = self.rgbhash(red, green, blue)

    def bhandle(self, _evt):
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
                      (255, green, blue), width=self.canvas_w)
        draw_gradient(self.gcan, (red, 0, blue),
                      (red, 255, blue), width=self.canvas_w)
        draw_agradient(self.acan, (127, 127, 127),
                       (red, green, blue), width=self.canvas_w)
        self.lab['background'] = self.rgbhash(red, green, blue)

    def ahandle(self, _evt):
        """command callback for alpha

        Parameters
        ----------
        None

        Results
        -------
        None
        """
        # red=self.rvar.get()
        # green=self.gvar.get()
        # blue=self.bvar.get()
        #draw_agradient(self.acan,(127,127,127),(red, green, blue),width=self.canvas_w)
        #self.lab['background'] = self.rgbhash(red, green, blue)
        pass

    def build(self):
        """widget construction

        Parameters
        ----------
        None

        Results
        -------
        None
        """

        fr1 = LabelFrame(self.parent, text='rgb')
        fr1.grid(column=0, row=0)

        rl0 = Label(fr1, text='red  ')
        rl0.grid(column=0, row=0, sticky='s')

        self.rcan = Canvas(
            fr1,
            width=self.canvas_w,
            height=self.canvas_h,
            bd=0,
            highlightthickness=0)
        self.rcan.grid(column=1, row=0, sticky='s')

        rsc = Scale(
            fr1,
            from_=0,
            to=255,
            variable=self.rvar,
            orient='horizontal',
            length=self.scale_l,
            command=self.rhandle,
            tickinterval=20,
            showvalue=0)
        rsc.grid(column=1, row=1, sticky='nw')

        rsb = Spinbox(fr1, from_=0, to=255, textvariable=self.rvar,
                      command=self.rhandle, width=5)
        rsb.grid(column=2, row=1, sticky='nw')

        gl0 = Label(fr1, text='green')
        gl0.grid(column=0, row=2)

        self.gcan = Canvas(
            fr1,
            width=self.canvas_w,
            height=self.canvas_h,
            bd=0,
            highlightthickness=0)
        self.gcan.grid(column=1, row=2, sticky='s')

        gsc = Scale(
            fr1,
            from_=0,
            to=255,
            variable=self.gvar,
            orient='horizontal',
            length=self.scale_l,
            command=self.ghandle,
            tickinterval=20,
            showvalue=0)
        gsc.grid(column=1, row=3, sticky='nw')

        gsb = Spinbox(fr1, from_=0, to=255, textvariable=self.gvar,
                      command=self.ghandle, width=5)
        gsb.grid(column=2, row=3, sticky='nw')

        bl0 = Label(fr1, text='blue ')
        bl0.grid(column=0, row=4, sticky='s')

        self.bcan = Canvas(
            fr1,
            width=self.canvas_w,
            height=self.canvas_h,
            bd=0,
            highlightthickness=0)
        self.bcan.grid(column=1, row=4, sticky='n')

        bsc = Scale(
            fr1,
            from_=0,
            to=255,
            variable=self.bvar,
            orient='horizontal',
            length=self.scale_l,
            command=self.bhandle,
            tickinterval=20,
            showvalue=0)
        bsc.grid(column=1, row=5, sticky='nw')

        bsb = Spinbox(fr1, from_=0, to=255, textvariable=self.bvar,
                      command=self.bhandle, width=5)
        bsb.grid(column=2, row=5, sticky='nw')

        fr3 = LabelFrame(self.parent, text='colour mix')
        fr3.grid(column=1, row=0, sticky='nw')

        self.lab = lab = Label(fr3, height=4, width=10)
        lab.grid(column=0, row=0, sticky='nw')
        lab.grid_propagate(0)
        lab['background'] = self.rgbhash(self.rvar.get(), self.gvar.get(),
                                         self.bvar.get())

        fr2 = LabelFrame(self.parent, text='opacity')
        fr2.grid(column=0, row=1, sticky='w')

        al0 = Label(fr2, text='alpha')
        al0.grid(column=0, row=0, sticky='s')

        self.acan = Canvas(fr2, width=self.canvas_w, height=self.canvas_h)
        self.acan.grid(column=1, row=0, sticky='n')

        asc = Scale(
            fr2,
            from_=0,
            to=255,
            variable=self.avar,
            orient='horizontal',
            length=self.scale_l,
            command=self.ahandle,
            tickinterval=20,
            showvalue=0)
        asc.grid(column=1, row=1, sticky='nw')

        asb = Spinbox(fr2, from_=0, to=255, textvariable=self.avar,
                      command=self.ahandle, width=5)
        asb.grid(column=2, row=1, sticky='nw')

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
    fra1 = Frame(root)
    fra1.grid(row=0, column=0)
    RgbSelect(fra1)
    root.mainloop()
