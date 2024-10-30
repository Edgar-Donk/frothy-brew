from tkinter import *

ws = Tk()
ws.title('PythonGuides')

frame = Frame(
    ws,
    width=500,
    height=400
    )
frame.pack(expand=True, fill=BOTH)

canvas=Canvas(
    frame,
    bg='#4A7A8C',
    width=500,
    height=400,
    scrollregion=(0,0,700,700)
    )

vertibar=Scrollbar(
    frame,
    orient=VERTICAL
    )
vertibar.pack(side=RIGHT,fill=Y)
vertibar.config(command=canvas.yview)

horibar=Scrollbar(
    frame,
    orient=HORIZONTAL
    )
horibar.pack(side=BOTTOM,fill=X)
horibar.config(command=canvas.xview)

canvas.config(width=500,height=400)

canvas.config(
    xscrollcommand=horibar.set,
    yscrollcommand=vertibar.set
    )
canvas.pack(expand=True,side=LEFT,fill=BOTH)

ws.mainloop()