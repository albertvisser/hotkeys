# -*- coding: UTF-8 -*-

import os
import sys
import shutil
import collections
import csv
import importlib

HERE = os.path.abspath(os.path.dirname(__file__))
HERELANG = os.path.join(HERE, 'languages')
## try:
    ## HOME = os.environ('HOME')
## except KeyError:
    ## HOME = os.environ('USERPROFILE') # Windows
CONF = 'editor.hotkey_config' # don't import, can be modified at runtime
VRS = "2.1.x"
AUTH = "(C) 2008-today Albert Visser"
WIN = True if sys.platform == "win32" else False
## LIN = True if sys.platform == 'linux2' else False
LIN = True if os.name == 'posix' else False

csv_linetypes = ['Setting', 'Title', 'Width', 'is_type', 'Keydef']
csv_settingtype, csv_keydeftype = csv_linetypes[0], csv_linetypes[-1]
csv_titletype, csv_widthtype, csv_istypetype = csv_linetypes[1:-1]
csv_settingnames = ['PluginName', 'PanelName', 'RebuildCSV', 'ShowDetails',
    'RedefineKeys']
csv_plgsett, csv_pnlsett, csv_rbldsett, csv_detsett, csv_redefsett = csv_settingnames
plugin_skeleton = '''# -*- coding: UTF-8 -*-\n
"""
See example_app_keys.py for a description of the plugin API.
Only define the functions that need to be defined,
for everything that's not in here
the default code in the main program will be used.
"""
'''
mode_f, mode_r = 'Fixed', 'Remember'
named_keys = ['Insert', 'Del', 'Home', 'End', 'PgUp', 'PgDn', 'Space', 'Backspace',
    'Tab', 'Num+', 'Num-', 'Num*', 'Num/', 'Enter', 'Esc', 'Left', 'Right', 'Up',
    'Down', 'Letter', 'Letter(s)']
#
# non-gui and csv related functions
#
def readlang(lang):
    captions = {}
    with open(os.path.join(HERELANG, lang)) as f_in:
        for x in f_in:
            if x[0] == '#' or x.strip() == "":
                continue
            key, value = x.strip().split(None,1)
            captions[key] = value
        return captions

def get_csv_oms(lang):
    captions = readlang(lang)
    csv_oms = dict(zip(csv_settingnames + csv_linetypes[1: -1], (
        captions['T_NAMOF'].format(captions['S_PLGNAM'], captions['T_NOPY']),
        captions['T_INSEL'].format(captions['S_PNLNAM']),
        captions['T_BOOL'].format(captions['S_RBLD']),
        captions['T_BOOL'].format(captions['S_DETS']),
        captions['T_BOOL'].format(captions['S_RSAV']),
        captions['T_COLTTL'],
        captions['T_COLWID'],
        captions['T_BOOL'].format(captions['T_COLIND']),
        )))
    return csv_oms

def build_csv_sample_data(lang):
    csv_sample_data = []
    csv_oms = get_csv_oms(lang)
    for indx, data in enumerate((
            ['C_KEY', 'C_MODS', 'C_DESC'],
            [120, 90, 292],
            [0, 0, 0],)):
        name = csv_linetypes[indx + 1]
        oms = csv_oms[name]
        data.insert(0, name)
        data.append(oms)
        csv_sample_data.append(data)
    return csv_sample_data

def get_pluginname(csvname):
    with open(csvname) as _in:
        for line in _in:
            test = line.split(',')
            if test[:2] == [csv_settingtype, csv_settingnames[0]]:
                pl_name = test[2]
                break
    # ideally we should import the given module to determine the actual file name
    return pl_name.replace('.', '/') + '.py'

def read_settings():

    settings = {}
    try:
        sett = importlib.import_module(CONF)
        settings['filename'] = sett.__file__
    except ImportError:
        sett = None
    try:
        settings['plugins'] = sett.PLUGINS
    except AttributeError:
        settings['plugins'] = []
    try:
        settings['lang'] = sett.LANG
    except AttributeError:
        settings['lang'] = 'english.lng'
    try:
        settings['initial'] = sett.INITIAL
    except AttributeError:
        pass
    try:
        settings['startup'] = sett.STARTUP
    except AttributeError:
        pass
    return settings

def modify_settings(ini):
    # modify the settings file
    inifile = ini['filename']
    shutil.copyfile(inifile, inifile + '.bak')
    data = []
    dontread = False
    with open(inifile + '.bak') as _in:
        for line in _in:
            if dontread:
                if line.strip() == ']':
                    data.append(line)
                    dontread = False
            else:
                data.append(line)
                if 'PLUGINS' in line:
                    dontread = True
                    for name, path in ini["plugins"]:
                        data.append('    ("{}", "{}"),\n'.format(name, path))
    with open(inifile, 'w') as _out:
        for line in data:
            _out.write(line)

def change_setting(setting, old, new, inifile):
    setting = setting.upper()
    shutil.copyfile(inifile, inifile + '.bak')
    with open(inifile + '.bak') as _in:
        lines = _in.readlines()
    for ix, line in enumerate(lines):
        if setting is not None and line.startswith(setting):
            if not old:
                lines[ix] = line.replace("''", "'{}'".format(new))
            elif not new:
                lines[ix] = line.replace("'{}'".format(old), "''")
            else:
                lines[ix] = line.replace(old, new)
            break
    else:
        if setting == 'INITIAL':
            lines.append('# application to show on startup\n')
        elif setting == 'STARTUP':
            lines.append('# application to show: selected or remember on closing\n')
        lines.append("{} = '{}'\n".format(setting, new))
    with open(inifile, 'w') as _out:
        _out.writelines(lines)

