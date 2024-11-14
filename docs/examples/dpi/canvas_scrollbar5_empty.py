import tkinter as tk

ws = tk.Tk()
ws.title('PythonGuides')

frame = tk.Frame(
    ws,
    width=500,
    height=400
    )
frame.pack(expand=True, fill=tk.BOTH)

canvas=tk.Canvas(
    frame,
    bg='#4A7A8C',
    width=500,
    height=400,
    scrollregion=(0,0,700,700)
    )

vertibar=tk.Scrollbar(
    frame,
    orient=tk.VERTICAL
    )
vertibar.pack(side=tk.RIGHT,fill=tk.Y)
vertibar.config(command=canvas.yview)

horibar=tk.Scrollbar(
    frame,
    orient=tk.HORIZONTAL
    )
horibar.pack(side=tk.BOTTOM,fill=tk.X)
horibar.config(command=canvas.xview)

canvas.config(width=500,height=400)

canvas.config(
    xscrollcommand=horibar.set,
    yscrollcommand=vertibar.set
    )
canvas.pack(expand=True,side=tk.LEFT,fill=tk.BOTH)

ws.mainloop()