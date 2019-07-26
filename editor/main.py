"""hotkeys.py - PyQt5 version

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
import string
import importlib
## import shutil

import editor.shared as shared
from .gui import Gui, TabbedInterface, SingleDataInterface
# from .gui_qt import DummyPage
NO_PATH = 'NO_PATH'


class HotkeyPanel:
    """scherm met de gegevens voor een bepaald tool

    coldata is een list of tuple van 4-tuples die achtereenvolgens aangeven:
        de kolomtitel, de breedte, de index op self.data en of het een soort aangeeft
    verwacht dat de subclass van te voren een attribuut `reader` (de module om de settings
        te lezen) gedefinieerd heeft
    """
    def __init__(self, parent, pad):
        self.pad = pad
        self.parent = parent
        # switch om het gedrag van bepaalde routines tijdens initialisatie te beïnvloeden
        self.initializing_screen = True
        self.modified = False

        self.gui = SingleDataInterface(self.parent.gui, self)

        self.captions = self.parent.parent.captions
        self.filtertext = ''
        self.has_extrapanel = False

        shared.log(self.pad)
        if self.pad == NO_PATH:
            print('init HotkeyPanel with NO_PATH')
            # self.gui.setup_empty_screen(nodata, self.parent.parent.title)
            return

        nodata = ''
        if self.pad:
            try:
                self.settings, self.column_info, self.data = shared.readcsv(self.pad)
            except ValueError as e:
                shared.logging.exception('')
                nodata = self.captions['I_NOSET'].format(e, self.pad)
            except FileNotFoundError:
                shared.logging.exception('')
                nodata = self.captions['I_NOSETFIL'].format(self.pad)
        else:
            nodata = self.captions['I_NOSETFIL'].format(self.pad)
        if nodata:
            self.settings, self.column_info, self.data = {}, [], {}
        self.otherstuff = {}  # ruimte voor zaken als een lijst met mogelijke commando's

        if not self.settings or not self.column_info:
            tmp = ":\n\n" + nodata if nodata else ""
            nodata = self.captions['I_NODATA'] + tmp
        else:
            try:
                modulename = self.settings[shared.SettType.PLG.value]
            except KeyError:
                shared.logging.exception('')
                nodata = True
            else:
                try:
                    self.reader = importlib.import_module(modulename)
                except ImportError:
                    shared.logging.exception('')
                    nodata = True
            if nodata:
                nodata = self.captions['I_NODATA'].replace('data', 'plugin code')

            self.parent.page = self
            try:
                test = self.reader.buildcsv
            except AttributeError:
                pass
            else:
                try:
                    self.otherstuff = self.reader.buildcsv(parent, showinfo=False)[1]
                except FileNotFoundError:
                    nodata = "Can't build settings for {}".format(modulename)
                # except AttributeError:
                #    print('Got AttributeError for {}'.format(modulename))
                #    raise

        if nodata:
            print('init HotkeyPanel with no data', nodata)
            # self.gui.setup_empty_screen(nodata, self.parent.parent.title)
            return

        try:
            self.has_extrapanel = bool(int(self.settings[shared.SettType.DETS.value]))
        except KeyError:
            pass

        self.title = self.settings["PanelName"]

        # self.has_extrapanel controleert extra initialisaties en het opbouwen van het extra
        # schermdeel - het vullen van veldwaarden hierin gebeurt als gevolg van het vullen
        # van de eerste rij in de listbox, daarom moet deze het laatst
        # self.otherstuff = self.reader.getotherstuff()
        if self.has_extrapanel:
            shared.log('extrapanel: %s', self.has_extrapanel)
            self.fields = [x[0] for x in self.column_info]
            self.add_extra_attributes()
            self.gui.add_extra_fields()

        self.gui.setup_list()
        self.initializing_screen = False

    def readkeys(self):
        "(re)read the data for the keydef list"
        self.data = shared.readcsv(self.pad)[2]

    def savekeys(self):
        """save modified keydef back

        allows saving back to csv without (?) saving to the tool settings
        """
        self.parent.data = self.data
        try:
            self.reader.savekeys(self)
        except AttributeError:
            pass
        shared.writecsv(self.pad, self.settings, self.column_info, self.data,
                     self.parent.parent.ini['lang'])
        self.gui.set_title(modified=False)

    def setcaptions(self):
        """update captions according to selected language
        """
        self.gui.set_title()
        if self.has_extrapanel:
            self.gui.captions_extra_fields()
        if self.data:
            self.populate_list()

    def populate_list(self, pos=0):
        """vullen van de lijst
        """
        self.gui.clear_list()

        items = self.data.items()
        # if not items:  # if items is None or len(items) == 0:
        #     return

        for key, data in items:
            try:
                int(key)
            except ValueError:
                continue
            new_item = self.gui.build_listitem(key)
            for indx, col in enumerate(self.column_info):
                is_soort = col[2]
                value = data[indx]
                if is_soort:
                    value = 'C_DFLT' if value == 'S' else 'C_RDEF'
                    value = self.captions[value]
                self.gui.set_listitemtext(new_item, indx, value)
            self.gui.add_listitem(new_item)
        self.gui.set_listselection(pos)

    def add_extra_attributes(self):
        """pertaining to details for selected keydef, to make editing possible
        """
        self.init_origdata = []
        ix_item = 0
        if 'C_KEY' in self.fields:
            self.init_origdata.append('')
            self.ix_key = ix_item
            ix_item += 1
            self.keylist = [x for x in string.ascii_uppercase] + \
                [x for x in string.digits] + ["F" + str(i) for i in range(1, 13)] + \
                shared.named_keys + \
                ['.', ',', '+', '=', '-', '`', '[', ']', '\\', ';', "'", '/']
        if 'C_MODS' in self.fields:
            self.init_origdata += [False, False, False, False]
            self.ix_mods = []
            for _ in range(4):
                self.ix_mods.append(ix_item)
                ix_item += 1
        if 'C_CNTXT' in self.fields:
            self.init_origdata.append('')
            self.ix_cntxt = ix_item
            ix_item += 1
        if 'C_CMD' in self.fields:
            self.init_origdata.append('')
            self.ix_cmd = ix_item
            ix_item += 1
        self.contextslist = []
        self.contextsactionsdict = {}
        self.commandslist = []
        try:
            self.reader.add_extra_attributes(self)  # user exit
        except AttributeError:
            pass
        if self.keylist:
            self.keylist.sort()


class ChoiceBook:
    """Het schermdeel dat de selector, zoekfunctie en de gegevenstabel toont
    """
    def __init__(self, parent):
        self.parent = parent

        self.gui = TabbedInterface(self.parent.gui, self)
        self.gui.setup_selector()
        self.gui.setup_search()

        for txt, loc in self.parent.ini['plugins']:
            if loc and not os.path.exists(loc):
                loc = os.path.join(shared.BASE, loc)
            win = HotkeyPanel(self, loc)
            self.gui.add_subscreen(win)
            # self.parent.gui.page = DummyPage()
            try:
                fl = win.settings[shared.SettType.PLG.value]
            except KeyError:
                fl = ''  # error is handled elsewhere
            self.parent.pluginfiles[txt] = fl
            self.gui.add_to_selector(txt)

        self.gui.format_screen()


class Editor:
    """Hoofdscherm van de applicatie
    """
    def __init__(self, args):
        ini = args.conf or shared.CONF
        self.ini = shared.read_settings(ini)
        self.readcaptions(self.ini['lang'])  # set up defaults
        self.title = self.captions["T_MAIN"]
        self.pluginfiles = {}
        self.book = None
        self.gui = Gui(self)
        # self.book.setup_gui()
        if self.ini['plugins'] == []:
            # self.book.page = HotkeyPanel(self.book, NO_PATH)
            # self.book.page.setup_gui()
            self.gui.show_empty_screen()
            self.gui.go()
            return

        self.gui.set_window_title(self.title)
        self.gui.statusbar_message(self.captions["T_HELLO"].format(self.captions["T_MAIN"]))

        self.setup_tabs()
        # self.gui.setup_menu()
        self.gui.go()

    def setup_tabs(self):
        start = 0
        if 'title' in self.ini and self.ini['title']:
            self.title = self.ini['title']
        if 'initial' in self.ini and self.ini['initial'] != '':
            start = [x for x, y in self.ini['plugins']].index(self.ini['initial'])
        self.book = ChoiceBook(self)
        self.gui.setup_tabs(start)

    def get_menudata(self):
        return (('M_APP', (('M_SETT', ((('M_TITLE', (self.m_title, '')),
                                        ('M_LOC', (self.m_loc, 'Ctrl+F')),
                                        ('M_LANG', (self.m_lang, 'Ctrl+L')),
                                        ('M_PREF', (self.m_pref, ''))), '')),
                           ('M_EXIT', (self.m_exit, 'Ctrl+Q')), )),
                ('M_TOOL', (('M_SETT', ((('M_COL', (self.m_col, '')),
                                         ('M_MISC', (self.m_tool, '')),
                                         ('M_ENTR', (self.m_entry, '')), ), '')),
                            ('M_READ', (self.m_read, 'Ctrl+R')),
                            ('M_RBLD', (self.m_rebuild, 'Ctrl+B')),
                            ('M_SAVE', (self.m_save, 'Ctrl+S')), )),
                ('M_HELP', (('M_ABOUT', (self.m_about, 'Ctrl+H')), )))

    # menu callbacks
    def m_read(self):
        """(menu) callback voor het lezen van de hotkeys

        vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
        zet de gelezen keys daarna ook in de gui
        """
        if not self.gui.page.settings:
            self.gui.show_message('I_ADDSET')
            return
        if not self.gui.page.modified:
            if not self.gui.ask_question('Q_NOCHG'):
                return
        self.gui.page.readkeys()
        self.gui.page.populate_list()

    def m_save(self):
        """(menu) callback voor het terugschrijven van de hotkeys

        vraagt eerst of het ok is om de hotkeys weg te schrijven
        vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
        """
        if not self.gui.page.modified:
            if not hkd.ask_question(self, 'Q_NOCHG'):
                return
        try:
            self.gui.page.savekeys()
        except AttributeError:
            hkd.show_message(self, 'I_DEFSAV')
            return
        hkd.show_message(self, 'I_RSTRT')

    def m_title(self):
        """menu callback voor het aanpassen van de schermtitel
        """
        oldtitle = self.title
        newtitle, ok = qtw.QInputDialog.getText(self, oldtitle, self.captions["T_TITLE"],
                                                text=oldtitle)
        if ok == qtw.QDialog.Accepted:
            if newtitle != oldtitle:
                self.title = self.ini['title'] = newtitle
                shared.change_setting('title', oldtitle, newtitle, self.ini['filename'])
                if not newtitle:
                    hkd.show_message(self, 'I_STITLE')
                    self.title = self.captions["T_MAIN"]
                self.set_title()

    def m_loc(self):
        """(menu) callback voor aanpassen van de bestandslocaties

        vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
        toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
        (met name of de opgegeven paden kloppen)
        """
        # self.ini["plugins"] bevat de lijst met tools en csv locaties
        current_programs = [x for x, y in self.ini["plugins"]]
        current_paths = [y for x, y in self.ini["plugins"]]
        ok = hkd.FilesDialog(self).exec_()
        if ok == qtw.QDialog.Accepted:
            selection = self.book.sel.currentIndex()
            shared.modify_settings(self.ini)

            # update the screen(s)
            # clear the selector and the stackedwidget while pairing up programs and windows
            # that need to be kept or replaced
            hlpdict = {}
            self.book.sel.clear()
            current_items = reversed([(x, y) for x, y in enumerate(current_programs)])
            new_programs = [x for x, y in self.ini["plugins"]]
            new_paths = [y for x, y in self.ini["plugins"]]
            for indx, program in current_items:  # we need to do this in reverse
                win = self.book.pnl.widget(indx)
                self.book.pnl.removeWidget(win)
                if program in new_programs:
                    hlpdict[program] = win  # keep the widget
                else:
                    win.close()  # lose the widget
            # add new ones, modify existing or leave them alone
            for indx, program in enumerate(new_programs):
                if program in current_programs:
                    # compare the new and the existing path
                    old_loc = current_paths[current_programs.index(program)]
                    new_loc = new_paths[new_programs.index(program)]
                    if new_loc == old_loc:  # unchanged
                        win = hlpdict[program]
                    else:  # take data from different location
                        win = HotkeyPanel(self.book, new_loc)
                else:  # new entry
                    loc = new_paths[indx]
                    if not os.path.exists(loc):
                        loc = os.path.join(shared.BASE, loc)
                    win = HotkeyPanel(self.book, loc)
                self.book.sel.addItem(program)
                self.book.pnl.addWidget(win)
            if self.last_added:
                selection = self.book.sel.findText(self.last_added)
            if selection > len(self.ini['plugins']) - 1:
                selection -= 1
            self.book.sel.setCurrentIndex(selection)

    def m_rebuild(self):
        """rebuild csv data from (updated) settings
        """
        if not self.page.settings:
            hkd.show_message(self, 'I_ADDSET')
            return
        try:
            test = self.page.reader.buildcsv
        except AttributeError:
            hkd.show_message(self, 'I_DEFRBLD')
            return
        try:
            newdata = test(self)
        except FileNotFoundError:
            hkd.show_message(self, 'I_ERRRBLD')
            return
        if newdata[0]:
            self.page.data = newdata[0]
            self.page.otherstuff = newdata[1]
            shared.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                         self.page.data, self.ini['lang'])
            self.page.populate_list()
            mld = 'keyboard definitions rebuilt'
        else:
            mld = 'No definition data'
            try:
                test = newdata[1]
            except IndexError:
                mld = 'No extra definition'
            mld = self.captions['I_#FOUND'].format(mld)
        hkd.show_message(self, text=mld)

    def m_tool(self):
        """define tool-specific settings
        """
        if not self.gui.page.settings:
            self.gui.page.settings = {x: '' for x in shared.csv_settingnames}
        old_redef = bool(int(self.gui.page.settings[shared.SettType.RDEF.value]))
        dlg = hkd.ExtraSettingsDialog(self).exec_()
        if dlg == qtw.QDialog.Accepted:
            shared.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                         self.page.data, self.ini['lang'])
            test_redef = bool(int(self.page.settings[shared.SettType.RDEF.value]))
            test_dets = bool(int(self.page.settings[shared.SettType.DETS.value]))
            test_rbld = bool(int(self.page.settings[shared.SettType.RBLD.value]))
            self.gui.menuitems['M_SAVE'].setEnabled(test_redef)
            self.gui.menuitems['M_RBLD'].setEnabled(test_rbld)
            indx = self.book.sel.currentIndex()
            win = self.book.pnl.widget(indx)
            if test_dets != self.page.has_extrapanel:
                self.page.has_extrapanel = test_dets
                newwin = HotkeyPanel(self.book, self.book.plugins[indx][1])
                self.book.pnl.insertWidget(indx, newwin)
                self.book.pnl.setCurrentIndex(indx)
                self.book.pnl.removeWidget(win)
            elif test_redef != old_redef and test_dets:
                win = self.gui.book.pnl.currentWidget()
                win.set_extrascreen_editable(test_redef)

    def m_col(self):
        """define tool-specific settings: column properties
        """
        if not self.page.settings:
            hkd.show_message(self, 'I_ADDSET')
            return
        dlg = hkd.ColumnSettingsDialog(self).exec_()
        if dlg == qtw.QDialog.Accepted:
            new_pagedata = {}
            for key, value in self.page.data.items():
                newvalue = []
                for colinf in self.page.column_info:
                    test = colinf[-1]
                    if test == 'new':
                        newvalue.append('')
                    else:
                        newvalue.append(value[test])
                new_pagedata[key] = newvalue
            self.page.data = new_pagedata
            self.page.column_info = [x[:-1] for x in self.page.column_info]

            shared.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                         self.page.data, self.ini['lang'])
            if not self.page.data:
                return
            headers = [self.captions[col[0]] for col in self.page.column_info]
            self.page.gui.p0list.setHeaderLabels(headers)
            self.book.find_loc.clear()
            self.book.find_loc.addItems(headers)
            hdr = self.page.gui.p0list.header()
            hdr.setSectionsClickable(True)
            for indx, col in enumerate(self.page.column_info):
                hdr.resizeSection(indx, col[1])
            hdr.setStretchLastSection(True)
            self.page.populate_list()

    def m_entry(self):
        """manual entry of keyboard shortcuts
        """
        if not all((self.page.settings, self.page.column_info)):
            hkd.show_message(self, 'I_ADDCOL')
            return
        dlg = hkd.EntryDialog(self).exec_()
        if dlg == qtw.QDialog.Accepted:
            if self.page.data:
                shared.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                             self.page.data, self.ini['lang'])
                self.page.populate_list()

    def m_lang(self):
        """(menu) callback voor taalkeuze

        past de settings aan en leest het geselecteerde language file
        """
        # bepaal welke language files er beschikbaar zijn
        choices = [x.name for x in shared.HERELANG.iterdir() if x.suffix == ".lng"]
        # bepaal welke er momenteel geactiveerd is
        oldlang = self.ini['lang']
        indx = choices.index(oldlang) if oldlang in choices else 0
        lang, ok = qtw.QInputDialog.getItem(self, self.title, self.captions["P_SELLNG"],
                                            choices, current=indx, editable=False)
        if ok:
            shared.change_setting('lang', oldlang, lang, self.ini['filename'])
            self.ini['lang'] = lang
            self.readcaptions(lang)
            self.setcaptions()

    def m_about(self):
        """(menu) callback voor het tonen van de "about" dialoog
        """
        hkd.show_message(self, text='\n'.join(self.captions['T_ABOUT'].format(
            self.captions['T_SHORT'], shared.VRS, shared.AUTH,
            self.captions['T_LONG']).split(' / ')))

    def m_pref(self):
        """mogelijkheid bieden om een tool op te geven dat default getoond wordt
        """
        oldpref = self.ini.get("initial", None)
        oldmode = self.ini.get("startup", None)
        self.prefs = oldmode, oldpref
        ok = hkd.InitialToolDialog(self).exec_()
        if ok == qtw.QDialog.Accepted:
            mode, pref = self.prefs
            if mode:
                self.ini['startup'] = mode
                shared.change_setting('startup', oldmode, mode, self.ini['filename'])
            if mode == 'Fixed':
                self.ini['initial'] = pref
                shared.change_setting('initial', oldpref, pref, self.ini['filename'])

    def m_exit(self):
        """(menu) callback om het programma direct af te sluiten
        """
        self.exit()

    # other methods
    def exit(self):  # , e=None):
        """quit the application
        """
        if not self.book.page.gui.exit():
            return
        self.close()

    def close(self):
        """extra actions to perform on closing
        """
        # TODO bevat nog gui_specifieke zaken
        mode = self.ini.get("startup", '')
        pref = self.ini.get("initial", '')
        # when setting is 'fixed', don't remember a startup tool that is removed from the config
        # TODO: should actually be handled in the files definition dialog
        if mode == shared.mode_f and pref not in [x[0] for x in self.ini['plugins']]:
            oldmode, mode = mode, shared.mode_r
            print(oldmode, mode)
            self.ini['startup'] = mode
            shared.change_setting('startup', oldmode, mode, self.ini['filename'])
        # when setting is 'remember', set the remembered tool to the current one
        if mode == shared.mode_r:
            try:
                oldpref, pref = pref, self.gui.book.sel.currentText()
                shared.change_setting('initial', oldpref, pref, self.ini['filename'])
            except AttributeError:  # sel bestaat niet als er geen tool pages zijn
                pass
        # super().close()
        self.gui.close()

    def readcaptions(self, lang):
        """get captions from language file or settings
        """
        self.captions = shared.readlang(lang)

    def set_title(self):
        """adjust title and modified flag
        """
        title = self.title
        # if self.gui.page.modified:
        #     title += ' ' + self.captions["T_MOD"]
        self.gui.set_window_title(title)

    def setcaptions(self):
        """propagate captions to other parts of the application
        """
        self.set_title()
        # for menu, item in self.gui.menuitems.items():
        #     try:
        #         item.setTitle(self.captions[menu])
        #     except AttributeError:
        #         item.setText(self.captions[menu])
        # self.gui.book.setcaptions()
        # self.gui.page.setcaptions()
