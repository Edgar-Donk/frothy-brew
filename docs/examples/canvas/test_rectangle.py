from tkinter import Tk, Canvas, Button
from PIL import Image
from io import BytesIO

def save():
    ps = canvas.postscript(colormode='color',pagewidth=w-1,pageheight=h-1)
    img = Image.open(BytesIO(ps.encode('utf-8')))
    img.save('../../images/canvas/rectangle_test'+str(b)+'.png')

w = 200
h = 200
b = 1

root = Tk()
canvas = Canvas(root, width=w, height=h, bg='white')
canvas.grid()

canvas.create_rectangle((b-1)//2, (b-1)//2, w+4-(b-1)//2, h+4-(b-1)//2,
                        outline='yellow', width=b)

but = Button(root, text="save", command=save)
but.grid()

root.mainloop()
