# Valid arguments for the ...Awareness call below are defined in the following.
# https://msdn.microsoft.com/en-us/library/windows/desktop/dn280512(v=vs.85).aspx
import sys
if sys.platform == 'win32':
    try:
        import ctypes
        PROCESS_SYSTEM_DPI_AWARE = 1  # Int required.
        ctypes.OleDLL('shcore').SetProcessDpiAwareness(PROCESS_SYSTEM_DPI_AWARE)
    except (ImportError, AttributeError, OSError):
        pass