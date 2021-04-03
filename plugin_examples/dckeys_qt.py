"""Hotkeys plugin voor Double Commander - qt specifieke code
"""
import os.path
import shutil
import csv
import functools
import PyQt5.QtWidgets as qtw
from ..dialogs_qt import CompleteDialog


def layout_extra_fields(win, layout):
    """add the extra fields to the layout
    """
    sizer2 = qtw.QGridLayout()
    line = 0
    sizer2.addWidget(win.lbl_parms, line, 0)
    sizer2.addWidget(win.txt_parms, line, 1)
    line += 1
    sizer2.addWidget(win.lbl_controls, line, 0)
    sizer3 = qtw.QHBoxLayout()
    sizer3.addWidget(win.cmb_controls)
    sizer3.addStretch()
    sizer2.addLayout(sizer3, line, 1)
    layout.addLayout(sizer2, 1)


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
            new_item = qtw.QTableWidgetItem()
            new_item.setText(key)
            self.p0list.setItem(row, 0, new_item)
            # TODO: rubriek context toevoegen? (in elk geval voor DC)
            # in CompleteDialog kan ik het eerste en het laatste item uit de rij blijven gebruiken
            new_item = qtw.QTableWidgetItem()
            new_item.setText(desc)
            self.p0list.setItem(row, 1, new_item)
            row += 1
