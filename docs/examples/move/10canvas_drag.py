from tkinter import Tk, Canvas
X = 40
Y = 40
def callback(event):
    global X, Y
    drag(event.x-X, event.y-Y)
    X = event.x
    Y = event.y


def drag(dx, dy):
    can.move(circle, dx, dy)

root = Tk()
can = Canvas(root)
can.bind('<Motion>', callback)
can.pack()

circle = can.create_oval(X-20, Y-20, X+20, Y+20, fill='orange')
root.mainloop()
