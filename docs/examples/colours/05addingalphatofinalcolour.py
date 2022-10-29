""" Construction four gradients in rgba using PPM image, added final colour"""

from tkinter import Tk, Canvas, Spinbox, Scale, Label, IntVar, StringVar, Frame
from tkinter.ttk import LabelFrame, Entry
from colourTools import rgb2hash, draw_gradient, draw_agradient, vdraw_gradient

class RgbSelect:
    """Class to construct rgba gradients and final colour

    Parameters
    ----------
    fr : str
        parent widget
    """

    def __init__(self, parent, enlargement):
        self.parent = parent
        self.e = enlargement
        self.rvar = IntVar()
        self.gvar = IntVar()
        self.bvar = IntVar()
        self.avar = IntVar()
        self.evar = StringVar()

        self.scale_l = 300 * self.e
        self.canvas_w = self.scale_l - 30 * self.e
        self.canvas_h = 26 * self.e
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
                        width=30*self.e, height=30*self.e)
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
                        width=30*self.e, height=30*self.e)
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

        red = self.rvar.get()
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
                        width=30*self.e, height=30*self.e)
        self.evar.set(rgb2hash(red, green, blue))

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
        vdraw_gradient(self.cmcan, (red, green, blue), self.e, alpha=alpha,
                        width=30*self.e, height=30*self.e)

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
            showvalue=0,
            width=15*self.e,
            sliderlength=30*self.e)
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
            showvalue=0,
            width=15*self.e,
            sliderlength=30*self.e)
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
            showvalue=0,
            width=15*self.e,
            sliderlength=30*self.e)
        bsc.grid(column=1, row=5, sticky='nw')

        bsb = Spinbox(fr1, from_=0, to=255, textvariable=self.bvar,
                      command=self.bhandle, width=5)
        bsb.grid(column=2, row=5, sticky='nw')

        fr3 = LabelFrame(self.parent, text='colour mix')
        fr3.grid(column=1, row=0, sticky='nw')

        self.cmcan = cmcan = Canvas(fr3, width=30*self.e, height=30*self.e, bd=0,
                                    highlightthickness=0)
        cmcan.grid(column=0, row=0, sticky='n', columnspan=2)
        cmcan.grid_propagate(0)
        vdraw_gradient(self.cmcan, (255, 0, 0), self.e, alpha=255,
                        width=30*self.e, height=30*self.e)

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
            showvalue=0,
            width=15*self.e,
            sliderlength=30*self.e)
        asc.grid(column=1, row=1, sticky='nw')

        asb = Spinbox(fr2, from_=0, to=255, textvariable=self.avar,
                      command=self.ahandle, width=5)
        asb.grid(column=2, row=1, sticky='nw')

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
    enlargement = int(scaling / BASELINE + 0.5)
    fra1 = Frame(root)
    fra1.grid(row=0, column=0)
    RgbSelect(fra1, enlargement)
    root.mainloop()

root.mainloop()
