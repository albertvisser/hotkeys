# -*- coding: UTF-8 -*-
"""hotkeys.py

    main gui (choicebook)
    importeert de verschillende applicatiemodules
    hierin wordt het menu gedefinieerd en de functies die daarbij horen
    het idee is dat de menuopties wanneer nodig uitgegrijsd zijn en dat
        in de routines wordt uitgevraagd wat te doen bij welke applicatie
    voor wat betreft de instellingen:
        taalkeuze: op dit niveau
        paden: op applicatie niveau (in betreffende csv file)
"""
from __future__ import print_function
import os
import sys
import csv
import shutil
import collections
import functools
import importlib
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

import editor.hotkeys_constants as hkc
#
# non-gui and csv related functions
# perhaps also add to hotkeys_constants (rename?)
def read_settings(filename):
    lang, plugins = 'english.lng', []
    with open(filename) as _in:
        read_plugins = False
        for line in _in:
            if read_plugins:
                if line.strip() == ']':
                    read_plugins = False
                elif line.strip().startswith('#'):
                    continue
                else:
                    name, value = line.split(', ',1)
                    _, name = name.split('(')
                    value, _ = value.split(')')
                    plugins.append((name.strip('"'),
                        value.strip('"')))
            if line.startswith('PLUGINS'):
                read_plugins = True
            elif line.startswith('LANG'):
                lang = line.strip().split('=')[1].strip("'")
    return lang, plugins

def modify_settings(ini):
    # modify the settings file
    inifile = ini['filename']
    shutil.copyfile(inifile, inifile + '.bak')
    data = []
    dontread = False
    with open(inifile + '.bak') as _in:
        for line in _in:
            if dontread:
                if line.strip() == ']':
                    data.append(line)
                    dontread = False
            else:
                data.append(line)
                if 'PLUGINS' in line:
                    dontread = True
                    for name, path in ini["plugins"]:
                        data.append('    ("{}", "{}"),\n'.format(name, path))
    with open(inifile, 'w') as _out:
        for line in data:
            _out.write(line)

def change_language(oldlang, lang, inifile):
    shutil.copyfile(inifile, inifile + '.bak')
    with open(inifile + '.bak') as _in, open(inifile, 'w') as _out:
        for line in _in:
            if line.startswith('LANG'):
                line = line.replace(oldlang, lang)
            _out.write(line)

def read_columntitledata(self):
    """read the current language file and extract the already defined column headers
    """
    column_textids = []
    column_names = []
    last_textid = ''
    in_section = False

    with open(os.path.join(hkc.HERELANG, self.parent.ini["lang"])) as f_in:
        for line in f_in:
            line = line.strip()
            if line == '':
                continue
            elif line.startswith('#'):
                if in_section:
                    in_section = False
                elif 'Keyboard mapping' in line:
                    in_section = True
                continue
            test = line.split()
            if test[0] > last_textid and test[0] < '100':
                    last_textid = test[0]
            if in_section:
                column_textids.append(test[0])
                column_names.append(test[1])
    return column_textids, column_names, last_textid

def add_columntitledata(newdata):
    """add the new column title(s) to all language files

    input is a list of tuples (textid, text)"""
    ## pass
    ## # TODO: actually build this function
    choices = [os.path.join(hkc.HERELANG, x) for x in os.listdir(hkc.HERELANG)
        if os.path.splitext(x)[1] == ".lng"]
    for choice in choices:
        choice_o = choice + '~'
        shutil.copyfile(choice, choice_o)
        in_section = False
        with open(choice_o) as f_in, open(choice, 'w') as f_out:
            for line in f_in:
                if line.startswith('# Keyboard mapping'):
                    in_section = True
                elif in_section and line.strip() == '':
                    for textid, text in newdata:
                        f_out.write('{} {}\n'.format(textid, text))
                    in_section = False
                f_out.write(line)

def update_paths(paths, pathdata):
    """read the paths to the csv files from the data returned by the dialog
    if applicable also write a skeleton plugin file
    """
    newpaths = []
    for name, path in paths:
        loc = path.input.text()
        newpaths.append((name, loc))
        if name in pathdata:
            data = pathdata[name]
            with open(os.path.join('editor', data[0] + '.py'), 'w') as _out:
                _out.write(hkc.plugin_skeleton)
            initcsv(loc, data)
    return newpaths

def initcsv(loc, data):
    """Initialize csv file

    save some basic settttings to a csv file together with some sample data
    """
    with open(loc, "w") as _out:
        wrt = csv.writer(_out)
        for indx, sett in enumerate(hkc.csv_settingnames):
            wrt.writerow([hkc.csv_linetypes[0], sett, data[indx], hkc.csv_oms[sett]])
        for row in hkc.csv_sample_data:
            wrt.writerow(row)

def readcsv(pad):
    """lees het csv bestand op het aangegeven pad en geeft de inhoud terug

    retourneert dictionary van nummers met (voorlopig) 4-tuples
    """
    data = collections.OrderedDict()
    coldata = []
    settings = collections.OrderedDict()
    with open(pad, 'r') as _in:
        rdr = csv.reader(_in)
        key = 0
        first = True
        for row in rdr:
            rowtype, rowdata = row[0], row[1:]
            if rowtype == hkc.csv_settingtype:
                name, value, oms = rowdata
                settings[name] = (value, oms)
            elif rowtype == hkc.csv_titletype:
                for item in rowdata[:-1]:
                    coldata_item = ['', '', '', '', '']
                    coldata_item[1] = item
                    coldata.append(coldata_item)
            elif rowtype == hkc.csv_widthtype:
                for ix, item in enumerate(rowdata[:-1]):
                    coldata[ix][2] = int(item)
            elif rowtype == hkc.csv_seqnumtype:
                for ix, item in enumerate(rowdata[:-1]):
                    coldata[ix][0] = int(item)
                    coldata[ix][3] = ix
            elif rowtype == hkc.csv_istypetype:
                for ix, item in enumerate(rowdata[:-1]):
                    coldata[ix][4] = bool(int(item))
                coldata.sort()
                coldata = [x[1:] for x in coldata]
            elif rowtype == hkc.csv_keydeftype:
                key += 1
                data[key] = ([x.strip() for x in rowdata])
            elif not rowtype.startswith('#'):
                raise NotImplementedError("Unknown setting type '{}' in csv "
                    "file". format(rowtype))
    return settings, coldata, data

