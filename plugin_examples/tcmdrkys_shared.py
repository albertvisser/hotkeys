"""Total  Commander plugin for HotKeys - shared code
"""
import os
import csv
import collections
import editor.gui


def read_lines(fn):
    "return lines read from file"
    result = []
    try:
        with open(fn) as f_in:
            result = f_in.readlines()
    except UnicodeDecodeError:
        with open(fn, encoding='latin-1') as f_in:
            result = f_in.readlines()
    return result


def keymods(x):
    """hulp bij omzetten keyboard.txt definitie in standaard definitie
    """
    extra = ""
    if x[-1] == "+":
        x = x[:-1]
        extra = "+"
    mods = ""
    h = x.split("+", 1)
    while len(h) > 1:
        # if h[0] in ('SHIFT','ALT','CTRL'):
        if h[0] in ('CTRL', 'ALT', 'SHIFT'):
            mods += h[0][0]
        h = h[1].split("+", 1)
    keyc = h[0].replace(" ", "").capitalize() + extra
    if keyc == '\\':
        keyc = 'OEM_US\\|'
    # keyc = ' + '.join((keyc,mods))
    mods = mods.replace('SC', 'CS')
    return keyc, mods


def defaultcommands(root):
    """mapping uit totalcmd.inc omzetten in een Python dict
    """
    cmdict = {'': {"oms": "no command available"}}
    for x in read_lines(root):
        h = x.strip()
        if h == '' or h[0] == '[' or h[0] == ';':
            continue
        cm_naam, rest = h.split('=', 1)
        cm_num, cm_oms = rest.split(';', 1)
        cmdictitem = {"oms": cm_oms}
        if int(cm_num) > 0:
            cmdictitem["number"] = cm_num
        if " <" in cm_naam:
            cm_naam, argsitem = cm_naam.split(' <')
            cmdictitem['args'] = argsitem.split('>')[0]
        cmdict[cm_naam] = cmdictitem
    return cmdict


def defaultkeys(root):
    """keydefs lezen uit keyboard.txt - mapping maken van deze op ...
    vooralsnog alleen omschrijving
    """
    data = {}
    ky = []
    ky_desc = ''
    join_keys = False
    temp = read_lines(root)
    for x in temp[6:]:
        x = x.rstrip()
        if x == "":
            break
        # if len(x) < 24:
            # continue
        deel1 = x[:23].strip()
        deel2 = x[23:].strip()
        if deel1 == '':
            ky_desc += " " + deel2
        elif join_keys:
            join_keys = False
            ky_desc += " " + deel2
            ky[1] = deel1
        else:
            if ky:
                for k in ky:
                    h = k.rsplit('+', 1)
                    if '/' in h[-1] and not h[-1].endswith('/'):
                        hlp = h[-1].split('/')
                        for it in hlp:
                            data[keymods('+'.join((h[0], it)))] = {"oms": ky_desc}
                    else:
                        data[keymods(k)] = {"oms": ky_desc}
            ky_desc = deel2
            if " or " in deel1:
                ky = deel1.split(" or ")
                s2 = "+".join(ky[0].split("+")[:-1])
                if s2 != "":
                    for y in enumerate(ky[1:]):
                        ky[y[0] + 1] = "+".join((s2, y[1]))
            elif deel1.endswith(" or"):
                ky = [deel1[:-3], ""]
                join_keys = True
            else:
                ky = [deel1]
    if ky:
        for k in ky:
            h = k.rsplit('+', 1)
            if '/' in h[-1] and not h[-1].endswith('/'):
                hlp = h[-1].split('/')
                for it in hlp:
                    data[keymods('+'.join((h[0], it)))] = {"oms": ky_desc}
            else:
                data[keymods(k)] = {"oms": ky_desc}
    return data


