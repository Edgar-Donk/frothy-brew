""" Construct hsv colour wheel image

Parameters
----------
None

Results
-------
None
"""

from tkinter import Tk
from PIL import Image
from math import atan2, pi
from colourTools import hsv_to_rgb

if __name__ == "__main__":
    root = Tk()
    winsys = root.tk.call("tk", "windowingsystem")
    BASELINE = 1.33398982438864281 if winsys != 'aqua' else 1.000492368291482
    scaling = root.tk.call("tk", "scaling")
    enlargement = e = int(scaling / BASELINE + 0.5)

    im = Image.new("RGBA", (317*e, 317*e), "#FFFFFF00")
    inner = (299*e, 299*e)
    radius = min(inner) // 2
    centre = im.size[0] // 2, im.size[1] // 2
    pix = im.load()

    for x in range(im.width):
        for y in range(im.height):
            rx = centre[0] - x
            ry = centre[1] - y
            sat = 100 * (rx**2.0 + ry**2.0)**0.5 / radius
            if sat <= 100:
                hue = 360 * ((atan2(ry, rx) / pi) + 1.0) / 2.0
                pix[x, y] = hsv_to_rgb(hue, sat, 100)

    im.save('../../figures/colour_wheel'+str(e)+'.png')

