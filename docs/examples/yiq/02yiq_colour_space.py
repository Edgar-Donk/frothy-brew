""" Construction yiq colour space

Parameters
----------
None

Results
-------
image
"""

from PIL import Image
from tkinter import Tk
from yiqTools import yiq_to_rgb
     

root = Tk()
winsys = root.tk.call("tk", "windowingsystem")
BASELINE = 1.33398982438864281 if winsys != 'aqua' else 1.000492368291482
scaling = root.tk.call("tk", "scaling")
enlargement = e = int(scaling / BASELINE + 0.5)

im = Image.new("RGB", (301*e,301*e), "#FFFFFF")
centre = im.size[0] // 2, im.size[1] // 2
pix = im.load()

for x in range(im.width):
    for y in range(im.height):
        i=(x-centre[0])*2/3
        q=(y-centre[1])*2/3
        pix[x,y]=yiq_to_rgb(50,i,q)

im.save('../../figures/colour_space'+str(e)+'.png')