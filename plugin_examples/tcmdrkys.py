"""Hotkeys plugin for Total Commander - general code
"""
import os
import collections
import editor.gui
import editor.plugins.mergetool_shared as shared
from ..toolkit import toolkit
if toolkit == 'qt':
    from .mergetool_qt import MergeDialog
elif toolkit == 'wx':
    from .mergetool_wx import MergeDialog
DFLT_TCLOC = "C:/totalcmd"


def read_lines(fn):
    "return lines read from file"
    result = []
    if not os.path.exists(fn):
        fn = os.path.join(os.path.dirname(__file__), 'tc_fallback', os.path.basename(fn))
    try:
        with open(fn) as f_in:
            result = f_in.readlines()
    except UnicodeDecodeError:
        with open(fn, encoding='latin-1') as f_in:
            result = f_in.readlines()
    return result


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
            cm_naam, argsitem = cm_naam.split(' <', 1)
            cmdictitem['args'] = argsitem.split('>')[0].replace('> <', ', ')
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
               'Slash/Questionmark': '/', 'OEM_US\\|': '\\'}
    return convert.get(inp, inp)


def build_data(page):
    """implementation of generic function to build the keydef file

    zo geschreven komt her erop neer dat de te rebuilden gegevens in het match file zitten
    (want alleen de settings- en help files zijn niet voldoende)
    """
    # start bij loading the stuff we need for the dialog
    page.matchfile = os.path.join(os.path.dirname(__file__), 'tc_default_hotkeys_mapped.csv')
    page.keylist_data = defaultkeys(page.settings['KB_PAD'])
    # user defined keys (should be added to left list box)
    # page.keylist_data.update((userkeys(self.parent.settings['TC_PAD'])))
    page.cmdlist_data = defaultcommands(page.settings['CI_PAD'])
    # user commands (should be added to right list box)
    # usrdict, uomsdict = usercommands(self.parent.settings['UC_PAD'])
    # page.cmdlist_data.update({usrdict[y]: uomsdict[x] for x, y in usrdict.items()}
    page.matchlist_data = shared.load_matchdata(page.matchfile)

    ok = editor.gui.show_dialog(page, MergeDialog)
    if ok:
        shared.save_matchdata(page.tempdata, page.matchfile)
        shortcuts, ix = {}, 0
        for keytext, cmd in page.tempdata:
            key, mods = keytext.split(' ', 1)
            desc = page.cmdlist_data[cmd]['oms'] if cmd else page.keylist_data[(key, mods)]['oms']
            ix += 1
            shortcuts[ix] = (translate_keyname(key), mods, 'S', cmd, desc)
    else:
        # shortcuts = []
        return None
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
    win.cmdict = defaultcommands(win.settings['CI_PAD'])
    win.descriptions.update({x: y['oms'] for x, y in win.cmdict.items()})
    win.ucmdict = usercommands(win.settings['UC_PAD'])
    win.descriptions.update({x: y['oms'] for x, y in win.ucmdict.items()})
    win.defkeys = defaultkeys(win.settings['KB_PAD'])
    win.udefkeys = userkeys(win.settings['TC_PAD'])

    win.commandslist = list(win.cmdict.keys()) + list(win.ucmdict.keys())


def get_frameheight():
    """return standard height for the subscreen
    """
    return 110


def savekeys(parent):
    """schrijft de listbox data terug via een tckeys object
    """
    save_message = ('Press "OK" to build and save the keyboard definitions files\n'
                    'or "Cancel" to return to the main program')
    ok = editor.gui.show_cancel_message(parent, text=save_message)
    if not ok:
        return
    keydict = {}
    for val in parent.data.values():
        ky, mod, srt, cmd, desc = val
        hotkey = f"{ky} + {mod}" if mod != '' else ky
        keydict[hotkey] = (srt, desc, cmd)
        shortcuts, shortcutswin = [], []
        for key, item in keydict.items():
            ## print(key, item)
            if item[0] != 'U':
                continue
            test = [x for x in reversed(key.split())]
            ## print(test)
            if len(test) == 1:
                shortcuts.append(f'{test[0]}={item[2]}\n')
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
