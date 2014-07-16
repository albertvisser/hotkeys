# -*- coding: UTF-8 -*-
"""Hotkeys plugin voor Double Commander
"""
from __future__ import print_function
import sys
import os
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

from .hotkeys_shared import * # constants
from editor import dckeys as keys


class MyPanel(HotkeyPanel):

    def __init__(self, parent):

        self._keys = keys
        coldata = (
            (C_KEY, 100, 0, False),
            (C_MOD, 90, 1, False),
            (C_SRT, 120, 2, True),
            ('047', 70, 3, False),
            (C_CMD, 160, 4, False),
            (C_OMS, 292, 5, False)
            )
        HotkeyPanel.__init__(self, parent, coldata, ini="dckey_config.py",
            title="Double Commander keys")


def main(args=None):
    app = gui.QApplication(sys.argv)
    frame = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
