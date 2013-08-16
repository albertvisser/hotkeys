# -*- coding: UTF-8 -*-
"""Hotkeys plugin voor Opera
"""
from __future__ import print_function
import sys
import os
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

from .hotkeys_shared import * # constants


class MyPanel(HotkeyPanel):

    def __init__(self, parent, txt=""):

        coldata = ()
        self._txt = txt
        HotkeyPanel.__init__(self, parent, coldata, ini="",
            title="default_title")

    def add_extra_fields(self):
        self.txt = gui.QLabel(self._txt, self)

    def layout_extra_fields(self):
        self._sizer.addWidget(self.txt)

    def readkeys(self):
        self.data = {}

    def savekeys(self):
        pass


def main(args=None):
    app = gui.QApplication(sys.argv)
    frame = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
