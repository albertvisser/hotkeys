"""Hotkeys plugin for Total Commander - wxPython specific code
"""
# TODO: ombouwen en gui-onafhanlkelijke onderdelen uitlichten
import os
import csv
# import functools
import wx
# import editor.shared as shared
from .tcmdrkys_shared import PATHS, defaultkeys, defaultcommands, translate_keyname
OKICON = '/usr/share/icons/Adwaita/16x16/emblems/emblem-ok-symbolic.symbolic.png'

def send_mergedialog(page):
    """show the dialog for connecting commands to keyboard shortcuts
    """
    with TcMergeDialog(page) as dlg:
        paths = [page.settings[x] for x in reversed(PATHS[:4])]
        paths.append(page.pad)
        dlg.load_files(paths)
        ok = dlg.ShowModal()
        return ok == wx.ID_OK


class TcMergeDialog(wx.Dialog):
    """Dialoog om een gedocumenteerde toetscombinatie te koppelen aan een commando

    In het ene ini bestand staat namelijk toets + omschrijving en in het andere
    command + omschrijving en de omschrijvingen hoeven uiteraard niet 100% gelijk
    te zijn, dus moeten ze handmatig gekoppeld worden. Vandaar de ietwat misleidende
    naam "links"
    """
    def __init__(self, parent):
        """Opbouwen van het scherm"""
        self.shortcuts = {}
        self.basedir = os.getcwd()
        super().__init__(parent.gui, title="TCCM", size=(1000, 600))
        # image voor het vinkje opzetten dat m.b.v. SetItemColumnImage ingesteld kan worden
        # self.okicon = wx.Icon(OKICON)
        self.imglist = wx.ImageList(16, 16)

        self.listkeys = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.listkeys.InsertColumn(0, 'Key')
        self.listkeys.InsertColumn(1, 'Description')
        # self.listkeys.setMouseTracking(True)
        # self.listkeys.itemEntered.connect(self.popuptext)

        self.findkeytext = wx.TextCtrl(self)
        self.nextkey = wx.Button(self, label='&Next')
        # self.nextkey.setMaximumWidth(50)
        self.nextkey.Bind(wx.EVT_BUTTON, self.findnextkey)
        self.prevkey = wx.Button(self, label='&Prev')
        # self.prevkey.setMaximumWidth(50)
        self.prevkey.Bind(wx.EVT_BUTTON, self.findprevkey)

        self.listcmds = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.listcmds.InsertColumn(0, 'Command')
        self.listcmds.InsertColumn(1, 'Description')
        # self.listcmds.setMouseTracking(True)
        # self.listcmds.itemEntered.connect(self.popuptext)

        self.findcmdtext = wx.TextCtrl(self)
        self.nextcmd = wx.Button(self, label='Ne&xt')
        # self.nextcmd.setMaximumWidth(50)
        self.nextcmd.Bind(wx.EVT_BUTTON, self.findnextcmd)
        self.prevcmd = wx.Button(self, label='Pre&v')
        # self.prevcmd.setMaximumWidth(50)
        self.prevcmd.Bind(wx.EVT_BUTTON, self.findprevcmd)

        self.listlinks = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.listlinks.InsertColumn(0, 'Key')
        self.listlinks.InsertColumn(1, 'Command')

        self.btn_link = wx.Button(self, label="&+ Add/Replace Link")
        self.btn_link.Bind(wx.EVT_BUTTON, self.make_link)
        ## self.btn_edit = wx.Button(pnl,-1,"&Modify Link")
        ## self.btn_edit.Bind(wx.EVT_BUTTON,self.edit_link)
        self.btn_delete = wx.Button(self, label="&- Discard Link")
        self.btn_delete.Bind(wx.EVT_BUTTON, self.delete_link)

        self.btn_load = wx.Button(self, label="&Load Links")
        self.btn_load.Bind(wx.EVT_BUTTON, self.load_links)
        self.btn_clear = wx.Button(self, label="&Clear All")
        self.btn_clear.Bind(wx.EVT_BUTTON, self.reset_all)
        self.btn_save = wx.Button(self, label="&Save Links")
        self.btn_save.Bind(wx.EVT_BUTTON, self.save_links)
        self.btn_quit = wx.Button(self, label="&Afsluiten")
        self.btn_quit.Bind(wx.EVT_BUTTON, self.cancel)
        self.btn_build = wx.Button(self, label="&Build CSV")
        self.btn_build.Bind(wx.EVT_BUTTON, self.confirm)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.listkeys, 1, wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.AddStretchSpacer()
        hbox2.Add(wx.StaticText(self, label='Find text:'), 0, wx.ALIGN_CENTER_VERTICAL)
        hbox2.Add(self.findkeytext, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox2.Add(self.nextkey, 0)
        hbox2.Add(self.prevkey, 0)
        hbox2.AddStretchSpacer()
        vbox2.Add(hbox2, 0, wx.EXPAND)
        hbox.Add(vbox2, 1, wx.EXPAND | wx.LEFT, 10)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.listcmds, 1, wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.AddStretchSpacer()
        hbox2.Add(wx.StaticText(self, label='Find text:'), 0, wx.ALIGN_CENTER_VERTICAL)
        hbox2.Add(self.findcmdtext, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox2.Add(self.nextcmd, 0)
        hbox2.Add(self.prevcmd, 0)
        hbox2.AddStretchSpacer()
        vbox2.Add(hbox2, 0, wx.EXPAND)
        hbox.Add(vbox2, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.listlinks, 1, wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.AddStretchSpacer()
        hbox2.Add(self.btn_link)
        hbox2.Add(self.btn_delete)
        hbox2.AddStretchSpacer()
        vbox2.Add(hbox2, 0, wx.EXPAND)
        hbox.Add(vbox2, 0, wx.EXPAND | wx.RIGHT, 10)
        vbox.Add(hbox, 1, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer()
        hbox.Add(self.btn_load, 0, wx.ALL, 2)
        hbox.Add(self.btn_clear, 0), wx.ALL, 2
        hbox.Add(self.btn_save, 0, wx.ALL, 2)
        hbox.Add(self.btn_quit), 0, wx.ALL, 2
        hbox.Add(self.btn_build)
        hbox.AddStretchSpacer()
        vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(vbox)
        vbox.SetSizeHints(self)  # Layout()

        # for text, callback, keyseq in (
        #         ('keylist', self.focuskeylist, 'Ctrl+1'),
        #         ('cmdlist', self.focuscmdlist, 'Ctrl+2'),
        #         ('findkey', self.focusfindkey, 'Ctrl+F'),
        #         ('nextkey', self.findnextkey, 'Ctrl+N'),
        #         ('prevkey', self.findprevkey, 'Ctrl+P'),
        #         ('findcmd', self.focusfindcmd, 'Ctrl+Shift+F'),
        #         ('nextcmd', self.findnextcmd, 'Ctrl+Shift+N'),
        #         ('prevcmd', self.findprevcmd, 'Ctrl+Shift+P'),
        #         ('addlink', self.make_link, 'Ctrl++'),
        #         ('remlink', self.delete_link, 'Del'),
        #         ('load', self.load_links, 'Ctrl+L'),
        #         ('clear', self.reset_all, 'Ctrl+Del'),
        #         ('save', self.accept, 'Ctrl+S'),
        #         ('quit', self.close, 'Ctrl+Q')):
        #     act = wx.Action(text, self)
        #     act.triggered.connect(callback)
        #     act.setShortcut(keyseq)
        #     self.addAction(act)

        self.keysearch = self.cmdsearch = ''
        self.keyresults, self.cmdresults = [], []

    def load_files(self, files):
        """load definitions from the various input files"""
        self.keyspad = files[0]
        self.cmdspad = files[1]
        self.linkspad = os.path.join(os.path.dirname(__file__),
                                     'tc_default_hotkeys_mapped.csv')
        self.load_keys()
        self.load_commands()

        ## # user commands (should be added to right list box?)
        ## self.usrdict, self.uomsdict = usercommands(files[2])

        ## # user defined keys (should be added to left list box?)
        ## self.usrkeys = dict(userkeys(files[3]))
        self.listlinks.DeleteAllItems()

    def load_keys(self):
        """load keyboard definitions"""

        # keycombinations
        # fill list box
        self.keydict = defaultkeys(self.keyspad)  # dict(keyboardtext(pad))
        self.listkeys.DeleteAllItems()
        self.keydata, self.keytexts = [], []
        for key, value in sorted(self.keydict.items()):
            index = self.listkeys.InsertItem(self.listkeys.GetItemCount(), ' '.join(key))
            self.listkeys.SetItem(index, 1, value['oms'])
            self.keydata.append(key)
            self.listkeys.SetItemData(index, self.keydata.index(key))
            self.keytexts.append(value['oms'])

    def load_commands(self):
        """load command definitions"""
        # commands
        # fill list box
        self.cmddict = defaultcommands(self.cmdspad)
        self.listcmds.DeleteAllItems()
        self.cmddata, self.cmdtexts = [], []
        for key, value in sorted(self.cmddict.items()):
            index = self.listcmds.InsertItem(self.listkeys.GetItemCount(), key)
            self.listcmds.SetItem(index, 1, value['oms'])
            self.cmddata.append(key)
            self.listcmds.SetItemData(index, self.cmddata.index(key))
            self.cmdtexts.append(value['oms'])

    def load_links(self):
        "load keydefs from temp file"
        self.reset_all()
        try:
            _in = open(self.linkspad, 'r')
        except FileNotFoundError:
            wx.MessageBox.information(self, 'Load data', "No saved data found")
            return

        with _in:
            rdr = csv.reader(_in)
            lines = [row for row in rdr]
        for key, mods, command in sorted(lines):
            keytext = ' '.join((key, mods))
            new = wx.TreeWidgetItem()
            new.setText(0, keytext)
            new.setData(0, core.Qt.UserRole, (key, mods))
            new.setText(1, command)
            self.listlinks.addTopLevelItem(new)
            try:
                item = self.listkeys.findItems(keytext, core.Qt.MatchFixedString, 0)[0]
            except IndexError:
                # geen item - geen vermelding in KEYBOARD.TXT, wel bekend in hotkeys.hky
                pass
            item.setIcon(0, self.okicon)

    def focuskeylist(self):
        "Enter search phrase"
        self.listkeys.setFocus()

    def focuscmdlist(self):
        "Enter search phrase"
        self.listcmds.setFocus()

    def focusfindkey(self):
        "Enter search phrase"
        self.findkeytext.setFocus()

    def focusfindcmd(self):
        "Enter search phrase"
        self.findcmdtext.setFocus()

    def popuptext(self, item, colno):
        "show complete text of description if moused over"
        if colno == 1:
            item.setToolTip(colno, item.text(colno))

    def make_link(self):
        """connect the choices
        """
        keychoice = self.listkeys.currentItem()
        keytext, key = keychoice.text(0), keychoice.data(0, core.Qt.UserRole)
        cmdchoice = self.listcmds.currentItem()
        cmdtext = cmdchoice.text(0)

        # let op: als link al bestaat: vervangen, niet toevoegen
        found = False
        for ix in range(self.listlinks.topLevelItemCount()):
            item = self.listlinks.topLevelItem(ix)
            if item.text(0) == keytext:
                found = True
                break
        if not found:
            item = wx.TreeWidgetItem()
            item.setText(0, keytext)
            item.setData(0, core.Qt.UserRole, key)
            self.listlinks.addTopLevelItem(item)
        item.setText(1, cmdtext)
        ## item.setText(2, gekozen_cmd)
        ## item.setText(3, gekozen_oms)
        ## if found:
        self.listlinks.scrollTo(self.listlinks.indexFromItem(item))
        ## else:
        ## if not found:
            ## self.listlinks.scrollToBottom()
        keychoice.setIcon(0, self.okicon)

    def delete_link(self):
        """remove an association
        """
        item = self.listlinks.currentItem()
        if not item:
            wx.MessageBox.information(self, "Delete entry", "Choose an item to " "delete")
            return
        ok = wx.MessageBox.question(self, "Delete entry", "Really delete?",
                                      wx.MessageBox.Yes | qtw.QMessageBox.No,
                                      defaultButton=wx.MessageBox.Yes)
        if ok == wx.MessageBox.Yes:
            ix = self.listlinks.indexOfTopLevelItem(item)
            item = self.listlinks.takeTopLevelItem(ix)
            find = item.text(0)
            ## self.listkeys.finditems(find, core.Qt.MatchExactly, 0)
            item = self.listkeys.findItems(find, core.Qt.MatchFixedString, 0)[0]
            # beetje omslachtige manier van een icon verwijderen bij een TreeWidgetItem!
            newitem = wx.TreeWidgetItem()
            newitem.setText(0, item.text(0))
            newitem.setData(0, core.Qt.UserRole, item.data(0, core.Qt.UserRole))
            newitem.setText(1, item.text(1))
            ix = self.listkeys.indexOfTopLevelItem(item)
            self.listkeys.takeTopLevelItem(ix)
            self.listkeys.insertTopLevelItem(ix, newitem)

    def finditem(self, input, search, list, results):
        "check if search string has changed"
        to_find = input.text()
        if not to_find:
            wx.MessageBox.information(self, 'Find text', 'Please enter text to search for')
            return None, None, None
        newsearch = to_find != search
        if newsearch:
            search = to_find
            results = list.findItems(search, core.Qt.MatchContains, 1)
        return newsearch, search, results

    def findnextitem(self, input, search, list, results):
        "search forward"
        newsearch, search, results = self.finditem(input, search, list, results)
        if not search:
            return
        current = list.currentItem()
        if not current:
            current = list.topLevelItem(0)
        if newsearch:
            # positioneren na huidige en klaar
            for item in results:
                if item.text(0) > current.text(0):
                    list.setCurrentItem(item)
                    return search, results
        else:
            # huidige zoeken in resultatenlijst, positioneren op volgende
            newix = results.index(current) + 1
            if newix < len(results):
                list.setCurrentItem(results[newix])
            else:
                list.setCurrentItem(results[0])
            return
        wx.MessageBox.information(self, 'Find text', 'No (next) item found')

    def findprevitem(self, input, search, list, results):
        "search backward"
        newsearch, search, results = self.finditem(input, search, list, results)
        if not search:
            return
        current = list.currentItem()
        if not current:
            current = list.topLevelItem(list.topLevelItemCount() - 1)
        if newsearch:
            # positioneren vóór huidige en klaar
            for item in reversed(results):
                if item.text(0) < current.text(0):
                    list.setCurrentItem(item)
                    return search, results
        else:
            # huidige zoeken in resultatenlijst, positioneren op vorige
            newix = results.index(current) - 1
            if newix >= 0:
                list.setCurrentItem(results[newix])
            else:
                list.setCurrentItem(results[-1])
            return
        wx.MessageBox.information(self, 'Find text', 'No previous item found')

    def findnextkey(self):
        "find next matching key item"
        test = self.findnextitem(self.findkeytext, self.keysearch, self.listkeys, self.keyresults)
        if test:
            self.keysearch, self.keyresults = test

    def findprevkey(self):
        "find previous matching key item"
        test = self.findprevitem(self.findkeytext, self.keysearch, self.listkeys, self.keyresults)
        if test:
            self.keysearch, self.keyresults = test

    def findnextcmd(self):
        "find next matching command item"
        test = self.findnextitem(self.findcmdtext, self.cmdsearch, self.listcmds, self.cmdresults)
        if test:
            self.cmdsearch, self.cmdresults = test

    def findprevcmd(self):
        "find previous matching command item"
        test = self.findprevitem(self.findcmdtext, self.cmdsearch, self.listcmds, self.cmdresults)
        if test:
            self.cmdsearch, self.cmdresults = test

    def reset_all(self):
        """remove all associations
        """
        self.listlinks.clear()
        self.load_keys()  # to reset all indicators

    def save_links(self):
        """save the changes to a temp file
        """
        num_items = self.listlinks.topLevelItemCount()
        if num_items == 0:
            wx.MessageBox.information(self, 'Save data', 'No data to save')
            return
        with open(self.linkspad, "w") as _out:
            writer = csv.writer(_out)
            for ix in range(num_items):
                item = self.listlinks.topLevelItem(ix)
                try:
                    key, mods = item.data(0, core.Qt.UserRole)
                except ValueError:
                    key, mods = item.data(0, core.Qt.UserRole), ''
                    print(key)
                writer.writerow((key, mods, item.text(1)))
        wx.MessageBox.information(self, 'Save data', 'Data saved')

    def cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def confirm(self, event):
        self.EndModal(wx.ID_OK)

    def accept(self):
        """confirm the changes

        don't save to file; just assign to a global variable
        """
        shortcuts = {}
        for ix in range(self.listlinks.topLevelItemCount()):
            item = self.listlinks.topLevelItem(ix)
            key, mods = item.data(0, core.Qt.UserRole)
            cmd = item.text(1)
            if cmd:
                desc = self.cmddict[cmd]['oms']
            else:
                desc = self.keydict[(key, mods)]['oms']
            shortcuts[ix] = (translate_keyname(key), mods, 'S', cmd, desc)
        self.parent().tempdata = shortcuts
        super().accept()
