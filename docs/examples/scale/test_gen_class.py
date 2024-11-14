from tkinter import Tk, Frame, IntVar
from tkinter.ttk import Style, Separator, Spinbox
from gen_scale_class import TtkScale

root = Tk()
st = Style()
st.theme_use('default')
style_val = 'my.Horizontal.TScale'
style_val2 = 'my2.Vertical.TScale'
st.configure(style_val, background='blue')
st.configure(style_val2, background='yellow')

fr = Frame(root)
fr.pack(fill='both')

hv = IntVar()

h = TtkScale(fr, from_=0, to=150, orient='horizontal', variable=hv,
                    tickinterval=10, digits=0, style=style_val,
                    length=400, showvalue=True, resolution=10)
h.grid(row=1, column=1, padx=5, pady=40, sticky ='ew')

sh = Spinbox(fr, from_=0, to=150, textvariable=hv, width=3)
sh.grid(row=0, column=1)

s = Separator(fr, orient='vertical')
s.grid(row=0, column=2, sticky='ns')

vv = IntVar()
v = TtkScale(fr, from_=0, to=100, orient='vertical', variable=vv,
                    tickinterval=10, digits=0, style=style_val2,
                     length=150, showvalue=True, resolution=10)
v.grid(row=0, column=4, rowspan=2, pady=5, padx=40, sticky ='ns')

sv = Spinbox(fr, from_=0, to=100, textvariable=vv, width=3)
sv.grid(row=0, column=3)

root.mainloop()