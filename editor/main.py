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
# import sys
import pdb
import string
import importlib
## import shutil

import editor.shared as shared
import editor.gui as gui
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

        self.gui = gui.SingleDataInterface(self.parent.gui, self)

        self.captions = self.parent.parent.captions
        self.filtertext = ''
        self.has_extrapanel = False

        shared.log(self.pad)
        if self.pad == NO_PATH:
            print('init HotkeyPanel with NO_PATH')
            self.gui.setup_empty_screen('No path data for HotKeyPanel', self.parent.parent.title)
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
        self.set_title(modified=False)

    def setcaptions(self):
        """update captions according to selected language
        """
        self.set_title()
        if self.has_extrapanel:
            self.gui.captions_extra_fields()
        # if self.data:
        #     self.populate_list()

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

    def set_title(self, modified=None):
        """set title and adapt to modified flag
        if modified flag is not supplied, use its current state
        """
        if modified is not None:
            self.modified = False
        title = self.parent.parent.title
        if self.modified:
            title += ' ' + self.captions["T_MOD"]
        self.gui.set_title(title)

    def exit(self):
        "ask if we cal leave the page"
        if self.modified:
            ok, noexit = hkd.ask_ync_question(self, 'Q_SAVXIT')
            if ok:
                self.savekeys()
            if noexit:
                return False
        return True


class ChoiceBook:
    """Het schermdeel dat de selector, zoekfunctie en de gegevenstabel toont
    """
    def __init__(self, parent):
        self.parent = parent
        self.page = None

        self.gui = gui.TabbedInterface(self.parent.gui, self)
        self.gui.setup_selector()
        self.gui.setup_search()

        for txt, loc in self.parent.ini['plugins']:
            if loc and not os.path.exists(loc):
                loc = os.path.join(shared.BASE, loc)
            win = HotkeyPanel(self, loc)
            self.gui.add_subscreen(win)
            try:
                fl = win.settings[shared.SettType.PLG.value]
            except KeyError:
                fl = ''  # error is handled elsewhere
            self.parent.pluginfiles[txt] = fl
            self.gui.add_to_selector(txt)

        self.gui.format_screen()

    def on_page_changed(self, indx):
        """callback for change in tool page
        """
        # no use finishing this method if certain conditions aren't met
        if self.parent.book is None:
            print("leaving: no choicebook setup yet - should this be possible?")
            return
        page = self.gui.get_panel()
        if page is None:                     # leaving: no page selected yet
            return
        if page.master.modified:
            ok = page.exit()
            if not ok:                       # leaving: can't exit modified page yet
                return
        self.parent.gui.statusbar_message(self.parent.captions["M_DESC"].format(
            self.gui.get_selected_tool()))
        self.gui.set_selected_panel(indx)
        self.parent.page = self.gui.get_panel().master  # change to new selection
        print('in on_page_changed - going to set up menu')
        self.parent.gui.setup_menu()
        if not all((self.parent.page.settings, self.parent.page.column_info,
                    self.parent.page.data)):  # leaving: page data incomplete (e.g. no keydefs)
            return
        self.parent.page.setcaptions()
        items = [self.parent.captions[x[0]] for x in self.parent.page.column_info]
        self.gui.update_search(items)

    def on_text_changed(self, text):
        """callback for change in search text
        """
        page = self.page  # self.pnl.currentWidget()
        for ix, item in enumerate(page.column_info):
            if page.captions[item[0]] == self.gui.get_search_text():
                self.zoekcol = ix
                break
        self.items_found = self.gui.find_items(page)
        self.gui.init_search_buttons()
        if self.items_found:
            self.gui.set_selected_keydef_item(self, page, 0)
            self.founditem = 0
            if len(self.items_found) < len(self.master.page.data.items()):
                self.gui.enable_search_buttons(next=True, filter=True)
            message = self.parent.captions["I_#FOUND"].format(len(self.items_found))
        else:
            message = self.parent.captions["I_NOTFND"].format(text)
        self.parent.gui.statusbar_message(message)

    def find_next(self, event=None):
        """to next search result
        """
        self.gui.enable_search_buttons(prev=True)
        if self.founditem < len(self.items_found) - 1:
            self.founditem += 1
            self.gui.set_selected_keydef_item(self.parent.page, self.founditem)
        else:
            self.parent.statusbar_message(self.parent.editor.captions["I_NONXT"])
            self.gui.enable_search_buttons(next=False)

    def find_prev(self, event=None):
        """to previous search result
        """
        self.gui.enable_search_buttons(next=True)
        if self.founditem == 0:
            self.parent.statusbar_message(self.parent.editor.captions["I_NOPRV"])
            self.gui.enable_search_buttons(prev=False)
        else:
            self.founditem -= 1
            self.gui.set_selected_keydef_item(self.parent.page, self.founditem)


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
        self.gui = gui.Gui(self)
        if self.ini['plugins'] == []:
            self.gui.show_empty_screen()
        else:
            self.gui.set_window_title(self.title)
            self.gui.statusbar_message(self.captions["T_HELLO"].format(self.captions["T_MAIN"]))
            self.book = ChoiceBook(self)
            self.gui.setup_tabs()
            start = 0
            if 'title' in self.ini and self.ini['title']:
                self.title = self.ini['title']
            if 'initial' in self.ini and self.ini['initial'] != '':
                start = [x for x, y in self.ini['plugins']].index(self.ini['initial'])
            self.book.on_page_changed(start)
            self.book.gui.set_selected(start)
            self.setcaptions()
        self.gui.go()

