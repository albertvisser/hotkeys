# -*- coding: UTF-8 -*-

import os
import sys
import shutil
import collections
import csv

HERE = os.path.abspath(os.path.dirname(__file__))
HERELANG = os.path.join(HERE, 'languages')
## try:
    ## HOME = os.environ('HOME')
## except KeyError:
    ## HOME = os.environ('USERPROFILE') # Windows
CONF = os.path.join(HERE, 'hotkey_config.py') # don't import, can be modified at runtime
VRS = "2.1.x"
AUTH = "(C) 2008-today Albert Visser"
WIN = True if sys.platform == "win32" else False
## LIN = True if sys.platform == 'linux2' else False
LIN = True if os.name == 'posix' else False

# constanten voor  captions en dergelijke (correspondeert met nummers in language files)
# *** toegesneden op TC verplaatsen naar TC plugin? ***
C_KEY, C_MOD, C_SRT, C_CMD, C_OMS = '001', '043', '002', '003', '004'
C_DFLT, C_RDEF = '005', '006'
M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'
C_SAVE, C_DEL, C_EXIT, C_KTXT, C_CTXT ='010', '011', '012', '018', '019'
C_NEXT, C_PREV, C_SEL, C_NONE  = '014', '015', '050', "052"
C_FIND, C_FILTER, C_FLTOFF = '051', "068", "066"
M_APP, M_READ, M_SAVE, M_RBLD, M_EXIT = '200', '201', '202', '203', '209'
M_SETT, M_LOC, M_LANG, M_TOOL, M_COL = '210', '211', '212', '213', '214'
M_MISC, M_ENTR, M_PREF = '215', '216', '217'
M_HELP, M_ABOUT = '290', '299'
NOT_IMPLEMENTED = '404'

csv_linetypes = ['Setting', 'Title', 'Width', 'Seq', 'is_type', 'Keydef']
csv_settingtype, csv_keydeftype = csv_linetypes[0], csv_linetypes[-1]
csv_titletype, csv_widthtype, csv_seqnumtype, csv_istypetype = csv_linetypes[1:-1]
csv_settingnames = ['PluginName', 'PanelName', 'RebuildCSV', 'RedefineKeys']
csv_plgsett, csv_pnlsett, csv_rbldsett, csv_redefsett = csv_settingnames
csv_oms = dict(zip(csv_settingnames + csv_linetypes[1: -1], (
 'Naam van de module met toolspecifieke code (zonder .py)',
 'Naam van het toolpanel in de selector',
 "1 = possible to rebuild this file from the tools' settings; else 0",
 '1 = possible to change keydefs and save them back; else 0',
 'Titles of the columns in the display; refer to keys in the language file',
 'Column widths',
 'Column sequence numbers in the display',
 '1 = Column indicates if keydef is original or (re)defined; else 0')))
csv_sample_data = []
for indx, data in enumerate((
        [C_KEY, C_MOD, C_OMS],
        [120, 90, 292],
        [0, 1, 2],
        [0, 0, 0],)):
    name = csv_linetypes[indx + 1]
    oms = csv_oms[name]
    data.insert(0, name)
    data.append(oms)
    csv_sample_data.append(data)
plugin_skeleton = '''# -*- coding: UTF-8 -*-\n
"""
See example_app_keys.py for a description of the plugin API.
Only define the functions that need to be defined,
for everything that's not in here
the default code in the main program will be used.
"""
'''
mode_f, mode_r = 'Fixed', 'Remember'
#
# non-gui and csv related functions
# perhaps also add to hotkeys_constants (rename?)
def get_pluginname(csvname):
    with open(csvname) as _in:
        for line in _in:
            test = line.split(',')
            if test[:2] == [csv_settingtype, csv_settingnames[0]]:
                pl_name = test[2]
                break
    # ideally we should import the given module to determine the actual file name
    return pl_name.replace('.', '/') + '.py'

def read_settings(filename):
    settings = {'filename': CONF}
    lang, plugins = 'english.lng', []
    with open(filename) as _in:
        read_plugins = False
        for line in _in:
            if read_plugins:
                if line.strip() == ']':
                    read_plugins = False
                elif line.strip().startswith('#'):
                    continue
                else:
                    name, value = line.split(', ',1)
                    _, name = name.split('(')
                    value, _ = value.split(')')
                    plugins.append((name.strip('"'),
                        value.strip('"')))
            if line.startswith('PLUGINS'):
                read_plugins = True
            elif line.startswith('LANG'):
                lang = line.strip().split(' = ')[1].strip("'")
            elif line.startswith('INITIAL'):
                settings['initial'] = line.strip().split(' = ')[1].strip("'")
            elif line.startswith('STARTUP'):
                settings['startup'] = line.strip().split(' = ')[1].strip("'")
    settings['plugins'] = plugins
    settings['lang'] = lang
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
    choices = [os.path.join(HERELANG, x) for x in os.listdir(hkc.HERELANG)
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

def update_paths(paths, pathdata):
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
            initcsv(loc, data)
    return newpaths

def initcsv(loc, data):
    """Initialize csv file

    save some basic settttings to a csv file together with some sample data
    """
    with open(loc, "w") as _out:
        wrt = csv.writer(_out)
        for indx, sett in enumerate(csv_settingnames):
            wrt.writerow([csv_linetypes[0], sett, data[indx], csv_oms[sett]])
        for row in csv_sample_data:
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
                name, value, oms = rowdata
                settings[name] = (value, oms)
            elif rowtype == csv_titletype:
                for item in rowdata[:-1]:
                    coldata_item = ['', '', '']
                    coldata_item[0] = item
                    coldata.append(coldata_item)
            elif rowtype == csv_widthtype:
                for ix, item in enumerate(rowdata[:-1]):
                    coldata[ix][1] = int(item)
            elif rowtype == csv_seqnumtype:
                pass
                ## for ix, item in enumerate(rowdata[:-1]):
                    ## coldata[ix][2] = int(item)
            elif rowtype == csv_istypetype:
                for ix, item in enumerate(rowdata[:-1]):
                    coldata[ix][2] = bool(int(item))
            elif rowtype == csv_keydeftype:
                key += 1
                data[key] = ([x.strip() for x in rowdata])
            elif not rowtype.startswith('#'):
                raise ValueError(self.captions['040'].format(rowtype))
    return settings, coldata, data

def writecsv(pad, settings, coldata, data):
    ## os.remove(_outback)
    if os.path.exists(pad):
        shutil.copyfile(pad, pad + '~')
    with open(pad, "w") as _out:
        wrt = csv.writer(_out)
        for name, value in settings.items():
            rowdata = csv_settingtype, name, value[0], value[1]
            wrt.writerow(rowdata)
        for ix, row in enumerate([[csv_titletype], [csv_widthtype]]):
            row += [x[ix] for x in coldata] + [csv_oms[row[0]]]
            wrt.writerow(row)
        wrt.writerow([csv_istypetype] + [int(x[2]) for x in coldata] +
            [csv_oms[csv_istypetype]])
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