def writecsv(pad, settings, coldata, data):
    ## os.remove(_outback)
    if os.path.exists(pad):
        shutil.copyfile(pad, pad + '~')
    with open(pad, "w") as _out:
        wrt = csv.writer(_out)
        for name, value in settings.items():
            rowdata = hkc.csv_settingtype, name, value[0], value[1]
            wrt.writerow(rowdata)
        for ix, row in enumerate([[hkc.csv_titletype], [hkc.csv_widthtype],
                [hkc.csv_seqnumtype]]):
            row += [x[ix] for x in coldata] + [hkc.csv_oms[row[0]]]
            wrt.writerow(row)
        wrt.writerow([hkc.csv_istypetype] + [int(x[3]) for x in coldata] +
            [hkc.csv_oms[hkc.csv_istypetype]])
        for keydef in data.values():
            row = [hkc.csv_keydeftype] + [x for x in keydef]
            wrt.writerow(row)

def quick_check(filename):
    """quick and dirty function for checking a csv file outside of the application

    replicates some things that are done in building the list with keydefs
    so we can catch errors in advance
    """
    _, column_info, data = readcsv(filename)
    items = data.items()
    if items is None or len(items) == 0:
        print('No keydefs found in this file')
        return
    for key, data in items:
        try:
            for indx, col in enumerate(column_info):
                from_indx, is_soort = col[2], col[3]
                value = data[from_indx]
        except Exception as e:
            print(key, data)
            raise
    print('{}: No errors found'.format(filename))

