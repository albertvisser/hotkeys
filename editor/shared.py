# -*- coding: UTF-8 -*-
"""HotKeys: non-gui and csv related functions
"""
import os
import sys
import pathlib
import shutil
import collections
import csv
import enum
import importlib
import logging

HERE = pathlib.Path(__file__).parent.resolve()  # os.path.abspath(os.path.dirname(__file__))
HERELANG = HERE / 'languages'    # os.path.join(HERE, 'languages')
VRS = "2.1.x"
AUTH = "(C) 2008-today Albert Visser"
WIN = True if sys.platform == "win32" else False
## LIN = True if sys.platform == 'linux2' else False
LIN = True if os.name == 'posix' else False
CONF = 'editor.hotkey_config'  # default configuration file
BASE = str(HERE.parent)

LOGFILE = HERE / 'logs' / 'hotkeys.log'
DO_LOGGING = os.environ.get("DEBUG", '') not in ('', "0")
if DO_LOGGING:
    LOGFILE.parent.mkdir(exist_ok=True)
    LOGFILE.touch(exist_ok=True)
    logging.basicConfig(filename=str(LOGFILE),
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s')


def log(message, always=False):
    "output to log"
    if always or DO_LOGGING:
        logging.info(message)


class LineType(enum.Enum):
    """Types of lines in the csv file (first value)
    """
    SETT = 'Setting'
    CAPT = 'Title'
    WID = 'Width'
    ORIG = 'is_type'
    KEY = 'Keydef'


class SettType(enum.Enum):
    """Types of settings (second value on line with first value = setting
    """
    PLG = 'PluginName'
    PNL = 'PanelName'
    RBLD = 'RebuildCSV'
    DETS = 'ShowDetails'
    RDEF = 'RedefineKeys'


csv_linetypes = [x.value for x in LineType.__members__.values()]
csv_settingnames = [x.value for x in SettType.__members__.values()]
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
              'Tab', 'Num+', 'Num-', 'Num*', 'Num/', 'Enter', 'Esc', 'Left', 'Right',
              'Up', 'Down', 'Letter', 'Letter(s)']


def readlang(lang):
    "get captions from language file"
    captions = {}
    with (HERELANG / lang).open() as f_in:
        for x in f_in:
            if x[0] == '#' or x.strip() == "":
                continue
            key, value = x.strip().split(None, 1)
            captions[key] = value
        return captions


def get_csv_oms(lang):
    "build descriptions for csv file"
    captions = readlang(lang)
    csv_oms = {SettType.PLG.value: captions['T_NAMOF'].format(captions['S_PLGNAM'],
                                                              captions['T_NOPY']),
               SettType.PNL.value: captions['T_INSEL'].format(captions['S_PNLNAM']),
               SettType.RBLD.value: captions['T_BOOL'].format(captions['S_RBLD']),
               SettType.DETS.value: captions['T_BOOL'].format(captions['S_DETS']),
               SettType.RDEF.value: captions['T_BOOL'].format(captions['S_RSAV']),
               LineType.CAPT.value: captions['T_COLTTL'],
               LineType.WID.value: captions['T_COLWID'],
               LineType.ORIG.value: captions['T_BOOL'].format(captions['T_COLIND'])}
    return csv_oms


def build_csv_sample_data(lang):
    "create default data lines in the csv file"
    csv_sample_data = []
    csv_oms = get_csv_oms(lang)
    for indx, data in enumerate((['C_KEY', 'C_MODS', 'C_DESC'],
                                 [120, 90, 292],
                                 [0, 0, 0],)):
        name = csv_linetypes[indx + 1]
        oms = csv_oms[name]
        data.insert(0, name)
        data.append(oms)
        csv_sample_data.append(data)
    return csv_sample_data


def get_pluginname(csvname):
    "return the plugin's filename from the plugin's module name"
    with open(csvname) as _in:
        for line in _in:
            test = line.split(',')
            if test[:2] == [LineType.SETT.value, SettType.PLG.value]:
                pl_name = test[2]
                break
    # ideally we should import the given module to determine the actual file name
    return pl_name.replace('.', '/') + '.py'


def read_settings(ini):
    "get application settings from a given location"
    settings = {}
    try:
        sett = importlib.import_module(ini)
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
    try:
        settings['title'] = sett.TITLE
    except AttributeError:
        pass
    return settings


def modify_settings(ini):
    "modify the settings file at the given location"
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
    "change a setting and write it immediately"
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
                if setting == 'TITLE':
                    lines[ix - 2: ix + 1] = [lines[ix - 2]]
            else:
                lines[ix] = line.replace(old, new)
            break
    else:
        if setting == 'INITIAL':
            lines.append('# application to show on startup\n')
        elif setting == 'STARTUP':
            lines.append('# application to show: selected or remember on closing\n')
        elif setting == 'TITLE':
            lines.append('# screen title (not needed if default)\n')
        lines.append("{} = '{}'\n".format(setting, new))
    with open(inifile, 'w') as _out:
        _out.writelines(lines)


def read_columntitledata(editor):
    """read the current language file and extract the already defined column headers
    """
    column_textids = []
    column_names = []
    last_textid = ''
    in_section = False

    with (HERELANG / editor.ini["lang"]).open() as f_in:
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
            test = line.split(None, 1)
            if test[0] > last_textid and test[0] < '100':
                last_textid = test[0]
            if in_section:
                column_textids.append(test[0])
                column_names.append(test[1])
    return column_textids, column_names, last_textid


