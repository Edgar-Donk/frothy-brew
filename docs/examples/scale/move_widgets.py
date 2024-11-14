from tkinter import Frame, Label, Tk

def clamp(lo, hi, x):
    return min(max(x, lo), hi)

class blah:
    all = []

    def MoveWindowStart(self, event):
        self.move_lastx = event.x_root
        self.move_lasty = event.y_root
        self.focus()

    def MoveWindow(self, event):
        self.root.update_idletasks()

        dx = event.x_root - self.move_lastx
        dy = event.y_root - self.move_lasty
        self.move_lastx = event.x_root
        self.move_lasty = event.y_root
        self.x = clamp(0, 640-200, self.x + dx) # should depend on
        self.y = clamp(0, 480-200, self.y + dy) # actual size here
        self.f.place_configure(x=self.x, y=self.y)

    def __init__(self, root, title, x, y):
        self.root = root

        self.x = x; self.y = y
        self.f = Frame(self.root, bd=1, relief='raised')
        self.f.place(x=x, y=y, width=200, height=200)

        self.l = Label(self.f, bd=1, bg="#08246b", fg="white",text=title)
        self.l.pack(fill='x')

        self.l.bind('<1>', self.MoveWindowStart)
        self.f.bind('<1>', self.focus)
        self.l.bind('<B1-Motion>', self.MoveWindow)
        # self.f.bind('<B1-Motion>', self.MoveWindow)
        self.all.append(self)
        self.focus()

    def focus(self, event=None):
        self.f.tkraise()
        for w in self.all:
            if w is self:
                w.l.configure(bg="#08246b", fg="white")
            else:
                w.l.configure(bg="#d9d9d9", fg="black")

root = Tk()
root.title("...")
root.resizable(0,0)
root.geometry("%dx%d%+d%+d"%(640, 480, 0, 0))
x = blah(root, "Window 1", 10, 10)
y = blah(root, "Window 2", 220, 10)
y = blah(root, "Window 3", 10, 220)
root.mainloop()