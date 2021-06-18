import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import numpy as np

from_val = -1
to_val = 1
len_val = 500
res_val = 0.10
tick_val = 0.10
dig_val = 2
bw_val = 1 # trough border width
slider_val = 36
sc_range = abs(to_val - from_val) # scale range

def selh(val):
    sbh.config(text=round(float(scth.get())+0.0049,2))

root = tk.Tk()
root.geometry(str(len_val+150)+"x200+500+500")
s = ttk.Style()
s.theme_use('default')

def_font = font.nametofont('TkDefaultFont')
from_size = def_font.measure(from_val)
to_size = def_font.measure(to_val)

sch = tk.Scale(root, from_=from_val, to=to_val, label='Bogusstuinuous', orient='horizontal',
            resolution=res_val, showvalue=1, tickinterval=tick_val, digits=dig_val,
            length=len_val)
sch.grid(sticky='ew')

sep = ttk.Separator(root, orient='horizontal')
sep.grid(row=1, column=0, columnspan=2)

def convert_to_relx(curr_val):
    return ((curr_val - from_val) * (rel_max - rel_min) / (to_val - from_val) \
            + rel_min)

def display_value(value):
    # position (in pixel) of the center of the slider
    rel_x = convert_to_relx(float(value))
    disp_lab.place_configure(relx=rel_x)
    my_precision = '{:.{}f}'.format
    disp_lab.configure(text=my_precision(float(value), int(dig_val)))

slider = tk.StringVar()
slider.set('0.00')

scth = ttk.Scale(root, from_=from_val, to=to_val, length=len_val,
        command=display_value)

scth.grid(row=2, column=0, sticky='ew', padx=5, pady=15)

rel_min = ((slider_val - from_size) / 2 + bw_val) / len_val
rel_max = 1 - (slider_val /2 - bw_val) / len_val

# using numpy arange instead of range so tick intervals less than 1 can be used
data = np.arange(from_val, to_val+tick_val, tick_val)
data = np.round(data,1)
range_vals = tuple(data)
len_rvs = len(range_vals)

for i, rv in enumerate(range_vals):
    item = ttk.Label(root, text=rv)
    item.place(in_=scth, bordermode='outside',
                relx=(rel_min + i / (len_rvs - 1) * (rel_max - rel_min)) ,
                rely=1, anchor='n')

disp_lab = ttk.Label(root, textvariable = slider)
disp_lab.place(in_=scth, bordermode='outside',
                relx=0.5, rely=0, anchor='s')
display_value(scth.get())

sbh = ttk.Spinbox(root, from_=from_val, to=to_val, textvariable=slider,
                  width=5, increment=res_val)
sbh.grid(row=2, column=1)

root.mainloop()