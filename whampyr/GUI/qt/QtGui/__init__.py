try:
    from PyQt5.QtGui import *
except ImportError:
    try:
        from PySide2.QtGui import *
    except ImportError:
        raise ImportError("Neither PyQt5 nor PySide2 are installed, please install on of them")
