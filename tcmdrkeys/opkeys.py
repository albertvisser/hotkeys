# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import csv
import shutil

def readkeys(pad):
    """lees het csv bestand op het aangegeven pad en geeft de inhoud terug

    retourneert dictionary van nummers met (voorlopig) 3-tuples
    """
    data = {}
    try:
        rdr = csv.reader(open(os.path.join(pad, "Opera_hotkeys.csv"), 'r'))
    except IOError:
        rdr = []
    key = 0
    for row in rdr:
        key += 1
        data[key] = ([x.strip() for x in row])
    return data

def savekeys(pad):
    """schrijf de gegevens terug

    voorlopig nog niet mogelijk
    contexts die aangepaste keydefs bevatten terugschrijven in door OP_USER
    aangegeven bestand
    """
    pass

class Settings(object):
    """bevat de settings uit het aangegeven bestand

    self.std = waar het bestand met standaard definities staat
    self.user = waar het bestand met user definities staat
    self.pad = waar het csv bestand staat
    self.lang = taalkeuze
    de gegevens worden hier gezamenlijk weggeschreven dus niet voor elke
    wijziging apart
    """
    def __init__(self, fnaam):
        self.fnaam = fnaam
        self.namen = ['OP_STD', 'OP_USER', 'OP_CSV', 'LANG']
        self.pad = self.lang = ''
        if not os.path.exists(self.fnaam):
            return
        with open(self.fnaam) as f_in:
            for line in f_in:
                if line.strip() == "" or line.startswith('#'):
                    continue
                try:
                    naam, waarde = line.strip().split('=')
                except ValueError:
                    continue
                if naam == self.namen[0]:
                    self.std = waarde
                elif naam == self.namen[1]:
                    self.user = waarde
                elif naam == self.namen[2]:
                    self.csv = waarde
                elif naam == self.namen[3]:
                    self.lang = waarde

    def write(self):
        fn_o = self.fnaam + '.bak'
        shutil.copyfile(self.fnaam, fn_o)
        with open(fn_o) as f_in, open(self.fnaam, 'w') as f_out:
            for line in f_in:
                if line.startswith('#') or '=' not in line:
                    f_out.write(line)
                    continue
                try:
                    naam, waarde = line.strip().split('=')
                except ValueError:
                    f_out.write(line)
                    continue
                if naam == self.namen[0]:
                    f_out.write(line.replace(waarde, self.pad))
                elif naam == self.namen[1]:
                    f_out.write(line.replace(waarde, self.lang))
                else:
                    f_out.write(line)

def test_readkeys(pad):
    data = readkeys(pad)
    print(data)

if __name__ == '__main__':
    test_readkeys('/home/albert/tcmdrkeys/opera')
