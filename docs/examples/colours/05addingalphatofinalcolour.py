""" Construction four gradients in rgba using PPM image, added final colour"""

from tkinter import Tk, Canvas, Spinbox, Scale, Label, IntVar, StringVar, Frame, PhotoImage
from tkinter.ttk import LabelFrame, Entry
import numpy as np


def rgbhash(red, green, blue):
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
    width : int
        canvas width
    height : int
        canvas height
    square_size : int
        size each square

    Returns
    -------
    array of integers
    """

    array = np.zeros([height, width, 3], dtype=np.uint8)  # ,dtype=np.uint8
    for x in range(width):
        for y in range(height):
            if (x % square_size * 2) // square_size ==\
                (y % square_size * 2) // square_size:
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


def vcheck(width, height, alpha, square_size=4):
    """Draw vertical chequers in numpy as array
        chequer value to grey or white depends on y position

    Parameters
    ----------
    width : int
        canvas width
    height : int
        canvas height
    alpha : int
        opacity
    square_size : int
        size each square

    Returns
    -------
    array of integers
    """

    # Set check value to grey or black depending on y position and alpha
    al0 = 127 - alpha // 2
    ah0 = al0 / height
    array = np.zeros([height, width, 3], dtype=np.uint8)  # ,dtype=np.uint8
    for y in range(height):
        for x in range(width):
            if (x % square_size * 2) // square_size == (y % square_size * 2) \
                    // square_size:
                array[y, x] = int(0.5 + ah0 * y)
    return array


def vgenerate_gradient(to_colour, alpha, height, width):
    """Draw vertical gradient in numpy as array

    Parameters
    ----------
    to_colour : tuple of int
        end colour
    alpha : int
        opacity
    height : int
        canvas height
    width : int
        canvas width

    Returns
    -------
    array of integers
    """

    al0 = alpha / 255
    res0 = 1 - al0
    from_colour = (int(to_colour[0] * al0 + 127 *  res0),
                  int(to_colour[1] * al0 + 127 *  res0),
                  int(to_colour[2] * al0 + 127 *  res0))  # changing from_colour
    new_ch = [
        np.tile(
            np.linspace(
                to_colour[i], from_colour[i], height, dtype=np.uint8), [
                    width, 1]).T for i in range(3)]
    return np.dstack(new_ch)


def vdraw_gradient(canvas, colour1, alpha=255, width=30, height=30):
    """Either fill in background
        or import vertical gradient into tkinter

    Parameters
    ----------
    canvas : str
        parent widget
    colour1 : tuple of int
        start colour
    alpha : int
        opacity
    width : int
        canvas width
    height : int
        canvas height

    Returns
    -------
    None
    """
    if alpha > 240:
        hash_value = rgbhash(colour1[0], colour1[1], colour1[2])
        canvas['background'] = hash_value
        canvas.background = hash_value
    else:
        arr = vgenerate_gradient(colour1, alpha, height, width)
        arr1 = vcheck(width, height, alpha)
        xdata = 'P6 {} {} 255 '.format(
            width, height).encode() + (arr + arr1).tobytes()
        gradient = PhotoImage(
            width=width,
            height=height,
            data=xdata,
            format='PPM')
        canvas.create_image(0, 0, anchor="nw", image=gradient)
        canvas.image = gradient


class RgbSelect:
    """Class to construct rgba gradients and final colour

    Parameters
    ----------
    fr : str
        parent widget
    """

    def __init__(self, parent):
        self.parent = parent
        self.rvar = IntVar()
        self.gvar = IntVar()
        self.bvar = IntVar()
        self.avar = IntVar()
        self.evar = StringVar()

        self.scale_l = 300
        self.canvas_w = self.scale_l - 30
        self.canvas_h = 26
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
        draw_gradient(self.gcan, (red, 0, blue),
                      (red, 255, blue), width=self.canvas_w)
        draw_gradient(self.bcan, (red, green, 0),
                      (red, green, 255), width=self.canvas_w)
        draw_agradient(self.acan, (127, 127, 127),
                       (red, green, blue), width=self.canvas_w)
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)
        self.evar.set(rgbhash(red, green, blue))

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
        draw_gradient(self.rcan, (0, green, blue),
                      (255, green, blue), width=self.canvas_w)
        draw_gradient(self.bcan, (red, green, 0),
                      (red, green, 255), width=self.canvas_w)
        draw_agradient(self.acan, (127, 127, 127), (red, green, blue),
                       width=self.canvas_w)
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)
        self.evar.set(rgbhash(red, green, blue))

    def bhandle(self, *args):
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
        alpha = self.avar.get()
        draw_gradient(self.rcan, (0, green, blue),
                      (255, green, blue), width=self.canvas_w)
        draw_gradient(self.gcan, (red, 0, blue),
                      (red, 255, blue), width=self.canvas_w)
        draw_agradient(self.acan, (127, 127, 127),
                       (red, green, blue), width=self.canvas_w)
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)
        self.evar.set(rgbhash(red, green, blue))

    def ahandle(self, *args):
        """command callback for opacity

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
        vdraw_gradient(self.cmcan, (red, green, blue), alpha=alpha)

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

        rl1 = Label(fr1, text='red  ')
        rl1.grid(column=0, row=0, sticky='s')

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

        gl1 = Label(fr1, text='green')
        gl1.grid(column=0, row=2)

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

        bl1 = Label(fr1, text='blue ')
        bl1.grid(column=0, row=4, sticky='s')

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

        self.cmcan = cmcan = Canvas(fr3, width=30, height=30, bd=0,
                                    highlightthickness=0)
        cmcan.grid(column=0, row=0, sticky='n', columnspan=2)
        cmcan.grid_propagate(0)
        vdraw_gradient(self.cmcan, (255, 0, 0), alpha=255)

        cml = Label(fr3, text='hash\nvalue')
        cml.grid(column=0, row=1)

        ent1 = Entry(fr3, width=8, textvariable=self.evar)
        ent1.grid(column=1, row=1)

        fr2 = LabelFrame(self.parent, text='opacity')
        fr2.grid(column=0, row=1, sticky='w')

        al1 = Label(fr2, text='alpha')
        al1.grid(column=0, row=0, sticky='s')

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

        draw_gradient(self.rcan, (0, 0, 0), (255, 0, 0), width=self.canvas_w)
        draw_gradient(self.gcan, (255, 0, 0),
                      (255, 255, 0), width=self.canvas_w)
        draw_gradient(self.bcan, (255, 0, 0),
                      (255, 0, 255), width=self.canvas_w)
        draw_agradient(self.acan, (127, 127, 127),
                       (255, 0, 0), width=self.canvas_w)


if __name__ == "__main__":
    root = Tk()
    fra1 = Frame(root)
    fra1.grid(row=0, column=0)
    RgbSelect(fra1)
    root.mainloop()

root.mainloop()
