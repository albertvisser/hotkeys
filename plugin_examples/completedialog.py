"""Hotkeys: GUI for adding descriptions
"""
import csv
import shutil
import pathlib
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
## import PyQt5.QtCore as core


class AccelCompleteDialog(qtw.QDialog):
    """(re)definition of generic dialog used in the main program
    """
    def __init__(self, parent, outfile, cmds, desc):
        self.parent = parent
        ## self.captions = self.parent.captions

        super().__init__(parent)
        self.resize(680, 400)

        ## self.cmds = {y: x for x, y in cmds.items()}
        self.outfile = pathlib.Path(outfile)
        try:
            _in = self.outfile.open()
        except FileNotFoundError:
            print(str(self.outfile), 'not found')   # pass
        else:
            with _in:
                rdr = csv.reader(_in)
                for line in rdr:
                    if line:
                        key, oms = line
                        ## print(key, oms)
                        if oms:
                            desc[int(key)] = oms
        self.p0list = qtw.QTableWidget(len(cmds), 2, self)
        ## self.p0list.setColumnCount(2)
        self.p0list.setHorizontalHeaderLabels(['Command', 'Description'])
        hdr = self.p0list.horizontalHeader()
        ## p0hdr.resizeSection(0, 300)
        hdr.setStretchLastSection(True)
        row = 0
        self.cmds = {}
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
                new_item.setText(desc[key])
            except KeyError:
                new_item.setText('')
            self.p0list.setItem(row, 1, new_item)
            row += 1
        ## self.p0list.setVerticalHeaderLabels([y for x, y in self.cmds.items()])
        self.p0list.setColumnWidth(0, 260)
        ## self.p0list.resizeColumnToContents(0)

        self.sizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(self.p0list)
        self.sizer.addLayout(hsizer)

        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)

    def accept(self):
        """confirm changes
        """
        new_values = {}
        for rowid in range(self.p0list.rowCount()):
            cmd = self.p0list.item(rowid, 0).text()
            desc = self.p0list.item(rowid, 1).text()
            new_values[self.cmds[cmd]] = desc
        self.parent.dialog_data = new_values
        if self.outfile.exists():
            shutil.copyfile(str(self.outfile), str(self.outfile) + '~')
        with self.outfile.open('w') as _out:
            writer = csv.writer(_out)
            for key, value in new_values.items():
                if value:
                    writer.writerow((key, value))
        qtw.QDialog.accept(self)


class DcCompleteDialog(qtw.QDialog):
    """(re)definition of generic dialog used in the main program
    """
    def __init__(self, parent, outfile, cmds):
        self.parent = parent
        ## self.captions = self.parent.captions

        super().__init__(parent)
        self.resize(680, 400)

        self.outfile = pathlib.Path(outfile)
        # listitems = []
        try:
            _in = self.outfile.open()
        except (IsADirectoryError, FileNotFoundError):
            print(str(self.outfile), 'not found')   # pass
        else:
            with _in:
                rdr = csv.reader(_in)
                for key, oms in rdr:
                    cmds[key] = oms
        self.p0list = qtw.QTableWidget(len(cmds), 2, self)
        ## self.p0list.setColumnCount(2)
        self.p0list.setHorizontalHeaderLabels(['Command', 'Description'])
        hdr = self.p0list.horizontalHeader()
        ## p0hdr.resizeSection(0, 300)
        hdr.setStretchLastSection(True)
        row = 0
        for key, desc in sorted(cmds.items()):
            new_item = qtw.QTableWidgetItem()
            new_item.setText(key)
            self.p0list.setItem(row, 0, new_item)
            new_item = qtw.QTableWidgetItem()
            new_item.setText(desc)
            self.p0list.setItem(row, 1, new_item)
            row += 1
        ## self.p0list.setVerticalHeaderLabels(names)
        self.p0list.setColumnWidth(0, 260)
        ## self.numrows = len(values)

        self.sizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(self.p0list)
        self.sizer.addLayout(hsizer)

        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)

    def accept(self):
        """confirm changes
        """
        new_values = {}
        for rowid in range(self.p0list.rowCount()):
            key = self.p0list.item(rowid, 0).text()
            desc = self.p0list.item(rowid, 1).text()
            new_values[key] = desc
        self.parent.dialog_data = new_values
        if self.outfile.exists():
            shutil.copyfile(str(self.outfile), str(self.outfile) + '~')
        ## with open(self.outfile, 'w') as _out:
            ## for key, value in new_values.items():
                ## _out.write('{}: {}\n'.format(key, value))
        with self.outfile.open('w') as _out:
            writer = csv.writer(_out)
            for key, value in new_values.items():
                if value:
                    writer.writerow((key, value))
        qtw.QDialog.accept(self)
