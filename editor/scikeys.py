# -*- coding: utf-8 -*-
"""
usage: scikeys.py <csvfile>
"""
from __future__ import print_function
import os
import sys
if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import collections                  # tbv defaultdict
import xml.etree.ElementTree as et  # for xml parsing
import bs4 as bs                    # import BeautifulSoup for html parsing
import tarfile                      # t.b.v. read_source
from editor.hotkeys_qt import read_settings, readcsv, writecsv


def nicefy_props(data):
    """split keydef into key and modifiers
    """
    from_, to = 'Keypad+', 'KeypadPlus'
    data = data.replace(from_, to)
    test = data.split('+')
    mods = ''
    if 'Ctrl' in data:
        mods += 'C'
    if 'Alt' in data:
        mods += 'A'
    if 'Shift' in data:
        mods += 'S'
    key = test[-1].replace(to, from_)
    return key, mods


def nicefy_source(data):
    """split keydef into key and modifiers
    """
    key = data.rsplit('>')[-1].strip().strip('"')
    mods = ''
    if '<control>' in data:
        mods += 'C'
    if '<alt>' in data:
        mods += 'A'
    if '<shift>' in data:
        mods += 'S'
    return key, mods


def read_commands(path):
    """read names/ids of menu commands and internal commands from Commandvalues.html

    """
    with open(path) as doc:

        soup = bs.BeautifulSoup(doc)

    menus, internals = soup.find_all('table')

    menu_commands, keydefs = {}, {}
    for row in menus.find_all('tr'):
        command, text = [tag.string for tag in row.find_all('td')]
        menu_commands[command] = text

    command_list = {}
    for row in internals.find_all('tr'):
        command, text, description = [tag.string for tag in row.find_all('td')]
        command_list[command] = (text, description)

    return menu_commands, command_list


def read_docs(path):
    """read keydefs from SciTEDoc.html
    """
    with open(path) as doc:

        soup = bs.BeautifulSoup(doc)

    keyboard_commands = soup.find('table', summary="Keyboard commands")

    ## keydefs = {}
    keydefs = []
    for row in keyboard_commands.find_all('tr'):
        description, shortcut = [tag.string for tag in row.find_all('td')]
        ## parts = shortcut.lower().split('+')
        ## if parts[-1] == '':
            ## parts[-2] += '+'
            ## parts.pop()
        ## shortcut = ' '.join(reversed(parts))
        key, mods = nicefy_props(shortcut)
        ## keydefs[shortcut] = ('', description)
        keydefs.append((key, mods, description))

    return keydefs


def read_source_gtk(fname):
    """read keydefs from a given SciTE source file (Linux version)
    """
    menu_keys = []
    in_menu = False
    with open(fname) as source:
        data = source.read()
    source = data.split('\n')
    for line in source:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if in_menu:
            if '};' in line:
                in_menu = False
                continue
            test = line.split(",")
            if test[1].strip() in ('NULL', '""'):
                continue
            key, mods = nicefy_source(test[1])
            command = test[3].strip()
            if command.startswith('bufferCmdID +'):
                command = 'IDM_BUFFER' + command[-1]
            menu_keys.append((key, mods, command))
        else:
            in_menu = 'menuItems[] =' in line
            if in_menu: continue
            in_menu = 'menuItemsOptions[] =' in line
            if in_menu: continue
            in_menu = 'menuItemsBuffer[] =' in line
            if in_menu: continue
            in_menu = 'menuItemsHelp[] =' in line
    return menu_keys


def read_source_win(fname=''):
    """get keydefs from a given SciTE source file (Windows version)

    definitions are like
    	MENUITEM "Open Selected &Filename\tCtrl+Shift+O",	IDM_OPENSELECTED
    """
    menu_keys = []
    return menu_keys


