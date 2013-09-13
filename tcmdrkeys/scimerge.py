# -*- coding: utf-8 -*-

import os
import csv
import shutil
from bs4 import BeautifulSoup
from scikeys import Settings

def main():
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

if __name__ == '__main__':
    main()
