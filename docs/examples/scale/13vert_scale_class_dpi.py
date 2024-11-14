from tkinter import Tk, font
from tkinter.ttk import Style, Scale, Label, Frame
import numpy as np
import ctypes

# increased padx TtkScale

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class  TtkScale(Scale):
    def __init__(self, parent, length=0, from_=0, to=255, orient='vertical',
                variable=0, digits=None, tickinterval=None,
                 command=None, style=None, showvalue=True, resolution=1):

        self.from_ = from_
        self.to = to
        self.variable = variable
        self.length = length
        self.command = command
        self.parent = parent

        super().__init__(parent, length=length, from_=from_, to=to, orient=orient,
                        variable=variable, command=command, style=style)

        self.digits = digits
        self.tickinterval = tickinterval
        self.showvalue = showvalue
        self.resolution = resolution

        # set sliderlength
        st = Style(self)
        self.bw_val = bw_val = st.lookup('Vertical.Scale.trough','borderwidth')
        print(bw_val)
        self.sliderlength = sliderlength = 32

        if showvalue:
            self.configure(command=self.display_value)

        def_font = font.nametofont('TkDefaultFont')
        # if from_ more than to swap values
        if from_ < to:
            pass
        else:
            from_, to = to, from_

        data = np.arange(from_, (to+1 if tickinterval >=1 else to+tickinterval),
                        tickinterval)
        self.data = data = np.round(data,1)
        range_vals = tuple(data)
        len_rvs = len(range_vals)
        lspace = def_font.metrics('linespace')
        len_rvs = len(range_vals)
        data_size = len_rvs * lspace
        space_size = len_rvs * 3
        sizes = data_size + space_size
        min_len = (sizes if sizes % 50 == 0 else sizes + 50 - sizes % 50)
        self.len_val = len_val = min_len if length < min_len else length
        self.configure(length=len_val)
        if bw_val == "":
            bw_val = 0
        self.rel_min = rel_min = (sliderlength / 2 + bw_val) / len_val
        self.rel_max = rel_max = 1 - (sliderlength /2 - bw_val) / len_val
        if range_vals[-1] == to:
            pass
        else:
            max_rv = range_vals[-1]
            self.mult_y = mult_y = ((max_rv - from_)*rel_max/(to - from_))
        self.bind("<Button-1>", self.resolve)

        self.build(from_, to, rel_min, rel_max, range_vals, len_rvs)

    def build(self, from_, to, rel_min, rel_max, range_vals, len_rvs):

        for i, rv in enumerate(range_vals):
            item = Label(self.parent, text=rv)
            item.place(in_=self, bordermode='outside',
                rely=(rel_min + i / (len_rvs - 1) *
                ((rel_max if range_vals[-1] == to else self.mult_y) - rel_min)) ,
                relx=1, anchor='w')

        if self.showvalue:
            self.disp_lab = Label(self.parent, text=self.get())
            rel_y = self.convert_to_rely(float(self.get())) #, textvariable = self.act_val)
            self.disp_lab.place(in_=self, bordermode='outside',
                rely=rel_y, relx=0, anchor='e')

    def convert_to_rely(self, curr_val):
        return ((curr_val - self.from_) * (self.rel_max - self.rel_min) /
                (self.to - self.from_) + self.rel_min)

    def convert_to_acty(self, curr_val):
        y_max = self.rel_max * self.len_val
        y_min = self.rel_min * self.len_val
        return ((curr_val - self.from_) * (y_max - y_min) /
                (self.to - self.from_) + y_min)

    def display_value(self, value):
        # position (in pixel) of the center of the slider
        rel_y = self.convert_to_rely(float(value))
        self.disp_lab.config(text=value) # text=""
        self.disp_lab.place_configure(rely=rel_y)
        self.disp_lab.configure(text=f'{float(value):.{dig_val}f}')
        # if your python is not 3.6 or above use the following 2 lines
        #   instead of the line above
        #my_precision = '{:.{}f}'.format
        #self.disp_lab.configure(text=my_precision(float(value), digits))

    def resolve(self, evt):
        resolution = self.resolution
        if resolution < 1 or self.tickinterval < 1:
            pass
        else:
            value = self.get()
            curr_y = self.convert_to_acty(value)
            if evt.y < curr_y - self.sliderlength / 2:
                self.set(value - resolution + 1)
            elif evt.y > curr_y + self.sliderlength / 2:
                self.set(value + resolution - 1)

if __name__ == "__main__":
    root = Tk()
    ORIGINAL_DPI = 96
    current_dpi = root.winfo_fpixels('1i')
    SCALE = current_dpi / ORIGINAL_DPI
    # when current_dpi is 192 SCALE becomes 2.0
    root.tk.call('tk', 'scaling', SCALE)

    len_val = 400
    from_val = 0
    to_val = 255
    tick_val = 10
    dig_val = 2
    res_val = 5

    style = Style()
    style.theme_use('default')
    style.configure('my.Vertical.TScale')

    fr = Frame(root)
    fr.pack(fill='y')

    ttks = TtkScale(fr, from_=from_val, to=to_val, orient='vertical',
                    tickinterval=tick_val, digits=dig_val,
                    style='my.Vertical.TScale', resolution=res_val)
    ttks.pack(fill='y', pady=5, padx=60)

    root.mainloop()
