import tkinter as tk
import tkinter.ttk as ttk
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
ORIGINAL_DPI = 96
current_dpi = root.winfo_fpixels('1i')
SCALE = current_dpi / ORIGINAL_DPI
# when current_dpi is 192 SCALE becomes 2.0
root.tk.call('tk', 'scaling', SCALE)

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
scth.grid(row=2, column=0)

sctv = ttk.Scale(root, from_=0, to=10, length=200, orient='vertical')
sctv.grid(row=2, column=1)

root.mainloop()