'''
Normal scaling, made scale lengths points
'''

from tkinter import Tk, Scrollbar, Scale, LabelFrame, IntVar, Frame, Spinbox, \
Canvas
import tkinter.font as tkFont
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
ORIGINAL_DPI = 96
current_dpi = root.winfo_fpixels('1i')
SCALE = current_dpi / ORIGINAL_DPI
# when current_dpi is 192 SCALE becomes 2.0
root.tk.call('tk', 'scaling', SCALE)

# make the canvas expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

lF = LabelFrame(root,text="Slider")


can = Canvas(lF)

vsb = Scrollbar(lF, orient="vertical", command=can.yview)
hsb = Scrollbar(lF, orient="horizontal", command=can.xview)

scrollable_frame = Frame(can)
scrollable_frame.bind(
    "<Configure>",
    lambda e: can.configure(
        scrollregion=can.bbox("all")
    )
)

can.create_window((0, 0), window=scrollable_frame, anchor="nw")
can.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)



from_=-5
to=105
value=19
step=11
fontSize = 9
scvar = IntVar()

sc = Scale(scrollable_frame, from_=from_, to=to, variable=scvar,
                    orient='vertical',length='150p', showvalue=True,
                        command=lambda s: scvar.set('%d' % float(s) ),
                        tickinterval=5, resolution=5, width='12p')

sc.set(value)

l1 = Spinbox(scrollable_frame, from_=from_, to=to, textvariable=scvar, width=4,
    font=tkFont.Font(family='Helvetica', size=10))
l1.grid(row=0,column=0,pady=2)
sc.grid(row=0,column=1, pady=5, padx=40)

schvar = IntVar()
a=-5
b=105

sch = Scale(scrollable_frame, from_=a, to=b, length='300p', variable=schvar,
                         orient='horizontal', showvalue=True,
                         command=lambda s: schvar.set('%d' % float(s) ),
                         tickinterval=5, resolution=5, width='12p')

sch.set(23)

l2 = Spinbox(scrollable_frame, from_=a, to=b, textvariable=schvar, width=4,
    font=tkFont.Font(family='Helvetica', size=10))
l2.grid(row=1,column=1,pady=2)

sch.grid(row=2,column=0, columnspan=2, pady=40, padx=5,sticky='nw')

lF.grid(row=0,column=0,sticky='nsew')
lF.columnconfigure(0,weight=1)
lF.rowconfigure(0,weight=1)

can.grid(row=0,column=0,sticky='nsew')
can.columnconfigure(0,weight=1)
can.rowconfigure(0,weight=1)

vsb.grid(column=1, row=0, sticky='ns')
vsb.columnconfigure(1,weight=1)
hsb.grid(column=0, row=1, sticky='ew')
hsb.rowconfigure(1,weight=1)

root.mainloop()