def usercommands(root):
    """definities uit usercmd.ini omzetten in een Python dict compatible met die
    voor de standaard commando's
    """
    ucmdict = collections.defaultdict(dict)
    em_name = ""  # , em_value = {}
    for x in read_lines(root):
        if x.startswith("["):
            # if em_name:
            #     ucmdict[em_name] = em_value
            em_name = x[1:].split("]")[0]  # x[1:-1] had ook gekund maar dit is safer
            # em_value = {}
        elif x.startswith("cmd"):
            # em_value["cmd"] = x.strip().split("=")[1]
            ucmdict[em_name]["cmd"] = x.strip().split("=")[1]
        elif x.startswith("menu"):
            # em_value["oms"] = x.strip().split("=")[1]
            ucmdict[em_name]["oms"] = x.strip().split("=")[1]
        elif x.startswith("param"):
            # em_value["args"] = x.strip().split("=")[1]
            ucmdict[em_name]["args"] = x.strip().split("=")[1]
    # ucmdict[em_name] = em_value
    return ucmdict


def userkeys(root):
    """user key definities uit wincmd.ini lezen - mapping maken van deze op...
    vooralsnog alleen commandonaam
    """
    data = {}
    in_user = in_win = False
    for line in read_lines(root):
        line = line.rstrip()
        ## linesplit = line.split("=")
        ## for symbol in ('+', '-', '/', '*'):
            ## if linesplit[0].endswith(symbol):
                ## linesplit[0] = linesplit[0][:-1] + 'NUM' + linesplit[0][-1]
        if line.startswith("["):
            in_user = in_win = False
            if line.startswith("[Shortcuts]"):
                in_user = True
            elif line.startswith("[ShortcutsWin]"):
                in_win = True
        elif in_user or in_win:
            key, cmd = line.split('=')
            try:
                mods, key = key.split('+')
            except ValueError:
                mods = ''
            if in_win:
                mods += 'W'
            data[(key, mods)] = {'cm_name': cmd}
        ## elif in_win:
            ## key, cmd = line.split('=')
                ## if not '+' in key:
                    ## key = '+' + key
                ## key = 'W' + key
                ## data[key] = {'cm_name': cmd}
    return data


def translate_keyname(inp):
    """helper function to convert text from settings into text for this app
    """
    convert = {'Pgup': 'PgUp', 'Pgdn': 'PgDn', 'Period': '.', 'Comma': ',',
               'Plus': '+', 'Minus': '-', 'Backtick/Tilde': '`',
               'Brackets open': '[', 'Brackets close': ']', 'Backslash/Pipe': '\\',
               'Semicolon/colon': ';', 'Apostrophe/Quote': "'",
               'Slash/Questionmark': '/', 'OEM_US\|': '\\'}
    if inp in convert:
        out = convert[inp]
    else:
        out = inp
    return out


