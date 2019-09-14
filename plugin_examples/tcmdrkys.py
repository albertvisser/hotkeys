"""Hotkeys plugin for Total Commander - general code
"""
import os
import csv
import editor.gui
import editor.plugins.tcmdrkys_shared as shared
from ..toolkit import toolkit
if toolkit == 'qt':
    from .tcmdrkys_qt import TcMergeDialog
elif toolkit == 'wx':
    from .tcmdrkys_wx import TcMergeDialog
DFLT_TCLOC = "C:/totalcmd"


def keymods_old(x):
    """hulp bij omzetten wincmd.ini definitie in standaard definitie
    """
    if x == "NUM +":
        y = ''
        keyc = x
    else:
        y = x.split('+', 1)
        keyc = y[-1]
    keyc = keyc.replace(" ", "").capitalize()
    if len(y) > 1:
        mods = [z[0] for z in y[0]]
        keyc = ' + '.join((keyc, ''.join(mods)))
    return keyc


def buildcsv(page, showinfo=True):
    """implementation of generic function to build the csv file
    """
    if showinfo:
        ok = editor.gui.show_dialog(page, TcMergeDialog)
        if ok:
            shortcuts = page.tempdata
        else:
            shortcuts = []
    else:
        shortcuts = []
    return shortcuts, {}


def add_extra_attributes(win):
    """define stuff needed to make editing in the subscreen possible
    """
    win.keylist += ['Pause', 'Smaller/Greater', 'OEM_FR!']
    ## ['PAUSE', 'OEM_.', 'OEM_,', 'OEM_+', 'OEM_-', 'OEM_</>', 'OEM_US`~',
    ## 'OEM_US[{', 'OEM_US]}', 'OEM_US\\|', 'OEM_US;:', "OEM_US'" + '"',
    ## 'OEM_US/?', 'OEM_FR!']

    win.mag_weg = True
    win.newfile = win.newitem = False
    win.oldsort = -1
    win.idlist = win.actlist = win.alist = []
    ## paden = [win.settings[x][0] for x in PATHS[:4]] + [win.pad]
    ## self.cmdict, self.omsdict, self.defkeys, _ = readkeys(paden)
    win.descriptions = {}
    win.cmdict = shared.defaultcommands(win.settings['CI_PAD'])
    win.descriptions.update({x: y['oms'] for x, y in win.cmdict.items()})
    win.ucmdict = shared.usercommands(win.settings['UC_PAD'])
    win.descriptions.update({x: y['oms'] for x, y in win.ucmdict.items()})
    win.defkeys = shared.defaultkeys(win.settings['KB_PAD'])
    win.udefkeys = shared.userkeys(win.settings['TC_PAD'])

    win.commandslist = list(win.cmdict.keys()) + list(win.ucmdict.keys())


def get_frameheight():
    """return standard height for the subscreen
    """
    return 110


def savekeys(parent):
    """schrijft de listbox data terug via een tckeys object
    """
    keydict = {}
    for val in parent.data.values():
        ky, mod, srt, cmd, desc = val
        hotkey = " + ".join((ky, mod)) if mod != '' else ky
        keydict[hotkey] = (srt, desc, cmd)
        shortcuts, shortcutswin = [], []
        for key, item in keydict.items():
            ## print(key, item)
            if item[0] != 'U':
                continue
            test = [x for x in reversed(key.split())]
            ## print(test)
            if len(test) == 1:
                shortcuts.append('{}={}\n'.format(test[0], item[2]))
            elif 'W' in test[0]:
                if 'W+' in test[0]:
                    test[0] = test[0].replace('W+', '')
                else:
                    test[0] = test[0].replace('W', '')
                shortcutswin.append('{}={}\n'.format(''.join(test), item[2]))
            else:
                shortcuts.append('{}={}\n'.format(''.join(test), item[2]))

    fn = parent.settings['TC_PAD']
    fno = fn + ".bak"
    os.rename(fn, fno)
    schrijfdoor, shortcuts_geschreven, win_geschreven = True, False, False
    with open(fno) as f_in, open(fn, 'w') as f_out:
        for line in f_in:
            if not schrijfdoor and line.strip()[0] == "[":
                schrijfdoor = True
            elif line.strip() == '[Shortcuts]':
                f_out.write(line)
                schrijfdoor = False
                shortcuts_geschreven = True
                for newline in shortcuts:
                    f_out.write(newline)
            elif line.strip() == '[ShortcutsWin]':
                f_out.write(line)
                schrijfdoor = False
                ## win_geschreven = True
                for newline in shortcutswin:
                    f_out.write(newline)
            if schrijfdoor:
                f_out.write(line)
        if not shortcuts_geschreven and shortcuts:
            for newline in shortcuts:
                f_out.write(newline)
        if not win_geschreven and shortcuts:
            for newline in shortcutswin:
                f_out.write(newline)
