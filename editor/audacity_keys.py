# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
import csv

def buildcsv(path=''):
    if not path:
        path = '~/projects/hotkeys/data/audacity_keys.csv'
    data = ET.parse('~/projects/hotkeys/data/audacity/Audacity-keys.xml')
    root = data.getroot()
    data = []
    with open(path, 'w', newline='') as _out:
        for item in root.findall('command'):
            line = ['Keydef']
            keydef = item.get('key').split('+')
            keyname = keydef[-1] if keydef else ''
            line.append(keyname)
            keymods = ''
            if len(keydef) > 1:
                keymods = ''.join([x[0] for x in keydef[:-1]])
            line.append(keymods)
            line.append(item.get('name'))
            line.append(item.get('label'))
            data.append(line)
            writer = csv.writer(_out, )
            writer.writerow(line)
