""" Construction simple gradient"""

from tkinter import Tk, Canvas


def lerp_hex(colour1, colour2, fraction):
    """linear gradient

    Parameters
    ----------
    colour1 : tuple of int
        start colour
    colour2 : tuple of int
        end colour
    fraction : float
        normalised colour fraction

    Results
    -------
    string
        hexadecimal colour
    """

    return '#%02x%02x%02x' % (int(colour1[0] + (colour2[0] - colour1[0]) * fraction),
                              int(colour1[1] + (colour2[1] - colour1[1]) * fraction),
                              int(colour1[2] + (colour2[2] - colour1[2]) * fraction))


COLOUR1 = (255, 255, 255)
COLOUR2 = (0, 0, 0)
STEPS = 256
WIDTH = 300
HEIGHT = 26

root = Tk()
winsys = root.tk.call("tk", "windowingsystem")
BASELINE = 1.33398982438864281 if winsys != 'aqua' else 1.000492368291482
scaling = root.tk.call("tk", "scaling")
enlargement = int(scaling / BASELINE + 0.5)
WIDTH = 300
HEIGHT = 26
we = WIDTH * enlargement
he = HEIGHT * enlargement
can = Canvas(root)
can.pack(fill='both', expand=1)

for i in range(STEPS):
    x0 = int((we * i) / STEPS)
    x1 = int((we * (i + 1)) / STEPS)

    can.create_rectangle((x0, 0, x1, he), fill=lerp_hex(
        COLOUR1, COLOUR2, i / (STEPS - 1)), outline='')

root.mainloop()
