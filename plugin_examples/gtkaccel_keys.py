"""basic plugin for tool using a gtkaccel_map

delivers:
actions: mapping van een volgnummer/code op een tuple van "sectie" en "commando"
actionscontext: mapping van een sectie op een list van commando's
contexts: list van mogelijke contexts (keys van actionscontext)
descriptions: mapping van een volgnummer/code keys van actions) op een omschrijving
-- dit is de tabel die ik niet uit de tool settings kan afleiden en dus apart moet opslaan
keydefs: list van tuples bestaande uit key, modifiers, commando (key van actions)

extra bij Dia:
others: mapping van volgnummer/code op ebuilden tuple van type contextmenu (?) en actie
otherkeys: list van tuples a la keydefs
othercontext: mapping a la actioncontext (mag nog een keer onderverdeeld)
"""
import collections
import os.path
import string
from ..gui import get_file_to_open, get_file_to_save
# from ..gui import show_dialog
# from .gtkaccel_keys_gui import AccelCompleteDialog
# import editor.plugins.gtkaccel_keys_data as dml

settname = ''
FDESC = ("File containing keymappings", "File containing command descriptions")
KEYDEF = 'gtk_accel_path'
conversion_map = (('bracketright', ']'),
                  ('bracketleft', '['),
                  ('less', '<'),
                  ('plus', '+'),
                  ('minus', '-'),
                  ('comma', ','),
                  ('grave', '`'),
                  ('period', '.'),
                  ('greater', '>'),
                  ('semicolon', ';'),
                  ('backslash', '\\'),
                  ('KP_', 'Num'),
                  ('Add', '+'),
                  ('Subtract', '-'))


def _translate_keyname(inp):
    """map key names in settings file to key names in HotKeys
    """
    convert = {'Equal': '=', 'Escape': 'Esc', 'Delete': 'Del', 'Return': 'Enter',
               'Page_up': 'PgUp', 'Page_down': 'PgDn'}
    return convert.get(inp, inp)


