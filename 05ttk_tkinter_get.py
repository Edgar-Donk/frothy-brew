import tkinter as tk
import tkinter.ttk as ttk

mult = 2.6 # multiplier on my high definition screen
from_val = 0
to_val = 360
len_val = 600
res_val = 1
tick_val = 30
dig_val = 3

slider_val = int(15 * mult + 0.5)

sc_range = to_val - from_val # scale range

def selh(val):
    labh.config(text=round(float(scth.get())+0.0049,2))
    print('horiz', scth.get(), val.x)

def selv(val):
    labv.config(text=round(float(sctv.get())+0.0049,2))
    print('vert', sctv.get(), val.y)

root = tk.Tk()
root.geometry(str(len_val+50)+"x175+500+500")
s = ttk.Style()
s.theme_use('default')

s.configure('Horizontal.TScale', borderwidth=2, sliderlength=33)

sch = tk.Scale(root, from_=from_val, to=to_val, label='Bogusstuinuous', orient='horizontal',
            resolution=res_val, showvalue=1, tickinterval=tick_val, digits=dig_val,
            length=len_val)
sch.grid(sticky='ew')

sep = ttk.Separator(root, orient='horizontal')
sep.grid(row=1, column=0, columnspan=2)

scth = ttk.Scale(root, from_=from_val, to=to_val, length=len_val)
scth.bind("<ButtonRelease-1>", selh)
scth.grid(row=2, column=0, sticky='ew')

for i in range(from_val, to_val+1, tick_val):
    item = ttk.Label(root, text=i)
    item.place(in_=scth, bordermode='outside',
                relx=slider_val / len_val / 2 +
                i / sc_range * (1 - slider_val / len_val),
                rely=1, anchor='n')
    if i in (0 , 100):
        relx=slider_val / len_val / 2 + i / sc_range * (1 - slider_val / len_val)

labh = ttk.Label(root, text=str(scth.get()))
labh.grid(row=2, column=1)

root.mainloop()