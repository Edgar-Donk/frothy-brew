import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import numpy as np

###############################################
from_val = 0   # from_
to_val = 100      # to
tick_val = 10   # tickinterval
res_val = 10    # resolution
dig_val = 0     # digits
bw_val = 1      # trough border width
slider_val = 32 # sliderlength
#################################################

root = tk.Tk()

def_font = font.nametofont('TkDefaultFont')
# using numpy arange instead of range so tick intervals less than 1 can be used
data = np.arange(from_val, (to_val+1 if tick_val >=1 else to_val+tick_val), tick_val) # tick_val
data = np.round(data,1)
range_vals = tuple(data)
lspace = def_font.metrics('linespace')
len_rvs = len(range_vals)
data_size = len_rvs * lspace

space_size = len_rvs * 3
sizes = data_size + space_size
len_val = (sizes if sizes % 50 == 0 else sizes + 50 - sizes % 50)

theme_sl = {'alt': 9, 'clam': 30, 'classic': 30, 'default': 30,
                    'lime': 9, 'winnative': 9}

theme_bw = {'alt': 0, 'clam': 1, 'classic': 2, 'default': 1,
                    'lime': 6, 'winnative': 0}

root.geometry("200x"+str(len_val+200)+"+500+300")
s = ttk.Style()
############################
s.theme_use('alt') # default
###############################

theme_used = s.theme_use()
if theme_used in ('alt', 'clam', 'classic', 'default', 'lime', 'winnative'):
    bw_val = theme_bw[theme_used]
    slider_val = theme_sl[theme_used]
else:
    bw_val = 1

fr = ttk.Frame(root)
fr.pack(fill='y', expand=1)

def show_y(val):
    print('sch.get()',sch.get(),'val', val.y)

sch = tk.Scale(fr, from_=from_val, to=to_val, label='tk', orient='vertical',
            resolution=res_val, showvalue=1, tickinterval=tick_val, digits=dig_val,
            length=len_val)
sch.grid(sticky='ns')
sch.bind("<ButtonRelease-1>", show_y)

def resolve(evt):
    if res_val < 1 or tick_val < 1:
        pass
    else:
        value = scth.get()
        curr_y = convert_to_acty(value)
        if evt.y < curr_y - slider_val / 2:
            scth.set(value - res_val + 1)
        elif evt.y > curr_y + slider_val / 2:
            scth.set(value + res_val - 1)

def convert_to_acty(curr_val):
    return ((curr_val - from_val) * (y_max - y_min) / (to_val - from_val) \
                + y_min)

def display_value(value):
    # position (in pixel) of the center of the slider
    act_y = convert_to_acty(float(value))
    disp_lab.place_configure(y=act_y)
    disp_lab.configure(text=f'{float(value):.{dig_val}f}')

act_var = tk.StringVar()
act_var.set('0.00')

scth = ttk.Scale(fr, from_=from_val, to=to_val, length=len_val,
        command=display_value, variable=act_var, orient='vertical')
scth.grid(row=0, column=1, sticky='ns', pady=5, padx=15)
scth.bind("<Button-1>", resolve)

y_min = slider_val // 2 + bw_val
y_max = len_val - slider_val // 2 - bw_val

if range_vals[-1] == to_val:
    pass
else:
    max_rv = range_vals[-1]
    mult_y = ((max_rv-from_val)*y_max/(to_val-from_val))

for i, rv in enumerate(range_vals):
    ################################################
    item = ttk.Label(fr, text=rv) #  text='—'
    ################################################
    item.place(in_=scth, bordermode='outside',
                y=(y_min + i / (len_rvs - 1) *
                ((y_max if range_vals[-1] == to_val else mult_y) - y_min)),
                relx=0.7, anchor='w') # rely=1

disp_lab = ttk.Label(fr)
act_y = convert_to_acty(float(scth.get()))
disp_lab.place(in_=scth, bordermode='outside',
                y=act_y, relx=0, anchor='e')
display_value(scth.get())

sbh = ttk.Spinbox(fr, from_=from_val, to=to_val, textvariable=act_var,
                  width=5, increment=res_val)
sbh.grid(row=0, column=2, sticky='ew', padx=5)

root.mainloop()