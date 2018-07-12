#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `whampyr` package."""

import pytest


def test_can_import_qtgui():
    from whampyr.GUI.qt import QtGui
    # simple test, should fail if QtGui isn't properly imported
    assert QtGui.qRgb(0xF0,0xAA,0x11) == 0xFFF0AA11


def test_can_import_qtcore():
    from whampyr.GUI.qt import QtCore
    # simple test, should fail if QtCore isn't properly imported
    assert QtCore.qrand() != QtCore.qrand()
