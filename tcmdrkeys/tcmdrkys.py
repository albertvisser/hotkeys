# -*- coding: utf-8 -*-

from __future__ import print_function
import os
## import datetime
from xml.etree import ElementTree as ET
import csv
import shutil

def keymods(x):
    """hulp bij omzetten wincmd.ini definitie in standaard definitie
    """
    m = {'A': 'Alt','C':'Ctrl','S':'Shift', 'W': 'Win'}
    if x == "NUM +":
        y = ''
        keyc = x
    else:
        y = x.split('+', 1)
        keyc = y[-1]
    keyc = keyc.replace(" ","").capitalize()
    if len(y) > 1:
        mods = [z[0] for z in y[0]]
        keyc = ' + '.join((keyc,''.join(mods)))
    return keyc

def keymods2(x):
    """hulp bij omzetten keyboard.txt definitie in standaard definitie
    """
    extra = ""
    if x[-1] == "+":
        x = x[:-1]
        extra = "+"
    mods = ""
    h = x.split("+",1)
    while len(h) > 1:
        if h[0] in ('SHIFT','ALT','CTRL'):
            mods += h[0][0]
        h = h[1].split("+",1)
    keyc = h[0].replace(" ","").capitalize() + extra
    if mods != "":
        keyc = ' + '.join((keyc,mods))
    return keyc

def keyboardtext(root):
    """definities uit keyboard.txt omzetten in standaard definities
    """
    data = []
    i = 0
    ky = []
    join_keys = False
    with open(os.path.join(root,'KEYBOARD.TXT')) as f_in:
        temp = f_in.readlines()
    for x in temp[6:]:
        x = x.rstrip()
        if x == "":
            break
        ## if len(x) < 24:
            ## continue
        deel1 = x[:23].strip()
        deel2 = x[23:].strip()
        if deel1 == '':
            ky_desc += " " + deel2
        elif join_keys:
            join_keys = False
            ky_desc += " " + deel2
            ky[1] = deel1
        else:
            if len(ky) > 0:
                for k in ky:
                    h = k.rsplit('+',1)
                    if '/' in h[-1] and not h[-1].endswith('/'):
                        hlp = h[-1].split('/')
                        for it in hlp:
                            data.append((keymods2('+'.join((h[0], it))), ky_desc))
                    else:
                        data.append((keymods2(k), ky_desc))
            ky_desc = deel2
            if " or " in deel1:
                ky = deel1.split(" or ")
                s2 = "+".join(ky[0].split("+")[:-1])
                if s2 != "":
                    for y in enumerate(ky[1:]):
                        ky[y[0]+1] = "+".join((s2,y[1]))
            elif deel1.endswith(" or"):
                ky = [deel1[:-3],""]
                join_keys = True
            else:
                ky = [deel1,]
            ## print ky,ky_desc
    if len(ky) > 0:
        for k in ky:
            h = k.rsplit('+',1)
            if '/' in h[-1] and not h[-1].endswith('/'):
                hlp = h[-1].split('/')
                for it in hlp:
                    data.append((keymods2('+'.join((h[0], it))), ky_desc))
            else:
                data.append((keymods2(k), ky_desc))
    ## f = open("keyboard_keys.txt","w")
    ## for x,y in data:
        ## f.write("%s:: %s\n" % (x,y))
    ## f.close()
    return data

def defaultcommands(root):
    """definities uit totalcmd.inc omzetten in standaard definites

    geeft commandonamen en omschrijvingen terug in dictionaries met commandonummer
    als sleutel
    """
    omsdict = {'': "no command available"}
    cmdict = {'': ''}
    with open(os.path.join(root,'TOTALCMD.INC')) as _in:
        for x in _in:
            h = x.strip()
            if h == '' or h[0] == '[' or h[0] == ';':
                continue
            cm_naam, rest = h.split('=',1)
            cm_num, cm_oms = rest.split(';',1)
            if int(cm_num) > 0:
                cmdict[cm_num] = cm_naam
                omsdict[cm_naam] = cm_oms # c[1] is omschrijving
    return cmdict, omsdict

def usercommands(root, cmdict=None, omsdict=None):
    """definities uit usercmd.ini omzetten in standaard definities

    vult cmdict en omsdict aan en retourneert ze
    """
    if cmdict is None:
        cmdict = {}
    if omsdict is None:
        omsdict = {}
    s0 = ""
    with open(os.path.join(root,"usercmd.ini")) as _in:
        for x in _in:
            if x.startswith("["):
                if s0 != "":
                    omsdict[s0] = c1
                s0 = x[1:].split("]")[0]
                c1 = ""
            elif x.startswith("cmd") and c1 == "":
                c1 = x.strip().split("=")[1]
            elif x.startswith("menu"):
                c1 = x.strip().split("=")[1]
        omsdict[s0] = c1
    ## print "na lezen usercmd.ini",datetime.datetime.today()
    ## f = open("cmdict.txt","w")
    ## for x in cmdict:
        ## f.write("%s:: %s\n" % (x,cmdict[x]))
    ## f.close()
    ## f = open("omsdict.txt","w")
    ## for x in omsdict:
        ## f.write("%s:: %s\n" % (x,omsdict[x]))
    ## f.close()
    return cmdict,omsdict

