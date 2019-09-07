"""Hotkeys plugins voor gtk-accel based apps - GUI toolkit specifieke code
"""
import wx
import wx.grid as wxg
from ..dialogs_wx import CompleteDialog
import editor.plugins.gtkaccel_keys_csv as dml


class AccelCompleteDialog(CompleteDialog):
    """(re)definition of generic dialog used in the main program
    """
        ## self.p0list.setVerticalHeaderLabels([y for x, y in self.cmds.items()])
        ## self.p0list.resizeColumnToContents(0)
    def read_data(self):  # , outfile, cmds, desc):
        "lees de vóór aanroep van de class ingestelde gegevens in"
        self.outfile = self.master.dialog_data['descfile']
        self.cmds = self.master.dialog_data['actions']
        mld, self.desc = dml.read_data(self.outfile, self.master.dialog_data['omsdict'])
        return mld

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

    def write_data(self, new_data):
        "schrijf de omschrijvingsgegevens terug"
        dml.write_data(self.outfile, new_data)
