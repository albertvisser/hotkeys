"""Hotkeys plugins voor gtk-accel based apps - GUI toolkit specifieke code
"""
import wx
import wx.grid as wxg
from ..dialogs_wx import CompleteDialog


class AccelCompleteDialog(CompleteDialog):
    """(re)definition of generic dialog used in the main program
    """
    def read_data(self):  # , outfile, cmds, desc):
        "lees de vóór aanroep van de class ingestelde gegevens in"
        self.desc = self.master.dialog_data['descdict']
        self.cmds = self.master.dialog_data['actions']

    def build_table(self):
        "vul de tabel met in te voeren gegevens"
        row = 0
        cmds, self.cmds = self.cmds, {}
        for key, cmd in sorted(cmds.items(), key=lambda x: x[1]):
            print(key, cmd)
            try:
                new_item, dummy = cmd
            except ValueError:  # assuming we get ValueError: too many values to unpack (expected 2)
                self.cmds[cmd] = key
            else:
                new_item = '/'.join(cmd)
                self.cmds[new_item] = key
            self.p0list.SetCellValue(row, 0, new_item)

            self.p0list.SetCellValue(row, 1, self.desc.get(key, ''))
            row += 1