class Properties:
    """read currently defined shortcuts from a given .properties file

    self.data finally contains a list of tuples: shortcut, context, command
    """
    def __init__(self):
        self._user_shortcuts = []
        self._number_commands = collections.defaultdict(list)
        self._number_shortcuts = collections.defaultdict(list)
        self.data = []

    def expand_variables(self, path):
        """variable substitution
        """
        try:
            with open(path) as _in:
                buffer = _in.readlines()
        except UnicodeDecodeError:
            with open(path, encoding='iso-8859-1') as _in:
                buffer = _in.readlines()

        # first pass: read which symbols are defined (check for $(...))
        symbol_uses = collections.defaultdict(list)
        lookfor_first, lookfor_next = '$(', ')'
        for index, line in enumerate(buffer):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            test = line.split(lookfor_first, 1)
            while len(test) > 1:
                test2 = test[1].split(lookfor_next, 1)
                if len(test2) < 2:
                    continue # or is this an error?
                symbol_uses[test2[0]].append(index)
                test = test2[1].split(lookfor_first, 1)

        # second pass: read the definitions
        self.symbol_defs = collections.defaultdict(list)
        in_definition = ''
        for index, line in enumerate(buffer):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if in_definition:   # definition over multiple lines
                definition.append(line)
                if not line.endswith('\\'): # statement continues
                    self.symbol_defs[in_definition].append((defined_at, definition))
                    in_definition = ''

            for symbol in symbol_uses:
                if symbol in line and not symbol.join((lookfor_first,
                        lookfor_next)) in line:         # on first line of definition
                    test = line.split(symbol, 1)        # get the rest of the line
                    test2 = test[1].split('=', 1)       # get the value
                    if len(test2) > 1:
                        defined_at, definition = index, [test2[1],]
                        if definition[0].endswith('\\'):     # first part of multiline definition
                            in_definition = symbol
                        else:
                            self.symbol_defs[symbol].append((defined_at, definition))

        # variable substitution in the symbols themselves
        # for now doing this once should be enough
        for key, value in self.symbol_defs.items():
            ## print(key, value)
            new_value = []
            for lineno, data in value:
                newdata = []
                for item in data:
                    if lookfor_first not in item:
                        newdata.append(item)
                        continue
                    item_n = item.split(lookfor_first)
                    newdata.append(item_n[0])
                    for part in item_n[1:]:
                        test = part.split(lookfor_next, 1)
                        if len(test) < 2:
                            newdata[-1] += part
                            continue
                        # use first substitution
                        to_substitute = self.symbol_defs[test[0]][0][1]
                        newdata[-1] += to_substitute[0]
                        if len(to_substitute) > 1:
                            newdata += to_substitute[1:]
                        newdata[-1] += test[1]
                new_value.append((lineno, newdata))
                ## new_value.append((lineno, newdata_n))
            self.symbol_defs[key] = new_value
            ## print(key, new_value)

        # third pass: substitute and write to temp file
        # if they can't be expanded, they're defined in other properties files - nothing to do about that
        _temp = 'temp.properties'
        with open(_temp, 'w') as _out:
            for indx, line in enumerate(buffer):
                line = line.rstrip()
                if lookfor_first not in line:
                    print(line, file=_out)
                    continue
                # regel opsplitsen op start van te vervangen variabele
                line_n = line.split(lookfor_first)
                newline_n = [line_n[0]] # nieuwe regel = eerste deel
                for item in line_n[1:]:
                    # regeldeel opsplitsen op eind van te vervangen variabele
                    test = item.split(lookfor_next, 1)
                    if len(test) < 2:
                        newline_n[-1] += '$(' + item
                        continue
                    if self.symbol_defs[test[0]]:   #  vervanging aanwezig
                        substitution = self.symbol_defs[test[0]][0][1]
                        newline_n[-1] += substitution[0]
                        if len(substitution) > 1:
                            newline_n += substitution[1:] # rekening houden met...
                    else:
                        newline_n[-1] += '$(' + test[0] + ')'
                    newline_n[-1] += test[1]
                newline = '\n'.join(newline_n)         #  ...vervanging over meer regels
                print(newline, file=_out)

        return _temp


    def read_data_from_file(self, path):
        """collect interesting data from the expanded file
        """
        gather_user_shortcuts = in_language_menu = False
        _temp = self.expand_variables(path)
        with open(_temp) as doc:
            for line in doc:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('user.shortcuts'):
                    gather_user_shortcuts = True
                elif line.startswith('command.'):
                    test = line.split('.')
                    if (test[1].isdigit() or test[1] == 'help'
                            ) and test[2] != 'subsystem':
                        self._number_commands[test[1]].append('.'.join(test[2:]))
                    elif test[1] == 'shortcut':
                        self._number_shortcuts[test[2]].append('.'.join(test[3:]))
                elif line.startswith('menu.language'):
                    in_language_menu = True
                if gather_user_shortcuts:
                    if line.startswith('user.shortcuts'):
                        line = line.split('user.shortcuts=', 1)[1]
                    test = line.lstrip('\\')
                    if test:
                        self._user_shortcuts.append(test)
                    if not line.endswith('\\'):
                        gather_user_shortcuts = False
                if in_language_menu:
                    if line.startswith('menu.language'):
                        line = line.split('menu.language=', 1)[1]
                    test = line.lstrip('\\')
                    if test:
                        menu_item = test.split('|')
                        ## print(menu_item)
                        if menu_item[2]:
                            self.data.append((menu_item[2], '*',
                                'Show {} files (*.{})'.format(
                                    menu_item[0].replace('&', ''), menu_item[1])))
                    if not line.endswith('\\'):
                        in_language_menu = False

    def process_file_data(self):
        """convert the collected data into the result list
        """
        combos = collections.defaultdict(list)

        # add the entries from the "user.shortcuts" property to the intermediary dict
        for item in self._user_shortcuts:
            data = item.split('|')
            if data[1].isdigit() and data[1].startswith('11'):
                self._number_shortcuts[data[1][2:]].append('*=' + data[0])
            else:
                combos[data[0]].append(data[1]) # add empty string to force list

        # add the numbered command properties to the intermediary dict
        for number, command in self._number_commands.items():
            if len(number) == 1:
                for detail in command:
                    combos['Ctrl+' + number] = command
            elif number == 'help':
                for item in command:
                    if item:
                        context, data = item.split('=', 1)
                        self.data.append(('F1', context, data))
            else:
                # look up key combo in self._number_shortcuts
                shortcuts = []
                for item in self._number_shortcuts[number]:
                    if item:
                        shortcuts.append(item.split('=', 1))
                for item in command:
                    if item:
                        context, data = item.split('=', 1)
                        found = False
                        for test in shortcuts:
                            if test[0] == context:
                                self.data.append((test[1], context, data))
                                found = True
                        if not found:
                            for test in shortcuts:
                                if test[0] == '*':
                                    self.data.append((test[1], context, data))

        # parse the intermediary dict for syntax-dependent entries
        for item, value in combos.items():
            for subitem in value:
                if subitem: # ignore empty strings
                    try:
                        context, command = subitem.split('=', 1)
                    except ValueError:
                        context, command = '*', subitem
                    self.data.append((item, context, command))

        # split up key and modifiers
        for idx, item in enumerate(self.data):
            key, mods = nicefy_props(item[0])
            self.data[idx] = key, mods, item[1], item[2]