def read_columntitledata(self):
    """read the current language file and extract the already defined column headers
    """
    column_textids = []
    column_names = []
    last_textid = ''
    in_section = False

    with open(os.path.join(HERELANG, self.parent.ini["lang"])) as f_in:
        for line in f_in:
            line = line.strip()
            if line == '':
                continue
            elif line.startswith('#'):
                if in_section:
                    in_section = False
                elif 'Keyboard mapping' in line:
                    in_section = True
                continue
            test = line.split()
            if test[0] > last_textid and test[0] < '100':
                    last_textid = test[0]
            if in_section:
                column_textids.append(test[0])
                column_names.append(test[1])
    return column_textids, column_names, last_textid

def add_columntitledata(newdata):
    """add the new column title(s) to all language files

    input is a list of tuples (textid, text)"""
    choices = [os.path.join(HERELANG, x) for x in os.listdir(HERELANG)
        if os.path.splitext(x)[1] == ".lng"]
    for choice in choices:
        choice_o = choice + '~'
        shutil.copyfile(choice, choice_o)
        in_section = False
        with open(choice_o) as f_in, open(choice, 'w') as f_out:
            for line in f_in:
                if line.startswith('# Keyboard mapping'):
                    in_section = True
                elif in_section and line.strip() == '':
                    for textid, text in newdata:
                        f_out.write('{} {}\n'.format(textid, text))
                    in_section = False
                f_out.write(line)

def update_paths(paths, pathdata, lang):
    """read the paths to the csv files from the data returned by the dialog
    if applicable also write a skeleton plugin file
    """
    newpaths = []
    for name, path in paths:
        loc = path.input.text()
        newpaths.append((name, loc))
        if name in pathdata:
            data = pathdata[name]
            parts = data[0].split('.')
            if parts[0] == '': parts = parts[1:]
            newfile = os.path.join(*parts) + '.py'
            with open(newfile, 'w') as _out:
                _out.write(plugin_skeleton)
            initcsv(loc, data, lang)
    return newpaths

def initcsv(loc, data, lang):
    """Initialize csv file

    save some basic settings to a csv file together with some sample data
    """
    csv_oms = get_csv_oms(lang)
    with open(loc, "w") as _out:
        wrt = csv.writer(_out)
        for indx, sett in enumerate(csv_settingnames):
            wrt.writerow([csv_linetypes[0], sett, data[indx], csv_oms[sett]])
        for row in build_csv_sample_data(lang):
            wrt.writerow(row)

def readcsv(pad):
    """lees het csv bestand op het aangegeven pad en geeft de inhoud terug

    retourneert dictionary van nummers met (voorlopig) 4-tuples
    """
    data = collections.OrderedDict()
    coldata = []
    settings = collections.OrderedDict()
    with open(pad, 'r') as _in:
        rdr = csv.reader(_in)
        key = 0
        first = True
        for row in rdr:
            rowtype, rowdata = row[0], row[1:]
            if rowtype == csv_settingtype:
                name, value, desc = rowdata
                settings[name] = value
                if name not in csv_settingnames:
                    data[name] = desc
            elif rowtype == csv_titletype:
                for item in rowdata[:-1]:
                    coldata_item = ['', '', '']
                    coldata_item[0] = item
                    coldata.append(coldata_item)
            elif rowtype == csv_widthtype:
                for ix, item in enumerate(rowdata[:-1]):
                    coldata[ix][1] = int(item)
            elif rowtype == csv_istypetype:
                for ix, item in enumerate(rowdata[:-1]):
                    coldata[ix][2] = bool(int(item))
            elif rowtype == csv_keydeftype:
                key += 1
                data[key] = ([x.strip() for x in rowdata])
            elif not rowtype.startswith('#'):
                raise ValueError(rowtype)
    return settings, coldata, data

def writecsv(pad, settings, coldata, data, lang):
    csvoms = get_csv_oms(lang)
    if os.path.exists(pad):
        shutil.copyfile(pad, pad + '~')
    with open(pad, "w") as _out:
        wrt = csv.writer(_out)
        for name, value in settings.items():
            try:
                settdesc = csvoms[name]
            except KeyError:
                settdesc = data.pop(name)
            rowdata = csv_settingtype, name, value, settdesc
            wrt.writerow(rowdata)
        for ix, row in enumerate([[csv_titletype], [csv_widthtype]]):
            row += [x[ix] for x in coldata] + [csvoms[row[0]]]
            wrt.writerow(row)
        wrt.writerow([csv_istypetype] + [int(x[2]) for x in coldata] +
            [csvoms[csv_istypetype]])
        for keydef in data.values():
            row = [csv_keydeftype] + [x for x in keydef]
            wrt.writerow(row)

def quick_check(filename):
    """quick and dirty function for checking a csv file outside of the application

    replicates some things that are done in building the list with keydefs
    so we can catch errors in advance
    """
    _, column_info, data = readcsv(filename)
    items = data.items()
    if items is None or len(items) == 0:
        print('No keydefs found in this file')
        return
    for key, data in items:
        try:
            for indx, col in enumerate(column_info):
                is_soort = col[2]
                value = data[indx]
        except Exception as e:
            print(key, data)
            raise
    print('{}: No errors found'.format(filename))