class TcMergeMixin:
    """Dialoog om een gedocumenteerde toetscombinatie te koppelen aan een commando
    Mixin class die de gezamenlijke code bevat
    """
    def __init__(self, parent):
        self.parent = parent
        self.master = parent
        self.matchespad = os.path.join(os.path.dirname(__file__), 'tc_default_hotkeys_mapped.csv')
        self.keysearch = ['', 1]
        self.cmdsearch = ['', 1]
        self.keyresults, self.cmdresults = [], []
        self.set_match_from_key = self.set_key_from_match = False
        self.set_match_from_command = self.set_command_from_match = False

    def getshortcuts(self):
        "provide data for dialog command shortcuts"
        return (('keylist', self.focus_keylist, 'Ctrl+1', 'Focus list of keyboard shortcuts'),
                ('cmdlist', self.focus_cmdlist, 'Ctrl+2', 'Focus list of commands'),
                ('matchlist', self.focus_matchlist, 'Ctrl+3', 'Focus list of connections'),
                ('findkey', self.focus_findkey, 'Ctrl+F', 'Enter search phrase for shortcut'),
                ('nextkey', self.findnextkey, 'Ctrl+N', 'Forward in shortcut search results'),
                ('prevkey', self.findprevkey, 'Ctrl+P', 'Back in shortcut search results'),
                ('findcmd', self.focus_findcmd, 'Ctrl+Shift+F', 'Enter search phrase for command'),
                ('nextcmd', self.findnextcmd, 'Ctrl+Shift+N', 'Forward in command search results'),
                ('prevcmd', self.findprevcmd, 'Ctrl+Shift+P', 'Back in command search results'),
                ('addmatch', self.make_match, 'Ctrl+C', 'Connect command to shortcut'),
                ('remmatch', self.delete_match, 'Ctrl+D', 'Disconnect command from shortcut'),
                ('load', self.load_matches, 'Ctrl+L', 'Load previously made connections'),
                ('update', self.save_matches, 'Ctrl+U', 'Save all command-shortcut connections'),
                ('clear', self.reset_all, 'Ctrl+Del', 'Discard all command-shortcut connections'),
                ('save', self.confirm, 'Ctrl+S', 'Save connections to settings and leave dialog'),
                ('quit', self.close, 'Ctrl+Q', 'Leave dialog without saving'),
                ('help', self.help, 'F1', 'This help'))

    def load_files(self):
        """load definitions from the various input files"""
        self.load_keys(self.parent.settings['KB_PAD'])
        self.load_commands(self.parent.settings['CI_PAD'])

        ## # user commands (should be added to right list box?)
        ## self.usrdict, self.uomsdict = usercommands(self.parent.settings['UC_PAD'])

        ## # user defined keys (should be added to left list box?)
        ## self.usrkeys = dict(userkeys(self.parent.settings['TC_PAD']))
        self.clear_listmatches()

    def load_keys(self, keyspad):
        """load keyboard definitions"""
        self.keydict = defaultkeys(keyspad)
        self.clear_listkeys()
        self.keydata, self.keytexts = [], []
        for key, value in sorted(self.keydict.items()):
            keytext = ' '.join(key)
            self.add_listkeys_item(keytext, value)
            self.keydata.append(keytext)
            self.keytexts.append(value['oms'])

    def load_commands(self, cmdspad):
        """load command definitions"""
        self.cmddict = defaultcommands(cmdspad)
        self.clear_listcmds()
        self.cmddata, self.cmdtexts = [], []
        for key, value in sorted(self.cmddict.items()):
            self.add_listcmds_item(key, value)
            self.cmddata.append(key)
            self.cmdtexts.append(value['oms'])

    def load_matches(self, event=None):
        "load keydefs from temp file"
        self.reset_all()
        try:
            _in = open(self.matchespad, 'r')
        except FileNotFoundError:
            editor.gui.show_message(self, text="No saved data found")
            return

        with _in:
            rdr = csv.reader(_in)
            lines = [row for row in rdr]
        for key, mods, command in sorted(lines):
            keytext = ' '.join((key, mods))
            ix = self.add_listmatches_item(keytext, command)
            itemindex = self.find_in_listkeys(keytext)
            if itemindex is not None:  # != -1:
                self.set_listitem_icon(itemindex)

    def reset_all(self, event=None):
        """remove all associations
        """
        self.clear_listmatches()

    def make_match(self, event=None):
        """connect the choices
        """
        keychoice, keytext, keyoms = self.get_selected_key_data()
        cmdchoice, cmdtext = self.get_selected_cmd_data()
        itemindex = self.find_in_listmatches(keytext)
        if itemindex != -1:
            self.replace_matchlist_item(itemindex, cmdtext)
        else:
            itemindex = self.add_listmatches_item(keytext, cmdtext)
            keychoice = self.find_in_listkeys(keytext)
        self.ensure_item_visible(itemindex)
        self.set_listitem_icon(keychoice)

    def delete_match(self, event=None):
        """remove an association
        """
        itemindex = self.get_selected_matchitem()
        if not itemindex:
            editor.gui.show_message(self, text="choose an item to delete")
            return
        ok = editor.gui.ask_question(self, text="Really delete?")
        if ok:
            keytext = self.get_item_text(self.listmatches, itemindex, 0)
            self.remove_matchitem(itemindex)
            itemix = self.find_in_listkeys(keytext)
            if itemix:
                self.reset_listitem_icon(itemix)

    def save_matches(self, event=None):
        """save the changes to a temp file
        """
        num_items = self.count_matches()
        if num_items == 0:
            editor.gui.show_message(self, text='No data to save')
            return
        with open(self.matchespad, "w") as _out:
            writer = csv.writer(_out)
            for ix in range(num_items):
                keytext, cmdtext = self.get_matchitem_data(ix)
                writer.writerow((*keytext.split(' ', 1) , cmdtext))
        editor.gui.show_message(self, text='Data saved')

    def focus_keylist(self, event=None):
        "shift focus for selecting a keycombo item"
        self.focuskeylist()

    def focus_cmdlist(self, event=None):
        "shift focus for selecting a command item"
        self.focuscmdlist()

    def focus_matchlist(self, event=None):
        "shift focus for selecting a mapping item"
        self.focusmatchlist()

    def focus_findkey(self, event=None):
        "Enter search phrase"
        self.focusfindkey()

    def focus_findcmd(self, event=None):
        "Enter search phrase"
        self.focusfindcmd()

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

    def finditem(self, searchbutton, searchfield, search, itemlist, results):
        "check if search string has changed"
        to_find = self.get_entry_text(searchfield)
        if not to_find:
            editor.gui.show_message(self, text='Please enter text to search for')
            return None
        find_what = self.get_search_choice(searchbutton)  # column number in list
        newsearch = to_find != search[0]
        if not newsearch:
            newsearch = find_what != search[1]
        print('in finditem, to_find is', to_find, 'itemlist is', itemlist, 'newsearch is', newsearch)
        if newsearch:
            search = (to_find, find_what)
            results = self.find_listitems(itemlist, to_find, find_what)
            print('in finditem, results is', results)
        return newsearch, search, results

    def findnextitem(self, searchbutton, searchfield, search, itemlist, results):
        "search forward"
        print('in findnextitem, search is', search, 'itemlist is', itemlist)
        search = self.finditem(searchbutton, searchfield, search, itemlist, results)
        if not search:
            return None
        newsearch, search, results = search
        current = self.get_selected_item(itemlist)
        if current == -1 or current is None:
            current = self.get_first_item(itemlist)
        print('in findnextitem, current is', current)
        # print(itemlist, current, itemlist.GetItemCount())
        # print(self.listkeys, current, self.listkeys.GetItemCount())
        if newsearch:
            # positioneren na huidige en klaar
            for item in results:
                # print('new search, first item is', item, self.get_item_text(itemlist, item, 0))
                if self.get_item_text(itemlist, item, 0) > self.get_item_text(itemlist, current, 0):
                    print('new search, set current to', item)
                    if itemlist == self.listkeys:
                        self.set_match_from_key = True
                    elif itemlist == self.listcmds:
                        self.set_match_from_command = True
                    self.set_selected_item(itemlist, item)
                    if itemlist == self.listkeys:
                        self.set_match_from_key = False
                    elif itemlist == self.listcmds:
                        self.set_match_from_command = False
                    return search, results
        else:
            # huidige zoeken in resultatenlijst, positioneren op volgende
            # print('find next, current item is', current, self.get_item_text(itemlist, current, 0))
            # print('    should be in', results)
            newix = results.index(current) + 1
            print('huidige positie:', results.index(current), len(results))
            if newix >= len(results): # was <
                newix = 0
            print('find next, setting current to', results[newix])
            if itemlist == self.listkeys:
                self.set_match_from_key = True
            elif itemlist == self.listcmds:
                self.set_match_from_command = True
            self.set_selected_item(itemlist, results[newix])
            if itemlist == self.listkeys:
                self.set_match_from_key = False
            elif itemlist == self.listcmds:
                self.set_match_from_command = False
            return None
        editor.gui.show_message(self, text='No (next) item found')
        return None

    def findprevitem(self, searchbutton, searchfield, search, itemlist, results):
        "search backward"
        search = self.finditem(searchbutton, searchfield, search, itemlist, results)
        if not search:
            return None
        newsearch, search, results = search
        current = self.get_selected_item(itemlist)
        if current == -1:
            current = self.get_last_item(itemlist)
        if newsearch:
            # positioneren vóór huidige en klaar
            for item in reversed(results):
                if self.get_item_text(itemlist, item, 0) < self.get_item_text(itemlist, current, 0):
                    self.set_selected_item(itemlist, item)
                    return search, results
        else:
            # huidige zoeken in resultatenlijst, positioneren op vorige
            newix = results.index(current) - 1
            if newix < 0:  # >= 0:  # moet dit niet < zijn?
                newix = -1
            self.set_selected_item(itemlist, results[newix])
            return None
        editor.gui.show_message(self, text='No previous item found')
        return None

    def select_match_fromkeys(self):
        "positioneer in matches lijst n.a.v. positioneren in keys lijst"
        if self.count_matches() == 0:
            return
        if not self.set_key_from_match:
            self.set_match_from_key = True
            associated_matchitem = self.find_related((self.listkeys, 0), (self.listmatches, 0))
            if associated_matchitem:
                self.set_selected_item(self.listmatches, associated_matchitem)
            self.set_match_from_key = False

    def select_match_from_cmds(self):
        "positioneer in matches lijst n.a.v. positioneren in commands lijst"
        if self.count_matches() == 0:
            return
        if not self.set_command_from_match:
            self.set_match_from_command = True
            associated_matchitem = self.find_related((self.listcmds, 0), (self.listmatches, 1))
            if associated_matchitem:
                self.set_selected_item(self.listmatches, associated_matchitem)
            self.set_match_from_command = False

    def select_listitems_from_matches(self):
        "positioneer in lijsten n.a.v. positioneren in matches lijst"
        if self.count_matches() == 0:
            return
        if not self.set_match_from_key:
            self.set_key_from_match = True
            associated_keyitem = self.find_related((self.listmatches, 0), (self.listkeys, 0))
            if associated_keyitem:
                self.set_selected_item(self.listkeys, associated_keyitem)
            self.set_key_from_match = False
        if not self.set_match_from_command:
            self.set_command_from_match = True
            associated_commanditem = self.find_related((self.listmatches, 1), (self.listcmds, 0))
            if associated_commanditem:
                self.set_selected_item(self.listcmds, associated_commanditem)
            self.set_command_from_match = False

    def find_related(self, fromstuff, to_stuff):
        """zoek waarde in een kolom in een lijst op in een kolom in een andere lijst
        """
        fromlist, fromcol = fromstuff
        to_list, to_col = to_stuff
        findstr = self.get_item_text(fromlist, self.get_selected_item(fromlist), fromcol)
        result = self.find_listitems(to_list, findstr, to_col)
        return result[0] if result else None

    def confirm(self, event=None):
        """confirm the changes

        don't save to file; just assign to a global variable
        """
        print('in confirm')
        shortcuts = {}
        for ix in range(self.count_matches()):
            keytext, cmd = self.get_matchitem_data(ix)
            key, mods = keytext.split(' ', 1)
            if cmd:
                desc = self.cmddict[cmd]['oms']
            else:
                desc = self.keydict[(key, mods)]['oms']
            shortcuts[ix] = (translate_keyname(key), mods, 'S', cmd, desc)
        self.parent.tempdata = shortcuts
        self.finish()

    def close(self, event=None):
        "close without saving (cancel dialog)"
        self.reject()

    def help(self, event=None):
        """help on shortcuts"""
        text = '\n'.join(['{:30}{}'.format(x[2], x[3]) for x in self.getshortcuts()])
        editor.gui.show_message(self, text=text)