#
# shared (menu) functions
#
def show_message(self, message_id='', text='', caption_id='000'):
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    na sluiten van de dialoog
    """
    if message_id:
        text = self.captions[message_id]
    if not text:
        text = 'No message to show'
    ok = gui.QMessageBox.question(self, self.captions[caption_id], text,
        gui.QMessageBox.Yes | gui.QMessageBox.No | gui.QMessageBox.Cancel)
    return ok

def m_read(self):
    """(menu) callback voor het lezen van de hotkeys

    vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
    zet de gelezen keys daarna ook in de gui
    """
    doit = True
    if not self.page.modified:
        doit = False
        h = show_message(self, '041')
        if h == gui.QMessageBox.Yes:
            doit = True
    if doit:
        self.page.readkeys()
        self.page.populate_list()

def m_save(self):
    """(menu) callback voor het terugschrijven van de hotkeys

    vraagt eerst of het ok is om de hotkeys weg te schrijven
    vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
    """
    if not self.page.modified:
        h = show_message(self, '041')
        if h != gui.QMessageBox.Yes:
            return
    self.page.savekeys()
    gui.QMessageBox.information(self, self.captions['000'], self.captions['037'])

def m_loc(self):
    """(menu) callback voor aanpassen van de bestandslocaties

    vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
    toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
    (met name of de opgegeven paden kloppen)
    """
    # self.ini["plugins"] bevat de lijst met tools en csv locaties
    current_programs = [x for x, y in self.ini["plugins"]]
    current_paths = [y for x, y in self.ini["plugins"]]
    ok = FilesDialog(self).exec_()
    if ok == gui.QDialog.Accepted:
        modify_settings(self.ini)

        # update the screen(s)
        # clear the selector and the stackedwidget while pairing up programs and windows
        # that need to be kept or replaced
        hlpdict = {}
        self.book.sel.clear()
        current_items = reversed([(x, y) for x, y in enumerate(current_programs)])
        new_programs = [x for x, y in self.ini["plugins"]]
        new_paths = [y for x, y in self.ini["plugins"]]
        for indx, program in current_items: # we need to do this in reverse
            win = self.book.pnl.widget(indx)
            self.book.pnl.removeWidget(win)
            if program in new_programs:
                hlpdict[program] = win # keep the widget
            else:
                win.close() # lose the widget
        # add new ones, modify existing or leave them alone
        for indx, program in enumerate(new_programs):
            if program in current_programs:
                #compare the new and the existing path
                old_loc = current_paths[current_programs.index(program)]
                new_loc = new_paths[new_programs.index(program)]
                if new_loc == old_loc:  # unchanged
                    win = hlpdict[program]
                else: # take data from different location
                    win = HotkeyPanel(self.book, new_loc) or EmptyPanel(
                        self.book.pnl, self.captions["052"].format(program))
            else: # new entry
                 win = HotkeyPanel(self.book, new_paths[indx]) or EmptyPanel(
                        self.book.pnl, self.captions["052"].format(program))
            self.book.sel.addItem(program)
            self.book.pnl.addWidget(win)

def m_user(self):
    """(menu) callback voor een nog niet geïmplementeerde actie"""
    return self.captions[NOT_IMPLEMENTED]

def m_rebuild(self):

    csvfile = self.page.pad
    # read data from the csv file
    settings, coldata, _ = readcsv(csvfile)
    if not settings:
        return 'Settings could not be determined from', csvfile

    shortcuts = self.page._keys.buildcsv(settings, self)
    if shortcuts:
        writecsv(csvfile, settings, coldata, shortcuts)

def m_tool(self):
    """define tool-specific settings
    """
    dlg = ExtraSettingsDialog(self).exec_()
    if dlg == gui.QDialog.Accepted:
        writecsv(self.page.pad, self.page.settings, self.page.column_info,
            self.page.data)

def m_col(self):
    """define tool-specific settings: column properties
    """
    print(self.page.column_info)
    column_count = len(self.page.column_info)
    print(column_count)
    dlg = ColumnSettingsDialog(self).exec_()
    if dlg == gui.QDialog.Accepted:
        print('dialog was accepted')
        print(self.page.column_info)
        print(column_count)
        writecsv(self.page.pad, self.page.settings, self.page.column_info,
            self.page.data)
        if len(self.page.column_info) > column_count:
            gui.QMessageBox.information(self, self.captions['000'],
                "You have now defined more columns for this tool than are in the "
                "keydefs. Reloading them will result in an error.")

def m_entry(self):
    dlg = EntryDialog(self).exec_()
    if dlg == gui.QDialog.Accepted:
        writecsv(self.page.pad, self.page.settings, self.page.column_info,
            self.page.data)
        self.page.populate_list()

def m_lang(self):
    """(menu) callback voor taalkeuze

    past de settings aan en leest het geselecteerde language file
    """
    # bepaal welke language files er beschikbaar zijn
    choices = [x for x in os.listdir(hkc.HERELANG) if os.path.splitext(x)[1] == ".lng"]
    # bepaal welke er momenteel geactiveerd is
    oldlang = self.ini['lang']
    indx = choices.index(oldlang) if oldlang in choices else 0
    lang, ok = gui.QInputDialog.getItem(self, self.captions["027"],
        self.captions["000"], choices, current=indx, editable=False)
    if ok:
        change_language(oldlang, lang, self.ini['filename'])
        self.ini['lang'] = lang
        self.readcaptions(lang)
        self.setcaptions()

def m_about(self):
    """(menu) callback voor het tonen van de "about" dialoog
    """
    text = '\n'.join(self.captions['057'].format(self.captions['071'],
        hkc.VRS, hkc.AUTH, self.captions['072']).split(' / '))
    info = gui.QMessageBox.information(self, self.captions['000'], text)

def m_exit(self):
    """(menu) callback om het programma direct af te sluiten"""
    self.exit()

#
# application classes (screens and subscreens)
#
class FileBrowseButton(gui.QFrame):
    """Combination widget showing a text field and a button
    making it possible to either manually enter a filename or select
    one using a FileDialog
    """
    def __init__(self, parent, text="", level_down=False):
        self.parent = parent.parent
        if level_down:
            self.parent = self.parent.parent
        self.startdir = ''
        if text:
            self.startdir = os.path.dirname(text)
        gui.QFrame.__init__(self, parent)
        self.setFrameStyle(gui.QFrame.Panel | gui.QFrame.Raised);
        vbox = gui.QVBoxLayout()
        box = gui.QHBoxLayout()
        self.input = gui.QLineEdit(text, self)
        self.input.setMinimumWidth(200)
        box.addWidget(self.input)
        caption = self.parent.captions['058']
        self.button = gui.QPushButton(caption, self, clicked=self.browse)
        box.addWidget(self.button)
        vbox.addLayout(box)
        self.setLayout(vbox)

    def browse(self):
        startdir = str(self.input.text()) or os.getcwd()
        path = gui.QFileDialog.getOpenFileName(self,
            self.parent.captions['059'], startdir)
        if path:
            self.input.setText(path)

class SetupDialog(gui.QDialog):
    """dialoog voor het opzetten van een csv bestand

    geeft de mogelijkheid om alvast wat instellingen vast te leggen en zorgt er
    tevens voor dat het correcte formaat gebruikt wordt
    """
    def __init__(self, parent, name):
        self.parent = parent
        gui.QDialog.__init__(self)
        self.setWindowTitle('Initieel opzetten CSV bestand')

        grid = gui.QGridLayout()

        text = gui.QLabel('Naam van de module met de toolspecifieke code (will also'
            ' create it)', self)
        self.t_program = gui.QLineEdit(name.lower() + '_keys', self)
        grid.addWidget(text, 1, 0, 1, 3)
        grid.addWidget(self.t_program, 1, 3) #, 1, 1)
        text = gui.QLabel('Naam voor de titel van het toolpanel', self)
        self.t_title = gui.QLineEdit(name + ' hotkeys', self)
        grid.addWidget(text, 2, 0, 1, 3)
        grid.addWidget(self.t_title, 2, 3) #, 1, 1)
        self.c_rebuild = gui.QCheckBox("Make it possible to rebuild this file "
            "from the tool's settings", self)
        grid.addWidget(self.c_rebuild, 3, 1, 1, 3)
        self.c_redef = gui.QCheckBox("Make it possible to redefine the keydefs "
            "and save them back", self)
        grid.addWidget(self.c_redef, 4, 1, 1, 3)
        ## grid.addSpacer(5, 0, 1, 3)
        text = gui.QLabel('Waar zullen we dit bestand opslaan?', self)
        grid.addWidget(text, 5, 0, 1, 2)
        self.t_loc = FileBrowseButton(self, text = name + "_hotkeys.csv",
            level_down=True)
        grid.addWidget(self.t_loc, 5, 2, 1, 3)

        buttonbox = gui.QDialogButtonBox()
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        box = gui.QVBoxLayout()
        box.addStretch()
        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addLayout(grid)
        hbox.addStretch()
        box.addLayout(hbox)
        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(buttonbox)
        hbox.addStretch()
        box.addLayout(hbox)
        box.addStretch()
        self.setLayout(box)

    def accept(self):
        """
        set self.parent.loc to the chosen filename
        write the settings to this file along with some sample data
        """
        loc = self.t_loc.input.text()
        if loc == "":
            gui.QMessageBox.information(self, self.parent.title, "Sorry, can't"
                " continue without a name - please enter one or cancel")
            return
        self.parent.loc = loc
        self.parent.data = [self.t_program.text(), self.t_title.text(),
            int(self.c_rebuild.isChecked()), int(self.c_redef.isChecked())]
        gui.QDialog.accept(self)

class ColumnSettingsDialog(gui.QDialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent):
        self.parent = parent
        gui.QDialog.__init__(self, parent)
        ## self.resize(680, 400)

        self.sizer = gui.QVBoxLayout()
        ## self.sizer.addStretch()
        text = self.parent.captions['079'].format(
            self.parent.page.settings["PanelName"][0])
        hsizer = gui.QHBoxLayout()
        label = gui.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(41)
        hsizer.addWidget(gui.QLabel(self.parent.captions['080'], self),
            alignment = core.Qt.AlignHCenter | core.Qt.AlignVCenter)
        hsizer.addSpacing(102) #82)
        hsizer.addWidget(gui.QLabel(self.parent.captions['081'], self),
            alignment = core.Qt.AlignVCenter)
        hsizer.addSpacing(8) # 84)
        hsizer.addWidget(gui.QLabel(self.parent.captions['082'], self),
            alignment = core.Qt.AlignVCenter)
        hsizer.addWidget(gui.QLabel(self.parent.captions['086'], self),
            alignment = core.Qt.AlignVCenter)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        pnl = gui.QFrame(self)
        self.scrl = gui.QScrollArea(self)
        self.scrl.setWidget(pnl)
        self.scrl.setAlignment(core.Qt.AlignBottom)
        self.scrl.setWidgetResizable(True)
        self.bar = self.scrl.verticalScrollBar()
        self.gsizer = gui.QGridLayout()
        rownum = 0
        self.rownum = rownum
        self.data, self.checks = [], []
        self.col_textids, self.col_names, self.last_textid = read_columntitledata(
            self)
        for item in self.parent.page.column_info:
            self.add_row(*item)
        box = gui.QVBoxLayout()
        box.addLayout(self.gsizer)
        box.addStretch()
        pnl.setLayout(box)
        self.sizer.addWidget(self.scrl)

        buttonbox = gui.QDialogButtonBox()
        # should be: add setting
        btn = buttonbox.addButton(self.parent.captions['084'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.add_column)
        # should be: remove checked settings
        btn = buttonbox.addButton(self.parent.captions['085'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.remove_columns)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        ## self.sizer.addStretch()
        self.setLayout(self.sizer)

    def exec_(self):
        if self.last_textid == '099':
            gui.QMessageBox.information(self, self.parent.title, "Can't perform "
                "this function: no language text identifiers below 100 left")
            self.reject()
        else:
            return super().exec_()

    def accept(self):
        column_info, new_titles = [], []
        for w_name, w_width, w_colno, w_flag in self.data:
            name = w_name.currentText()
            if name in self.col_names:
                name = self.col_textids[self.col_names.index(name)]
            else:
                self.last_textid = "{:0>3}".format(int(self.last_textid) + 1)
                new_titles.append((self.last_textid, name))
                name = self.last_textid
            column_info.append([name, int(w_width.text()), int(w_colno.text()) - 1,
                w_flag.isChecked()])
        if new_titles:
            add_columntitledata(new_titles)
        print('transferring column info')
        self.parent.page.column_info = column_info
        gui.QDialog.accept(self)

    def add_row(self, name='', width='', colno='', is_flag=False):
        self.rownum += 1
        colnum = 0
        check = gui.QCheckBox(self)
        self.gsizer.addWidget(check, self.rownum, colnum)
        self.checks.append(check)
        colnum += 1
        w_name = gui.QComboBox(self)
        w_name.addItems(self.col_names)
        ## w_name.setFixedWidth(88)
        w_name.setEditable(True)
        if name:
            w_name.setCurrentIndex(self.col_textids.index(name))
        else:
            w_name.clearEditText()
        ## w_name.setMaxLength(50)
        self.gsizer.addWidget(w_name, self.rownum, colnum)
        colnum += 1
        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(20)
        ## w_width = gui.QLineEdit(str(width), self)
        w_width = gui.QSpinBox(self)
        w_width.setMaximum(999)
        if width:
            w_width.setValue(width)
        w_width.setFixedWidth(48)
        hsizer.addWidget(w_width)
        hsizer.addSpacing(20)
        self.gsizer.addLayout(hsizer, self.rownum, colnum)
        colnum += 1
        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(40)
        w_flag = gui.QCheckBox(self)
        w_flag.setChecked(is_flag)
        w_flag.setFixedWidth(32)
        hsizer.addWidget(w_flag)
        hsizer.addSpacing(24)
        self.gsizer.addLayout(hsizer, self.rownum, colnum)
        colnum += 1
        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(68)
        val = self.rownum if colno == '' else colno + 1
        ## w_colno = gui.QLineEdit(str(val), self)
        w_colno = gui.QLabel(self)
        w_colno.setText(str(val))
        w_colno.setFixedWidth(20)
        ## w_colno.setReadOnly(True)
        hsizer.addWidget(w_colno)
        hsizer.addStretch()
        self.gsizer.addLayout(hsizer, self.rownum, colnum)
        self.data.append((w_name, w_width, w_colno, w_flag))
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 31)
        vbar.setValue(vbar.maximum())

    def delete_row(self, rownum):
        check = self.checks[rownum]
        w_name, w_width, w_colno, w_flag = self.data[rownum]
        for widget in check, w_name, w_width, w_colno, w_flag:
            self.gsizer.removeWidget(widget)
            widget.close() # destroy()
        self.checks.pop(rownum)
        self.data.pop(rownum)

    def add_column(self):
        """nieuwe rij aanmaken in self.gsizer"""
        self.add_row()

    def remove_columns(self):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        test = [x.isChecked() for x in self.checks]
        checked = [x for x, y in enumerate(test) if y]
        if any(test):
            ok = gui.QMessageBox.question(self, self.parent.title,
                self.parent.captions['083'],
                gui.QMessageBox.Yes | gui.QMessageBox.No)
            if gui.QMessageBox.Yes:
                for row in reversed(checked):
                    self.delete_row(row)
        return


class ExtraSettingsDialog(gui.QDialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent):
        self.parent = parent
        gui.QDialog.__init__(self, parent)
        ## self.resize(680, 400)

        self.sizer = gui.QVBoxLayout()
        ## self.sizer.addStretch()
        text = self.parent.captions['073'].format(
            self.parent.page.settings["PanelName"][0])
        hsizer = gui.QHBoxLayout()
        label = gui.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(41)
        hsizer.addWidget(gui.QLabel(self.parent.captions['074'], self),
            alignment = core.Qt.AlignHCenter)
        hsizer.addSpacing(52)
        hsizer.addWidget(gui.QLabel(self.parent.captions['075'], self),
            alignment = core.Qt.AlignHCenter)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        pnl = gui.QFrame(self)
        self.scrl = gui.QScrollArea(self)
        self.scrl.setWidget(pnl)
        self.scrl.setWidgetResizable(True)
        self.bar = self.scrl.verticalScrollBar()

        self.gsizer = gui.QGridLayout()
        rownum = colnum = 0
        self.rownum = rownum
        self.data, self.checks = [], []
        for name, value in self.parent.page.settings.items():
            if name not in hkc.csv_settingnames:
                self.add_row(name, value)
        box = gui.QVBoxLayout()
        box.addLayout(self.gsizer)
        box.addStretch()
        pnl.setLayout(box)
        self.sizer.addWidget(self.scrl)

        buttonbox = gui.QDialogButtonBox()
        # should be: add setting
        btn = buttonbox.addButton(self.parent.captions['076'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.add_setting)
        # should be: remove checked settings
        btn = buttonbox.addButton(self.parent.captions['077'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.remove_settings)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        ## self.sizer.addStretch()
        self.setLayout(self.sizer)

    def add_row(self, name='', value=''):
        if value:
            value, desc = value
        else:
            desc = ''
        self.rownum += 1
        colnum = 0
        check = gui.QCheckBox(self)
        self.gsizer.addWidget(check, self.rownum, colnum)
        self.checks.append(check)
        colnum += 1
        w_name = gui.QLineEdit(name, self)
        w_name.setFixedWidth(88)
        if name:
            w_name.setReadOnly(True)
        ## w_name.setMaxLength(50)
        self.gsizer.addWidget(w_name, self.rownum, colnum)
        colnum += 1
        w_value = gui.QLineEdit(value, self)
        self.gsizer.addWidget(w_value, self.rownum, colnum)
        self.rownum += 1
        w_desc = gui.QLineEdit(desc, self)
        self.gsizer.addWidget(w_desc, self.rownum, colnum)
        self.data.append((w_name, w_value, w_desc))
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 62)
        vbar.setValue(vbar.maximum())

    def delete_row(self, rownum):
        check = self.checks[rownum]
        w_name, w_value, w_desc = self.data[rownum]
        for widget in check, w_name, w_value, w_desc:
            self.gsizer.removeWidget(widget)
            widget.close() # destroy()
        self.checks.pop(rownum)
        self.data.pop(rownum)

    def add_setting(self):
        """nieuwe rij aanmaken in self.gsizer"""
        self.add_row()

    def remove_settings(self):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        test = [x.isChecked() for x in self.checks]
        checked = [x for x, y in enumerate(test) if y]
        if any(test):
            ok = gui.QMessageBox.question(self, self.parent.title,
                self.parent.captions['078'],
                gui.QMessageBox.Yes | gui.QMessageBox.No)
            if gui.QMessageBox.Yes:
                for row in reversed(checked):
                    self.delete_row(row)
                ## self.update()

    def accept(self):
        settings = []
        settingsdict = {}
        for w_name, w_value, w_desc in self.data:
            settingsdict[w_name.text()] = (w_value.text(), w_desc.text())
        for setting in self.parent.page.settings:
            if setting not in hkc.csv_settingnames:
                del self.parent.page.settings[setting]
        self.parent.page.settings.update(settingsdict)
        gui.QDialog.accept(self)

class FilesDialog(gui.QDialog):
    """dialoog met meerdere FileBrowseButtons

    voor het instellen van de bestandslocaties
    """
    def __init__(self, parent):
        self.parent = parent
        gui.QDialog.__init__(self, parent)
        self.resize(680, 400)

        self.sizer = gui.QVBoxLayout()
        ## self.sizer.addStretch()
        text = '\n'.join((self.parent.captions['069'], self.parent.captions['070']))
        hsizer = gui.QHBoxLayout()
        label = gui.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(36)
        hsizer.addWidget(gui.QLabel(self.parent.captions['060'], self),
            alignment = core.Qt.AlignHCenter | core.Qt.AlignVCenter)
        hsizer.addSpacing(84)
        hsizer.addWidget(gui.QLabel(self.parent.captions['061'], self),
            alignment = core.Qt.AlignVCenter)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        pnl = gui.QFrame(self)
        self.scrl = gui.QScrollArea(self)
        self.scrl.setWidget(pnl)
        self.scrl.setWidgetResizable(True)
        self.bar = self.scrl.verticalScrollBar()
        self.gsizer = gui.QGridLayout()
        rownum = colnum = 0
        self.rownum = rownum
        self.checks = []
        self.paths = []
        self.data = [] #
        self.pathdata = {}
        for name, path in self.parent.ini["plugins"]:
            self.add_row(name, path)
        box = gui.QVBoxLayout()
        box.addLayout(self.gsizer)
        box.addStretch()
        pnl.setLayout(box)
        self.sizer.addWidget(self.scrl)

        buttonbox = gui.QDialogButtonBox()
        btn = buttonbox.addButton(self.parent.captions['062'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.add_program)
        btn = buttonbox.addButton(self.parent.captions['063'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.remove_programs)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        ## self.sizer.addStretch()
        self.setLayout(self.sizer)

    def add_row(self, name, path=''):
        self.rownum += 1
        colnum = 0
        check = gui.QCheckBox(name, self)
        self.gsizer.addWidget(check, self.rownum, colnum)
        self.checks.append(check)
        colnum += 1
        browse = FileBrowseButton(self, text=path)
        self.gsizer.addWidget(browse, self.rownum, colnum)
        self.paths.append((name, browse))
        if self.data:
            self.pathdata[name] = self.data
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 52)
        vbar.setValue(vbar.maximum())

    def delete_row(self, rownum):
        check = self.checks[rownum]
        _, win = self.paths[rownum]
        self.gsizer.removeWidget(check)
        check.close() # destroy()
        self.gsizer.removeWidget(win)
        win.close() # destroy()
        self.checks.pop(rownum)
        self.paths.pop(rownum)

    def add_program(self):
        """nieuwe rij aanmaken in self.gsizer"""
        self.data = []
        newtool, ok = gui.QInputDialog.getText(self, self.parent.title,
            self.parent.captions['064'])
        if ok:
            if newtool == "":
                gui.QMessageBox.information(self, self.parent.title, "Sorry, can't"
                    " continue without a name")
                return
            ok = gui.QMessageBox.question(self, self.parent.title, "Initialize new "
                "csv file for this application?",
                gui.QMessageBox.Yes | gui.QMessageBox.No, gui.QMessageBox.Yes)
            self.loc = ""
            if ok == gui.QMessageBox.Yes:
                ok = SetupDialog(self, newtool).exec_()
            self.add_row(newtool, path=self.loc)
            ## self.update()

    def remove_programs(self):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        test = [x.isChecked() for x in self.checks]
        checked = [x for x, y in enumerate(test) if y]
        if any(test):
            ok = gui.QMessageBox.question(self, self.parent.title,
                self.parent.captions['065'],
                gui.QMessageBox.Yes | gui.QMessageBox.No)
            if gui.QMessageBox.Yes:
                for row in reversed(checked):
                    self.delete_row(row)
                ## self.update()

    def accept(self):
        self.parent.ini["plugins"] = update_paths(self.paths, self.pathdata)
        gui.QDialog.accept(self)

class EntryDialog(gui.QDialog):

    def __init__(self, parent):
        self.parent = parent
        self.captions = self.parent.captions

        gui.QDialog.__init__(self, parent)
        self.resize(680, 400)

        # use self.parent.page.column_info to define grid
        names, widths = [], []
        for row in self.parent.page.column_info:
            names.append(self.captions[row[0]])
            widths.append(row[1])

        # use self.parent.page.data to populate grid
        self.data = self.parent.page.data

        self.p0list = gui.QTableWidget(self)
        self.p0list.setColumnCount(len(names))
        self.p0list.setHorizontalHeaderLabels(names)
        p0hdr = self.p0list.horizontalHeader()
        for indx, wid in enumerate(widths):
            p0hdr.resizeSection(indx, wid)
        num_rows = 0
        for rowkey, row in self.data.items():
            self.p0list.insertRow(num_rows)
            for i, element in enumerate(row):
                new_item = gui.QTableWidgetItem()
                new_item.setText(element)
                self.p0list.setItem(num_rows, i, new_item)
            num_rows += 1
        self.numrows = num_rows

        self.sizer = gui.QVBoxLayout()
        hsizer = gui.QHBoxLayout()
        hsizer.addWidget(self.p0list)
        self.sizer.addLayout(hsizer)

        buttonbox = gui.QDialogButtonBox()
        btn = buttonbox.addButton("&Add key",
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.add_key)
        btn = buttonbox.addButton("&Delete selected key(s)",
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.delete_key)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)

    def add_key(self):
        "add a line to the grid"
        self.p0list.insertRow(self.numrows)
        for i in range(self.p0list.columnCount()):
            new_item = gui.QTableWidgetItem()
            new_item.setText("")
            self.p0list.setItem(self.numrows, i, new_item)
        self.numrows += 1

    def delete_key(self):
        "remove selected line(s) from the grid"
        selected_rows = []
        for item in self.p0list.selectedRanges():
            for increment in range(item.rowCount()):
                selected_rows.append(item.topRow() + increment)
        for row in reversed(sorted(selected_rows)):
            self.p0list.removeRow(row)

    def accept(self):
        new_values = {}
        for rowid in range(self.p0list.rowCount()):
            value = []
            for colid in range(self.p0list.columnCount()):
                value.append(self.p0list.item(rowid, colid).text())
            if value != [''] * self.p0list.columnCount():
                new_values[len(new_values)] = value
        self.parent.page.data = new_values
        gui.QDialog.accept(self)


class DummyPanel(gui.QFrame):
    """
    Reimplement this class when a block of fields is needed in the screen
    to show details about the selected key and make it possible to change
    its definition
    """
    def __init__(self, parent):
        gui.QFrame.__init__(self)
        self.parent = parent
        self.initializing = False

    def add_extra_attributes(self):
        """
        Define extra instance attributes if needed
        """
        pass

    def add_extra_fields(self):
        """define other widgets to be used in the panel
        needed for showing details subpanel
        """
        pass

    def layout_extra_fields(self, sizer):
        """add extra widgets to self._sizer
        needed for showing details subpanel
        """
        pass

    def captions_extra_fields(self):
        """refresh captions for extra widgets
        needed for showing details subpanel
        """
        pass

    def vuldetails(self, value):
        """
        copy details of the selected key definition to the subpanel
        """
        pass

    def on_item_selected(self, olditem, newitem):
        """callback for list selection
        needed for copying details to subpanel
        """
        pass

    def aanpassen(self, delete=False):
        """
        copying details to the list after updating the subpanel
        """
        pass

class HotkeyPanel(gui.QFrame):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    definieert feitelijk een "custom widget"
    coldata is een list of tuple van 4-tuples die achtereenvolgens aangeven
    de kolomtitel, de breedte, de index op self.data en of het een soort aangeeft
    verwacht dat de subclass van te voren een attribuut gedefinieerd heeft:
    _keys: de module om de settings te lezen
    """
    def __init__(self, parent, pad):

        self.pad = pad
        # switch om het gedrag van bepaalde routines tijdens initialisatie te beïnvloeden
        self._initializing = True
        self.modified = False

        gui.QFrame.__init__(self, parent)
        self.parent = parent # .parent()
        self.captions = self.parent.parent.captions
        self.settings, self.column_info, self.data = readcsv(self.pad)
        if not self.settings or not self.column_info:
            gui.QLabel('No data for this program', self)
            return
        self.p0list = gui.QTreeWidget(self)
        modulename = "editor." + self.settings["PluginName"][0]
        self._keys = importlib.import_module(modulename)
        try:
            self._panel = self._keys.MyPanel(self)
        except AttributeError:
            self._panel = DummyPanel(self)
        self.title = self.settings["PanelName"][0]

        # gelegenheid voor extra initialisaties en het opbouwen van de rest van de GUI
        # het vullen van veldwaarden hierin gebeurt als gevolg van het vullen
        # van de eerste rij in de listbox, daarom moet deze het laatst
        self._panel.add_extra_attributes()
        self._panel.add_extra_fields()

        self._sizer = gui.QVBoxLayout()
        if self.column_info:
            self.p0list.setSortingEnabled(True)
            self.p0list.setHeaderLabels([self.captions[col[0]] for col in
                self.column_info])
            self.p0list.setAlternatingRowColors(True)
            self.p0list.currentItemChanged.connect(self._panel.on_item_selected)
            self.p0hdr = self.p0list.header()
            self.p0hdr.setClickable(True)
            for indx, col in enumerate(self.column_info):
                self.p0hdr.resizeSection(indx, col[1])
            self.p0hdr.setStretchLastSection(True)
            self.populate_list()
            sizer1 = gui.QHBoxLayout()
            sizer1.addWidget(self.p0list)
            self._sizer.addLayout(sizer1)

        # indien van toepassing (TC versie): toevoegen van de rest van de GUI aan de layout
        self._panel.layout_extra_fields(self._sizer)

        self.setLayout(self._sizer)
        self._initializing = False
        self.filtertext = ''

    def readkeys(self):
        "(re)read the data for the keydef list"
        self.data = readcsv(self.pad)[2]

    def savekeys(self, pad=None):
        "save modified keydef back"
        if not pad:
            pad = self.pad
        self._keys.savekeys(self.settings, self.data)
        writecsv(self.pad, self.settings, self.column_info, self.data)
        self.modified = False
        self.setWindowTitle(self.captions["000"])

    def setcaptions(self):
        title = self.captions["000"]
        if self.modified:
            title += ' ' + self.captions["017"]
        self.setWindowTitle(title)

        self._panel.captions_extra_fields()
        self.populate_list()

    def populate_list(self, pos=0):
        """vullen van de list control
        """
        self.p0list.clear()
        items = self.data.items()
        if items is None or len(items) == 0:
            return

        self._panel.initializing = True
        for key, data in items:
            new_item = gui.QTreeWidgetItem()
            new_item.setData(0, core.Qt.UserRole, key) # data[0])
            for indx, col in enumerate(self.column_info):
                from_indx, is_soort = col[2], col[3]
                value = data[from_indx]
                if is_soort:
                    value = hkc.C_DFLT if value == 'S' else hkc.C_RDEF
                    value = self.captions[value]
                new_item.setText(indx, value)
            self.p0list.addTopLevelItem(new_item)
            self.p0list.setCurrentItem(self.p0list.topLevelItem(pos))
        self._panel.initializing = False

    def exit(self):
        if self.modified:
            ok = show_message(self, '025')
            if ok == gui.QMessageBox.Yes:
                self.page.savekeys()
            elif ok == gui.QMessageBox.Cancel:
                return False
        return True

