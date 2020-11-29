"""Hotkeys plugin voor Double Commander - qt specifieke code
"""
import os.path
import shutil
import csv
import wx
import wx.grid as wxg
from ..dialogs_wx import CompleteDialog


def add_extra_fields(win, box):
    """fields showing details for selected keydef, to make editing possible
    """
    win.lbl_parms = wx.StaticText(box, label=win.master.captions['C_PARMS'])
    win.txt_parms = wx.TextCtrl(box, size=(280, -1))
    win.screenfields.append(win.txt_parms)
    win.ix_parms = 7
    win.lbl_controls = wx.StaticText(box, label=win.master.captions['C_CTRL'])
    cb = wx.ComboBox(box, choices=win.master.controlslist, style=wx.CB_READONLY)
    # cb.Bind(wx.EVT_COMBOBOX, functools.partial(on_combobox, win, cb, str))
    win.screenfields.append(cb)
    win.cmb_controls = cb
    win.ix_controls = 8


def layout_extra_fields(win, layout):
    """add the extra fields to the layout
    """
    sizer2 = wx.FlexGridSizer(2, 2, 2)
    line = 0
    sizer2.Add(win.lbl_parms, 0, wx.ALIGN_CENTER_VERTICAL)
    sizer2.Add(win.txt_parms, 1, wx.EXPAND)
    line += 1
    sizer2.Add(win.lbl_controls, 0, wx.ALIGN_CENTER_VERTICAL)
    sizer2.Add(win.cmb_controls, 1, wx.EXPAND)
    layout.Add(sizer2, 0, wx.LEFT, 5)


class DcCompleteDialog(CompleteDialog):
    """(re)definition of generic dialog used in the main program
    """
    def read_data(self):
        """lees eventuele extra commando's
        """
        self.cmds = self.master.dialog_data['descdict']
        self.desc = self.master.dialog_data['cmddict']
        # nog niet eerder opgenomen lege beschrijvingen toevoegen
        for key, value in self.desc.items():
            if key not in self.cmds and not value:
                self.cmds[key] = ''
        # en andersom
        for key, value in self.cmds.items():
            if key not in self.desc and not value:
                self.desc[key] = ''

    def build_table(self):
        "vul de tabel met in te voeren gegevens"
        row = 0
        for key, desc in sorted(self.cmds.items()):
            self.p0list.SetCellValue(row, 0, key)
            self.p0list.SetCellValue(row, 1, desc)
            row += 1
