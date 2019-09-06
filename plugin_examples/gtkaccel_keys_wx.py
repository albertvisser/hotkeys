"""Hotkeys plugins voor gtk-accel based apps - GUI toolkit specifieke code
"""
import wx
import wx.grid as wxg
from .completedialog import CompleteDialog
import editor.plugins.gtkaccel_keys_csv as dml


def send_completedialog(parent, descfile, actions, omsdict):
    with AccelCompleteDialog(parent.gui, descfile, actions, omsdict) as dlg:
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            dlg.accept()
    return ok == wx.ID_OK


class AccelCompleteDialog(CompleteDialog):
    """(re)definition of generic dialog used in the main program
    """
        ## self.p0list.setVerticalHeaderLabels([y for x, y in self.cmds.items()])
        ## self.p0list.resizeColumnToContents(0)
    def read_data(self, outfile, cmds, desc):
        self.outfile = outfile
        self.cmds = cmds
        mld, self.desc = dml.read_data(outfile, desc)
        return mld

    def build_table(self):
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