def buildcsv(csvfile=''):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en schrijf ze naar het csv bestand
    """
    # the old csv file contains the location(s) for the keyboard definitions file(s)
    # overrideable default to allow for independent testing

    # we're not considering per-directory settings:
    # - Local properties file called "SciTE.properties" which may be present
    #   in the same  directory as the file being edited.
    # - Directory properties file called "SciTEDirectory.properties" which may be presen
    #   in the same or in a parent directory as the file being edited.
    if not csvfile:
        filename = os.path.join(os.path.dirname(__file__), 'hotkey_config.py')
        plugins = read_settings(filename)[1]
        for name, value in plugins:
            if name == 'SciTE':
                csvfile = value
                break

    # read data from the csv file
    settings, coldata, _ = readcsv(csvfile)
    if not settings:
        return 'Settings could not be determined from', csvfile

    menu_commands, command_list = read_commands(settings['SCI_CMDS'][0])

    data = tarfile.open(settings['SCI_SRCE'][0])
    data.extractall(path='/tmp')
    if sys.platform.startswith('linux'):
        menu_keys = read_source_gtk('/tmp/scite/gtk/SciTEGTK.cxx')
    elif sys.platform.startswith('win32'):
        menu_keys = read_source_win('/tmp/scite/win32/SciTERes.rc')

    keydefs = read_docs(settings['SCI_DOCS'][0]) # non menu keyboard bindings

    globals = Properties()
    globals.read_data_from_file(settings['SCI_GLBL'][0])
    globals.process_file_data()
    global_keys = globals.data

    user = Properties()
    user.read_data_from_file(settings['SCI_USER'][0])
    user.process_file_data()
    user_keys = user.data

    # now put the above stuff together
    default_keys = [(x, y, '*', 'S', z) for x, y, z in menu_keys + keydefs]
    default_keys += [(x, y, z, 'S', q) for x, y, z, q in global_keys]
    userdef_keys = [(x, y, z, 'U', q) for x, y, z, q in user_keys]

    sentinel = (chr(255), '', '', '')
    gen_def = (x for x in sorted(default_keys))
    def get_next_defitem():
        try:
            return next(gen_def)
        except StopIteration:
            return
    user_def = (x for x in sorted(userdef_keys))
    def get_next_useritem():
        try:
            return next(user_def)
        except StopIteration:
            return
    num = 0
    shortcuts = collections.OrderedDict()
    def_item = get_next_defitem()
    user_item = get_next_useritem()
    while def_item or user_item:
        ## print(def_item, user_item)
        test_def = def_item[:3] if def_item else sentinel
        test_user = user_item[:3] if user_item else sentinel
        ## print(test_def, test_user)
        num += 1
        if test_def < test_user:
            ## print('default is smaller')
            shortcuts[num] = def_item
            def_item = get_next_defitem()
        else:
            ## print('default is not smaller')
            shortcuts[num] = user_item
            user_item = get_next_useritem()
        if test_def == test_user:
            def_item = get_next_defitem()

    writecsv(csvfile + '.txt', settings, coldata, shortcuts)

def savekeys(pad):
    """schrijf de gegevens terug

    voorlopig nog niet mogelijk
    aangepaste keys samenstellen tot een user.shortcuts statement en dat
    invoegen in SciTEUser.properties
    """
    pass

if __name__ == '__main__':
    ## import plac; plac.call(buildcsv)
    from docopt import docopt
    args = docopt(__doc__)
    buildcsv(args['<csvfile>'])
