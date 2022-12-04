from tkinter import Tk, Canvas, Button
from PIL import Image
from io import BytesIO

def save():
    ps = canvas.postscript(colormode='color',pagewidth=w-1,pageheight=h-1)
    img = Image.open(BytesIO(ps.encode('utf-8')))
    img.save('../../images/canvas/line_test'+str(b)+'r.png')

w = 200
h = 200
b = 9

root = Tk()
canvas = Canvas(root, width=w, height=h, bg='white')
canvas.grid()

canvas.create_line((b-1)//2, 0, (b-1)//2, h+4, width=b, fill='red')  # left
canvas.create_line(0, (b-1)//2, w+4, (b-1)//2, width=b, fill='green')  # top
canvas.create_line(0, h+4-(b-1)//2, w+4, h+4-(b-1)//2, width=b, fill='blue') # bottom
canvas.create_line(w+4-(b-1)//2, 0, w+4-(b-1)//2, h+4, width=b, fill='orange') # right

but = Button(root, text="save", command=save)
but.grid()

root.mainloop()