def add_columntitledata(newdata):
    """add the new column title(s) to all language files

    input is a list of tuples (textid, text)"""
    ## with os.scandir(HERELANG) as choices:
    choices = os.scandir(HERELANG)
    for choice in choices:
        choice_file = pathlib.Path(choice.path)
        if choice_file.suffix != '.lng':
            continue
        choice_o = pathlib.Path(choice.path + '~')
        shutil.copyfile(str(choice), str(choice_o))
        in_section = False
        with choice_o.open() as f_in, choice.open('w') as f_out:
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
    updir = HERE.parent
    newpaths = []
    for name, path in paths:
        loc = path.input.text()         # bv editor/plugins/gitrefs_hotkeys.csv
        newpaths.append((name, loc))
        if name in pathdata:
            data = pathdata[name]       # bv. ['editor.plugins.gitrefs_keys', 'gitrefs hotkeys', 0, 0, 0]
            parts = data[0].split('.')
            if parts[0] == '':
                parts = parts[1:]
            newfile = updir / ('/'.join(parts) + '.py')
            with newfile.open('w') as _out:
                _out.write(plugin_skeleton)
            initcsv(updir / loc, data, lang)
    return newpaths


def initcsv(loc, data, lang):
    """Initialize csv file

    save some basic settings to a csv file together with some sample data
    """
    csv_oms = get_csv_oms(lang)
    with loc.open("w") as _out:
        wrt = csv.writer(_out)
        for indx, sett in enumerate(csv_settingnames):
            wrt.writerow([LineType.SETT.value, sett, data[indx], csv_oms[sett]])
        for row in build_csv_sample_data(lang):
            wrt.writerow(row)


def readcsv(pad):
    """lees het csv bestand op het aangegeven pad en geeft de inhoud terug

    retourneert dictionary van nummers met (voorlopig) 4-tuples
    """
    data = collections.OrderedDict()
    coldata = []
    settings = collections.OrderedDict()
    try:
        with open(pad, 'r') as _in:
            rdr = csv.reader(_in)
            rdrdata = [row for row in rdr]
    except (FileNotFoundError, IsADirectoryError):
        raise
    key = 0
    ## first = True
    extrasettings = {}
    for row in rdrdata:
        rowtype, rowdata = row[0], row[1:]
        if rowtype == LineType.SETT.value:
            name, value, desc = rowdata
            settings[name] = value
            if name not in csv_settingnames:
                extrasettings[name] = desc
        elif rowtype == LineType.CAPT.value:
            for item in rowdata[:-1]:
                coldata_item = ['', '', '']
                coldata_item[0] = item
                coldata.append(coldata_item)
        elif rowtype == LineType.WID.value:
            for ix, item in enumerate(rowdata[:-1]):
                coldata[ix][1] = int(item)
        elif rowtype == LineType.ORIG.value:
            for ix, item in enumerate(rowdata[:-1]):
                coldata[ix][2] = bool(int(item))
        elif rowtype == LineType.KEY.value:
            key += 1
            data[key] = ([x.strip() for x in rowdata])
        elif not rowtype.startswith('#'):
            raise ValueError(rowtype)
    if extrasettings:
        settings['extra'] = extrasettings
    return settings, coldata, data


def writecsv(pad, settings, coldata, data, lang):
    """schrijf de meegegeven data als csv bestand naar de aangegeven locatie
    """
    csvoms = get_csv_oms(lang)
    extrasettoms = ''
    if os.path.exists(pad):
        shutil.copyfile(pad, pad + '~')
    try:
        extrasettoms = settings.pop('extra')
    except KeyError:
        extrasettoms = ''
    with open(pad, "w") as _out:
        wrt = csv.writer(_out)
        for name, value in settings.items():
            try:
                settdesc = csvoms[name]
            except KeyError:
                settdesc = extrasettoms[name]
            rowdata = LineType.SETT.value, name, value, settdesc
            wrt.writerow(rowdata)
        for ix, row in enumerate([[LineType.CAPT.value], [LineType.WID.value]]):
            row += [x[ix] for x in coldata] + [csvoms[row[0]]]
            wrt.writerow(row)
        wrt.writerow([LineType.ORIG.value] + [int(x[2]) for x in coldata] +
                     [csvoms[LineType.ORIG.value]])
        for keydef in data.values():
            row = [LineType.KEY.value] + [x for x in keydef]
            wrt.writerow(row)
    if extrasettoms:
        settings['extra'] = extrasettoms


def quick_check(filename):
    """quick and dirty function for checking a csv file outside of the application

    replicates some things that are done in building the list with keydefs
    so we can catch errors in advance
    """
    _, column_info, data = readcsv(filename)
    items = data.items()
    if not items:   # if items is None or len(items) == 0:
        print('No keydefs found in this file')
        return
    for key, data in items:
        try:
            for indx, col in enumerate(column_info):
                _ = data[indx]
        except Exception:
            print(key, data)
            raise
    print('{}: No errors found'.format(filename))


# geëxtraheerd uit dialogs_qt.py
def get_text(win, message_id='', text='', args=None):
    """retourneer de tekst geïdentificeerd door <message_id>
    als <text> is opgegeven wordt die gebruikt
    <args> bevat een list van waarden die in de tekst kunnen worden ingevuld
    """
    try:
        win = win.editor
    except AttributeError:
        win = win.master
    if message_id:
        text = win.captions[message_id].replace(' / ', '\n')
    elif not text:
        text = win.captions['I_NOMSG']
        raise ValueError(text)
    if args:
        text = text.format(*args)
    return text


def get_title(win):
    "retourneer de titel voor de te tonen pagina"
    try:
        title = win.title
    except AttributeError:
        try:
            title = win.editor.title
        except AttributeError:
            title = win.master.title
    return title
