"""Hotkeys plugins voor gtk-accel based apps - GUI toolkit specifieke code
"""
import PyQt6.QtWidgets as qtw
from ..dialogs_qt import CompleteDialog


class AccelCompleteDialog(CompleteDialog):
    """(re)definition of generic dialog used in the main program
    """
    def read_data(self):
        "lees de vóór aanroep van de class ingestelde gegevens in"
        self.desc = self.master.dialog_data['descdict']
        self.cmds = self.master.dialog_data['actions']

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
