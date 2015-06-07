# -*- coding: utf-8 -*-
"""
usage: scikeys.py <csvfile>
"""
from __future__ import print_function
import os
import sys
import collections                  # tbv defaultdict
import xml.etree.ElementTree as et  # for xml parsing
import bs4 as bs                    # import BeautifulSoup for html parsing
import tarfile                      # t.b.v. read_source


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

    command_list, command_names = {}, {}
    for row in internals.find_all('tr'):
        command, text, description = [tag.string for tag in row.find_all('td')]
        command_list[command] = (text, description)
        command_names[text] = (command, description)

    return menu_commands, command_list, command_names


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

class PropertiesFile():
    """# read properties and remember them
    so they can instantly substituted when needed
    """
    def __init__(self, fnaam):
        self._default_platform = "all"
        self.properties = collections.defaultdict(dict)
        self._var_start, self._var_end = '$(', ')'
        self._continue_assignment = False
        self._platform = self._default_platform
        self._fnaam = fnaam
        self._acceptable_combinations = (
            ('PLAT_WIN', 'PLAT_WIN_GTK'),
            ('PLAT_GTK', 'PLAT_WIN_GTK'),
            ('PLAT_GTK', 'PLAT_UNIX'),
            ('PLAT_MAC', 'PLAT_UNIX'),
            )

    def _determine_platform(self, line):
        skip_line = False
        # reset platform on unindent
        if self._platform != self._default_platform and line.lstrip() == line:
            self._platform = self._default_platform
        # set platform if used
        if line.startswith('if'):
            _, condition = line.split(None, 1)
            if condition.startswith('PLAT_'):
                self._platform = condition
            skip_line = True
        return line, skip_line

    def _determine_continuation(self, line, result):
        """first, identify if line is to be continued
        if so, strip off continuation char and set switch
        otherwise clear switch
        finally, add line to result
        """
        line = line.lstrip()
        if line.endswith('\\'):
            line = line.rstrip('\\')
            self._continue_assignment = True
        else:
            self._continue_assignment = False
        result += line
        return result

    def read_props(self):
        try:
            with open(self._fnaam) as _in:
                self._data = _in.read()
        except UnicodeDecodeError:
            with open(self._fnaam, encoding='latin-1') as _in:
                self._data = _in.read()
        prop = ''
        result = ''
        for line in self._data.split('\n'):
            line = line.rstrip()
            test = line.lstrip()
            if not test or test.startswith('#'):
                continue
            line, skip = self._determine_platform(line)
            if skip:
                continue
            result = self._determine_continuation(line, result)
            if self._continue_assignment:
                continue
            line = result
            result = ''
            # break down definition
            try:
                prop, value = line.split('=', 1)
            except ValueError:
                # ignore non-assignments
                print('Not an assignment: {}'.format(line))
            # add definition to dictionary
            if not self._var_start in value:
                self.properties[prop][self._platform] = value
                continue
            test = self._do_substitutions(prop, value)
            if test != [[]]:
                for name, platform, definition in test:
                    self.properties[name][platform] = definition

    def get_keydef_props(self):
        self.data = [] # platgeslagen versie van self.properties
        number_commands = collections.defaultdict(list)
        number_shortcuts = collections.defaultdict(list)

        for platform, data in self.properties['user.shortcuts'].items():
            test = data.split('|')
            for x in range(0, len(test)-1, 2):
                self.data.append((test[x], '*', platform, test[x + 1]))

        for platform, data in self.properties['menu.language'].items():
            test = data.split('|')
            for x in range(0, len(test)-1, 3):
                if test[x + 2]:
                    test[x] = test[x].replace('&', '')
                    self.data.append((test[x + 2], '*', platform,
                        'Show as {} (*.{})'.format(test[x], test[x + 1])))

        namedkeys = {'help': 'F1', 'compile': 'Ctrl+F7', 'build': 'F7',
                'clean': 'Shift+F7', 'go': 'F5', 'print': 'Ctrl+P'}
        for name, value in self.properties.items():
            if name.startswith('command'):
                test = name.split('.', 3)
                if test[1].isdigit() or test[1] in namedkeys:
                    if test[2] in ('subsystem', 'needs'): continue
                    context = name.split('.', 2)[-1]
                else:
                    if test[1] != 'shortcut': continue
                    context = test[3]
                for platform, data in value.items():
                    if test[1] in namedkeys:
                        self.data.append((namedkeys[test[1]], context, platform,
                            data))
                    elif test[1] == 'shortcut':
                        number_shortcuts['11' + test[2]].append((context, platform,
                            data))
                    elif len(test[1]) == 1:
                        self.data.append((test[1], 'C', context, platform, data))
                    else:
                        number_commands['11' + test[1]].append((context, platform,
                            data))

        for ix, item in enumerate(self.data):
            if len(item) == 4:
                x, y = nicefy_props(item[0])
                self.data[ix] = x, y, item[1], item[2], item[3]
                item = self.data[ix]
            if item[4] in number_commands:
                print(item)
                for defined in number_commands[item[4]]:
                    print(defined)
                    if defined[:2] == item[2:4]:
                        self.data[ix] = item[:4] + (defined[-1],)
                    else:
                        self.data.append(item[:2] + defined)

        for key, value in number_shortcuts.items():
            if key in number_commands:
                for defkey in value:
                    found = False
                    for defitem in number_commands[key]:
                        if defkey[:2] == defitem[:2]:
                            found = True
                            self.data.append(nicefy_props(defkey[2]) + defitem)
                            break
                    if found:
                        break


    def _do_substitutions(self, prop, value):
        # start variable substitution in prop
        regel = ""
        test = prop.split(self._var_start)
        regel += test[0]
        for item in test[1:]:
            # don't substitute if not possible
            try:
                varnaam, eind = item.split(self._var_end)
            except ValueError:
                regel += self._var_start + item
                print('no variable found ->', regel)
                continue
            if varnaam not in self.properties:
                regel += self._var_start + item
                print('no substitution possible for', varnaam, '->', regel)
                continue
            # don't care about platform here; just take first value
            regel += list(self.properties[varnaam].values())[0] + eind
        prop = regel

        # start variable substitution in value
        regel = ""
        test = value.split(self._var_start)
        returnvalues = []
        regel += test[0]

        variants = {}
        for item in test[1:]:
            # don't substitute if not possible
            try:
                varnaam, eind = item.split(self._var_end)
            except ValueError:
                regel += self._var_start + item
                print('no variable found ->', regel)
                continue
            # check if setting exists at all
            if varnaam not in self.properties:
                regel += self._var_start + item
                print('no substitution possible for', varnaam, '->', regel)
                continue
            # current platform is not defined for this property
            if variants: # can't work with  regel  anymore
                for platform, data in variants.items():
                    try:
                        data += self.properties[varnaam][platform] + eind
                    except KeyError:
                        print('need to create another variant')
                    else:
                        variants[platform] = data
            elif self._platform == self._default_platform:
                for platform, data in self._create_variants(varnaam, regel, eind):
                    variants[platform] = data
                    ## returnvalues.append((prop, platform, data))
                continue
            else:
                test = self._expand_from_other(varnaam, regel, eind)
                if test:
                    regel = test
                else:
                    print('property {} substitution failed for platform {}'.format(
                        prop, self._platform))
                    regel += self._var_start + item
        if variants:
            for platform, data in variants.items():
                returnvalues.append((prop, platform, data))
        else:
            returnvalues.append((prop, self._platform, regel))
        return returnvalues

    def _create_variants(self, varnaam, regel, eind):
        returnvalues = []
        # create variants for defined substitutions
        for defined_platform in self.properties[varnaam]:
            returnvalues.append((defined_platform,
                regel + self.properties[varnaam][defined_platform] + eind))
        return returnvalues

    def _expand_from_other(self, varnaam, regel, eind):
        found = False
        for defined_platform, definition in self.properties[varnaam].items():
            if defined_platform == self._default_platform or (self._platform,
                    defined_platform) in self._acceptable_combinations:
                found = True
                break
        if found:
            regel += definition + eind
        else:
            regel = ''
        return regel

