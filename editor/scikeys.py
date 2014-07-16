# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import csv
import shutil
from bs4 import BeautifulSoup

def writecsv():
    ini = SciKSettings('/home/albert/tcmdrkeys/tcmdrkeys/scikey_config.py')
    csvfile = os.path.join(ini.pad, 'SciTE_hotkeys.csv')
    shutil.copyfile(csvfile, csvfile + '.backup')

    with open(os.path.join(ini.pad, 'CommandValues.html')) as doc:

        soup = BeautifulSoup(doc)


    with open(csvfile, 'w') as _out:

        writer = csv.writer(_out)

        menus, internals, others = soup.find_all('table')
        for row in menus.find_all('tr'):
            command, text, shortcut = [tag.string for tag in row.find_all('td')]
            writer.writerow((shortcut, 'S', '', command, text))

        for row in internals.find_all('tr'):
            command, text, description = [tag.string for tag in row.find_all('td')]
            writer.writerow(('', 'S', command, text, description))

        for row in others.find_all('tr'):
            description, shortcut = [tag.string for tag in row.find_all('td')]
            parts = shortcut.lower().split('+')
            if parts[-1] == '':
                parts[-2] += '+'
                parts.pop()
            shortcut = ' '.join(reversed(parts))
            writer.writerow((shortcut, 'S', '', '', description))

def savekeys(pad):
    """schrijf de gegevens terug

    voorlopig nog niet mogelijk
    aangepaste keys samenstellen tot een user.shortcuts statement en dat
    invoegen in SciTEUser.properties
    """
    pass

class Settings(object):
    """bevat de settings uit het aangegeven bestand

    self.pad = waar het csv bestand staat
    de gegevens worden hier gezamenlijk weggeschreven dus niet voor elke
    wijziging apart
    """
    def __init__(self, fnaam):
        self.fnaam = fnaam
        self.namen = ['SCI_PAD']
        self.pad = ''
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
                else:
                    f_out.write(line)

def test_readkeys(pad):
    data = readkeys(pad)
    print(data)

if __name__ == '__main__':
    test_readkeys('/home/albert/tcmdrkeys/scite')
