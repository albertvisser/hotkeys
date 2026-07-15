"""Total  Commander plugin for HotKeys - main code
"""
import contextlib
import csv
import editor.gui as gui
from editor.plugins.mergetool_gui import MergeDialogGui


def load_matchdata(matchfile):
    "load matches from intermediate file"
    try:
        _in = open(matchfile)
    except FileNotFoundError:
        data = []
    else:
        with _in:
            rdr = csv.reader(_in)
            data = [row for row in rdr]
    return data


def save_matchdata(lines, matchfile):
    "save matches in intermediate file"
    with open(matchfile, "w") as _out:
        writer = csv.writer(_out)
        for keytext, cmdtext in lines:
            writer.writerow((*keytext.split(' ', 1), cmdtext))


class Merger:
    """Dialoog om een gedocumenteerde toetscombinatie te koppelen aan een commando
    Deze klasse bevat de business logica en is "gui toolkit agnostic"
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.gui = MergeDialogGui(self, master)
        self.build_screen()
        self.create_shortcuts()
        self.load_files()
        self.keysearch = ['', 1, []]
        self.cmdsearch = ['', 1, []]
        self.keyresults, self.cmdresults = [], []

    def build_screen(self):
        """create the screen elements
        """
        screen = self.gui.init_display()
        row = self.gui.add_row(screen)

        col = self.gui.add_col_to_row(row)
        self.listkeys = self.gui.create_list(columns=['Key', 'Description'],
                                             callback=self.select_match_fromkeys)
        self.gui.add_row_to_col(col, self.listkeys, left_align=True)
        self.findkeybutton = self.gui.create_findbutton( columns=('key', 'text'))
        self.findkeytext = self.gui.create_text()
        self.nextkey = self.gui.create_button('&Next', self.findnextkey, size=50)
        self.prevkey = self.gui.create_button('&Prev', self.findprevkey, size=50)
        self.gui.add_row_to_col(col, self.findkeybutton, self.findkeytext, self.nextkey,
                                self.prevkey, left_align=True)

        col = self.gui.add_col_to_row(row)
        self.listcmds = self.gui.create_list(columns=['Command', 'Description'],
                                             callback=self.select_match_from_cmds)
        self.gui.add_row_to_col(col, self.listcmds, center=True)
        self.findcmdbutton = self.gui.create_findbutton( columns=('cmd', 'text'))
        self.findcmdtext = self.gui.create_text()
        self.nextcmd = self.gui.create_button('Ne&Xt', self.findnextcmd, size=50)
        self.prevcmd = self.gui.create_button('Pre&V', self.findprevcmd, size=50)
        self.gui.add_row_to_col(col, self.findcmdbutton, self.findcmdtext, self.nextcmd,
                                self.prevcmd, left_align=True)

        col = self.gui.add_col_to_row(row)
        self.listmatches = self.gui.create_list(columns=['Key', 'Command'],
                                                callback=self.select_listitems_from_matches)
        self.gui.add_row_to_col(col, self.listmatches, right_align=True)
        self.btn_match = self.gui.create_button("&+ Add/Replace match", self.make_match)
        self.btn_delete = self.gui.create_button("&- Discard match", self.delete_match)
        self.gui.add_row_to_col(col, self.btn_match, self.btn_delete, center=True)

        self.btn_load = self.gui.create_button("&Load matches", self.load_matches)
        self.btn_clear = self.gui.create_button("&Clear All", self.reset_all)
        self.btn_save = self.gui.create_button("&Save matches", self.save_matches)
        self.btn_quit = self.gui.create_button("&Afsluiten", self.close)
        self.btn_build = self.gui.create_button("&Build CSV", self.confirm)
        self.gui.add_row_to_col(screen, self.btn_load, self.btn_clear, self.btn_save,
                                self.btn_build, self.btn_quit, center=True)

        self.gui.finalize_display(screen)

    def create_shortcuts(self):
        "provide data for dialog command shortcuts"
        shortcuts = (
                ('keylist', self.focus_keylist, 'Ctrl+1', 'Focus list of keyboard shortcuts'),
                ('cmdlist', self.focus_cmdlist, 'Ctrl+2', 'Focus list of commands'),
                ('matchlist', self.focus_matchlist, 'Ctrl+3', 'Focus list of connections'),
                ('findkey', self.focus_findkey, 'Ctrl+F', 'Enter search phrase for shortcut'),
                ('nextkey', self.findnextkey, 'Ctrl+N', 'Forward in shortcut search results'),
                ('prevkey', self.findprevkey, 'Ctrl+P', 'Back in shortcut search results'),
                ('findcmd', self.focus_findcmd, 'Ctrl+Shift+F', 'Enter search phrase for command'),
                ('nextcmd', self.findnextcmd, 'Ctrl+Shift+N', 'Forward in command search results'),
                ('prevcmd', self.findprevcmd, 'Ctrl+Shift+P', 'Back in command search results'),
                ('match', self.make_match, 'Ctrl+M', 'Connect command to shortcut'),
                ('delmatch', self.delete_match, 'Ctrl+Shift+M', 'Disconnect command from shortcut'),
                ('load', self.load_matches, 'Ctrl+L', 'Load previously made connections'),
                ('update', self.save_matches, 'Ctrl+U', 'Save all command-shortcut connections'),
                ('clear', self.reset_all, 'Ctrl+Del', 'Discard all command-shortcut connections'),
                ('save', self.confirm, 'Ctrl+S', 'Save connections to settings and leave dialog'),
                ('quit', self.close, 'Ctrl+Q', 'Leave dialog without saving'),
                ('help', self.help, 'F1', 'This help'))
        for item in shortcuts:
            self.gui.create_hotkey(*item)
        return shortcuts

    def load_files(self):
        """load definitions from the various input files"""
        self.load_keys()
        self.load_commands()
        self.reset_all()  # self.clear_listmatches()

    def load_keys(self):
        """load keyboard definitions"""
        self.keydict = {x: y for x, y in sorted(self.parent.keylist_data.items())}
        self.gui.clear_list(self.listkeys)
        self.keydata, self.keytexts = [], []
        for key, value in sorted(self.keydict.items()):
            keytext = ' '.join(key)
            self.gui.add_listitem(self.listkeys, keytext, value['oms'])
            self.keydata.append(keytext)
            self.keytexts.append(value['oms'])

    def load_commands(self):
        """load command definitions"""
        self.cmddict = {x: y for x, y in sorted(self.parent.cmdlist_data.items())}
        self.gui.clear_list(self.listcmds)
        self.cmddata, self.cmdtexts = [], []
        for key, value in sorted(self.cmddict.items()):
            self.gui.add_listitem(self.listcmds, key, value['oms'])
            self.cmddata.append(key)
            self.cmdtexts.append(value['oms'])

    def load_matches(self, event=None):
        "load keydefs from temp file"
        self.reset_all()
        if not self.parent.matchlist_data:
            gui.show_message(self.gui, text="No saved data found")
            return
        for key, mods, command in sorted(self.parent.matchlist_data):
            keytext = f'{key} {mods}'
            self.gui.add_listitem(self.listmatches, keytext, command)
            itemindex = self.gui.find_in_listbox(self.listkeys, keytext)
            if itemindex is not None:  # != -1:
                self.gui.set_listitem_icon(self.listkeys, itemindex)

    def reset_all(self, event=None):
        """remove all associations
        """
        self.gui.clear_list(self.listmatches)
        for ix in range(self.gui.get_listbox_count(self.listkeys)):
            self.gui.reset_listitem_icon(self.listkeys, ix)

    def make_match(self, event=None):
        """connect the choices and register connection in keycombo listbox
        """
        keychoice, keytext, keyoms = self.gui.get_selected_listbox_data(self.listkeys)
        cmdchoice, cmdtext = self.gui.get_selected_listbox_data(self.listcmds)[:-1]
        itemindex = self.gui.find_in_listbox(self.listmatches, keytext)
        if itemindex is not None:  # != -1:
            self.gui.replace_listbox_item(self.listmatches, itemindex, cmdtext)
        else:
            itemindex = self.gui.add_listitem(self.listmatches, keytext, cmdtext)
            # keychoice = self.gui.find_in_listbox(self.listkeys, keytext)
        self.gui.ensure_listitem_visible(self.listmatches, itemindex)
        self.gui.set_listitem_icon(self.listkeys, keychoice)

    def delete_match(self, event=None):
        """remove an association
        """
        itemindex = self.gui.get_selected_listbox_data(self.listmatches)[0]
        if itemindex is None:
            gui.show_message(self.gui, text="choose an item to delete")
            return
        ok = gui.ask_question(self.gui, text="Really delete?")
        if ok:
            keytext = self.gui.get_item_text(self.listmatches, itemindex, 0)
            self.gui.remove_listbox_item(self.listmatches, itemindex)
            itemindex = self.gui.find_in_listbox(self.listkeys, keytext)
            if itemindex:
                self.gui.reset_listitem_icon(self.listkeys, itemindex)

    def save_matches(self, event=None, tofile=True):
        """save the changes to a temp file
        """
        num_items = self.gui.get_listbox_count(self.listmatches)
        if num_items == 0:
            gui.show_message(self.gui, text='No data to save')
            return
        # matches = [self.gui.get_selected_listbox_data(self.listmatches)[1:]
        matches = [(self.gui.get_item_text(self.listmatches, ix, 0),
                    self.gui.get_item_text(self.listmatches, ix, 1)) for ix in range(num_items)]
        if tofile:
            save_matchdata(matches, self.parent.matchfile)
            gui.show_message(self.gui, text='Data saved')
        else:
            self.parent.tempdata = matches

    def focus_keylist(self, event=None):
        "shift focus for selecting a keycombo item"
        self.gui.set_focus_to(self.listkeys)

    def focus_cmdlist(self, event=None):
        "shift focus for selecting a command item"
        self.gui.set_focus_to(self.listcmds)

    def focus_matchlist(self, event=None):
        "shift focus for selecting a mapping item"
        self.gui.set_focus_to(self.listmatches)

    def focus_findkey(self, event=None):
        "Enter search phrase"
        self.gui.set_focus_to(self.findkeytext)

    def focus_findcmd(self, event=None):
        "Enter search phrase"
        self.gui.set_focus_to(self.findcmdtext)

    def findnextkey(self, event=None):
        "find next matching key item"
        test = self.findnextitem(self.findkeybutton, self.findkeytext, self.keysearch,
                                 self.listkeys, self.keyresults)
        if test:
            self.keysearch, self.keyresults = test

    def findprevkey(self, event=None):
        "find previous matching key item"
        test = self.findprevitem(self.findkeybutton, self.findkeytext, self.keysearch,
                                 self.listkeys, self.keyresults)
        if test:
            self.keysearch, self.keyresults = test

    def findnextcmd(self, event=None):
        "find next matching command item"
        test = self.findnextitem(self.findcmdbutton, self.findcmdtext, self.cmdsearch,
                                 self.listcmds, self.cmdresults)
        if test:
            self.cmdsearch, self.cmdresults = test

    def findprevcmd(self, event=None):
        "find previous matching command item"
        test = self.findprevitem(self.findcmdbutton, self.findcmdtext, self.cmdsearch,
                                 self.listcmds, self.cmdresults)
        if test:
            self.cmdsearch, self.cmdresults = test

    def findnextitem(self, searchbutton, searchfield, search, itemlist, results):  # done
        "search forward"
        search = self.finditem(searchbutton, searchfield, search, itemlist, results)
        if not search:
            return None
        newsearch, search, results = search
        current = self.gui.get_selected_item(itemlist)
        if current == -1 or current is None:
            current = self.gui.get_first_item(itemlist)
        if newsearch:
            # positioneren na huidige en klaar
            for item in results:
                if self.gui.get_item_text(itemlist, item, 0) > self.gui.get_item_text(itemlist,
                                                                                      current, 0):
                    self.gui.set_selected_item(itemlist, item)
                    return search, results
        else:
            # huidige zoeken in resultatenlijst, positioneren op volgende
            newix = results.index(current) + 1
            if newix >= len(results):  # was <
                newix = 0
            self.gui.set_selected_item(itemlist, results[newix])
            return None
        gui.show_message(self.gui, text='No (next) item found')
        return None

    def findprevitem(self, searchbutton, searchfield, search, itemlist, results):  # done
        "search backward"
        search = self.finditem(searchbutton, searchfield, search, itemlist, results)
        if not search:
            return None
        newsearch, search, results = search
        current = self.gui.get_selected_item(itemlist)
        if current == -1 or current is None:
            current = self.gui.get_last_item(itemlist)
        if newsearch:
            # positioneren vóór huidige en klaar
            for item in reversed(results):
                if self.gui.get_item_text(itemlist, item, 0) < self.gui.get_item_text(itemlist,
                                                                                      current, 0):
                    self.gui.set_selected_item(itemlist, item)
                    return search, results
        else:
            # huidige zoeken in resultatenlijst, positioneren op vorige
            newix = results.index(current) - 1
            if newix < 0:  # >= 0:  # moet dit niet < zijn?
                newix = -1
            self.gui.set_selected_item(itemlist, results[newix])
            return None
        gui.show_message(self.gui, text='No previous item found')
        return None

    def finditem(self, searchbutton, searchfield, search, itemlist, results):
        "check if search string has changed"
        to_find = self.gui.get_entry_text(searchfield)
        if not to_find:
            gui.show_message(self.gui, text='Please enter text to search for')
            return None
        find_what = self.gui.get_search_choice(searchbutton)  # number of column to search in
        newsearch = to_find != search[0]
        if not newsearch:
            newsearch = find_what != search[1]
        if newsearch:
            search = (to_find, find_what)
            results = self.gui.find_listitems(itemlist, to_find, find_what)
        return newsearch, search, results

    def select_match_fromkeys(self, event=None):
        "positioneer in matches lijst n.a.v. positioneren in keys lijst"
        if self.gui.get_listbox_count(self.listmatches) == 0:
            return
        associated_matchitem = self.find_related((self.listkeys, 0), (self.listmatches, 0))
        if associated_matchitem:
            self.gui.set_selected_item(self.listmatches, associated_matchitem)

    def select_match_from_cmds(self, event=None):
        "positioneer in matches lijst n.a.v. positioneren in commands lijst"
        if self.gui.get_listbox_count(self.listmatches) == 0:
            return
        associated_matchitem = self.find_related((self.listcmds, 0), (self.listmatches, 1))
        if associated_matchitem:
            self.gui.set_selected_item(self.listmatches, associated_matchitem)

    def select_listitems_from_matches(self, event=None):
        "positioneer in lijsten n.a.v. positioneren in matches lijst"
        if self.gui.get_listbox_count(self.listmatches) == 0:
            return
        associated_keyitem = self.find_related((self.listmatches, 0), (self.listkeys, 0))
        if associated_keyitem:
            self.gui.set_selected_item(self.listkeys, associated_keyitem)
        associated_commanditem = self.find_related((self.listmatches, 1), (self.listcmds, 0))
        if associated_commanditem:
            self.gui.set_selected_item(self.listcmds, associated_commanditem)

    def find_related(self, fromstuff, to_stuff):
        """zoek waarde in een kolom in een lijst op in een kolom in een andere lijst
        """
        fromlist, fromcol = fromstuff
        to_list, to_col = to_stuff
        test = self.gui.get_selected_item(fromlist)
        if test is None or test == -1:
            result = None
        else:
            findstr = self.gui.get_item_text(fromlist, test, fromcol)
            result = self.gui.find_listitems(to_list, findstr, to_col)
        return result[0] if result else None

    def confirm(self, event=None):
        """confirm the changes

        don't save to file; just assign to a global variable
        """
        self.save_matches(tofile=False)
        self.gui.accept()

    def close(self, event=None):
        "close without saving (cancel dialog)"
        self.gui.reject()

    def help(self, event=None):
        """help on shortcuts"""
        text = '\n'.join([f'{x[2]:30}{x[3]}' for x in self.create_shortcuts()])
        gui.show_message(self.gui, text=text)
