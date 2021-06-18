import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import numpy as np

from_val = 0
to_val = 100
len_val = 500
res_val = 10
tick_val = 10
dig_val = 2
bw_val = 1 # trough border width
slider_val = 36
sc_range = abs(to_val - from_val) # scale range

def selh(val):
    labh.config(text=round(float(scth.get())+0.0049,2))
    print('horiz', scth.get(), val.x)

root = tk.Tk()
root.geometry(str(len_val+100)+"x200+500+500")
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

scth = ttk.Scale(root, from_=from_val, to=to_val, length=len_val)
scth.bind("<ButtonRelease-1>", selh)
scth.grid(row=2, column=0, sticky='ew')

rel_min = ((slider_val - from_size) / 2 + bw_val) / len_val
rel_max = 1 - (slider_val /2 - bw_val) / len_val

# using numpy arange instead of range so tick intervals less than 1 can be used
data = np.arange(from_val, to_val+tick_val, tick_val)
data = np.round(data,1)
range_vals = tuple(data)
len_rvs = len(range_vals)

mult = (1 if tick_val >= 1 else (len_rvs - 1) / sc_range)
for i, rv in enumerate(range_vals):
    item = ttk.Label(root, text=rv)
    item.place(in_=scth, bordermode='outside',
                relx=(rel_min + i / (len_rvs - 1) / mult * (rel_max - rel_min)) ,
                rely=1, anchor='n')

labh = ttk.Label(root, text=str(scth.get()))
labh.grid(row=2, column=1)

root.mainloop()