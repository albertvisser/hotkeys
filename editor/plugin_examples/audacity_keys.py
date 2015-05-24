# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
import collections

def buildcsv(settings, parent=None):

    shortcuts = collections.OrderedDict()

    tree = ET.parse(settings['AC_KEYS'])
    root = tree.getroot()
    data = []
    key = 0
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
        key += 1
        shortcuts[key] = line

    return shortcuts