def defaultkeys(root):
    """definities lezen uit TC_hotkeys.csv (mijn eigen omzetter - in plaats van die
    die bij Ultra TC Editors meekomt
    """
    data = []
    ## for x in file(os.path.join(root,"tc default hotkeys.hky")):
        ## if x[0] == ";":
            ## continue
        ## elif "=" in x:
            ## y = x[:-1].split("=")
            ## #~ print y
            ## for z in y[1:]:
                ## #~ print z
                ## q = z.split(" + ")
                ## q[-1] = q[-1].replace(" ","")
                ## if len(q) == 1:
                    ## key = q[0].capitalize()
                ## else:
                    ## key = "".join([w.strip()[0] for w in q[:-1]])
                    ## key = " + ".join((q[-1].capitalize(),key))
                ## #~ print datakey
                ## data.append((key,y[0]))
    ## #~ f = open("defaultkeys.txt","w")
    ## #~ for x,y in data:
    ## #~     f.write("%s:: %s\n" % (x,y))
    ## #~ f.close()
    try:
        rdr = csv.reader(open(os.path.join(root,"TC_hotkeys.csv"), 'r'))
    except IOError:
        rdr = []
    for row in rdr:
        data.append((row[0], row[1]))
        ## data = [(row[0],row[1]) for row in rdr]
    return data

def userkeys(root):
    """user key definities uit wincmd.ini lezen
    """
    data = []
    in_user = in_win = False
    with open(os.path.join(root,"wincmd.ini")) as f_in:
        for x in f_in:
            x = x.rstrip()
            y = x.split("=")
            if in_user:
                if x.startswith("["):
                    in_user = False
                else:
                    data.append(y)
            elif in_win:
                if x.startswith("["):
                    in_win = False
                else:
                    if '+' in y[0]:
                        y[0] = 'W' + y[0]
                    else:
                        y[0] = 'W+' + y[0]
                    data.append(y)
            elif x.startswith("[Shortcuts]"):
                in_user = True
            elif x.startswith("[ShortcutsWin]"):
                in_win = True
    return data

def readkeys(data):
    """lees key definities vanuit tckeys object

    geeft dictionaries terug met commando's, omschrijvingen en listbox data
    """
    cl = TCKeys(*data)
    cl.read()
    defkeys = cl.defkeys
    ## kys = cl.keydict.keys()
    ## kys.sort()
    data = {}
    for ix, hotkey in enumerate(sorted(cl.keydict.keys())):
        try:
            ky, mod = hotkey.split(" + ")
        except ValueError:
            ky,mod = hotkey,""
        srt, desc, cmd = cl.keydict[hotkey]
        data[ix] = (ky, mod, srt, cmd, desc)
    return cl.cmdict, cl.omsdict, cl.defkeys, data

def savekeys(pad, data):
    """schrijft de listbox data terug via een tckeys object
    """
    cl = TCKeys(pad)
    for ky, mod, srt, cmd, desc in data.values():
        hotkey = " + ".join((ky, mod)) if mod != '' else ky
        cl.keydict[hotkey] = (srt, desc, cmd)
    ## for x,y in cl.keydict.items():
        ## print(x,y)
    cl.write()