def buildcsv(settings, parent=None):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand
    """
    # we're not considering per-directory settings:
    # - Local properties file called "SciTE.properties" which may be present
    #   in the same  directory as the file being edited.
    # - Directory properties file called "SciTEDirectory.properties" which may be present
    #   in the same or in a parent directory as the file being edited.

    menu_commands, command_list, command_names = read_commands(
        settings['SCI_CMDS'][0])

    data = tarfile.open(settings['SCI_SRCE'][0])
    data.extractall(path='/tmp')
    if sys.platform.startswith('linux'):
        menu_keys = read_source_gtk('/tmp/scite/gtk/SciTEGTK.cxx')
    elif sys.platform.startswith('win32'):
        menu_keys = read_source_win('/tmp/scite/win32/SciTERes.rc')

    keydefs = read_docs(settings['SCI_DOCS'][0]) # non menu keyboard bindings

    globals = PropertiesFile(settings['SCI_GLBL'][0])
    globals.read_props()
    globals.get_keydef_props()
    global_keys = globals.data

    user_ = PropertiesFile(settings['SCI_USER'][0])
    user_.read_props()
    user_.get_keydef_props()
    user_keys = user_.data

    # now put the above stuff together
    # menu_commands - dict: map command naam op omschrijving
    #   name: oms
    # command_list: dict: map command nummer op (naam, omschrijving)
    #   num: (name, oms)
    # menu_keys: list of (key, modifiers, command)
    # keydefs: dict: map keycombo op (?, omschrijving)
    # global_keys, user_keys: list of (key, modifiers, context, platform, omschrijving_of_commando) items
    default_keys = [(x, y, '*', '*', 'S', z, "") for x, y, z in menu_keys]
    default_keys += [(x, y, '*', '*', 'S', "", z) for x, y, z in keydefs]
    default_keys += [(x, y, z, q, 'S', r, "") for x, y, z, q, r in global_keys]
    userdef_keys = [(x, y, z, q, 'U', r, "") for x, y, z, q, r in user_keys]

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
        test_def = def_item[:4] if def_item else sentinel
        test_user = user_item[:4] if user_item else sentinel
        num += 1
        if test_def < test_user:
            new_item = list(def_item)
            def_item = get_next_defitem()
        else:
            new_item = list(user_item)
            user_item = get_next_useritem()
        if test_def == test_user:
            def_item = get_next_defitem()
        # the last item can be a command; if so, get the description
        # add the description as a new last item; if not present, add an empty string
        # so now we get one column more
        test = new_item[-2]
        if test in menu_commands:
            new_item[-1] = menu_commands[test]
        elif test in command_list:
            new_item[-1] = new_item.append(command_list[test])
        elif test in command_names:
            new_item[-1] = new_item.append(command_names[test])
        elif test.startswith('IDM_BUFFER'):
            new_item[-1] = "Switch to buffer " + str(int(test[-1]) + 1)
        shortcuts[num] = new_item
    return shortcuts

def savekeys(pad):
    """schrijf de gegevens terug

    voorlopig nog niet mogelijk
    aangepaste keys samenstellen tot een user.shortcuts statement en dat
    invoegen in SciTEUser.properties
    waren er niet nog meer mogelijkheden? Ja: menu.language en command.shortcut
    """
    pass

