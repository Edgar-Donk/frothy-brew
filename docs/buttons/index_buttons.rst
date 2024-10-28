

=======================
Check and Radio Buttons
=======================

.. tabularcolumns:: |>{\centering\arraybackslash}\X{1}{5}|>{\centering\arraybackslash}\X{1}{5}

.. list-table::
    :header-rows: 1

    * - Pyscripter unscaled alt theme
      - Thonny unscaled alt theme

    * - .. figure:: ../figures/buttons/pyscripter_test_check.png
                    :width: 256
                    :height: 202

      - .. figure:: ../figures/buttons/thonny_test_check.png
                    :width: 249
                    :height: 166

Within an application these buttons are normally grouped together and 
superficially they should not cause any real problem. It is not until sizes
have to be changed that we run into problems - the alt theme has no simple
size adjustment.

At the end of this section a standalone module is created to make check
and radiobuttons scaleable.

.. topic:: Finding the Factor for Scaling
    
    Within the section on Monitor Resolution DPI a simplified method was
    used::
    
        from ctypes import windll

        # with Windows set the script to be dpi aware before calling Tk()
        windll.shcore.SetProcessDpiAwareness(1)
        .......
        root = Tk()

        # shcore gives the scaling factor directly
        scaleFactor = windll.shcore.GetScaleFactorForDevice(0) / 100
        root.tk.call('tk', 'scaling', scaleFactor)
    
    An alternative method, valid for Linux and Windows was also shown::
    
        from ctypes import windll

        # with Windows set the script to be dpi aware before calling Tk()
        windll.shcore.SetProcessDpiAwareness(1)
        .......
        root = Tk()
    
        ORIGINAL_DPI = 96
        current_dpi = root.winfo_fpixels('1i') # valid for Linux, Windows
        SCALE = current_dpi / ORIGINAL_DPI

        # when current_dpi is 192 SCALE becomes 2.0
        root.tk.call('tk', 'scaling', SCALE)

    Within this section a third variant is used, which includes Mac
    users::
    
        ............
        root = Tk()
        winsys = root.tk.call("tk", "windowingsystem")
        BASELINE = 1.33398982438864281 if winsys != 'aqua' else 1.000492368291482
        scaling = root.tk.call("tk", "scaling")
        dpi_scaling = int(scaling / BASELINE + 0.5)
    
    This last variant scales the widgets only if they have been created with
    a scaling factor, whereas the first two variants change the widgets
    through tk/tcl so can only affect the standard ttk widgets. Third party
    widgets are mostly image based so cannot be altered by any of these
    means, or else are already scaleable, `sphinx-bootstrap widgets <https://github.com/scotch/sphinx-bootstrap>`_.

.. toctree::
   :caption: Check- Radiobuttons...
   :maxdepth: 1
   
   intro_check
   scaleable_check
   scaleable_radio