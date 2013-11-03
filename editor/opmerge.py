# -*- coding: utf-8 -*-

import os
import csv
import shutil
from opkeys import OpKSettings

def get_keydefs(doc, soort, keydefs=None):
    if not keydefs:
        keydefs = {}

    context = ''
    for line in doc:

        line = line.strip()
        if not line or line.startswith(';') or line.startswith('#'):
            continue
        elif line.startswith('['):
            context = line.strip('[]')
            if context in keydefs or context.lower() in ('info', 'version'):
                context = ''
            else:
                keydefs[context] = []
        elif context:
            keydata, definition = line.split('=', 1)
            platform = ''
            feature = ''
            if "=" in definition:
                extra, definition = definition.split('=', 1)
                keydata = '='.join((keydata, extra)).replace('"', ' ')
            if ',' in keydata:
                extra, keydata = keydata.split(',')
                got_platform = got_feature = False
                for word in extra.split():
                    if got_platform:
                        platform = word
                        got_platform = False
                    elif got_feature:
                        feature = word
                        got_feature = False
                    elif word.lower() == 'platform':
                        got_platform = True
                    elif word.lower() == 'feature':
                        got_feature = True
            keydefs[context].append([platform, feature, keydata.strip(), soort,
                definition.strip()])
    return keydefs

def main():
    ini = OpKSettings('/home/albert/tcmdrkeys/tcmdrkeys/opkey_config.py')
    ## ini_pad = '/home/albert/tcmdrkeys/opera'
    ## stdfile = os.path.join(ini.std)
    ## userfile = os.path.join(ini.user)
    csvfile = os.path.join(ini.csv, 'Opera_hotkeys.csv')
    if os.path.exists(csvfile):
        shutil.copyfile(csvfile, csvfile + '.backup')

    keydefs = {}
    with open(ini.user) as doc:
        keydefs = get_keydefs(doc, 'R')

    with open(ini.std) as doc:
        keydefs = get_keydefs(doc, 'S', keydefs)

    with open(csvfile, 'w') as _out:
        writer = csv.writer(_out)
        for context in keydefs:
            for linedata in keydefs[context]:
                linedata.insert(0, context)
                writer.writerow(linedata)

if __name__ == '__main__':
    main()
