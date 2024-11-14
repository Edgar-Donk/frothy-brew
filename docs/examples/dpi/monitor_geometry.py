
# Author: Larz60+ Nov 2019

from screeninfo import get_monitors


class GetGeometry:
    def __init__(self):
        self.geometry = []

    def get_tkinter_geometry(self, percent_of_screen, xpad=None, ypad=None):
        '''
        Given percent of monitor size in floating point eg: 10 % = 10.0, calculates
        tkinter geometry for each monitor attached to computer
        requires screeninfo "pip install screeninfo"

        returns: list holding tkinter geometry strings padded with xpad and ypad
                or centered if xpad is None.

                None if bad pct passed
        '''

        if not isinstance(percent_of_screen, float):
            print("requires float percent eg: 10.0 for 10%")
            return

        pct = percent_of_screen / 100

        for size in get_monitors():
            cwidth = int(size.width * pct)
            cheight = int(size.height * pct)

            xoff = xpad
            yoff = ypad
            if xpad is None:
                xoff = int((size.width - cwidth) / 2)
                yoff = int((size.height - cheight) / 2)
            self.geometry.append(f"{cwidth}x{cheight}+{xoff}+{yoff}")