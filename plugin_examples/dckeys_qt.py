"""Hotkeys plugin voor Double Commander - qt specifieke code
"""
import functools
import PyQt5.QtWidgets as qtw
from .completedialog import CompleteDialog


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


def send_completedialog(parent, descfile, omsdict):
    dlg = DcCompleteDialog(parent, descfile, omsdict).exec_()
    return dlg == qtw.QDialog.Accepted


class DcCompleteDialog(CompleteDialog):
    """(re)definition of generic dialog used in the main program
    """
        ## self.p0list.setVerticalHeaderLabels(names)
        ## self.numrows = len(values)
    def read_data(self, outfile, cmds):
        """lees eventuele extra commando's
        """
        # listitems = []
        self.cmds = cmds
        self.desc = desc
        try:
            _in = open(outfile)
        except (IsADirectoryError, FileNotFoundError):
            return '{} not found'.format(outfile)
        else:
            with _in:
                rdr = csv.reader(_in)
                for key, oms in rdr:
                    self.cmds[key] = oms
        return ''

    def build_table(self):
        row = 0
        for key, desc in sorted(self.cmds.items()):
            new_item = qtw.QTableWidgetItem()
            new_item.setText(key)
            self.p0list.setItem(row, 0, new_item)
            new_item = qtw.QTableWidgetItem()
            new_item.setText(desc)
            self.p0list.setItem(row, 1, new_item)
            row += 1

    def write_data(self, new_data):
        pass
