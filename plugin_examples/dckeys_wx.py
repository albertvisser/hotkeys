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
        ## self.p0list.setVerticalHeaderLabels(names)
        ## self.numrows = len(values)
    def read_data(self):
        """lees eventuele extra commando's
        """
        self.outfile = self.master.dialog_data['descfile']
        self.cmds = {}
        self.desc = self.master.dialog_data['omsdict']
        try:
            _in = open(self.outfile)
        except (IsADirectoryError, FileNotFoundError):
            return '{} not found'.format(self.outfile)
        else:
            with _in:
                rdr = csv.reader(_in)
                for key, oms in rdr:
                    self.cmds[key] = oms
        # nog niet eerder opgenomen lege beschrijvingen toevoegen
        for key in self.desc:
            if key not in self.cmds:
                self.cmds[key] = ''
        return ''

    def build_table(self):
        "vul de tabel met in te voeren gegevens"
        row = 0
        for key, desc in sorted(self.cmds.items()):
            self.p0list.SetCellValue(row, 0, key)
            self.p0list.SetCellValue(row, 0, desc)
            row += 1

    def write_data(self, new_data):
        "schrijf de omschrijvingen terug"
        if new_data == self.cmds:  # no changes
            return
        if os.path.exists(self.outfile):
            shutil.copyfile(str(self.outfile), str(self.outfile) + '~')
        with open(self.outfile, 'w') as _out:
            writer = csv.writer(_out)
            for key, value in new_data.items():
                if value:
                    writer.writerow((key, value))
