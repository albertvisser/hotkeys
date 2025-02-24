"""basic plugin for tool using a gtkaccel_map
"""
import os.path
import string
from .read_gtkaccel import read_keydefs_and_stuff
from ..gui import get_file_to_open, get_file_to_save, show_dialog
from .gtkaccel_keys_gui import AccelCompleteDialog
import editor.plugins.gtkaccel_keys_data as dml

settname = ''
FDESC = ("File containing keymappings", "File containing command descriptions")


def _translate_keyname(inp):
    """map key names in settings file to key names in HotKeys
    """
    convert = {'Equal': '=', 'Escape': 'Esc', 'Delete': 'Del', 'Return': 'Enter',
               'Page_up': 'PgUp', 'Page_down': 'PgDn'}
    return convert.get(inp, inp)


def build_data(settnames, page, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het keydef bestand
    """
    shortcuts = {}
    kbfile, descfile = names2filenames(settnames, page, showinfo)
    if not kbfile and not descfile:
        return {}, {}
    stuffdict = read_keydefs_and_stuff(kbfile)
    keydefs = stuffdict.pop('keydefs')
    actions = stuffdict['actions']
    omsdict = stuffdict['descriptions']
    # omsdict is uit de accelmap afgeleid waar gewoonlijk geen omschrijvingen in staan.
    # Bij opnieuw opbouwen eerst kijken of deze misschien al eens zijn opgeslagen
    # De bestandsnaam kan als een extra setting worden opgenomen - dus: is er zo'n
    # setting bekend, dan dit bestand lezen
    # hier dan een GUI tonen waarin de omschrijvingen per command kunnen worden in/aangevuld
    # actions in de eerste kolom, descriptions in de tweede
    if descfile:
        msg, descdict = dml.read_data(descfile, omsdict)
        if msg:
            print(msg)
        elif showinfo:
            page.dialog_data = {'descdict': descdict, 'actions': actions}  # , 'omsdict': omsdict}
            if show_dialog(page, AccelCompleteDialog):
                result = page.dialog_data
                if result != descdict:
                    reverse_lookup = {'/'.join(y): x for x, y in actions.items()}
                    for key, value in result.items():
                        omsdict[reverse_lookup[key]] = value
                    dml.write_data(descfile, omsdict)

    lastkey = 0
    for key, mods, command in keydefs:
        lastkey += 1
        context, action = actions[command]
        description = omsdict[command]
        shortcuts[lastkey] = (_translate_keyname(key), mods, context, action, description)

    return shortcuts, stuffdict


def names2filenames(settnames, page, showinfo):
    """get the pathnames of the setting files and create them if necessary

    currently only two settings will be processed
    """
    for ix, name in enumerate(settnames[:2]):
        try:
            initial = page.settings[name]
        except KeyError:
            initial = ''
        if showinfo:
            oms = ' - '.join((page.captions['C_SELFIL'], FDESC[ix]))
            if not initial:
                initial = os.path.dirname(__file__)
                fname = get_file_to_save(page.gui, oms=oms, start=initial)
            else:
                fname = get_file_to_open(page.gui, oms=oms, start=initial)
            if fname and fname != initial:
                page.settings[name] = fname
                page.settings["extra"][name] = FDESC[ix]
        else:
            fname = initial
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
    win.descriptions = win.otherstuff['descriptions']
    try:
        win.otherslist = win.otherstuff['others']
    except KeyError:
        pass
    else:
        win.othersdict = win.otherstuff['othercontext']
        win.otherskeys = win.otherstuff['otherkeys']
