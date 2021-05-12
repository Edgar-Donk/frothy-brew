from tkinter import Tk, Canvas, font
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(0)

root = Tk()
meas = font.Font(family="Times", size=12, weight="bold")
mt = meas.measure('Test')
print(mt)


root.tk.call("tk", "scaling", 1.33)
can = Canvas(root, width=400, height=400)
can.pack(expand=True, fill='both')
can.create_text(200, 200, text='TestT', font=meas)


can.create_line(100, 100, 300, 100, width='3p', tags='resize')
can.create_line(100, 100, 100, 300, width='3p', tags='resize')

#can.scale('resize', 100, 100, 2, 2)
print ("dpi aware", root.tk.call("tk", "scaling"))
root.mainloop()