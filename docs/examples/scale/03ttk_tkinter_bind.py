import tkinter as tk
import tkinter.ttk as ttk

def selh(val):
    labh.config(text=round(float(scth.get())+0.0049,2))
    print('horiz', scth.get(), val.x)

def selv(val):
    labv.config(text=round(float(sctv.get())+0.0049,2))
    print('vert', sctv.get(), val.y)

root = tk.Tk()
s = ttk.Style()
s.theme_use('default')

sch = tk.Scale(root, from_=-1.0, to=1.0, label='Bogusstuinuous', orient='horizontal',
            resolution=0.02, showvalue=1, tickinterval=0.5, digits=3,
            length=200)
sch.grid()

scv = tk.Scale(root, from_=-0, to=10, label='Fun', orient='vertical',
            resolution=1, showvalue=1, tickinterval=2,
            length=200)
scv.grid(row=0, column=1)

sep = ttk.Separator(root, orient='horizontal')
sep.grid(row=1, column=0, columnspan=2)

scth = ttk.Scale(root, from_=-1.0, to=1.0, length=200)
scth.bind("<ButtonRelease-1>", selh)
scth.grid(row=2, column=0)

labh = ttk.Label(root, text=str(scth.get()))
labh.grid(row=2, column=1)

sctv = ttk.Scale(root, from_=0, to=10, length=200, orient='vertical')
sctv.bind("<ButtonRelease-1>", selv)
sctv.grid(row=3, column=0)

labv = ttk.Label(root, text=str(sctv.get()))
labv.grid(row=3, column=1)

root.mainloop()