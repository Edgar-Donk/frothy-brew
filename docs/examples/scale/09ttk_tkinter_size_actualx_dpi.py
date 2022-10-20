import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import numpy as np
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

mult = 2.6 # multiplier on my high definition screen
from_val = 0
to_val = 10
#len_val = 500
res_val = 1
tick_val = 1
dig_val = 0
bw_val = 1 # trough border width
slider_val = 20 # 36 # int(15 * mult + 0.5)
sc_range = abs(to_val - from_val) # scale range
'''
def place_ticks(evt):
    print('place_ticks')
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
'''
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
#len_val = int(ceil((data_size+space_size) / 50.0)) * 50
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
#sch.pack(fill='x', expand=1)
sch.grid(sticky='ew', pady=5)
# sch.columnconfigure(0, weight=1)

sep = ttk.Separator(fr, orient='horizontal')
#sep.pack(fill='x', expand=1)
sep.grid(row=1, column=0, columnspan=2, sticky='ew')
# sep.columnconfigure(0, weight=1)

def convert_to_actx(curr_val):
    return ((curr_val - from_val) * (x_max - x_min) / (to_val - from_val) \
            + x_min)

def display_value(value):
    # position (in pixel) of the center of the slider
    #print((0 - from_val) * (rel_max - rel_min) / (to_val - from_val) + rel_min)
    act_x = convert_to_actx(float(value))
    disp_lab.place_configure(x=act_x)
    disp_lab.configure(text=f'{float(value):.{dig_val}f}')
    #print(act_x, 'posx', disp_lab.winfo_rootx())

slider = tk.StringVar()
slider.set('0.00')

scth = ttk.Scale(fr, from_=from_val, to=to_val, length=len_val,
        command=display_value, variable=slider)

#scth.pack(fill='x', padx=5, pady=15, expand=1)
scth.grid(row=2, column=0, sticky='ew', padx=5, pady=25)
# scth.columnconfigure(0, weight=1)

# scth.bind('<Configure>', place_ticks)

#rel_min = ((slider_val - from_size) /2 + bw_val) / len_val
#rel_max = 1 - ((slider_val + to_size) /2 + bw_val) / len_val # 1 - ((slider_val - to_size) /2 + bw_val) / len_val
#rel_min = ((slider_val ) / 2 + bw_val) / len_val
#rel_max = 1 - ((slider_val ) / 2 - bw_val) / len_val

x_min = (slider_val) /2 + bw_val # (slider_val - from_size) /2 + bw_val
x_max = len_val - (slider_val + to_size) /2 + bw_val

print(str(from_val),' x', convert_to_actx(from_val))
print(str(to_val),' x', convert_to_actx(to_val))
for i, rv in enumerate(range_vals):
    # print('tick', i)
    item = ttk.Label(fr, text=rv)
    item.place(in_=scth, bordermode='outside',
                x=(x_min + i / (len_rvs - 1) * (x_max - x_min)),
                #relx=(rel_min + i / (len_rvs - 1) * (rel_max - rel_min)) ,
                rely=1, anchor='n')

    #print(rv,'rel_x ', (rel_min + i / (len_rvs - 1) * (rel_max - rel_min)) )
    #print(i, ' x ', (x_min + i / (len_rvs - 1) * (x_max - x_min)))

disp_lab = ttk.Label(fr)
act_x = convert_to_actx(float(scth.get()))
disp_lab.place(in_=scth, bordermode='outside',
                x=act_x, rely=0, anchor='s') # relx=0.5
display_value(scth.get())

sbh = ttk.Spinbox(fr, from_=from_val, to=to_val, textvariable=slider,
                  width=5, increment=res_val)
#sbh.pack()
sbh.grid(row=2, column=1, sticky='ew')
# sbh.columnconfigure(0, weight=1)
#print(sbh.winfo_toplevel())
root.mainloop()