"""Hotkeys plugins voor gtk-accel based apps - GUI toolkit specifieke code
"""
import PyQt5.QtWidgets as qtw
from ..dialogs_qt import CompleteDialog
import editor.plugins.gtkaccel_keys_csv as dml


class AccelCompleteDialog(CompleteDialog):
    """(re)definition of generic dialog used in the main program
    """
        ## self.p0list.setVerticalHeaderLabels([y for x, y in self.cmds.items()])
        ## self.p0list.resizeColumnToContents(0)
    def read_data(self):
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
