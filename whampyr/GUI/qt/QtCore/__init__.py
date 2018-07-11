try:
    from PyQt5.QtCore import *
except ImportError:
    try:
        from PySide2.QtCore import *
    except ImportError:
        raise ImportError("Neither PyQt5 nor PySide2 are installed, please install on of them")
