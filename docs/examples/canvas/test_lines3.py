from tkinter import Tk, Canvas, Button
from PIL import Image
from io import BytesIO

def save():
    ps = canvas.postscript(colormode='color',pagewidth=w-1,pageheight=h-1)
    img = Image.open(BytesIO(ps.encode('utf-8')))
    img.save('../../images/canvas/line_test3r.png')

w = 200
h = 200
b = 3

root = Tk()
canvas = Canvas(root, width=w, height=h, bg='white')
canvas.grid()

canvas.create_line(0, 0, 0, h+4, width=b, fill='red')  # left
canvas.create_line(0, 0, w+4, 0, width=b, fill='green')  # top
canvas.create_line(0, h+3, w+4, h+3, width=b, fill='blue') # bottom
canvas.create_line(w+3, 0, w+3, h+4, width=b, fill='orange') # right

but = Button(root, text="save", command=save)
but.grid()

root.mainloop()