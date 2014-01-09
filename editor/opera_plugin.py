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
from editor import opkeys as keys


class MyPanel(HotkeyPanel):

    def __init__(self, parent):

        self._keys = keys
        coldata = (
            (C_KEY, 120, 3, False),
            ('047', 120, 0, False),
            ('048', 120, 1, False),
            ('049', 120, 2, False),
            (C_SRT, 120, 4, True),
            (C_OMS, 292, 5, False)
            )
        HotkeyPanel.__init__(self, parent, coldata, ini="opkey_config.py",
            title="Opera keys")

    def readkeys(self):
        self.data = keys.readkeys(self.ini.csv)

    def savekeys(self):
        HotkeyPanel.savekeys(pad=self.ini.csv)
