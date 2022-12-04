from tkinter import Tk, Canvas, Button
from PIL import Image
import io
import os
import subprocess

root = Tk()

w = 60
h = 60

def save():
    ps = cv.postscript(colormode='color')
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    img.save('../../images/canvas/save_io.jpg', 'jpeg')

cv = Canvas(root, width=w, height=h, bg='white')
cv.pack()
b= Button(root, text='save', command=save)
b.pack()

# nothing to see unless rectangle is black and canvas has bg
# make sure the save is delayed
cv.create_rectangle(10,10,50,50, outline='black')

root.mainloop()