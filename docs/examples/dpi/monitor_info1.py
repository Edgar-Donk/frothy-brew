if PYTHON_V3 == sys.version_info >= (3,0,0) and sys.version_info < (4,0,0):
    #[...]
    def get_screen_resolution(self, measurement="px"):
        """
        Tries to detect the screen resolution from the system.
        @param measurement: The measurement to describe the screen resolution in. Can be either 'px', 'inch' or 'mm'.
        @return: (screen_width,screen_height) where screen_width and screen_height are int types according to measurement.
        """
        mm_per_inch = 25.4
        px_per_inch =  72.0 #most common
        try: # Platforms supported by GTK3, Fx Linux/BSD
            from gi.repository import Gdk
            screen = Gdk.Screen.get_default()
            if measurement=="px":
                width = screen.get_width()
                height = screen.get_height()
            elif measurement=="inch":
                width = screen.get_width_mm()/mm_per_inch
                height = screen.get_height_mm()/mm_per_inch
            elif measurement=="mm":
                width = screen.get_width_mm()
                height = screen.get_height_mm()
            else:
                raise NotImplementedError("Handling %s is not implemented." % measurement)
            return (width,height)
        except:
            try: #Probably the most OS independent way
                if PYTHON_V3:
                    import tkinter
                else:
                    import Tkinter as tkinter
                root = tkinter.Tk()
                if measurement=="px":
                    width = root.winfo_screenwidth()
                    height = root.winfo_screenheight()
                elif measurement=="inch":
                    width = root.winfo_screenmmwidth()/mm_per_inch
                    height = root.winfo_screenmmheight()/mm_per_inch
                elif measurement=="mm":
                    width = root.winfo_screenmmwidth()
                    height = root.winfo_screenmmheight()
                else:
                    raise NotImplementedError("Handling %s is not implemented." % measurement)
                return (width,height)
            except:
                try: #Windows only
                    from win32api import GetSystemMetrics
                    width_px = GetSystemMetrics (0)
                    height_px = GetSystemMetrics (1)
                    if measurement=="px":
                        return (width_px,height_px)
                    elif measurement=="inch":
                        return (width_px/px_per_inch,height_px/px_per_inch)
                    elif measurement=="mm":
                        return (width_px/mm_per_inch,height_px/mm_per_inch)
                    else:
                        raise NotImplementedError("Handling %s is not implemented." % measurement)
                except:
                    try: # Windows only
                        import ctypes
                        user32 = ctypes.windll.user32
                        width_px = user32.GetSystemMetrics(0)
                        height_px = user32.GetSystemMetrics(1)
                        if measurement=="px":
                            return (width_px,height_px)
                        elif measurement=="inch":
                            return (width_px/px_per_inch,height_px/px_per_inch)
                        elif measurement=="mm":
                            return (width_px/mm_per_inch,height_px/mm_per_inch)
                        else:
                            raise NotImplementedError("Handling %s is not implemented." % measurement)
                    except:
                        try: # Mac OS X only
                            import AppKit
                            for screen in AppKit.NSScreen.screens():
                                width_px = screen.frame().size.width
                                height_px = screen.frame().size.height
                                if measurement=="px":
                                    return (width_px,height_px)
                                elif measurement=="inch":
                                    return (width_px/px_per_inch,height_px/px_per_inch)
                                elif measurement=="mm":
                                    return (width_px/mm_per_inch,height_px/mm_per_inch)
                                else:
                                    raise NotImplementedError("Handling %s is not implemented." % measurement)
                        except:
                            try: # Linux/Unix
                                import Xlib.display
                                resolution = Xlib.display.Display().screen().root.get_geometry()
                                width_px = resolution.width
                                height_px = resolution.height
                                if measurement=="px":
                                    return (width_px,height_px)
                                elif measurement=="inch":
                                    return (width_px/px_per_inch,height_px/px_per_inch)
                                elif measurement=="mm":
                                    return (width_px/mm_per_inch,height_px/mm_per_inch)
                                else:
                                    raise NotImplementedError("Handling %s is not implemented." % measurement)
                            except:
                                try: # Linux/Unix
                                    if not self.is_in_path("xrandr"):
                                        raise ImportError("Cannot read the output of xrandr, if any.")
                                    else:
                                        args = ["xrandr", "-q", "-d", ":0"]
                                        proc = subprocess.Popen(args,stdout=subprocess.PIPE)
                                        for line in iter(proc.stdout.readline,''):
                                            if isinstance(line, bytes):
                                                line = line.decode("utf-8")
                                            if "Screen" in line:
                                                width_px = int(line.split()[7])
                                                height_px = int(line.split()[9][:-1])
                                                if measurement=="px":
                                                    return (width_px,height_px)
                                                elif measurement=="inch":
                                                    return (width_px/px_per_inch,height_px/px_per_inch)
                                                elif measurement=="mm":
                                                    return (width_px/mm_per_inch,height_px/mm_per_inch)
                                                else:
                                                    raise NotImplementedError("Handling %s is not implemented." % measurement)
                                except:
                                    # Failover
                                    screensize = 1366, 768
                                    sys.stderr.write("WARNING: Failed to detect screen size. Falling back to %sx%s" % screensize)
                                    if measurement=="px":
                                        return screensize
                                    elif measurement=="inch":
                                        return (screensize[0]/px_per_inch,screensize[1]/px_per_inch)
                                    elif measurement=="mm":
                                        return (screensize[0]/mm_per_inch,screensize[1]/mm_per_inch)
                                    else:
                                        raise NotImplementedError("Handling %s is not implemented." % measurement)