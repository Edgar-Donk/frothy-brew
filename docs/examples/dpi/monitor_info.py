import tkinter as tk
root = tk.Tk()

width_px = root.winfo_screenwidth()
height_px = root.winfo_screenheight()
width_mm = root.winfo_screenmmwidth()
height_mm = root.winfo_screenmmheight()
# 2.54 cm = in
width_in = width_mm / 25.4
height_in = height_mm / 25.4
width_dpi = width_px/width_in
height_dpi = height_px/height_in

print('Width: %i px, Height: %i px' % (width_px, height_px))
print('Width: %i mm, Height: %i mm' % (width_mm, height_mm))
print('Width: %f in, Height: %f in' % (width_in, height_in))
print('Width: %f dpi, Height: %f dpi' % (width_dpi, height_dpi))

import ctypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
print('Size is %f %f' % (w, h))

curr_dpi = w*96/width_px
print('Current DPI is %f' % (curr_dpi))

'''
# on pyscripter returned opposite dpi
Width: 1920 px, Height: 1080 px
Width: 508 mm, Height: 286 mm
Width: 20.000000 in, Height: 11.259843 in # seems half of what should be
Width: 96.000000 dpi, Height: 95.916084 dpi
Size is 3840.000000 2160.000000
Current DPI is 192.000000

# on older thonny returned opposite dpi
Width: 3840 px, Height: 2160 px
Width: 508 mm, Height: 286 mm
Width: 20.000000 in, Height: 11.259843 in
Width: 192.000000 dpi, Height: 191.832168 dpi
Size is 3840.000000 2160.000000
Current DPI is 96.000000

newer thonny
Width: 1920 px, Height: 1080 px
Width: 508 mm, Height: 286 mm
Width: 20.000000 in, Height: 11.259843 in
Width: 96.000000 dpi, Height: 95.916084 dpi
Size is 3840.000000 2160.000000
Current DPI is 192.000000
'''

# for Mac OS X
import AppKit
[(screen.frame().size.width, screen.frame().size.height)
    for screen in AppKit.NSScreen.screens()]

# will give you a list of tuples containing all screen sizes (if multiple monitors present)