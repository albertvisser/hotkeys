"""basic plugin for tool using a gtkaccel_map - PyQt5 version
"""
import os.path
## import sys
import collections
## import functools
import string
import pdb
from .read_gtkaccel import read_keydefs_and_stuff
from ..gui import get_file_to_open, get_file_to_save, show_dialog
from .gtkaccel_keys_gui import AccelCompleteDialog
import editor.plugins.gtkaccel_keys_csv as dml

settname = ''


def _translate_keyname(inp):
    """map key names in settings file to key names in HotKeys
    """
    convert = {'Equal': '=', 'Escape': 'Esc', 'Delete': 'Del', 'Return': 'Enter',
               'Page_up': 'PgUp', 'Page_down': 'PgDn'}
    if inp in convert:
        out = convert[inp]
    else:
        out = inp
    return out


def buildcsv(settnames, page, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand
    """
    shortcuts = collections.OrderedDict()
    fdesc = ("File containing keymappings", "File containing command descriptions")
    ## pdb.set_trace()
    for ix, name in enumerate(settnames):
        try:
            initial = page.settings[name]
        except KeyError:
            initial = ''
        if showinfo:
            oms = ' - '.join((page.captions['C_SELFIL'], fdesc[ix]))
            if not initial:
                initial = os.path.dirname(__file__)
                fname = get_file_to_save(page.gui, oms=fdesc[ix], start=initial)
            else:
                fname = get_file_to_open(page.gui, oms=fdesc[ix], start=initial)
            if fname and fname != initial:
                page.settings[name] = fname
                page.settings["extra"][name] = fdesc[ix]
        else:
            fname = initial
        if ix == 0:
            kbfile = fname
            if not fname:
                return {}, {}
        elif ix == 1:
            descfile = fname

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
                omsdict = page.dialog_data
            if omsdict != descdict:
                dml.write_data(descfile, omsdict)

    # als er sprake is van others dan ook deze meenemen (Dia)
    lastkey = 0
    for key, mods, command in keydefs:
        lastkey += 1
        context, action = actions[command]
        description = omsdict[command]
        shortcuts[lastkey] = (_translate_keyname(key), mods, context, action, description)

    return shortcuts, stuffdict


def add_extra_attributes(win):
    """specifics for extra panel
    """
    ## print(win.__dict__)
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
