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
        rdr = csv.reader(open(os.path.join(pad,"VI_hotkeys.csv"), 'r'))
    except IOError:
        rdr = []
    key = 0
    for row in rdr:
        key += 1
        data[key] = (row[0].strip(), row[1].strip(), row[2].strip())
    return data

def savekeys(pad):
    """schrijf de gegevens terug

    nog niet mogelijk zolang ik niet weet waar dat heen moet
    """
    pass

class VIKSettings(object):
    """bevat de settings uit het aangegeven bestand

    self.pad = waar het csv bestand staat
    self.lang = taalkeuze
    de gegevens worden hier gezamenlijk weggeschreven dus niet voor elke
    wijziging apart
    """
    def __init__(self, fnaam):
        self.fnaam = fnaam
        self.namen = ['VI_PAD', 'LANG']
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
                    self.pad = waarde
                elif naam == self.namen[1]:
                    self.lang = waarde
                else:
                    continue

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
    test_readkeys('/home/albert/tcmdrkeys/vim')
