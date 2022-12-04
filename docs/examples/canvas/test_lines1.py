from tkinter import Tk, Canvas, Button
from PIL import Image
from io import BytesIO

# valid for line widths 1 and 2 pixels, wider lines use the universal script
# test_linesr

def save():
    ps = canvas.postscript(colormode='color',pagewidth=w-1,pageheight=h-1)
    img = Image.open(BytesIO(ps.encode('utf-8')))
    img.save('../../images/canvas/line_test'+str(b)+'.png')

w = 200
h = 200
b = 1

root = Tk()
canvas = Canvas(root, width=w, height=h, bg='white')
canvas.grid()

canvas.create_line(0, 0, 0, h+4, width=b, fill='red')
canvas.create_line(0, 0, w+4, 0, width=b, fill='green')
canvas.create_line(0, h+4, w+4, h+4, width=b, fill='blue')
canvas.create_line(w+4, 0, w+4, h+4, width=b, fill='orange')

but = Button(root, text="save", command=save)
but.grid()

root.mainloop()