class EmptyPanel(HotkeyPanel):

    def __init__(self, parent):

        coldata = ()
        self._txt = "default"
        HotkeyPanel.__init__(self, parent, coldata, ini="",
            title="default_title")

    def add_extra_fields(self):
        self.txt = gui.QLabel(self._txt, self)

    def layout_extra_fields(self):
        self._sizer.addWidget(self.txt)

    def readkeys(self):
        self.data = {}

    def savekeys(self):
        pass

class ChoiceBook(gui.QFrame):
    """ Als QTabwidget, maar met selector in plaats van tabs
    """
    def __init__(self, parent, plugins):
        ## gui.QWidget.__init__(self, parent)
        self.plugins = plugins
        self.parent = parent.parent()
        gui.QFrame.__init__(self, parent)
        self.sel = gui.QComboBox(self)
        self.sel.currentIndexChanged.connect(self.on_page_changed)
        self.find = gui.QComboBox(self)
        self.find.setMinimumContentsLength(20)
        self.find.setEditable(True)
        self.find.editTextChanged.connect(self.on_text_changed)
        self.b_next = gui.QPushButton(self.parent.captions["014"])
        self.b_next.clicked.connect(self.find_next)
        self.b_next.setEnabled(False)
        self.b_prev = gui.QPushButton(self.parent.captions["015"])
        self.b_prev.clicked.connect(self.find_prev)
        self.b_prev.setEnabled(False)
        self.b_filter = gui.QPushButton(self.parent.captions["068"])
        self.b_filter.clicked.connect(self.filter)
        self.b_filter.setEnabled(False)
        self.filter_on = False
        self.pnl = gui.QStackedWidget(self)
        for txt, loc in self.plugins:
            win = HotkeyPanel(self, loc)
            if win is None:
                self.pnl.addWidget(EmptyPanel(self.pnl,
                    self.parent.captions["052"].format(txt)))
            else:
                self.pnl.addWidget(win)
            self.sel.addItem(txt)
        box = gui.QVBoxLayout()
        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        hbox.addSpacing(10)
        self.sel_text = gui.QLabel(self.parent.captions["050"], self)
        hbox.addWidget(self.sel_text)
        hbox.addWidget(self.sel)
        hbox.addStretch()
        self.find_text = gui.QLabel(self.parent.captions["051"], self)
        hbox.addWidget(self.find_text)
        hbox.addWidget(self.find)
        hbox.addWidget(self.b_filter)
        hbox.addWidget(self.b_next)
        hbox.addWidget(self.b_prev)
        ## hbox.addStretch()
        hbox.addSpacing(10)
        vbox.addLayout(hbox)
        box.addLayout(vbox)
        hbox = gui.QVBoxLayout()
        hbox.addWidget(self.pnl)
        box.addLayout(hbox)
        self.setLayout(box)

    def setcaptions(self):
        self.b_next.setText(self.parent.captions['014'])
        self.b_prev.setText(self.parent.captions['015'])
        self.sel_text.setText(self.parent.captions['050'])
        self.find_text.setText(self.parent.captions['051'])
        if self.filter_on:
            self.b_filter.setText(self.parent.captions["066"])
        else:
            self.b_filter.setText(self.parent.captions["068"])

    def on_page_changed(self, indx):
        page = self.pnl.currentWidget() ## self.parent().page
        if page is None:
            return
        self.parent.sb.showMessage(self.parent.captions["053"].format(
            self.sel.currentText()))
        if page.modified:
            ok = page.exit()
            if not ok:
                # ook nog de vorige tekst in de combobox selecteren?
                return
        self.pnl.setCurrentIndex(indx)
        self.parent.page = self.pnl.currentWidget()#@$&%$#% we just did this
        if not all((self.parent.page.settings, self.parent.page.column_info,
                self.parent.page.data)):
            return
        self.parent.setup_menu()
        if self.parent.page.filtertext:
            self.find.setEditText(self.parent.page.filtertext)
            self.b_filter.setText(self.parent.captions["066"])
            self.b_filter.setEnabled(True)
        else:
            self.find.setEditText('')
            self.find.setEnabled(True)
            self.b_next.setEnabled(False)
            self.b_prev.setEnabled(False)
            self.b_filter.setEnabled(False)

    def on_text_changed(self, text):
        page = self.parent.page # self.pnl.currentWidget()
        col = page.p0list.columnCount() - 1
        self.items_found = page.p0list.findItems(text, core.Qt.MatchContains, col)
        self.b_next.setEnabled(False)
        self.b_prev.setEnabled(False)
        self.b_filter.setEnabled(False)
        if self.items_found:
            page.p0list.setCurrentItem(self.items_found[0])
            self.founditem = 0
            if len(self.items_found) < len(self.parent.page.data.items()):
                self.b_next.setEnabled(True)
                self.b_filter.setEnabled(True)
            self.parent.sb.showMessage(self.parent.captions["067"].format(
                len(self.items_found)))
        else:
            self.parent.sb.showMessage(self.parent.captions["054"].format(text))

    def find_next(self):
        self.b_prev.setEnabled(True)
        if self.founditem < len(self.items_found) -1:
            self.founditem += 1
            self.parent.page.p0list.setCurrentItem(self.items_found[self.founditem])
        else:
            self.parent.sb.showMessage(self.parent.captions["055"])
            self.b_next.setEnabled(False)

    def find_prev(self):
        self.b_next.setEnabled(True)
        if self.founditem == 0:
            self.parent.sb.showMessage(self.parent.captions["056"])
            self.b_prev.setEnabled(False)
        else:
            self.founditem -= 1
            self.parent.page.p0list.setCurrentItem(self.items_found[self.founditem])

    def filter(self):
        if not self.items_found:
            return
        state = str(self.b_filter.text())
        text = str(self.find.currentText())
        item = self.parent.page.p0list.currentItem()
        self.reposition = item.text(0), item.text(1)
        if state == self.parent.captions['068']: # self.filter_on == False
            state = self.parent.captions['066']
            self.filter_on = True
            self.parent.page.filtertext = text
            self.parent.page.olddata = self.parent.page.data
            ## self.parent.page.olditems = self.items_found
            self.parent.page.data = {ix: item for ix, item in enumerate(
                self.parent.page.data.values()) if text.upper() in item[-1].upper()}
            self.b_next.setEnabled(False)
            self.b_prev.setEnabled(False)
            self.find.setEnabled(False)
        else:       # self.filter_on == True
            state = self.parent.captions['068']
            self.filter_on = False
            self.parent.page.filtertext = ''
            self.parent.page.data = self.parent.page.olddata
            self.b_next.setEnabled(True)
            self.b_prev.setEnabled(True)
            self.find.setEnabled(True)
        self.parent.page.populate_list()
        for ix in range(self.parent.page.p0list.topLevelItemCount()):
            item = self.parent.page.p0list.topLevelItem(ix)
            if (item.text(0), item.text(1)) == self.reposition:
                self.parent.page.p0list.setCurrentItem(item)
                break
        self.b_filter.setText(state)
        if self.parent.page.data == self.parent.page.olddata:
            ## self.items_found = self.parent.page.olditems
            self.on_text_changed(text) # reselect items_found after setting filter to off