def build_data(settnames, page):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het keydef bestand
    """
    olddescs = page.otherstuff['descriptions']
    shortcuts = {}
    kbfile, descfile = names2filenames(settnames, page)
    if not kbfile and not descfile:
        return {}, {}
    stuffdict = read_keydefs_and_stuff(kbfile)
    keydefs = stuffdict.pop('keydefs')
    actions = stuffdict['actions']
    compare_descriptions(stuffdict['descriptions'], olddescs) # worden deze ge-update?
    stuffdict['olddescs'] = olddescs
    omsdict = stuffdict['descriptions']
    # omsdict is uit de accelmap afgeleid waar gewoonlijk geen omschrijvingen in staan.
    # Bij opnieuw opbouwen eerst kijken of deze misschien al eens zijn opgeslagen
    # De bestandsnaam kan als een extra setting worden opgenomen - dus: is er zo'n
    # setting bekend, dan dit bestand lezen
    # hier dan een GUI tonen waarin de omschrijvingen per command kunnen worden in/aangevuld
    # actions in de eerste kolom, descriptions in de tweede
    # stuffdict['descdict'] = dml.read_data(descfile, omsdict) if descfile else {}
    # if descfile:
    #     msg, descdict = dml.read_data(descfile, omsdict)
    #     if msg:
    #         print(msg)
    #     page.dialog_data = {'descdict': descdict, 'actions': actions}  # , 'omsdict': omsdict}
    #     if show_dialog(page, AccelCompleteDialog):
    #         result = page.dialog_data
    #         if result != descdict:
    #             reverse_lookup = {'/'.join(y): x for x, y in actions.items()}
    #             for key, value in result.items():
    #                 omsdict[reverse_lookup[key]] = value
    #             dml.write_data(descfile, omsdict)

    lastkey = 0
    for key, mods, command in keydefs:
        lastkey += 1
        context, action = actions[command]
        description = omsdict[command]
        shortcuts[lastkey] = (_translate_keyname(key), mods, context, action, description)

    return shortcuts, stuffdict


def read_keydefs_and_stuff(filename):
    """Get data from file
    """
    keydefs, actions, others = readfile(filename)
    result = {'keydefs': keydefs}

    actions, actiondict, descriptions = expand_actions(actions)
    contextlist = list(actiondict)
    result.update({'actions': actions, 'actionscontext': actiondict,
                   'contexts': contextlist, 'descriptions': descriptions})
    if others:
        otheractions, othersdict, otherkeys = expand_others(others)
        result.update({'others': otheractions, 'othercontext': othersdict,
                       'otherkeys': otherkeys})
    return result


def readfile(filename):
    """ read and parse the accel file
    """
    keydefs = []
    actions, others = {}, []
    new_id = 0
    with open(filename) as _in:
        for line in _in:
            ## colon_ed = False
            if KEYDEF in line:
                # if line.startswith(';'):
                #     ## colon_ed = True  # don't know what this means: line ended in colon
                #     line = line[1:].strip()
                data = line.rsplit(')', 1)[0].split(KEYDEF, 1)[1].strip().split('" "')
                if len(data) != len(['two', 'items']):
                    print(line)
                    print('contains more/less that 2 items, what to do?')
                    continue
                name = data[0].lstrip('"')
                key = data[-1].rstrip('"')
                ## commented = coloned
                ## name, key = [x.replace('"', '') for x in data[-2:]]
                if '<Actions>' not in name:
                    others.append((name, key))
                    continue
                name = name.replace('<Actions>', '')
                new_id += 1
                actions[new_id] = name
                ## key = key.replace(')', '')
                if key:
                    key, mods = parse_actiondef(key)
                    keydefs.append((key, mods, new_id))
    return keydefs, actions, others


def parse_actiondef(key):
    "extract modifiers from action definition"
    test = key.split('>')
    key = test[-1]
    for x, y in conversion_map:
        key = key.replace(x, y)
    key = key.capitalize()
    mods = ''
    if len(test) > 1:
        if '<Primary' in test:
            mods += 'C'
        if '<Alt' in test:
            mods += 'A'
        if '<Shift' in test:
            mods += 'S'
    return key, mods


def expand_actions(actions):
    "extract ... from action definition"
    actiondict = collections.defaultdict(list)
    new_actions = {}  # collections.OrderedDict()
    descriptions = {}  # collections.OrderedDict()
    for key, value in actions.items():
        context, action = value.lstrip('/').split('/', 1)
        actiondict[context].append(action)
        new_actions[key] = (context, action)
        descriptions[key] = ''
    return new_actions, actiondict, descriptions


def expand_others(others):
    "extract ... from non-action definition"
    actiondict = collections.defaultdict(list)
    actions = {}
    actionkeys = []
    keyval = 0
    for key, value in others:
        context, action = key.lstrip('/').split('/', 1)
        actiondict[context].append(action)
        keyval += 1
        actions[keyval] = (context, action)
        if value:
            actionkeys.append((value, keyval))
    return actions, actiondict, actionkeys


def compare_descriptions(cmddict, olddescs):
    "identify and keep differing descriptions"
    for key, value in cmddict.items():
        if key in olddescs:
            if value == olddescs[key]:
                olddescs.pop(key)
            elif value == '':
                cmddict[key] = olddescs.pop(key)
    return cmddict, olddescs


def names2filenames(settnames, page):
    """get the pathnames of the setting files and create them if necessary

    currently only two settings will be processed
    """
    for ix, name in enumerate(settnames[:2]):
        try:
            initial = page.settings[name]
        except KeyError:
            initial = ''
        oms = ' - '.join((page.captions['C_SELFIL'], FDESC[ix]))
        if not initial:
            initial = os.path.dirname(__file__)
            fname = get_file_to_save(page.gui, oms=oms, start=initial)
        else:
            fname = get_file_to_open(page.gui, oms=oms, start=initial)
        if fname and fname != initial:
            page.settings[name] = fname
            page.settings["extra"][name] = FDESC[ix]
        if ix == 0:
            kbfile = fname
            if not fname:
                return '', ''
        else:  # if ix == 1:  enige andere mogelijkheid
            descfile = fname
    return kbfile, descfile


def add_extra_attributes(win):
    """specifics for extra panel
    """
    # print(win.__dict__)
    win.keylist += ['Num' + x for x in string.digits] + ['>', '<']
    win.contextslist = win.otherstuff['contexts']
    win.contextactionsdict = win.otherstuff['actionscontext']
    win.actionslist = win.otherstuff['actions']
    win.descriptions = win.otherstuff['descriptions']  # mapping van commando's op descriptions
    win.mydescs = win.otherstuff.get('olddescs', {})   # overgebleven afwijkende beschrijvingen
    try:
        win.otherslist = win.otherstuff['others']
    except KeyError:
        pass
    else:
        win.othersdict = win.otherstuff['othercontext']
        win.otherskeys = win.otherstuff['otherkeys']
