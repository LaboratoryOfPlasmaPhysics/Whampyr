#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication

from whampyr.GUI.WampyrMainWindow import WampyrMainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = WampyrMainWindow()
    MainWindow.show()
    app.exec_()
