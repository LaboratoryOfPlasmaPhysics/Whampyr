#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from whampyr.GUI.qt.QtWidgets import QApplication

from whampyr.GUI.WhampyrMainWindow import WhampyrMainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = WhampyrMainWindow()
    MainWindow.show()
    app.exec_()
