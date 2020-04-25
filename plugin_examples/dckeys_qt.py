"""Hotkeys plugin voor Double Commander - qt specifieke code
"""
import os.path
import shutil
import csv
import functools
import PyQt5.QtWidgets as qtw
from ..dialogs_qt import CompleteDialog


def add_extra_fields(win, box):
    """fields showing details for selected keydef, to make editing possible
    """
    win.lbl_parms = qtw.QLabel(win.master.captions['C_PARMS'], box)
    win.txt_parms = qtw.QLineEdit(box)
    win.txt_parms.setMaximumWidth(280)
    win.screenfields.append(win.txt_parms)
    win.ix_parms = 7
    win.lbl_controls = qtw.QLabel(win.master.captions['C_CTRL'], box)
    cb = qtw.QComboBox(box)
    cb.addItems(win.master.controlslist)
    cb.currentIndexChanged[str].connect(functools.partial(win.master.on_combobox, cb, str))
    win.screenfields.append(cb)
    win.cmb_controls = cb
    win.ix_controls = 8


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
            new_item = qtw.QTableWidgetItem()
            new_item.setText(key)
            self.p0list.setItem(row, 0, new_item)
            # TODO: rubriek context toevoegen? (in elk geval voor DC)
            # in CompleteDialog kan ik het eerste en het laatste item uit de rij blijven gebruiken
            new_item = qtw.QTableWidgetItem()
            new_item.setText(desc)
            self.p0list.setItem(row, 1, new_item)
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
