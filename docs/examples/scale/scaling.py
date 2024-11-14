from tkinter import Tk

ORIGINAL_DPI = 240.23645320197045   # This is the DPI of the computer you're making/testing the script on.

def get_dpi():
    screen = Tk()
    current_dpi = screen.winfo_fpixels('1i')
    screen.destroy()
    return current_dpi

SCALE = get_dpi()/ORIGINAL_DPI    # Now this is the appropriate scale factor you were mentioning.

# Now every time you use a dimension in pixels, replace it with scaled(*pixel dimension*)
def scaled(original_width):
    return round(original_width * SCALE)

if __name__ == '__main__':
    root = Tk()
    root.geometry(f'{scaled(500)}x{scaled(500)}')    # This window now has the same size across all monitors. Notice that the scaled factor is one if the script is being run on a the same computer with ORIGINAL_DPI.
    root.mainloop()

# Gave window 483x483 with pyscripter and 400x483 (wxh)with thonny