class Settings(object):
    def __init__(self, fn):
        self.fn = fn
        self.namen = ['TC_PAD','UC_PAD','CI_PAD','KB_PAD','HK_PAD','LANG','RESTART']
        self.paden = ['','','','','']
        self.lang = ''
        self.restart = ''
        if not os.path.exists(self.fn):
            return
        with open(self.fn) as _in:
            for x in _in:
                if x.strip() == "" or x.startswith('#'):
                    continue
                naam,waarde = x.strip().split('=')
                try:
                    ix = self.namen.index(naam)
                except ValueError:
                    ix = -1
                if 0 <= ix <= 4:
                    self.paden[ix] = waarde
                elif ix == 5:
                    self.lang = waarde
                elif ix == 6:
                    self.restart = waarde
        self.tcpad, self.ucpad, self.cipad, self.ktpad, self.hkpad = self.paden
        ## for x in reversed(self.paden):
            ## if x == '':
                ## self.paden.pop()
            ## else:
                ## break

    def set(self, item, value):
        items = []
        argnamen = ("tcpad","ucpad","cipad","ktpad","hkpad")
        arg_found = False
        for i,x in enumerate(argnamen):
            if item == x:
                item = self.namen[i]
                print(item, i)
                self.paden[i] = value
                arg_found = True
                break
        if not arg_found and item == "paden":
            if isinstance(value, list) and len(value) == 6:
                self.paden = value[:-1]
                self.restart = value[-1]
                arg_found = True
            else:
                raise ValueError("Tcksettings needs list with 6 'paden'")
        if not arg_found:
            for i, x in enumerate(self.namen):
                if item.upper() == x:
                    if i <= 4:
                        self.paden[i] = value
                    elif i == 5:
                        self.lang = value
                    elif i == 6:
                        self.restart = value
                    arg_found = True
                    break
        if not arg_found:
            raise ValueError("Tcksettings object doesn't know about '%s'" % item)
        new = self.fn
        old = new + ".bak"
        shutil.copyfile(new, old)
        with open(old) as ini, open(new, "w") as f:
            for x in ini:
                if "=" in x:
                    test = x.split('=')[0]
                    for ix, naam in enumerate(self.namen):
                        if test == naam:
                            if ix == 5:
                                y = self.lang
                            elif ix == 6:
                                y = self.restart
                            else:
                                y = self.paden[ix]
                            f.write("{}={}\n".format(self.namen[ix], y))
                            break
                else:
                    f.write(x)
        self.tcpad, self.ucpad, self.cipad, self.ktpad, self.hkpad = self.paden

class TCKeys(object):
    """stel gegevens samen vanuit de diverse bestanden

    kijkt naar de aangegeven locaties tenzij ze niet zijn ingesteld,
    dan wordt de standaard programma locatie gebruikt
    """
    def __init__(self, *tc_dir):
        self.ucloc = self.ciloc = self.ktloc = self.hkloc = ''
        try:
            self.tcloc = tc_dir[0] # plaats van wincmd.ini
        except IndexError:
            self.tcloc = "C:\totalcmd" # default
        try:
            self.ucloc = tc_dir[1] # plaats van usercmd.ini
        except IndexError:
            pass
        if not self.ucloc:
            self.ucloc = self.tcloc
        try:
            self.ciloc = tc_dir[2] # plaats van totalcmd.inc
        except IndexError:
            pass
        if not self.ciloc:
            self.ciloc = self.tcloc
        try:
            self.ktloc = tc_dir[3] # plaats van keyboard.txt
        except IndexError:
            pass
        if not self.ktloc:
            self.ktloc = self.tcloc
        try:
            self.hkloc = tc_dir[4] # plaats van tc_hotkeys.csv
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
        cmdict, omsdict = defaultcommands(self.ciloc)
        self.cmdict, self.omsdict = usercommands(self.ucloc, cmdict, omsdict)
        defkeys = {}
        for x, y in defaultkeys(self.hkloc):
            defkeys[x] = self.cmdict[y].strip()
        self.keydict = {}
        for key, oms in keyboardtext(self.ktloc):
            if key in defkeys:
                cm = defkeys[key]
            else:
                cm = ""
                defkeys[key] = oms
                if key == "Backspace":
                    ## try:
                        del defkeys["Back"]
                    ## except KeyError:
                        ## pass
            self.keydict[key] = ("S", oms, cm)
        self.defkeys = defkeys
        ## f = open("defkeys.txt","w")
        ## for x in self.defkeys:
            ## f.write("%s:: %s\n" % (x,defkeys[x]))
        ## f.close()
        for key, action in userkeys(self.tcloc):
            k = keymods(key)
            self.keydict[k] = ("U", omsdict[action], action)

    def turn_into_xml(self):
        """zet de gegevens uit keydict om in xml en schrijft ze weg
        """
        kys = self.keydict.keys()
        kys.sort()
        root = ET.Element("keys")
        for x in kys:
            h = ET.SubElement(root,"hotkey",naam=x,soort=self.keydict[x][0])
            k = ET.SubElement(h,"cmd")
            k.text = self.keydict[x][2]
            k = ET.SubElement(h,"oms")
            k.text = self.keydict[x][1]
        tree = ET.ElementTree(root)
        tree.write(os.path.join(self.tcloc,"tcmdrkeys.xml"))

    def write(self):
        """schrijf de gegevens terug naar waar ze terecht moeten komen
        """
        shortcuts, shortcutswin = [], []
        for key, item in self.keydict.items():
            print(key, item)
            if item[0] != 'U':
                continue
            test = [x for x in reversed(key.split())]
            print(test)
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
                    win_geschreven = True
                    for newline in shortcutswin:
                        f_out.write(newline)
                if schrijfdoor:
                    f_out.write(line)
            if not shortcuts_geschreven and len(shortcuts) > 0:
                for newline in shortcuts:
                    f_out.write(newline)
            if not shortcuts_geschreven and len(shortcuts) > 0:
                for newline in shortcutswin:
                    f_out.write(newline)
