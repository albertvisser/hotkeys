# -*- coding: UTF-8 -*-
"""Hotkeys plugin voor ABAP editor
"""
from __future__ import print_function
import sys
import os
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

from .hotkeys_shared import * # constants
from editor import abapkeys as keys

class MyPanel(HotkeyPanel):

    def __init__(self, parent, txt=""):

        self._keys = keys
        coldata = (
            (C_KEY, 120, 0, False),
            (C_MOD, 90, 1, False),
            (C_OMS, 292, 2, False)
            )
        self._txt = txt
        HotkeyPanel.__init__(self, parent, coldata, ini="abkey_config.py",
            title="ABAP hotkeys")

    ## def add_extra_fields(self):
        ## self.txt = gui.QLabel(self._txt, self)

    ## def layout_extra_fields(self):
        ## self._sizer.addWidget(self.txt)

    ## def readkeys(self):
        ## self.data = {}

    ## def savekeys(self):
        ## pass
