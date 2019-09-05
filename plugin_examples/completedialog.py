"""Hotkeys: GUI for adding descriptions
"""
# TODO: (wx versie van maken en) de dialoog naar de dialogs modules verplaatsen
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
## import PyQt5.QtCore as core
import wx
import wx.grid as wxg
import editor.shared
from ..toolkit import toolkit


class QCompleteDialog(qtw.QDialog):
    """(re)definition of generic dialog used in the main program
    """
    def __init__(self, parent, *args):
        self.parent = parent
        ## self.captions = self.parent.captions

        super().__init__(parent)
        self.resize(680, 400)

        mld = self.read_data(*args)
        if mld:
            raise ValueError(mld)

        self.p0list = qtw.QTableWidget(len(self.cmds), 2, self)
        ## self.p0list.setColumnCount(2)
        self.p0list.setHorizontalHeaderLabels(['Command', 'Description'])
        hdr = self.p0list.horizontalHeader()
        ## p0hdr.resizeSection(0, 300)
        hdr.setStretchLastSection(True)
        self.build_table()
        self.p0list.setColumnWidth(0, 260)

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
        self.write_data(new_values)
        qtw.QDialog.accept(self)

    def read_data(*args):
        raise NotImplementedError

    def build_table(self):
        pass

    def write_data(self, data):
        pass


class WCompleteDialog(wx.Dialog):
    """(re)definition of generic dialog used in the main program
    """
    def __init__(self, parent, *args):
        self.parent = parent

        super().__init__(parent, size=(680, 400))

        mld = self.read_data(*args)
        if mld:
            raise ValueError(mld)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.p0list = wxg.Grid(self)
        self.p0list.CreateGrid(len(self.cmds), 2)
        self.p0list.SetRowLabelSize(20)

        for ix, row in enumerate((('Command', 280), ('Description', 400))):
            self.p0list.SetColLabelValue(ix, row[0])
            self.p0list.SetColSize(ix, row[1])
        # hdr.setStretchLastSection(True)
        self.build_table()

        hsizer.Add(self.p0list, 1, wx.EXPAND)
        self.sizer.Add(hsizer, 1, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        self.sizer.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM | wx.BOTTOM, 2)
        self.SetSizer(self.sizer)

    def accept(self):
        """confirm changes
        """
        new_values = {}
        for rowid in range(self.p0list.GetNumberRows()):
            cmd = self.p0list.GetCellValue(rowid, 0)
            desc = self.p0list.GetCellValue(rowid, 1)
            new_values[self.cmds[cmd]] = desc
        self.parent.dialog_data = new_values
        self.write_data(new_values)

    def read_data(*args):
        raise NotImplementedError

    def build_table(self):
        pass

    def write_data(self, data):
        pass


if toolkit == 'qt':
    CompleteDialog = QCompleteDialog
elif toolkit == 'wx':
    CompleteDialog = WCompleteDialog
