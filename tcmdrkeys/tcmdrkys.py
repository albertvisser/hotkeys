# -*- coding: latin-1 -*-
import os
## import datetime
from xml.etree import ElementTree as ET
import csv

def keymods(x):
    m = {'A': 'Alt','C':'Ctrl','S':'Shift'}
    if x == "NUM +":
        y = ''
        keyc = x
    else:
        y = x.split('+',1)
        keyc = y[-1]
    keyc = keyc.replace(" ","").capitalize()
    if len(y) > 1:
        mods = [z[0] for z in y[0]]
        keyc = ' + '.join((keyc,''.join(mods)))
    return keyc

def keymods2(x):
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
    data = []
    i = 0
    ky = []
    join_keys = False
    try:
        for x in file(os.path.join(root,'keyboard.txt')):
            if i < 6:
                i += 1
                continue
            if x.strip() == "Command Line: Keys":
                break
            if len(x) < 24:
                continue
            deel1 = x[:23].strip()
            deel2 = x[23:].strip()
            if deel1.strip() == '':
                ky_desc = " ".join((ky_desc,deel2))
            elif join_keys:
                join_keys = False
                ky_desc = " ".join((ky_desc,deel2))
                ky[1] = deel1
            else:
                if len(ky) > 0:
                    for k in ky:
                        data.append((keymods2(k),ky_desc))
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
    except IOError:
        pass
    if len(ky) > 0:
        for k in ky:
            data.append((keymods2(k),ky_desc))
    ## f = open("keyboard_keys.txt","w")
    ## for x,y in data:
        ## f.write("%s:: %s\n" % (x,y))
    ## f.close()
    return data

def defaultcommands(root):
    omsdict = {'': "no command available"}
    cmdict = {'': ''}
    try:
        for x in file(os.path.join(root,'totalcmd.inc')):
            h = x.strip()
            if h == '' or h[0] == '[' or h[0] == ';':
                continue
            cm_naam, rest = h.split('=',1)
            cm_num, cm_oms = rest.split(';',1)
            if int(cm_num) > 0:
                cmdict[cm_num] = cm_naam
                omsdict[cm_naam] = cm_oms # c[1] is omschrijving
    except IOError:
        pass
    return cmdict,omsdict

def usercommands(root,cmdict=None,omsdict=None):
    if cmdict is None: cmdict = {}
    if omsdict is None: omsdict = {}
    s0 = ""
    try:
        for x in file(os.path.join(root,"usercmd.ini")):
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
    except IOError:
        pass
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
    data = []
    try:
        rdr = csv.reader(open(os.path.join(root,"TC_hotkeys.csv"),'rb'))
        data = [(row[0],row[1]) for row in rdr]
    except IOError:
        pass
    return data

## def defaultkeys(root):
    ## data = []
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
    ## return data

def userkeys(root):
    data=[]
    shortcut = False
    try:
        for x in file(os.path.join(root,"wincmd.ini")):
            if shortcut:
                if x.startswith("["):
                    break
                data.append(x[:-1].split("="))
            elif x.startswith("[Shortcuts]"):
                shortcut = True
    except IOError:
        pass
    return data


class tckeys(object):
    def __init__(self,*tc_dir):
        self.tcloc = "C:\Program Files\totalcmd" # default
        try:
            self.tcloc = tc_dir[0] # plaats van wincmd.ini
        except IndexError:
            pass
        try:
            self.ucloc = tc_dir[1] # plaats van usercmd.ini
        except IndexError:
            self.ucloc = self.tcloc
        try:
            self.ciloc = tc_dir[2] # plaats van totalcmd.inc
        except IndexError:
            self.ciloc = self.tcloc
        try:
            self.ktloc = tc_dir[3] # plaats van keyboard.txt
        except IndexError:
            self.ktloc = self.tcloc
        try:
            self.hkloc = tc_dir[4] # plaats van tc_hotkeys.csv
        except IndexError:
            self.hkloc = self.tcloc
        self.keydict = {}

    def read(self):
        dk = defaultkeys(self.hkloc)
        cmdict,omsdict = defaultcommands(self.ciloc)
        cmdict,omsdict = usercommands(self.ucloc,cmdict,omsdict)
        defkeys = {}
        for x,y in dk:
            defkeys[x] = cmdict[y].strip()
        self.keydict = {}
        for key,oms in keyboardtext(self.ktloc):
            cm = ""
            if key in defkeys:
                cm = defkeys[key]
            else:
                defkeys[key] = oms
                if key == "Backspace":
                    del defkeys["Back"]
            self.keydict[key] = ("S",oms,cm)
        self.defkeys = defkeys
        ## f = open("defkeys.txt","w")
        ## for x in self.defkeys:
            ## f.write("%s:: %s\n" % (x,defkeys[x]))
        ## f.close()
        iscmd = False
        try:
            for x in file(os.path.join(self.tcloc,'wincmd.ini')):
                if x.strip() == '[Shortcuts]':
                    iscmd = True
                elif not iscmd:
                    pass
                elif x.strip()[0] == '[':
                    iscmd = False
                else:
                    h = x.strip().split('=')
                    k = keymods(h[0])
                    self.keydict[k] = ("U",omsdict[h[1]],h[1])
        except IOError:
            pass
        return cmdict,omsdict

    def turn_into_xml(self):
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
        schrijfdoor = True
        for x,y in self.keydict.items():
            print x,y
        regels = []
        fn = os.path.join(self.tcloc,'wincmd.ini')
        for x in file(fn):
            if not schrijfdoor and x.strip()[0] == "[":
                schrijfdoor = True
            elif x.strip() == '[Shortcuts]':
                regels.append(x)
                schrijfdoor = False
                for x in self.keydict.keys():
                    if self.keydict[x][0] == "U":
                        regels.append('%s=%s\n' % (''.join(reversed(x.split())),self.keydict[x][2]))
            if schrijfdoor:
                regels.append(x)
        os.rename(fn,fn + ".bak")
        f = open(fn,"w")
        for x in regels:
            f.write(x)
        f.close()

def test_keyboardtext():
    ## print keymods2("F1")
    ## print keymods2("ALT+SHIFT+F5")
    ## print keymods2("NUM +")
    ## print keymods2("SHIFT+NUM +")
    ## print keymods2("SHIFT+NUM -")
    ## return
    kt = keyboardtext('.')

def test_tckeys():
    cl = tckeys(".")
    cl.read()
    ## cl.turn_into_xml()
    cl.write()
    ## h = raw_input()

if __name__ == "__main__":
    cl = tckeys(".")
    ## test_tckeys()
    ## test_keyboardtext()
