"""Module containing TtkScale based on the ttk Scale with the enhancements.
The following options are added:-

* display
    a range of values, corresponding to the from and to attributes.

* tickinterval
    the interval between the values in the range

* showvalue
    whether the Scale displays the actual value beside the slider

* digits
    the number of decimal places shown in the actual value display

* resolution
    the amount the slider will move if the trough is cliced

* sliderlength
    the length used in calculating the range

* length
    this value is overwritten if the range requires extra space

"""

from tkinter import Tk, font
from tkinter.ttk import Style, Scale, Label, Frame
import numpy as np

class  TtkScale(Scale):
    """ Enhanced ttk Scale

    Parameters
    ----------
    parent : str
                The parent tk widget, normally a Frame.
    length : int
                The Scale length in pixels.
    from_ : int
                The minimum extent of the range.
    to : int
                the maximum extent of slider movement.
    orient : str
                Either 'horizontal' or 'vertical'
    variable : var
                Name of a tkinter variable.
    digits : int
                Number of decimal places displayed on actual value.
    tickinterval : int or float
                Spacing between range values.
    sliderlength : int
                Length used to set range position.
    command : var
                Method that is called whenever the slider moves.
    style : str
                Used to set the Scale's appearance.
    showvalue : bool
                True turns on the actual display value.
    resolution : int
                Amount slider moves when the trough is clicked, in pixels.

    """


    def __init__(self, parent, length=0, from_=0, to=255, orient='horizontal',
                variable=0, digits=0, tickinterval=None, sliderlength=32,
                 command=None, style=None, showvalue=True, resolution=1):

        self.from_ = from_
        self.to = to
        self.variable = variable
        self.length = length
        self.command = command
        self.parent = parent
        self.orient = orient

        super().__init__(parent, length=length, from_=from_, to=to, orient=orient,
                        variable=variable, command=command, style=style)

        self.digits = digits
        self.tickinterval = tickinterval
        self.showvalue = showvalue
        self.resolution = resolution
        self.sliderlength = sliderlength # = 32

        theme_sl = {'alt': 9, 'clam': 30, 'classic': 30, 'default': 30,
                    'lime': 9, 'winnative': 9}

        theme_bw = {'alt': 0, 'clam': 1, 'classic': 2, 'default': 1,
                    'lime': 6, 'winnative': 0}

        # set trough borderwidth
        st = Style(self)
        theme_used = st.theme_use()
        if theme_used in ('alt', 'clam', 'classic', 'default','lime', 'winnative'):
            self.bw_val = bw_val = theme_bw[theme_used]
            self.sliderlength = sliderlength = theme_sl[theme_used]
        else:
            self.bw_val = bw_val = 1

        if showvalue:
            self.configure(command=self.display_value)

        if showvalue:
            self.configure(command=self.display_value)

        def_font = font.nametofont('TkDefaultFont')

        data = np.arange(from_, (to+1 if tickinterval >=1 else to+tickinterval),
                        tickinterval)
        self.data = data = np.round(data,1)
        range_vals = tuple(data)
        len_rvs = len(range_vals)
        if self.orient == 'horizontal':
            vals_size = [def_font.measure(str(i)) for i in range_vals]
            data_size = sum(vals_size)
            space_size = len_rvs * def_font.measure('0')
        else:
            lspace = def_font.metrics('linespace')
            data_size = len_rvs * lspace
            space_size = len_rvs * 3
        sizes = data_size + space_size
        min_len = (sizes if sizes % 50 == 0 else sizes + 50 - sizes % 50)
        self.len_val = len_val = min_len if length < min_len else length
        self.configure(length=len_val)

        self.rel_min = rel_min = (sliderlength // 2 + bw_val) / len_val
        self.rel_max = rel_max = 1 - (sliderlength // 2 - bw_val) / len_val

        if range_vals[-1] == to:
            pass
        else:
            max_rv = range_vals[-1]
            self.mult_l = ((max_rv - from_)*rel_max/(to - from_))

        self.bind("<Button-1>", self.resolve)

        self.build(to, rel_min, rel_max, range_vals, len_rvs)

    def build(self, to, rel_min, rel_max, range_vals, len_rvs):
        """Creates the Labels used to show the range and the first actual value.

        Parameters
        ----------
        to : int
                The maximum extent of slider movement.
        rel_min : float
                The range's minimum position as a relative size of the Scale.
        rel_max : float
                The range's maximum position as a relative size of the Scale.
        range_vals : tuple of int or floats
                The values shown in the range.
        len_rvs : int
                Size of the range values.

        """

        if self.orient == 'horizontal':
            for i, rv in enumerate(range_vals):
                item = Label(self.parent, text=rv)
                item.place(in_=self, bordermode='outside',
                relx=(rel_min + i / (len_rvs - 1) *
                ((rel_max if range_vals[-1] == to else self.mult_l) - rel_min)) ,
                rely=1, anchor='n')
        else:
            for i, rv in enumerate(range_vals):
                item = Label(self.parent, text=rv)
                item.place(in_=self, bordermode='outside',
                rely=(rel_min + i / (len_rvs - 1) *
                ((rel_max if range_vals[-1] == to else self.mult_l) - rel_min)) ,
                relx=1, anchor='w')

        if self.showvalue:
            self.disp_lab = Label(self.parent, text=self.get())
            rel_l = self.convert_to_rel(float(self.get()))
            if self.orient == 'horizontal':
                self.disp_lab.place(in_=self, bordermode='outside',
                relx=rel_l, rely=0, anchor='s')
            else:
                self.disp_lab.place(in_=self, bordermode='outside',
                rely=rel_l, relx=0, anchor='e')

    def convert_to_rel(self, curr_val):
        """Method to convert the actual value to a relative position.

        Parameters
        ----------
        curr_val : float
                    Actual value of the Scale.

        Returns
        -------
        float

        """
        return ((curr_val - self.from_) * (self.rel_max - self.rel_min) /
                (self.to - self.from_) + self.rel_min)

    def convert_to_act(self, curr_val):
        """Method to convert the actual value to an actual position.

        Parameters
        ----------
        curr_val : float
                    Actual value of the Scale.

        Returns
        -------
        float

        """

        l_max = self.rel_max * self.len_val
        l_min = self.rel_min * self.len_val
        return ((curr_val - self.from_) * (l_max - l_min) /
                (self.to - self.from_) + l_min)

    def display_value(self, value):
        """Position (in pixel) of the centre of the slider.

        Parameters
        ----------
        value : float
                    Actual value of the Scale.

        Returns
        -------
        float

        """

        rel_l = self.convert_to_rel(float(value))
        self.disp_lab.config(text=value) # text=""
        if self.orient == 'horizontal':
            self.disp_lab.place_configure(relx=rel_l)
        else:
            self.disp_lab.place_configure(rely=rel_l)
        digits = self.digits
        self.disp_lab.configure(text=f'{float(value):.{digits}f}')
        # if your python is not 3.6 or above use the following 2 lines
        #   instead of the line above
        #my_precision = '{:.{}f}'.format
        #self.disp_lab.configure(text=my_precision(float(value), digits))

    def resolve(self, evt):
        """Enables mouse click in trough to move slider selected pixel
            amount

        Parameters
        ----------
        evt : str
                    Actual position of the cursor.

        """

        resolution = self.resolution
        if resolution < 1 or self.tickinterval < 1:
            pass
        else:
            value = self.get()
            curr_l = self.convert_to_act(value)
            if self.orient == 'horizontal':
                if evt.x < curr_l - self.sliderlength / 2:
                    self.set(value - resolution + 1)
                elif evt.x > curr_l + self.sliderlength / 2:
                    self.set(value + resolution - 1)
            else:
                if evt.y < curr_l - self.sliderlength / 2:
                    self.set(value - resolution + 1)
                elif evt.y > curr_l + self.sliderlength / 2:
                    self.set(value + resolution - 1)

if __name__ == "__main__":
    root = Tk()

    LEN_VAL = 400
    FROM_VAL = 0
    TO_VAL = 255
    TICK_VAL = 10
    DIG_VAL = 2
    RES_VAL = 5
    OR_VAL = 'vertical'

    if OR_VAL =='horizontal':
        STYLE_VAL = 'my.Horizontal.TScale'
        root.geometry(str(LEN_VAL+200)+"x200+500+500")
    else:
        STYLE_VAL = 'my.Vertical.TScale'
        root.geometry("200x"+str(LEN_VAL+200)+"+500+300")

    style = Style()
    style.theme_use('default')
    style.configure(STYLE_VAL)

    fr = Frame(root)
    fr.pack(fill='y')

    ttks = TtkScale(fr, from_=FROM_VAL, to=TO_VAL, orient=OR_VAL,
                    tickinterval=TICK_VAL, digits=DIG_VAL,
                    style=STYLE_VAL, resolution=RES_VAL)
    if OR_VAL =='horizontal':
        ttks.pack(fill='x', pady=40, padx=5)
    else:
        ttks.pack(fill='y', pady=5, padx=40)

    root.mainloop()
