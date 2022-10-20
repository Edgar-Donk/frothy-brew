import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import numpy as np
import ctypes

# changed geometry and scale padding

ctypes.windll.shcore.SetProcessDpiAwareness(1)

###############################################
from_val = 0   # from_
to_val = 100      # to
tick_val = 10   # tickinterval
res_val = 5    # resolution
dig_val = 1     # digits
bw_val = 1      # trough border width
slider_val = 32 # sliderlength
#################################################

root = tk.Tk()
ORIGINAL_DPI = 96
current_dpi = root.winfo_fpixels('1i')
SCALE = current_dpi / ORIGINAL_DPI
# when current_dpi is 192 SCALE becomes 2.0
root.tk.call('tk', 'scaling', SCALE)

def_font = font.nametofont('TkDefaultFont')
# using numpy arange instead of range so tick intervals less than 1 can be used
data = np.arange(from_val, (to_val+1 if tick_val >=1 else to_val+tick_val), tick_val) # tick_val
data = np.round(data,1)
range_vals = tuple(data)

vals_size = [def_font.measure(str(i)) for i in range_vals]
data_size = sum(vals_size)
len_rvs = len(range_vals)
space_size = len_rvs * def_font.measure('0')
sizes = data_size + space_size
len_val = (sizes if sizes % 50 == 0 else sizes + 50 - sizes % 50)

theme_sl = {'alt': 9, 'clam': 30, 'classic': 30, 'default': 30,
                    'lime': 9, 'winnative': 9}

theme_bw = {'alt': 0, 'clam': 1, 'classic': 2, 'default': 1,
                    'lime': 6, 'winnative': 0}

root.geometry(str(len_val+200)+"x250+500+500")
s = ttk.Style()
##################
s.theme_use('alt')
##################

theme_used = s.theme_use()
if theme_used in ('alt', 'clam', 'classic', 'default', 'lime', 'winnative'):
    bw_val = theme_bw[theme_used]
    slider_val = theme_sl[theme_used]
else:
    bw_val = 1

fr = ttk.Frame(root)
fr.pack(fill='x', expand=1)

def show_x(val):
    print('sch.get()',sch.get(),'val', val.x)

sch = tk.Scale(fr, from_=from_val, to=to_val, label='Bogusstuinuous', orient='horizontal',
            resolution=res_val, showvalue=1, tickinterval=tick_val, digits=dig_val,
            length=len_val)
sch.grid(sticky='ew', padx=10, pady=5)
sch.bind("<ButtonRelease-1>", show_x)

def resolve(evt):
    if res_val < 1 or tick_val < 1:
        pass
    else:
        value = scth.get()
        curr_x = convert_to_actx(value)
        if evt.x < curr_x - slider_val / 2:
            scth.set(value - res_val + 1)
        elif evt.x > curr_x + slider_val / 2:
            scth.set(value + res_val - 1)

def convert_to_actx(curr_val):
    return ((curr_val - from_val) * (x_max - x_min) / (to_val - from_val) \
                + x_min)

def display_value(value):
    # position (in pixel) of the center of the slider
    act_x = convert_to_actx(float(value))
    disp_lab.place_configure(x=act_x)
    disp_lab.configure(text=f'{float(value):.{dig_val}f}')

act_var = tk.StringVar()
act_var.set('0.00')

scth = ttk.Scale(fr, from_=from_val, to=to_val, length=len_val,
        command=display_value, variable=act_var, style='my.Horizontal.TScale')
scth.grid(row=2, column=0, sticky='ew', padx=15, pady=25)
scth.bind("<Button-1>", resolve)

x_min = slider_val // 2 + bw_val
x_max = len_val - slider_val // 2 - bw_val
if range_vals[-1] == to_val:
    pass
else:
    max_rv = range_vals[-1]
    mult_x = ((max_rv-from_val)*x_max/(to_val-from_val))

for i, rv in enumerate(range_vals):
    ################################################
    item = ttk.Label(fr, text='|') # rv text='|'
    ################################################
    item.place(in_=scth, bordermode='outside',
                x=(x_min + i / (len_rvs - 1) *
                ((x_max if range_vals[-1] == to_val else mult_x) - x_min)),
                ################################
                rely=0.7, anchor='n') # rely=1
                ################################

disp_lab = ttk.Label(fr)
act_x = convert_to_actx(float(scth.get()))
disp_lab.place(in_=scth, bordermode='outside',
                x=act_x, rely=0, anchor='s')
display_value(scth.get())

sbh = ttk.Spinbox(fr, from_=from_val, to=to_val, textvariable=act_var,
                  width=5, increment=res_val)
sbh.grid(row=2, column=1, sticky='ew')

root.mainloop()