class MainFrame(gui.QMainWindow):
    """Hoofdscherm van de applicatie
    """
    def __init__(self, args):

        wid = 860 if hkc.LIN else 688
        hig = 594
        gui.QMainWindow.__init__(self)
        self.title = 'Hotkeys'
        self.setWindowTitle(self.title)
        self.resize(wid, hig)
        self.sb = self.statusBar()

        self.menu_bar = self.menuBar()
        self.ini = {'filename': hkc.CONF, 'plugins': []}

        self.ini['lang'], self.ini['plugins'] = read_settings(self.ini['filename'])

        self.readcaptions(self.ini['lang']) # set up defaults
        self.sb.showMessage('Welcome to {}!'.format(self.captions["000"]))
        pnl = gui.QWidget(self)
        self.book = ChoiceBook(pnl, self.ini['plugins']) # , size= (600, 700))
        sizer_v = gui.QVBoxLayout()
        sizer_h = gui.QHBoxLayout()
        sizer_h.addWidget(self.book)
        sizer_v.addLayout(sizer_h)
        self.b_exit = gui.QPushButton(self.captions[hkc.C_EXIT], pnl)
        self.b_exit.clicked.connect(self.exit)
        sizer_h = gui.QHBoxLayout()
        sizer_h.addStretch()
        sizer_h.addWidget(self.b_exit)
        sizer_h.addStretch()
        sizer_v.addLayout(sizer_h)
        pnl.setLayout(sizer_v)

        self.setCentralWidget(pnl)
        self.page = self.book.pnl.currentWidget()
        self.book.on_page_changed(0)
        self.setcaptions()
        self.show()

    def setup_menu(self):
        self.menu_bar.clear()
        self._menus = (
            (hkc.M_APP, (
                (hkc.M_READ, (m_read, 'Ctrl+R')),
                (hkc.M_RBLD, (m_rebuild, 'Ctrl+B')),
                (hkc.M_SAVE, (m_save, 'Ctrl+S')),
                -1,
                (hkc.M_EXIT, (m_exit, 'Ctrl+Q')),
                )),
            (hkc.M_SETT, (
                (hkc.M_LOC, (m_loc, 'Ctrl+F')),
                (hkc.M_TOOL, ((
                    (hkc.M_COL, (m_col, '')),
                    (hkc.M_MISC, (m_tool, '')),
                    (hkc.M_ENTR, (m_entry, '')),
                    ), '')),
                (hkc.M_LANG, (m_lang, 'Ctrl+L')),
                )),
            (hkc.M_HELP, (
                (hkc.M_ABOUT, (m_about, 'Ctrl+H')),
                )))
        self._menuitems = []
        for title, items in self._menus:
            menu = self.menu_bar.addMenu(self.captions[title])
            menuitem = ((menu, title), [])
            for sel in items:
                if sel == -1:
                    menu.addSeparator()
                    continue
                else:
                    sel, values = sel
                    callback, shortcut = values
                    if callable(callback):
                        act = self.create_menuaction(sel, callback, shortcut)
                        menu.addAction(act)
                        menuitem[1].append((act, sel))
                    else:
                        submenu = menu.addMenu(self.captions[sel])
                        submenuitem = ((submenu, sel), [])
                        for sel, values in callback:
                            callback, shortcut = values
                            act = self.create_menuaction(sel, callback, shortcut)
                            submenu.addAction(act)
                            submenuitem[1].append((act, sel))
                        self._menuitems.append(submenuitem)
            self._menuitems.append(menuitem)

    def create_menuaction(self, sel, callback, shortcut):
        act = gui.QAction(self.captions[sel], self)
        ## act.triggered.connect(functools.partial(self.on_menu, sel))
        act.triggered.connect(functools.partial(callback, self))
        act.setShortcut(shortcut)
        if sel == hkc.M_SAVE: # in (hkc.M_READ, hkc.M_SAVE):
            act.setEnabled(bool(int(self.page.settings['RedefineKeys'][0])))
        elif sel == hkc.M_RBLD:
            act.setEnabled(bool(int(self.page.settings['RebuildCSV'][0])))
        return act

    def exit(self,e=None):
        if not self.page.exit():
            return
        self.close()

    def readcaptions(self, lang):
        self.captions = {}
        with open(os.path.join(hkc.HERELANG, lang)) as f_in:
            for x in f_in:
                if x[0] == '#' or x.strip() == "":
                    continue
                key, value = x.strip().split(None,1)
                self.captions[key] = value
        self.captions['000'] = self.title

    def setcaptions(self):
        title = self.captions["000"]
        if self.page.modified:
            title += ' ' + self.captions["017"]
        self.setWindowTitle(title)
        for menu, items in self._menuitems:
            menu[0].setTitle(self.captions[menu[1]])
            for action in items:
                action[0].setText(self.captions[action[1]])
        self.b_exit.setText(self.captions[hkc.C_EXIT])
        self.book.setcaptions()
        self.page.setcaptions()

def main(args=None):
    app = gui.QApplication(sys.argv)
    frame = MainFrame(args)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv[1:])
