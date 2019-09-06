"""Hotkeys plugins voor gtk-accel based apps - GUI toolkit specifieke code
"""
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
## import PyQt5.QtCore as core
from .completedialog import CompleteDialog
import editor.plugins.gtkaccel_keys_csv as dml


def send_completedialog(parent, descfile, actions, omsdict):
    dlg = AccelCompleteDialog(parent.gui, descfile, actions, omsdict).exec_()
    return dlg == qtw.QDialog.Accepted


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
            ## print(key, cmd)
            new_item = qtw.QTableWidgetItem()
            try:
                new_item.setText(cmd)
                self.cmds[cmd] = key
            except TypeError:
                new_item.setText('/'.join(cmd))
                self.cmds['/'.join(cmd)] = key
            self.p0list.setItem(row, 0, new_item)
            new_item = qtw.QTableWidgetItem()
            try:
                new_item.setText(self.desc[key])
            except KeyError:
                new_item.setText('')
            self.p0list.setItem(row, 1, new_item)
            row += 1

    def write_data(self, new_data):
        "schrijf de omschrijvingsgegevens terug"
        dml.write_data(self.outfile, new_data)
