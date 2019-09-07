"""Hotkeys plugin for Total Commander - general code
"""
import os
import collections
from xml.etree import ElementTree as ET
DFLT_TCLOC = "C:/totalcmd"
from .tcmdrkys_gui import send_mergedialog
from .tcmdrkys_shared import PATHS, read_lines, defaultkeys, defaultcommands


def keymods(x):
    """hulp bij omzetten wincmd.ini definitie in standaard definitie
    """
    ## m = {'A': 'Alt', 'C': 'Ctrl', 'S': 'Shift', 'W': 'Win'}
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


def usercommands(root):
    """definities uit usercmd.ini omzetten in een Python dict compatible met die
    voor de standaard commando's
    """
    ucmdict = collections.DefaultDict(dict)
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


def readkeys(data):
    """lees key definities vanuit tckeys object

    geeft dictionaries terug met commando's, omschrijvingen en listbox data
    """
    cl = TCKeys(*data)
    cl.read()
    ## defkeys = cl.defkeys
    ## kys = cl.keydict.keys()
    ## kys.sort()
    data = {}
    for ix, hotkey in enumerate(sorted(cl.keydict.keys())):
        try:
            ky, mod = hotkey.split(" + ")
        except ValueError:
            ky, mod = hotkey, ""
        srt, desc, cmd = cl.keydict[hotkey]
        data[ix] = (ky, mod, srt, cmd, desc)
    return cl.cmdict, cl.omsdict, cl.defkeys, data


def savekeys(parent):
    """schrijft de listbox data terug via een tckeys object
    """
    paden = [parent.settings[x] for x in PATHS]
    cl = TCKeys(*paden)
    for val in parent.data.values():
        ky, mod, srt, cmd, desc = val
        hotkey = " + ".join((ky, mod)) if mod != '' else ky
        cl.keydict[hotkey] = (srt, desc, cmd)
    ## for x,y in cl.keydict.items():
        ## print(x,y)
    cl.write()


class TCKeys(object):
    """stel gegevens samen vanuit de diverse bestanden

    kijkt naar de aangegeven locaties tenzij ze niet zijn ingesteld,
    dan wordt de standaard programma locatie gebruikt
    """
    def __init__(self, *tc_dir):
        self.ucloc = self.ciloc = self.ktloc = self.hkloc = ''
        try:
            self.tcloc = tc_dir[0]  # plaats van wincmd.ini
        except IndexError:
            self.tcloc = DFLT_TCLOC
        try:
            self.ucloc = tc_dir[1]  # plaats van usercmd.ini
        except IndexError:
            pass
        if not self.ucloc:
            self.ucloc = self.tcloc
        try:
            self.ciloc = tc_dir[2]  # plaats van totalcmd.inc
        except IndexError:
            pass
        if not self.ciloc:
            self.ciloc = self.tcloc
        try:
            self.ktloc = tc_dir[3]  # plaats van keyboard.txt
        except IndexError:
            pass
        if not self.ktloc:
            self.ktloc = self.tcloc
        try:
            self.hkloc = tc_dir[4]  # plaats van tc_hotkeys.csv
        except IndexError:
            pass
        if not self.hkloc:
            self.hkloc = self.tcloc
        self.keydict = {}

    def read(self):
        """leest de gegevens uit de bestanden

        de gegevens worden omgezet in dictionaries
        die attributen zijn van deze class
        """
        self.cmdict = defaultcommands(self.ciloc)
        with open("cmdict.txt", "w") as _out:
            print(self.cmdict, file=_out)
        ucmdict = usercommands(self.ucloc)
        with open("usercmdict.txt", "w") as _out:
            print(ucmdict, file=_out)
        self.omsdict = {}
        # deze zijn hier aangevuld met de zaken uit usercommands
        defkeys = {}
        for x, y in defaultkeys(self.hkloc):
            defkeys[x] = self.cmdict[y].strip()
        # de nummers die ik in y wil hebben zitten in de vierde kolom alleen dan zijn het de
        # strings m.a.w. dit kan helemaal niet
        self.keydict = {}
        for key, oms in keyboardtext(self.ktloc):   # UNDEF keyboardtext - should be a function
            ## print(key, oms)
            if key in defkeys:
                cm = defkeys[key]
            else:
                cm = ""
                defkeys[key] = oms
                if key == "Backspace":
                    try:
                        del defkeys["Back"]
                    except KeyError:
                        pass
            self.keydict[key] = ("S", oms, cm)
        self.defkeys = defkeys
        ## f = open("defkeys.txt","w")
        ## for x in self.defkeys:
            ## f.write("%s:: %s\n" % (x,defkeys[x]))
        ## f.close()
        for key, action in userkeys(self.tcloc):
            k = keymods(key)
            self.keydict[k] = ("U", self.omsdict[action], action)

    def turn_into_xml(self):
        """zet de gegevens uit keydict om in xml en schrijft ze weg
        """
        kys = self.keydict.keys()
        kys.sort()
        root = ET.Element("keys")
        for x in kys:
            h = ET.SubElement(root, "hotkey", naam=x, soort=self.keydict[x][0])
            k = ET.SubElement(h, "cmd")
            k.text = self.keydict[x][2]
            k = ET.SubElement(h, "oms")
            k.text = self.keydict[x][1]
        tree = ET.ElementTree(root)
        tree.write(os.path.join(self.tcloc, "tcmdrkeys.xml"))

    def write(self):
        """schrijf de gegevens terug naar waar ze terecht moeten komen
        """
        shortcuts, shortcutswin = [], []
        for key, item in self.keydict.items():
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

        fn = os.path.join(self.tcloc, 'wincmd.ini')
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


def buildcsv(page, showinfo=True):
    """implementation of generic function to build the csv file
    """
    if showinfo:
        ok = send_mergedialog(page)
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
