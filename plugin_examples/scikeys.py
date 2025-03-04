"""Hotkeys plugin for SciTE
"""
    # we're not considering per-directory settings:
    # - Local properties file called "SciTE.properties" which may be present
    #   in the same  directory as the file being edited.
    # - Directory properties file called "SciTEDirectory.properties" which may be present
    #   in the same or in a parent directory as the file being edited.
import os
import sys
import logging
import collections                  # tbv defaultdict
import tarfile                      # t.b.v. read_source
## import xml.etree.ElementTree as et  # for xml parsing
import bs4 as bs                  # import BeautifulSoup for html parsing
LOGBASE = '/tmp/hotkeys'
if not os.path.exists(LOGBASE):
    os.mkdir(LOGBASE)
logging.basicConfig(filename=os.path.join(LOGBASE, 'scikeys.log'),
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


log = logging.info


def _translate_keyname(inp):
    """map key names in settings file to key names in HotKeys
    """
    convert = {'Equal': '=', 'Escape': 'Esc', 'Delete': 'Del', 'Return': 'Enter',
               'BackSpace': 'Backspace', 'PageUp': 'PgUp', 'PageDown': 'PgDn', 'space': 'Space',
               'Keypad*': 'Num*', 'Keypad+': 'Num+', 'Keypad-': 'Num-', 'Keypad/': 'Num/', }
    return convert.get(inp, inp)


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
        soup = bs.BeautifulSoup(doc, 'lxml')

    menu_commands, internal_commands = {}, {}

    try:
        menus, internals = soup.find_all('table')
        got_data = True
    except ValueError:
        got_data = False

    if got_data:
        count = 0
        for row in menus.find_all('tr'):
            if row.parent.name == 'thead':
                continue
            command, text = [tag.string for tag in row.find_all('td')]
            count += 1
            menu_commands[f"{count:0>4}"] = (command, text)

        for row in internals.find_all('tr'):
            if row.parent.name == 'thead':
                continue
            key, command, text = [tag.string for tag in row.find_all('td')]
            internal_commands[key] = (command, text)
            # command_names[text] = (key, command)

    return menu_commands, internal_commands


def read_docs(path):
    """read keydefs from SciTEDoc.html
    """
    with open(path) as doc:
        soup = bs.BeautifulSoup(doc, 'lxml')

    keyboard_commands = soup.find('table', summary="Keyboard commands")

    keydefs = []
    if keyboard_commands:
        for row in keyboard_commands.find_all('tr'):
            if not row.find_all('td'):
                continue
            description, shortcut = [tag.string for tag in row.find_all('td')][:2]
            key, mods = nicefy_props(shortcut)
            keydefs.append((key, mods, description))

    return keydefs


def read_symbols(fname):
    """read symbols for actions from "ItemFactory" tables

    eventueel de SCI_* symbolen ook nog (zelfde nummerrange als Function, geen overlap)
    """
    symbols, functions = {}, {}
    in_table = in_functions = False
    with open(fname) as source:
        data = source.read()
    source = data.split('\n')
    for line in source:
        line = line.strip()
        if in_table:
            if '};' in line:
                in_table = False
            elif line.startswith('{"IDM_'):
                command, number = line[1:-2].split(',', 1)
                symbols[number] = command.strip('"')
        elif in_functions:
            if '};' in line:
                in_functions = False
            else:
                command, number = line[1:].split(',')[:2]
                functions[number] = command.strip('"')
        elif line.startswith('static IFaceConstant'):
            in_table = True
        elif line.startswith('static IFaceFunction'):
            in_functions = True
    return symbols, functions


def read_menu_gtk(fname):
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
            if in_menu:
                continue
            in_menu = 'menuItemsOptions[] =' in line
            if in_menu:
                continue
            in_menu = 'menuItemsBuffer[] =' in line
            if in_menu:
                continue
            in_menu = 'menuItemsHelp[] =' in line
            # in_menu = any(('menuItems[] =' in line, 'menuItemsOptions[] =' in line,
            #                'menuItemsBuffer[] =' in line, 'menuItemsHelp[] =' in line))
    return menu_keys


def read_menu_win(fname):
    """get keydefs from a given SciTE source file (Windows version)

    definitions are like
    MENUITEM "Open Selected &Filename\tCtrl+Shift+O",	IDM_OPENSELECTED
    """
    menu_keys = []
    with open(fname) as source:
        data = source.read()
    source = data.split('\n')
    for line in source:
        line = line.strip()
        if line.startswith('MENUITEM'):
            parts = line.split('"')
            if len(parts) != 3:
                continue
            dummy, *keycombo = parts[1].split('\t', 1)
            if keycombo:
                key, mods = nicefy_props(keycombo)
                menu_keys.append((key, mods, parts[2].strip()))
    return menu_keys


class PropertiesFile:
    """read all assignments; ultimately only keep the keyboard shortcut definitions
    """
    def __init__(self, fnaam):  # , global_props):
        self._default_platform = "*"
        self.properties = collections.defaultdict(dict)
        # self.all_props = dict(global_props)
        # self.properties.update(global_props)
        self._var_start, self._var_end = '$(', ')'
        self._continue_assignment = False
        self._platform = self._default_platform
        self._fnaam = fnaam
        self._acceptable_combinations = (('PLAT_WIN', 'PLAT_WIN_GTK'),
                                         ('PLAT_GTK', 'PLAT_WIN_GTK'),
                                         ('PLAT_GTK', 'PLAT_UNIX'),
                                         ('PLAT_MAC', 'PLAT_UNIX'))

    def _determine_platform(self, line):
        """check if definition is meant for a specific platform (e.g. win, gtk)
        """
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
        """read a properties file
        """
        fnaam = os.path.basename(self._fnaam)
        try:
            with open(self._fnaam) as _in:
                data = _in.readlines()
        except UnicodeDecodeError:
            with open(self._fnaam, encoding='latin-1') as _in:
                data = _in.readlines()
        prop = ''
        result = ''
        for line in data:
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
            if '=' in line:  # try:
                prop, value = line.split('=', 1)
            else:  # except ValueError:
                # ignore non-assignments
                log(f"{fnaam:25} Not an assignment: '{line}'")  # doorgaans een import statement
                prop = value = ''
                continue
            # we don't do substitutions any more
            # if self._var_start in prop or self._var_start in value:
            #     test = self._do_substitutions(prop, value)
            #     if test != [[]]:
            #         for name, platform, definition in test:
            #             self.properties[name][platform] = definition
            # else:
            self.properties[prop][self._platform] = value  # add definition to dictionary

    def get_keydef_props(self):
        """extract the keydef properties from the file data
        """
        self.data = []  # platgeslagen versie van keydefs uit self.properties
        # helper attribute only used in the toolcommand subroutines:
        self.tooldata = {'commands': collections.defaultdict(list),
                         'shortcuts': collections.defaultdict(list),
                         'descriptions': collections.defaultdict(list)}

        for platform, data in self.properties['user.shortcuts'].items():
            test = data.split('|')
            for x in range(0, len(test) - 1, 2):
                key, mods = nicefy_props(test[x])
                self.data.append((key, mods, '*', platform, test[x + 1], ''))

        for platform, data in self.properties['menu.language'].items():
            test = data.split('|')
            for x in range(0, len(test) - 1, 3):
                if test[x + 2]:
                    test[x] = test[x].replace('&', '')
                    key, mods = nicefy_props(test[x + 2])
                    self.data.append((key, mods, '*', platform, f'to_{test[x + 1]}',
                                      f'Show as {test[x]} (*.{test[x + 1]})'))

        self._build_toolcommand_data()

        # dit blijkt a) niks te doen en b) zaken te bevatten die niet (meer) mogelijk zijn
        # self._probably_obsolete_routine()

        data = []
        self._process_manual_toolcommand_shortcuts(data)
        self._process_automatic_toolcommand_shortcuts(data)
        for item in data:
            self.data.append(tuple(item))

    def _build_toolcommand_data(self):
        """analyse definitions for tools menu commands
        """
        namedkeys = {'help': 'F1', 'compile': 'Ctrl+F7', 'build': 'F7',
                     'clean': 'Shift+F7', 'go': 'F5', 'print': 'Ctrl+P'}
        for name, value in self.properties.items():
            if name.startswith('command.'):
                test = name.split('.', 3)
                # namedkeys helemaal overslaan?
                if test[1].isdigit() or test[1] in namedkeys:
                    if test[2] in ('subsystem', 'needs', 'directory'):
                        continue
                    context = name.split('.', 2)[-1]
                else:
                    if test[1] not in ('shortcut', 'name'):
                        continue
                    context = test[3]
                for platform, data in value.items():
                    if test[1] in namedkeys:
                        key, mods = nicefy_props(namedkeys[test[1]])
                        self.data.append((key, mods, context, platform, data, test[1]))
                    elif test[1] == 'shortcut':
                        self.tooldata["shortcuts"]['11' + test[2]].append((context, platform, data))
                    elif test[1] == 'name':
                        self.tooldata["descriptions"]['11' + test[2]].append((context, platform,
                                                                              data))
                    # Ctrl-1 (command & name) hier net zo afhandelen als de andere
                    ## elif len(test[1]) == 1:
                        ## self.data.append((test[1], 'C', context, platform, data))
                    else:
                        self.tooldata["commands"]['11' + test[1]].append((context, platform, data))

    # def _probably_obsolete_routine(self):
    #     # merge tool commands with internally defined shortcuts into main data
    #     data = []
    #     for ix, item in enumerate(self.data):
    #         # dit komt nooit voor
    #         if len(item) == 4:
    #             # x, y = nicefy_props(item[0])
    #             # self.data[ix] = x, y, item[1], item[2], item[3]
    #             # item = self.data[ix]
    #             # self.data[ix][:1] = nicefy_props(item[0])
    #             item = nicefy_props(item[0])
    #         # als het 5e item voorkomt in de menu commands
    #         # maar dat zijn zelf aangelegde namen dus kan dat wel?
    #         if item[4] in self.tooldata["commands"]:
    #             breakpoint()
    #             for defined in self.tooldata["commands"][item[4]]:
    #                 if defined[:2] == item[2:4]:
    #                     loc = ix
    #                     dataitem = [x for x in item[:4]] + [defined[-1]]
    #                 else:
    #                     loc = -1
    #                     dataitem = [x for x in item[:2]] + [defined]
    #                 for defined in self.tooldata["descriptions"][item[4]]:
    #                     if defined[:2] == item[2:4]:
    #                         dataitem.append(defined[-1])
    #                 data.append((loc, dataitem))
    #     for loc, dataitem in data:
    #         dataitem = tuple(dataitem)
    #         if loc == -1:
    #             self.data.append(dataitem)
    #         else:
    #             self.data[loc] = dataitem

    def _process_manual_toolcommand_shortcuts(self, data):
        """merge tooldata commands and descriptions into shortcuts

        unfortunately they all lack a command string (item[4])
        # and therefore are discarded in build_data
        """
        for key, value in self.tooldata["shortcuts"].items():
            # if key in self.tooldata["commands"]:
            test = self.tooldata["commands"].get(key, [])
            if test:
                for defkey in value:
                    found = False
                    for defitem in self.tooldata["commands"][key]:
                        if defkey[:2] == defitem[:2]:
                            found = True
                            data.append(nicefy_props(defkey[2]) + defitem)
                            break
            # if key in self.tooldata["descriptions"]:
            test = self.tooldata["descriptions"].get(key, [])
            if test:
                for defkey in value:
                    found = False
                    for defitem in self.tooldata["descriptions"][key]:
                        if defkey[:2] == defitem[:2]:
                            ## found = True
                            test = nicefy_props(defkey[2]) + defitem[:2]
                            for ix, item in enumerate(data):
                                if item[:len(test)] == test:
                                    found = True
                                    data[ix] = list(item)
                                    data[ix].append(defitem[-1])
                                    break
                            if found:
                                break
                    if found:
                        break

    def _process_automatic_toolcommand_shortcuts(self, data):
        """merge tooldata descriptions into commands for which the shortcut follows from the
        definition name e.g. command.1 indicaties Ctrl+1
        """
        for key, value in self.tooldata["commands"].items():
            if len(key) != 3:
                continue
            if key in self.tooldata["descriptions"]:
                for defkey in value:
                    ## found = False
                    for defitem in self.tooldata["descriptions"][key]:
                        if defkey[:2] == defitem[:2]:
                            ## found = True
                            data.append([key[2], 'C'] + list(defkey) + list(defitem[-1:]))
                            break
            else:
                for defkey in value:
                    data.append([key[2], 'C'] + list(defkey) + [''])

    # substitueren levert meer gedoe op dan me waard is
    # def _do_substitutions(self, prop, value):
    #     """helper method to substitute symbols by values definied earlier in the file
    #     """
    #     fnaam = os.path.basename(self._fnaam)
    #     self.all_props.update(self.properties)
    #     # start variable substitution in prop
    #     regel = ""
    #     test = prop.split(self._var_start)
    #     regel += test[0]
    #     for item in test[1:]:
    #         if self._substitution_not_possible(item, [regel]):
    #             continue
    #         # don't care about platform here; just take first value
    #         varnaam, eind = item.split(self._var_end)
    #         # regel += list(self.properties[varnaam].values())[0] + eind
    #         regel += list(self.all_props[varnaam].values())[0] + eind
    #     prop = regel

    #     # start variable substitution in value
    #     regel = ""
    #     test = value.split(self._var_start)
    #     returnvalues = []
    #     regel += test[0]

    #     variants = {}
    #     for item in test[1:]:
    #         if self._substitution_not_possible(item, [regel]):
    #             continue
    #         varnaam, eind = item.split(self._var_end)
    #         # if self._platform == self._default_platform:
    #         #     for platform, data in self._create_variants(varnaam, regel, eind):
    #         #         variants[platform] = data
    #         #         ## returnvalues.append((prop, platform, data))
    #         #     continue
    #         # current platform is not defined for this property
    #         if variants:  # can't work with  regel  anymore
    #             for platform, data in variants.items():
    #                 try:
    #                     # data += self.properties[varnaam][platform] + eind
    #                     data += self.all_props[varnaam][platform] + eind
    #                 except KeyError:
    #                     log(f"{fnaam:25} can't create all needed variants for {varnaam}")
    #                 else:
    #                     variants[platform] = data
    #         elif self._platform == self._default_platform:
    #             for platform, data in self._create_variants(varnaam, regel, eind):
    #                 variants[platform] = data
    #                 ## returnvalues.append((prop, platform, data))
    #             continue
    #         else:
    #             test = self._expand_from_other(varnaam, regel, eind)
    #             if test:
    #                 regel = test
    #             else:
    #                 log(f'{fnaam:25} property {prop} substitution failed for platform'
    #                     f' {self._platform}')
    #                 regel += self._var_start + item
    #     if variants:
    #         for platform, data in variants.items():
    #             returnvalues.append((prop, platform, data))
    #     else:
    #         returnvalues.append((prop, self._platform, regel))
    #     return returnvalues

    # def _substitution_not_possible(self, item, regel):
    #     """signal to not substitute if not possible

    #     regel wordt als list aangeboden zodat deze gemuteerd teruggegeven kan worden
    #     """
    #     fnaam = os.path.basename(self._fnaam)
    #     try:
    #         varnaam, eind = item.split(self._var_end)
    #     except ValueError:
    #         regel[0] += self._var_start + item
    #         log(f"{fnaam:25} no variable found in line '{regel}'")
    #         return True
    #     if varnaam not in self.properties:
    #         regel[0] += self._var_start + item
    #         log(f"{fnaam:25} no substitution possible for {varnaam} in line {regel}")
    #         return True
    #     return False

    # def _create_variants(self, varnaam, regel, eind):
    #     """helper method to create multiple definitions for a property if applicable
    #     """
    #     returnvalues = []
    #     # create variants for defined substitutions
    #     for defined_platform in self.properties[varnaam]:
    #         returnvalues.append((defined_platform,
    #                              regel + self.properties[varnaam][defined_platform] + eind))
    #     return returnvalues

    # def _expand_from_other(self, varnaam, regel, eind):
    #     """helper method to expand definition if applicable
    #     """
    #     found = False
    #     for defined_platform, definition in self.properties[varnaam].items():
    #         if (defined_platform == self._default_platform
    #                 or (self._platform, defined_platform) in self._acceptable_combinations):
    #             found = True
    #             break
    #     if found:
    #         regel += definition + eind
    #     else:
    #         regel = ''
    #     return regel


def merge_command_dicts(dict_from_text, dict_from_src):
    """voeg dictionaries vanuit verschillende bronnen samen
    """
    fromtext = {y[0]: (x, y[1]) for x, y in dict_from_text.items()}
    fromsrc = {y: (x, '') for x, y in dict_from_src.items()}
    numbers = {x: y[0] for x, y in fromsrc.items()}
    fromsrc.update(fromtext)
    newfromsrc = {x: (numbers[x] if x in numbers else y[0], y[1]) for x, y in fromsrc.items()}
    return {y[0]: (x, y[1]) for x, y in newfromsrc.items()}


def build_data(page, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het keydef bestand

    showinfo argument is for API compatibility
    """
    settings = page.settings
    special_keys = ('help', 'go', 'build', 'compile', 'clean')
    # menu_commands - dict: map volgnummer op (commandonaam, omschrijving)
    # command_list: dict: map command nummer op (naam, omschrijving)
    menu_commands, internal_commands = read_commands(settings['SCI_CMDS'])

    with tarfile.open(settings['SCI_SRCE']) as data:
        data.extractall(path='/tmp')
    # menu_keys: list of (key, modifiers, command)
    if sys.platform.startswith('linux'):
        menu_keys = read_menu_gtk('/tmp/scite/gtk/SciTEGTK.cxx')
    elif sys.platform.startswith('win32'):
        menu_keys = read_menu_win('/tmp/scite/win32/SciTERes.rc')
    else:
        menu_keys = {}
    all_menu_cmds, all_int_cmds = read_symbols('/tmp/scite/src/IFaceTable.cxx')  # ook in SciTE.h
        # dit is een mapping van nummers op strings (geen omschrijvingen)
        # samenvoegen met menu_commands resp. internal_commands
        # resultaat is mappings van een nummer op een tuple van commando en omschrijving
    default_keys = [(_translate_keyname(x), y, '*', '*', 'S', z, "") for x, y, z in menu_keys]
    menu_commands = merge_command_dicts(menu_commands, all_menu_cmds)
    internal_commands = merge_command_dicts(internal_commands, all_int_cmds)

    # keydefs: list of (key. modifiers, omschrijving))
    keydefs = read_docs(settings['SCI_DOCS'])  # non menu keyboard bindings
        # dit is een list van tuples van key, modifiers, description
        # je zou nog een matcher kunnen definiëren om descriptions aan internal_commands
        # toe te voegen
    default_keys += [(_translate_keyname(x), y, '*', '*', 'S', "", z) for x, y, z in keydefs]

    # global_keys, user_keys: list of (key, modifiers, context, platform, command, omschrijving)
    #   commando kan een menu commando zijn of een intern commando of een tool aanroep of een
    #   lua functie gedefinieerd in luastartup
    global_keys = []
    global_keys_without = []  # zonder commando-aanduiding
    global_keys_with = []   # inclusief commando's als go, compile, help etc
    # global_props = {}
    root = os.path.dirname(settings['SCI_GLBL'])
    for path in os.listdir(root):
        fname = os.path.join(root, path)
        name, ext = os.path.splitext(path)
        if os.path.isfile(fname) and ext == '.properties' and name not in (
                'SciTE', 'Embedded'):
            global_stuff = PropertiesFile(fname)  # , global_props)
            global_stuff.read_props()
            global_stuff.get_keydef_props()
            global_keys += [x for x in global_stuff.data if x[4] and x[5] not in special_keys]
            global_keys_without += [x for x in global_stuff.data if not x[4]]
            global_keys_with += [x for x in global_stuff.data if x[4]]
            # global_props.update(global_stuff.properties)
    default_keys += [(_translate_keyname(x), y, z, q, 'S', r, s) for x, y, z, q, r, s in global_keys]
    # breakpoint()

    user_keys = []
    user_keys_without = []
    user_keys_with = []
    root = os.path.dirname(settings['SCI_USER'])
    for path in os.listdir(root):
        fname = os.path.join(root, path)
        _, ext = os.path.splitext(path)
        if os.path.isfile(fname) and ext == '.properties':
            user_stuff = PropertiesFile(fname)  # , global_props)
            user_stuff.read_props()
            user_stuff.get_keydef_props()
            user_keys += [x for x in user_stuff.data if x[4] and x[5] not in special_keys]
            user_keys_without += [x for x in user_stuff.data if not x[4]]
            user_keys_with += [x for x in user_stuff.data if x[4]]
    userdef_keys = [(_translate_keyname(x), y, z, q, 'U', r, s) for x, y, z, q, r, s in user_keys]
    # breakpoint()

    shortcuts, contexts_list = merge_keydefs(default_keys, userdef_keys,
                                             menu_commands, internal_commands)
    return shortcuts, {'menucommands': menu_commands, 'internal_commands': internal_commands,
                       'contexts': list(contexts_list)}


def merge_keydefs(default_keys, userdef_keys, menu_commands, internal_commands):
    """turn keydef lists into generators and merge into sorted dict
    """
    sentinel = (chr(255), '', '', '')
    gen_def = (x for x in sorted(default_keys))
    user_def = (x for x in sorted(userdef_keys))
    shortcuts = {}
    num = 0
    contexts_list = set()
    def_item = next(gen_def, None)  # get_next_defitem()
    user_item = next(user_def, None)  # _get_next_useritem()
    while def_item or user_item:
        if def_item:
            test_def = def_item[:4]
            contexts_list.add(def_item[2])
        else:
            test_def = sentinel
        if user_item:
            test_user = user_item[:4]
            contexts_list.add(user_item[2])
        else:
            test_user = sentinel
        num += 1
        if test_def < test_user:
            new_item = list(def_item)
            def_item = next(gen_def, None)  # get_next_defitem()
        else:
            new_item = list(user_item)
            user_item = next(user_def, None)  # _get_next_useritem()
        if test_def == test_user:
            def_item = next(gen_def, None)  # get_next_defitem()
        # the last item can be a command; if so, get the description
        # add the description as a new last item; if not present, add an empty string
        # so now we get one column more
        menu_desc = dict(menu_commands.values())
        int_desc = dict(internal_commands.values())
        test = new_item[-2]
        if test in menu_desc:
            new_item[-1] = menu_desc[test]
        elif test in int_desc:
            new_item[-1] = int_desc[test]
        elif test.startswith('IDM_BUFFER'):
            new_item[-1] = "Switch to buffer " + str(int(test[-1]) + 1)
        shortcuts[num] = new_item
    return shortcuts, contexts_list


def add_extra_attributes(win):
    """define plugin-specific variables
    """
    # context en commando hebben hier geen relatie
    win.contextslist = win.otherstuff['contexts']
    actionslist = [(x, y[0], y[1]) for x, y in win.otherstuff['menucommands'].items()]
    actionslist += [(x, y[0], y[1]) for x, y in win.otherstuff['internal_commands'].items()]
    win.commandskeys = [x for x, y, z in actionslist] + ['']
    win.commandslist = [y for x, y, z in actionslist] + ['']
    win.contextactionsdict = {}
    win.descriptions = {y: z for x, y, z in actionslist}
    win.keylist.append('Movement')


def savekeys(parent):
    """schrijf de gegevens terug

    voorlopig nog niet mogelijk
    aangepaste keys samenstellen tot een user.shortcuts statement en dat
    invoegen in SciTEUser.properties
    waren er niet nog meer mogelijkheden? Ja: menu.language en command.shortcut
    """

# for use in python shell
# import scikeys
# import types
# page = types.SimpleNamespace(settings={'SCI_GLBL': '/usr/share/scite/SciTEGlobal.properties',
#                                        'SCI_USER': '/home/albert/.SciTEUser.properties',
#                                        'SCI_CMDS': '/usr/share/scite/CommandValues.html',
#                                        'SCI_DOCS': '/usr/share/scite/SciTEDoc.html',
#                                        'SCI_SRCE': '/home/albert/Downloads/scite538.tgz'})}
# scikeys.build_data(page)
