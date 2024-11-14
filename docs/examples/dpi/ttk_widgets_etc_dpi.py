from tkinter import Tk, IntVar, Canvas, font
from tkinter.ttk import Scrollbar, LabelFrame, Frame, Spinbox, Style, \
    Combobox, Label, Button, Progressbar
import sys
sys.path.append('../scale')
from gen_scale_class import TtkScale
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

def change_style(event=None):
    """set the Style to the content of the Combobox"""
    content = cb.get()
    st0.theme_use(content)
    fact = font.Font(font="TkDefaultFont").metrics('linespace')
    st0.configure('font.Treeview', rowheight=fact,
    font=font.nametofont("TkDefaultFont"))
    #st0.configure('dpi.TSpinbox', arrowsize='8p')
    root.title(content)

def _do_bars(op, pbar, pb2):
    pbar = pbar.nametowidget('.fr0.can.sf.lF1.pb1')
    pb2 = pb2.nametowidget('.fr0.can.sf.lF1.pb2')

    if op == 'start':
        pbar.start()
        pb2.start()
    else:
        pbar.stop()
        pb2.stop()

root = Tk()
ORIGINAL_DPI = 96
current_dpi = root.winfo_fpixels('1i')
SCALE = current_dpi / ORIGINAL_DPI
# when current_dpi is 192 SCALE becomes 2.0
root.tk.call('tk', 'scaling', SCALE)

# make the canvas expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

st0 = Style()
#st0.configure('dpi.TSpinbox', arrowsize='8p')

#lF = LabelFrame(root,text="Slider")
fr0 = Frame(root, name="fr0")

can = Canvas(fr0, name="can")

vsb = Scrollbar(fr0, orient="vertical", command=can.yview)
hsb = Scrollbar(fr0, orient="horizontal", command=can.xview)

scrollable_frame = Frame(can, name="sf")
scrollable_frame.bind(
    "<Configure>",
    lambda e: can.configure(
        scrollregion=can.bbox("all")
    )
)

can.create_window((0, 0), window=scrollable_frame, anchor="nw")
can.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

lF = LabelFrame(scrollable_frame,text="Slider")
lF.grid(row=0,column=0,sticky='nwse', pady=5)

themes = list(sorted(st0.theme_names())) # get_themes
themes.insert(0, "Pick a theme")
cb = Combobox(lF, values=themes, state="readonly", height=10)
cb.set(themes[0])
cb.bind('<<ComboboxSelected>>', change_style)
cb.grid(row=0,column=0,sticky='nw', pady=5)

from_=-5
to=105
value=19
step=11
fontSize = 9
scvar = IntVar()

sc = TtkScale(lF, from_=from_, to=to, variable=scvar,
                    orient='vertical',length=200, showvalue=True,
                        command=lambda s: scvar.set('%d' % float(s) ),
                        tickinterval=5, resolution=5)

sc.set(value)

l1 = Spinbox(lF, from_=from_, to=to, textvariable=scvar, width=4) #, style='dpi.TSpinbox')
l1.grid(row=1,column=0,pady=2)
sc.grid(row=1,column=1, pady=5, padx=40)

schvar = IntVar()
a=-5
b=105

sch = TtkScale(lF, from_=a, to=b, length=400, variable=schvar,
                         orient='horizontal', showvalue=True,
                         command=lambda s: schvar.set('%d' % float(s) ),
                         tickinterval=5, resolution=5)

sch.set(23)

l2 = Spinbox(lF, from_=a, to=b, textvariable=schvar, width=4) #, style='dpi.TSpinbox')
l2.grid(row=2,column=1,pady=2)

sch.grid(row=3,column=0, columnspan=2, pady=40, padx=5,sticky='nw')

lF1 = LabelFrame(scrollable_frame,text="Progressbar",name="lF1")
lF1.grid(row=1,column=0,sticky='nwse', pady=5)

pb1var = IntVar()
pb2var = IntVar()
pbar = Progressbar(lF1, variable = pb1var, length = 150,
                        mode ="indeterminate", name='pb1', orient='horizontal')
pb2 = Progressbar(lF1, variable = pb2var, mode='indeterminate',
                               name='pb2', orient='vertical')
pbar["value"] = 25
pbar.grid(row=1,column=0,padx=5,pady=5,sticky='nw')
pb2.grid(row=1,column=1,padx=5,pady=5,sticky='nw')
l3 = Label(lF1,textvariable=pb1var)
l3.grid(row=0,column=0,pady=2,sticky='nw')
l4 = Label(lF1,textvariable=pb2var)
l4.grid(row=0,column=1,pady=2,sticky='nw')
start = Button(lF1, text='Start Progress',
                   command=lambda: _do_bars('start',pbar,pb2))
stop = Button(lF1, text='Stop Progress',
                   command=lambda: _do_bars('stop',pbar,pb2))
start.grid(row=2,column=0,padx=5,pady=5,sticky='nw')
stop.grid(row=3,column=0,padx=5,pady=5,sticky='nw')

fr0.grid(row=0,column=0,sticky='nsew')
fr0.columnconfigure(0,weight=1)
fr0.rowconfigure(0,weight=1)

can.grid(row=0,column=0,sticky='nsew')
can.columnconfigure(0,weight=1)
can.rowconfigure(0,weight=1)

vsb.grid(column=1, row=0, sticky='ns')
vsb.columnconfigure(1,weight=1)
hsb.grid(column=0, row=1, sticky='ew')
hsb.rowconfigure(1,weight=1)

root.mainloop()