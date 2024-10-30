from tkinter import Tk, IntVar, Canvas, font
from tkinter.font import Font
from tkinter.ttk import Scrollbar, Scale, LabelFrame, Frame, Spinbox, Style, Combobox
import sys
sys.path.append('../scale')
from gen_scale_class import TtkScale

def change_style(event=None):
    """set the Style to the content of the Combobox"""
    content = cb.get()
    st0.theme_use(content)
    fact = font.Font(font="TkDefaultFont").metrics('linespace')
    st0.configure('font.Treeview', rowheight=fact,
    font=font.nametofont("TkDefaultFont"))

    root.title(content)

root = Tk()

# make the canvas expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

st0 = Style()

#lF = LabelFrame(root,text="Slider")
fr0 = Frame(root)

can = Canvas(fr0)

vsb = Scrollbar(fr0, orient="vertical", command=can.yview)
hsb = Scrollbar(fr0, orient="horizontal", command=can.xview)

scrollable_frame = Frame(can)
scrollable_frame.bind(
    "<Configure>",
    lambda e: can.configure(
        scrollregion=can.bbox("all")
    )
)

can.create_window((0, 0), window=scrollable_frame, anchor="nw")
can.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)



themes = list(sorted(st0.theme_names())) # get_themes
themes.insert(0, "Pick a theme")
cb = Combobox(scrollable_frame, values=themes, state="readonly", height=10)
cb.set(themes[0])
cb.bind('<<ComboboxSelected>>', change_style)
cb.grid(row=0,column=0,sticky='nw', pady=5)

from_=-5
to=105
value=19
step=11
fontSize = 9
scvar = IntVar()

sc = TtkScale(scrollable_frame, from_=from_, to=to, variable=scvar,
                    orient='vertical',length=200, showvalue=True,
                        command=lambda s: scvar.set('%d' % float(s) ),
                        tickinterval=5, resolution=5)

sc.set(value)

l1 = Spinbox(scrollable_frame, from_=from_, to=to, textvariable=scvar, width=4)
l1.grid(row=1,column=0,pady=2)
sc.grid(row=1,column=1, pady=5, padx=40)

schvar = IntVar()
a=-5
b=105

sch = TtkScale(scrollable_frame, from_=a, to=b, length=400, variable=schvar,
                         orient='horizontal', showvalue=True,
                         command=lambda s: schvar.set('%d' % float(s) ),
                         tickinterval=5, resolution=5)

sch.set(23)

l2 = Spinbox(scrollable_frame, from_=a, to=b, textvariable=schvar, width=4)
l2.grid(row=2,column=1,pady=2)

sch.grid(row=3,column=0, columnspan=2, pady=40, padx=5,sticky='nw')

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