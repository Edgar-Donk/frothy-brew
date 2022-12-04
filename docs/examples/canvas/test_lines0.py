from tkinter import Tk, Canvas, Button
from PIL import Image
from io import BytesIO

def save():
    ps = canvas.postscript(colormode='color',pagewidth=w-1,pageheight=h-1)
    img = Image.open(BytesIO(ps.encode('utf-8')))
    img.save('../../images/canvas/line_test0.png')

w = 200
h = 200
b = 1

root = Tk()
canvas = Canvas(root, width=w, height=h, bg='white')
canvas.grid()

canvas.create_line(0, 0, 0, h-1, width=b, fill='red')
canvas.create_line(0, 0, w-1, 0, width=b, fill='green')
canvas.create_line(0, h-1, w-1, h-1, width=b, fill='blue')
canvas.create_line(w-1, 0, w-1, h-1, width=b, fill='orange')

but = Button(root, text="save", command=save)
but.grid()

root.mainloop()