"""Hotkeys plugins voor gtk-accel based apps - GUI toolkit specifieke code
"""
import csv
import shutil
import wx
import wx.grid as wxg
from .completedialog import CompleteDialog


def send_completedialog(parent, descfile, actions, omsdict):
    with AccelCompleteDialog(parent.gui, descfile, actions, omsdict) as dlg:
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            dlg.accept()
    return dlg == wx.ID_OK


class AccelCompleteDialog(CompleteDialog):
    """(re)definition of generic dialog used in the main program
    """
        ## self.p0list.setVerticalHeaderLabels([y for x, y in self.cmds.items()])
        ## self.p0list.resizeColumnToContents(0)
    def read_data(self, outfile, cmds, desc):
        self.outfile = outfile
        self.cmds = cmds
        self.desc = desc
        try:
            _in = open(outfile)
        except FileNotFoundError:
            return '{} not found'.format(outfile)
        else:
            with _in:
                rdr = csv.reader(_in)
                for line in rdr:
                    if line:
                        key, oms = line
                        ## print(key, oms)
                        if oms:
                            desc[int(key)] = oms
        return ''

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
        if os.path.exists(outfile):
            shutil.copyfile(outfile, outfile + '~')
        with open(outfile, 'w') as _out:
            writer = csv.writer(_out)
            for key, value in new_values.items():
                if value:
                    writer.writerow((key, value))