#     def setup_tabs(self):
#         """add the tabbed window to the inteface
#         """

    def get_menudata(self):
        """provide the application's menu definition to the program
        """
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

    # menu callbacks (event argument is for compatibility between gui toolkits)
    def m_read(self, event=None):
        """(menu) callback voor het lezen van de hotkeys

        vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
        zet de gelezen keys daarna ook in de gui
        """
        if not self.book.page.settings:
            gui.show_message('I_ADDSET')
            return
        if not self.book.page.modified:
            if not gui.ask_question('Q_NOCHG'):
                return
        self.book.page.readkeys()
        self.book.page.populate_list()

    def m_save(self, event=None):
        """(menu) callback voor het terugschrijven van de hotkeys

        vraagt eerst of het ok is om de hotkeys weg te schrijven
        vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
        """
        if not self.book.page.modified:
            if not gui.ask_question('Q_NOCHG'):
                return
        try:
            self.book.page.savekeys()
        except AttributeError:
            gui.show_message('I_DEFSAV')
            return
        gui.show_message('I_RSTRT')

    def m_title(self, event=None):
        """menu callback voor het aanpassen van de schermtitel
        """
        oldtitle = self.title
        newtitle, ok = gui.get_textinput(oldtitle, self.captions["T_TITLE"])
        if ok:
            if newtitle != oldtitle:
                self.title = self.ini['title'] = newtitle
                shared.change_setting('title', oldtitle, newtitle, self.ini['filename'])
                if not newtitle:
                    gui.show_message('I_STITLE')
                    self.title = self.captions["T_MAIN"]
                self.book.page.set_title()

    def m_loc(self, event=None):
        """(menu) callback voor aanpassen van de bestandslocaties

        vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
        toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
        (met name of de opgegeven paden kloppen)
        """
        # self.ini["plugins"] bevat de lijst met tools en csv locaties
        current_programs = [x for x, y in self.ini["plugins"]]
        current_paths = [y for x, y in self.ini["plugins"]]

        self.last_added = None  # wordt in de hierna volgende dialoog ingesteld
        ok = gui.manage_filesettings(self)
        if ok:
            selection = self.book.gui.get_selected_index()
            shared.modify_settings(self.ini)

            # update the screen(s)
            # clear the selector and the stackedwidget while pairing up programs and windows
            # that need to be kept or replaced
            hlpdict = {}
            self.book.gui.clear_selector()

            current_items = reversed([(x, y) for x, y in enumerate(current_programs)])
            new_programs = [x for x, y in self.ini["plugins"]]
            new_paths = [y for x, y in self.ini["plugins"]]
            for indx, program in current_items:  # we need to do this in reverse
                # NB niet alleen de Gui, ook het HotkeyPanel verwijderen
                test = self.book.gui.remove_tool(indx, program, new_programs)
                if test:
                    hlpdict[program] = test
                else:
                    self.pluginfiles.pop(program)

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
                self.book.gui.add_tool(program, win)

            if self.last_added:
                selection = self.book.gui.get_new_selection(self.last_added)
            if selection > len(self.ini['plugins']) - 1:
                selection -= 1
            self.book.gui.set_selected(selection)

    def m_rebuild(self, event=None):
        """rebuild csv data from (updated) settings
        """
        if not self.book.page.settings:
            gui.show_message('I_ADDSET')
            return
        try:
            test = self.book.page.reader.buildcsv
        except AttributeError:
            gui.show_message('I_DEFRBLD')
            return
        try:
            newdata = test(self.book)
        except FileNotFoundError:
            gui.show_message('I_ERRRBLD')
            return
        if newdata[0]:
            self.book.page.data = newdata[0]
            self.book.page.otherstuff = newdata[1]
            shared.writecsv(self.book.page.pad, self.book.page.settings, self.book.page.column_info,
                            self.book.page.data, self.ini['lang'])
            self.book.page.populate_list()
            mld = 'keyboard definitions rebuilt'
        else:
            mld = 'No definition data'
            try:
                test = newdata[1]
            except IndexError:
                mld = 'No extra definition'
            mld = self.captions['I_#FOUND'].format(mld)
        gui.show_message(text=mld)

    def m_tool(self, event=None):
        """define tool-specific settings
        """
        if not self.book.page.settings:
            self.book.page.settings = {x: '' for x in shared.csv_settingnames}
        old_redef = bool(int(self.book.page.settings[shared.SettType.RDEF.value]))
        ok = gui.manage_extrasettings(self)
        if ok:
            shared.writecsv(self.book.page.pad, self.book.page.settings, self.book.page.column_info,
                            self.book.page.data, self.ini['lang'])
            test_redef = bool(int(self.book.page.settings[shared.SettType.RDEF.value]))
            test_dets = bool(int(self.book.page.settings[shared.SettType.DETS.value]))
            test_rbld = bool(int(self.book.page.settings[shared.SettType.RBLD.value]))
            self.gui.modify_menuitem('M_SAVE', test_redef)
            self.gui.modify_menuitem('M_RBLD', test_rbld)
            indx, win = self.book.gui.get_selected_panel()
            if test_dets != self.book.page.has_extrapanel:
                self.book.page.has_extrapanel = test_dets
                newwin = HotkeyPanel(self.book, self.book.plugins[indx][1])
                self.book.gui.replace_panel(indx, win, newwin)
            elif test_redef != old_redef and test_dets:
                self.book.gui.set_panel_editable(test_redef)

    def m_col(self, event=None):
        """define tool-specific settings: column properties
        """
        if not self.book.page.settings:
            gui.show_message('I_ADDSET')
            return
        ok = gui.manage_columnsettings(self)
        if ok:
            new_pagedata = {}
            for key, value in self.book.page.data.items():
                newvalue = []
                for colinf in self.book.page.column_info:
                    test = colinf[-1]
                    if test == 'new':
                        newvalue.append('')
                    else:
                        newvalue.append(value[test])
                new_pagedata[key] = newvalue
            self.book.page.data = new_pagedata
            self.book.page.column_info = [x[:-1] for x in self.book.page.column_info]

            shared.writecsv(self.book.page.pad, self.book.page.settings, self.book.page.column_info,
                            self.book.page.data, self.ini['lang'])
            if not self.book.page.data:
                return
            headers = [self.captions[col[0]] for col in self.book.page.column_info]
            self.book.gui.refresh_locs(headers)
            self.book.page.gui.refresh_headers(headers)
            self.book.page.populate_list()

    def m_entry(self, event=None):
        """manual entry of keyboard shortcuts
        """
        if not all((self.book.page.settings, self.book.page.column_info)):
            gui.show_message('I_ADDCOL')
            return
        ok = gui.manual_entry(self)
        if ok:
            if self.book.page.data:
                shared.writecsv(self.book.page.pad, self.book.page.settings,
                                self.book.page.column_info, self.book.page.data, self.ini['lang'])
                self.book.page.populate_list()

    def m_lang(self, event=None):
        """(menu) callback voor taalkeuze

        past de settings aan en leest het geselecteerde language file
        """
        # bepaal welke language files er beschikbaar zijn
        choices = [x.name for x in shared.HERELANG.iterdir() if x.suffix == ".lng"]
        # bepaal welke er momenteel geactiveerd is
        oldlang = self.ini['lang']
        indx = choices.index(oldlang) if oldlang in choices else 0
        lang, ok = gui.get_choice(self.title, self.captions["P_SELLNG"], choices,
                                       current=indx)
        if ok:
            shared.change_setting('lang', oldlang, lang, self.ini['filename'])
            self.ini['lang'] = lang
            self.readcaptions(lang)
            self.setcaptions()

    def m_about(self, event=None):
        """(menu) callback voor het tonen van de "about" dialoog
        """
        gui.show_message(
            text='\n'.join(self.captions['T_ABOUT'].format(self.captions['T_SHORT'], shared.VRS,
                                                           shared.AUTH,
                                                           self.captions['T_LONG']).split(' / ')))

    def m_pref(self, event=None):
        """mogelijkheid bieden om een tool op te geven dat default getoond wordt
        """
        oldpref = self.ini.get("initial", None)
        oldmode = self.ini.get("startup", None)
        self.prefs = oldmode, oldpref
        ok = gui.manage_startupsettings(self)
        if ok:
            mode, pref = self.prefs
            if mode:
                self.ini['startup'] = mode
                shared.change_setting('startup', oldmode, mode, self.ini['filename'])
            if mode == 'Fixed':
                self.ini['initial'] = pref
                shared.change_setting('initial', oldpref, pref, self.ini['filename'])

    def m_exit(self, event=None):
        """(menu) callback om het programma direct af te sluiten
        """
        self.exit()

    # other methods
    def exit(self, event=None):
        """quit the applicationi - extra actions to perform on closing
        """
        if not self.book.page.exit():
            return
        mode = self.ini.get("startup", '')
        pref = self.ini.get("initial", '')
        # when setting is 'fixed', don't remember a startup tool that is removed from the config
        # TODO: should actually be handled in the files definition dialog
        if mode == shared.mode_f and pref not in [x[0] for x in self.ini['plugins']]:
            oldmode, mode = mode, shared.mode_r
            self.ini['startup'] = mode
            shared.change_setting('startup', oldmode, mode, self.ini['filename'])
        # when setting is 'remember', set the remembered tool to the current one
        if mode == shared.mode_r:
            try:
                oldpref, pref = pref, self.book.gui.get_selected_text()
                shared.change_setting('initial', oldpref, pref, self.ini['filename'])
            except AttributeError:  # selector bestaat niet als er geen tool pages zijn
                pass
        # super().close()
        self.gui.close()

    def readcaptions(self, lang):
        """get captions from language file or settings
        """
        self.captions = shared.readlang(lang)

    # def set_title(self):
    #     """adjust title and modified flag
    #     """
    #     title = self.title
    #     # if self.book.page.modified:
    #     #     title += ' ' + self.captions["T_MOD"]
    #     self.gui.set_window_title(title)

    def setcaptions(self):
        """propagate captions to other parts of the application
        """
        # self.set_title()
        self.gui.setcaptions()
        self.book.gui.setcaptions()
        self.book.page.setcaptions()
