import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import numpy as np
import ctypes

# increased pady both scales

ctypes.windll.shcore.SetProcessDpiAwareness(1)

from_val = -1
to_val = 1
#len_val = 500
res_val = 0.1
tick_val = 0.1
dig_val = 2
bw_val = 1 # trough border width
slider_val = 36
sc_range = abs(to_val - from_val) # scale range

def place_ticks(evt):
    len_val = scth['length']
    rel_min = ((slider_val - from_size) / 2 + bw_val) / len_val
    rel_max = 1 - ((slider_val - to_size )/ 2 - bw_val) / len_val
    data = np.arange(from_val, to_val+tick_val, tick_val)
    data = np.round(data,1)
    range_vals = tuple(data)
    len_rvs = len(range_vals)

    for i, rv in enumerate(range_vals):
        rel_x=(rel_min + i / (len_rvs - 1) * (rel_max - rel_min))
        item.place_configure(relx=rel_x)

root = tk.Tk()
ORIGINAL_DPI = 96
current_dpi = root.winfo_fpixels('1i')
SCALE = current_dpi / ORIGINAL_DPI
# when current_dpi is 192 SCALE becomes 2.0
root.tk.call('tk', 'scaling', SCALE)

def_font = font.nametofont('TkDefaultFont')
# using numpy arange instead of range so tick intervals less than 1 can be used
data = np.arange(from_val, to_val+tick_val, tick_val)
data = np.round(data,1)
range_vals = tuple(data)

vals_size = [def_font.measure(str(i)) for i in range_vals]
data_size = sum(vals_size)
len_rvs = len(range_vals)
space_size = len_rvs * def_font.measure('0')
sizes = data_size + space_size
len_val = (sizes if sizes % 50 == 0 else sizes + 50 - sizes % 50)

root.geometry(str(len_val+200)+"x250+500+500")
s = ttk.Style()
s.theme_use('default')

fr = ttk.Frame(root)
fr.pack(fill='x', expand=1)

from_size = def_font.measure(from_val)
to_size = def_font.measure(to_val)

sch = tk.Scale(fr, from_=from_val, to=to_val, label='Bogusstuinuous', orient='horizontal',
            resolution=res_val, showvalue=1, tickinterval=tick_val, digits=dig_val,
            length=len_val)
sch.grid(sticky='ew', pady=5)

sep = ttk.Separator(fr, orient='horizontal')
sep.grid(row=1, column=0, columnspan=2, sticky='ew')

def convert_to_relx(curr_val):
    return ((curr_val - from_val) * (rel_max - rel_min) / (to_val - from_val) \
            + rel_min)


def display_value(value):
    # position (in pixel) of the center of the slider
    rel_x = convert_to_relx(float(value))
    disp_lab.place_configure(relx=rel_x)
    disp_lab.configure(text=f'{float(value):.{dig_val}f}')

slider = tk.StringVar()
slider.set('0.00')

scth = ttk.Scale(fr, from_=from_val, to=to_val, length=len_val,
        command=display_value, variable=slider)

scth.grid(row=2, column=0, sticky='ew', padx=5, pady=25)

rel_min = ((slider_val - from_size) /2 + bw_val) / len_val
rel_max = 1 - ((slider_val + to_size) /2 + bw_val) / len_val

x_min = (slider_val - from_size) /2 + bw_val
x_max = len_val - (slider_val + to_size) /2 + bw_val

for i, rv in enumerate(range_vals):
    item = ttk.Label(fr, text=rv)
    item.place(in_=scth, bordermode='outside',
                relx=(rel_min + i / (len_rvs - 1) * (rel_max - rel_min)) ,
                rely=1, anchor='n')

disp_lab = ttk.Label(fr)
rel_x = convert_to_relx(float(scth.get()))
disp_lab.place(in_=scth, bordermode='outside',
                relx=rel_x, rely=0, anchor='s')
display_value(scth.get())

sbh = ttk.Spinbox(fr, from_=from_val, to=to_val, textvariable=slider,
                  width=5, increment=res_val)
sbh.grid(row=2, column=1, sticky='ew')

root.mainloop()