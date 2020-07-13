""" Construct hsv colour wheel image

Parameters
----------
None

Results
-------
None
"""

from PIL import Image
from math import atan2, pi


def hsv_to_rgb(h, s, v):
    """Conversion hsv to rgb
        h 0-360, s & v 0-100

    Parameters
    ----------
    h : int
        hue
    s : int
        saturation
    v : int
        value

    Returns
    -------
    tuple integers for rgb
    """

    # normalize
    h, s, v = h / 360.0, s / 100.0, v / 100.0
    # calculate all 0 ÷ 1.0
    if s == 0.0:
        v *= 255
        v = int(v)
        return (v, v, v)
    i = int(h * 6.)  # XXX assume int() truncates!
    f = (h * 6.) - i
    p, q, t = int(255 * (v * (1. - s))),\
              int(255 * (v * (1. - s * f))), int(255 * (v * (1. - s * (1. - f))))
    v *= 255
    i %= 6
    v = int(v)
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)


if __name__ == "__main__":

    im = Image.new("RGBA", (317, 317), "#FFFFFF00")
    inner = (299, 299)
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

    im.save('../../figures/colour_wheel.png')
