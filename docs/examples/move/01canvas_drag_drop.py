from tkinter import Tk, Canvas

def callback(event):
    can.coords(circle, event.x-20, event.y-20, event.x+20, event.y+20)

root = Tk()
can = Canvas(root)
can.bind('<B1-Motion>', callback)
#can.bind('<B1-Button>') #, callback)
#can.bind('<Button>', find)
can.pack()

circle = can.create_oval(0, 0, 40, 40, fill='orange')
#poly = can.create_polygon((0, 0, 0, 0, 0, 0), fill="#4eccde")
root.mainloop()
