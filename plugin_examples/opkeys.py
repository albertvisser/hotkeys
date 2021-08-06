"""HotKeys plugin for Opera <= 12 - not maintained
"""
import os
import csv
import shutil


def get_keydefs(doc, soort, keydefs=None):
    """build dictionary of key combo definitions
    """
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


def writecsv():
    """implementation of standard function to build the csvfile

    i.v.m. obsolete raken niet buildcsv genoemd zodat ik me niet kan vergissen
    """
    ini = Settings('/home/albert/tcmdrkeys/tcmdrkeys/opkey_config.py')
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


def savekeys(parent):
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

    def write(self):
        """write settings back
        """
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
                    f_out.write(line.replace(waarde, self.std))
                elif naam == self.namen[1]:
                    f_out.write(line.replace(waarde, self.user))
                elif naam == self.namen[2]:
                    f_out.write(line.replace(waarde, self.csv))
                else:
                    f_out.write(line)
