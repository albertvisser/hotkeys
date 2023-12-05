"""Hotkeys: GUI independent code

    main gui (choicebook)
    importeert de verschillende applicatiemodules
    hierin wordt het menu gedefinieerd en de functies die daarbij horen
    het idee is dat de menuopties wanneer nodig uitgegrijsd zijn en dat
        in de routines wordt uitgevraagd wat te doen bij welke applicatie
    voor wat betreft de instellingen:
        taalkeuze: op dit niveau
        paden: op applicatie niveau (in betreffende csv file)
"""
from types import SimpleNamespace
import os
# import sys
import pathlib
import csv
import json
import enum
import shutil
import collections
import string
import importlib
import importlib.util

from editor import shared
from editor import gui
NO_PATH = 'NO_PATH'
named_keys = ['Insert', 'Del', 'Home', 'End', 'PgUp', 'PgDn', 'Space', 'Backspace',
              'Tab', 'Num+', 'Num-', 'Num*', 'Num/', 'Enter', 'Esc', 'Left', 'Right',
              'Up', 'Down', 'Letter', 'Letter(s)']
VRS = "2.1.x"
AUTH = "(C) 2008-today Albert Visser"
# CONF = 'editor.hotkey_config'  # default configuration file
BASE = shared.HERE.parent
CONF = BASE / 'editor' / 'hotkey_config.json'
plugin_skeleton = '''\n
"""
See example_app_keys.py for a description of the plugin API.
Only define the functions that need to be defined,
for everything that's not in here
the default code in the main program will be used.
"""
'''
initial_settings = {'plugins': [], 'lang': 'english.lng', 'startup': 'Remember', 'initial': ''}


class LineType(enum.Enum):
    """Types of lines in the csv file (first value)
    """
    SETT = 'Setting'
    CAPT = 'Title'
    WID = 'Width'
    ORIG = 'is_type'
    KEY = 'Keydef'


def readlang(lang):
    "get captions from language file"
    captions = {}
    with (shared.HERELANG / lang).open() as f_in:
        for x in f_in:
            if x[0] == '#' or x.strip() == "":
                continue
            key, value = x.strip().split(None, 1)
            captions[key] = value
        return captions


def get_csv_oms(lang):
    "build descriptions for csv file"
    captions = readlang(lang)
    csv_oms = {shared.SettType.PLG.value: captions['T_NAMOF'].format(captions['S_PLGNAM'],
                                                                     captions['T_NOPY']),
               shared.SettType.PNL.value: captions['T_INSEL'].format(captions['S_PNLNAM']),
               shared.SettType.RBLD.value: captions['T_BOOL'].format(captions['S_RBLD']),
               shared.SettType.DETS.value: captions['T_BOOL'].format(captions['S_DETS']),
               shared.SettType.RDEF.value: captions['T_BOOL'].format(captions['S_RSAV']),
               LineType.CAPT.value: captions['T_COLTTL'],
               LineType.WID.value: captions['T_COLWID'],
               LineType.ORIG.value: captions['T_BOOL'].format(captions['T_COLIND'])}
    return csv_oms


def build_csv_sample_data(lang):
    "create default data lines in the csv file"
    csv_linetypes = [x.value for x in LineType.__members__.values()]
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
            if test[:2] == [LineType.SETT.value, shared.SettType.PLG.value]:
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
        shared.log_exc()
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


def read_settings_json(ini):  # expects pathlib.Path
    "read the application settings from a given file"
    with ini.open() as _in:
        fulldict = json.load(_in)
    settings = {'filename': ini}
    for name in initial_settings:
        settings[name] = fulldict.get(name, '')
    return settings


def write_settings_json(settings, nobackup=False):  # expects settings, including path
    "rewrite the application settings file"
    inifile = settings.pop('filename')
    if inifile.exists() and not nobackup:
        shutil.copyfile(str(inifile), str(inifile) + '~')
    with inifile.open('w') as _in:
        json.dump(settings, _in)


def modify_settings(ini):
    """modify the settings file (specifically the PLUGINS setting)
    """
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
                        data.append(f'    ("{name}", "{path}"),\n')
    with open(inifile, 'w') as _out:
        for line in data:
            _out.write(line)


def read_columntitledata(editor):
    """read the current language file and extract the already defined column headers
    """
    column_textids = []
    column_names = []
    in_section = False

    with (shared.HERELANG / editor.ini["lang"]).open() as f_in:
        for line in f_in:
            line = line.strip()
            if line == '':
                continue
            if line.startswith('#'):
                if in_section:
                    in_section = False
                elif 'Keyboard mapping' in line:
                    in_section = True
                continue
            test = line.split(None, 1)
            shared.log(test, always=True)
            if in_section:
                column_textids.append(test[0])
                column_names.append(test[1])
    return column_textids, column_names


def add_columntitledata(newdata):
    """add the new column title(s) to all language files

    input is a dict of dicts ({language: {textid: text, ...}, ...})
    the previous code assumed a list of tuples ((textid, text), ...) where the same text was copied
      and the translation had to be made afterwards
    """
    for language, data in newdata.items():
        language_file = shared.HERELANG / language
        backup_file = shared.HERELANG / (language + '~')
        shutil.copyfile(str(language_file), str(backup_file))
        in_section = False
        with backup_file.open() as f_in, language_file.open('w') as f_out:
            for line in f_in:
                if line.startswith('# Keyboard mapping'):
                    in_section = True
                elif in_section and line.strip() == '':
                    for textid, text in data.items():
                        f_out.write(f'{textid} {text}\n')
                    in_section = False
                f_out.write(line)


def update_paths(paths, pathdata, lang):
    """read the paths to the csv files from the data returned by the dialog
    if applicable also write a skeleton plugin file
    """
    newpaths = []
    print('in update_paths')
    # for name, path in paths:
    #     print(paths)
    #     loc = path.input.text()         # bv editor/plugins/gitrefs_hotkeys.csv
    for name, loc in paths:
        newpaths.append((name, loc))
        if name in pathdata:
            data = pathdata[name]    # bv. ['editor.plugins.gitrefs_keys', 'gitrefs hotkeys', 0, 0, 0]
            parts = data[0].split('.')
            if parts[0] == '':
                parts = parts[1:]
            newfile = BASE / ('/'.join(parts) + '.py')
            with newfile.open('w') as _out:
                _out.write(plugin_skeleton)
            if os.path.splitext(loc)[1] == '.csv':
                initcsv(BASE / loc, data, lang)
            else:
                initjson(BASE / loc, data)
    return newpaths


def initcsv(loc, data, lang):
    """Initialize csv file

    save some basic settings to a csv file together with some sample data
    """
    csv_oms = get_csv_oms(lang)
    with loc.open("w") as _out:
        wrt = csv.writer(_out)
        for indx, sett in enumerate(shared.csv_settingnames):
            wrt.writerow([LineType.SETT.value, sett, data[indx], csv_oms[sett]])
        for row in build_csv_sample_data(lang):
            wrt.writerow(row)


def initjson(loc, data):    # intended to replace the previous function
    """Initialize json file

    Save some basic settings together with some column info
    """
    writejson(loc, {x: data[i] for i, x in enumerate(shared.csv_settingnames)},
              [["C_KEY", 120, False], ["C_MODS", 90, False], ["C_DESC", 292, False]],
              {}, {})


def readcsv(pad):
    """lees het csv bestand op het aangegeven pad en geeft de inhoud terug

    retourneert dictionary van nummers met (voorlopig) 4-tuples
    """
    data = collections.OrderedDict()
    coldata = []
    settings = collections.OrderedDict()
    # try:
    with open(pad, 'r') as _in:
        rdr = csv.reader(_in)
        rdrdata = list(rdr)
    # except (FileNotFoundError, IsADirectoryError):
    #     raise
    key = 0
    ## first = True
    extrasettings = {}
    for row in rdrdata:
        rowtype, rowdata = row[0], row[1:]
        if rowtype == LineType.SETT.value:
            name, value, desc = rowdata
            settings[name] = value
            if name not in shared.csv_settingnames:
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


def readjson(pad):    # intended to replace the previous function
    """lees het json bestand op het aangegeven pad en geeft de inhoud terug in diverse tabellen
    """
    plugin_name = os.path.splitext(os.path.basename(pad))[0]
    with open(pad) as _in:
        fulldict = json.load(_in)
    settings = fulldict.pop('settings')
    column_info = fulldict.pop('column_info')
    keydata = fulldict.pop('keydata')
    otherstuff = fulldict
    for name, item in otherstuff.items():
        if isinstance(item, set):
            item = list(item)
        if ((plugin_name == 'DC_hotkeys' and name in ('stdkeys', 'defaults'))
                or (plugin_name == 'Nemo_hotkeys' and name == 'defaultkeys')):
            newitem = {}
            for key, value in item.items():
                newkey = ' '.join(list(key))
                if isinstance(value, set):
                    value = list(value)
                newitem[newkey] = value
            item = newitem
        otherstuff[name] = item
    return settings, column_info, keydata, otherstuff


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
                try:
                    settdesc = extrasettoms[name]
                except KeyError:
                    settdesc = ''
            rowdata = LineType.SETT.value, name, value, settdesc
            wrt.writerow(rowdata)
        for ix, row in enumerate([[LineType.CAPT.value], [LineType.WID.value]]):
            row += [x[ix] for x in coldata] + [csvoms[row[0]]]
            wrt.writerow(row)
        wrt.writerow([LineType.ORIG.value] + [int(x[2]) for x in coldata]
                     + [csvoms[LineType.ORIG.value]])
        for keydef in data.values():
            row = [LineType.KEY.value] + list(keydef)
            wrt.writerow(row)
    if extrasettoms:
        settings['extra'] = extrasettoms


def writejson(pad, settings, coldata, data, otherstuff):  # intended to replace the previous function
    """schrijf de meegegeven data als json bestand naar de aangegeven locatie
    """
    if os.path.exists(pad):
        shutil.copyfile(pad, pad + '~')
    plugin_name = os.path.splitext(os.path.basename(pad))[0]
    fulldict = {'settings': settings, 'column_info': coldata, 'keydata': data}
    for name, item in otherstuff.items():
        if isinstance(item, set):
            item = list(item)
        if ((plugin_name == 'DC_hotkeys' and name in ('stdkeys', 'defaults'))
                or (plugin_name == 'Nemo_hotkeys' and name == 'defaultkeys')):
            newitem = {}
            for key, value in item.items():
                newkey = ' '.join(list(key))
                if isinstance(value, set):
                    value = list(value)
                newitem[newkey] = value
            item = newitem
        fulldict[name] = item
    with open(pad, 'w') as out:
        json.dump(fulldict, out)


def quick_check(filename):
    """quick and dirty function for checking a csv file outside of the application

    replicates some things that are done in building the list with keydefs
    so we can catch errors in advance
    """
    if os.path.splitext(filename)[1] == '.csv':
        _, column_info, data = readcsv(filename)
    else:
        column_info, data = readjson(filename)[1:3]
    items = data.items()
    if not items:   # if items is None or len(items) == 0:
        print('No keydefs found in this file')
        return
    for key, data in items:
        try:
            for indx, col in enumerate(column_info):
                _ = data[indx]
        except Exception:
            shared.log_exc()
            print(key, data)
            raise
    print('{filename}: No errors found')


class HotkeyPanel:
    """scherm met de gegevens voor een bepaald tool

    coldata is een list of tuple van 4-tuples die achtereenvolgens aangeven:
        de kolomtitel, de breedte, de index op self.data en of het een soort aangeeft
    verwacht dat de subclass van te voren een attribuut `reader` (de module om de settings
        te lezen) gedefinieerd heeft
    """
    def __init__(self, parent, pad):
        self.pad = pad
        self.parent = parent
        # switch om het gedrag van bepaalde routines tijdens initialisatie te beïnvloeden
        self.initializing_screen = True
        self.modified = False
        self.title = self.parent.parent.title

        self.gui = gui.SingleDataInterface(self.parent.gui, self)

        self.captions = self.parent.parent.captions
        self.filtertext = ''
        self.has_extrapanel = False

        shared.log(self.pad)
        if self.pad == NO_PATH:
            # print('init HotkeyPanel with NO_PATH')
            self.gui.setup_empty_screen(self.captions['I_NOPATH'], self.title)
            return

        nodata = ''
        if self.pad:
            try:
                if os.path.splitext(self.pad)[1] == '.csv':
                    self.settings, self.column_info, self.data = readcsv(self.pad)
                else:
                    self.settings, self.column_info, self.data, self.otherstuff = readjson(self.pad)
            except ValueError as e:
                shared.log_exc()
                nodata = self.captions['I_NOSET'].format(e, self.pad)
            except FileNotFoundError:
                shared.log_exc()
                nodata = self.captions['I_NOSETFIL'].format(self.pad)
        else:
            nodata = self.captions['I_NOSETFIL'].format(self.pad)
        if nodata:
            self.settings, self.column_info, self.data = {}, [], {}

        if not self.settings or not self.column_info:
            tmp = ":\n\n" + nodata if nodata else ""
            nodata = self.captions['I_NODATA'] + tmp
        else:
            try:
                modulename = self.settings[shared.SettType.PLG.value]
            except KeyError:
                shared.log_exc()
                nodata = True
            else:
                try:
                    self.reader = importlib.import_module(modulename)
                except ImportError:
                    shared.log_exc()
                    nodata = True
            if nodata:
                nodata = self.captions['I_NODATA'].replace('data', 'plugin code')

            self.parent.page = self
            # try:
            #     test = self.reader.buildcsv
            # except AttributeError:
            #     shared.log_exc()
            # else:
            # bij json hoeft otherstuff niet meer via buildcsv te worden opgehaald
            if os.path.splitext(self.pad)[1] == '.csv':
                self.otherstuff = {}  # ruimte voor zaken als een lijst met mogelijke commando's
                if hasattr(self.reader, 'buildcsv'):
                    try:
                        self.otherstuff = self.reader.buildcsv(self, showinfo=False)[1]
                    except FileNotFoundError as exception:
                        # shared.log_exc()
                        nodata = self.captions['I_NOSETT'].format(modulename) + f'\n{exception}'

        if nodata:
            # print('init HotkeyPanel with no data', nodata)
            self.gui.setup_empty_screen(nodata, self.title)
            return

        # dump all data to a json file
        # plugin_name = os.path.splitext(os.path.basename(self.pad))[0]
        # with (BASE / f'{plugin_name}.pprint').open('w') as out:
        #     pprint.pprint(self.otherstuff, width=80, stream=out)
        # writejson(str(BASE / f'{plugin_name}.json'), self.settings, self.column_info, self.data,
        #           self.otherstuff)

        try:
            self.has_extrapanel = bool(int(self.settings[shared.SettType.DETS.value]))
        except KeyError:
            shared.log_exc()

        self.title = self.settings["PanelName"]

        # self.has_extrapanel controleert extra initialisaties en het opbouwen van het extra
        # schermdeel - het vullen van veldwaarden hierin gebeurt als gevolg van het vullen
        # van de eerste rij in de listbox, daarom moet deze het laatst
        # self.otherstuff = self.reader.getotherstuff()
        # print('in init: has_extrapanel is', self.has_extrapanel, 'voor', self)
        if self.has_extrapanel:
            # shared.log('extrapanel: %s', self.has_extrapanel)
            self.fields = [x[0] for x in self.column_info]
            self.add_extra_attributes()
            self.gui.add_extra_fields()
            self.gui.set_extrascreen_editable(bool(int(self.settings['RedefineKeys'])))

        self.gui.setup_list()
        if self.has_extrapanel:
            self.refresh_extrascreen(self.gui.getfirstitem())
        self.initializing_screen = False

    def readkeys(self):
        "(re)read the data for the keydef list"
        if os.path.splitext(self.pad)[1] == '.csv':
            self.data = readcsv(self.pad)[2]
        else:
            self.data = readjson(self.pad)[2]

    def savekeys(self):
        """save modified keydef back

        plugin decides if they're also saved back into the tool settings
        """
        self.parent.data = self.data
        try:
            self.reader.savekeys(self)
        except AttributeError:
            shared.log_exc()
        if os.path.splitext(self.pad)[1] == '.csv':
            writecsv(self.pad, self.settings, self.column_info, self.data,
                     self.parent.parent.ini['lang'])
        else:
            writejson(self.pad, self.settings, self.column_info, self.data, self.otherstuff)
        self.set_title(modified=False)

    def setcaptions(self):
        """update captions according to selected language
        """
        self.captions = self.parent.parent.captions
        self.set_title()
        if self.has_extrapanel:
            if 'C_KEY' in self.fields:
                self.gui.set_label_text(self.gui.lbl_key, self.captions['C_KTXT'])
            if 'C_MODS' in self.fields:
                self.gui.set_label_text(self.gui.cb_win, self.captions['M_WIN'].join(("+", "  ")))
                self.gui.set_label_text(self.gui.cb_ctrl, self.captions['M_CTRL'].join(("+", "  ")))
                self.gui.set_label_text(self.gui.cb_alt, self.captions['M_ALT'].join(("+", "  ")))
                self.gui.set_label_text(self.gui.cb_shift, self.captions['M_SHFT'].join(("+", "  ")))
            if 'C_CNTXT' in self.fields:
                self.gui.set_label_text(self.gui.lbl_context, self.captions['C_CNTXT'] + ':')
            if 'C_CMD' in self.fields:
                self.gui.set_label_text(self.gui.txt_cmd, self.captions['C_CMD'])
            if 'C_PARMS' in self.fields:
                self.gui.set_label_text(self.gui.lbl_parms, self.captions['C_PARMS'])
            if 'C_CTRL' in self.fields:
                self.gui.set_label_text(self.gui.lbl_controls, self.captions['C_CTRL'])
            if 'C_BPARMS' in self.fields:
                self.gui.set_label_text(self.gui.pre_parms_label, self.captions['C_BPARMS'] + ':')
            if 'C_APARMS' in self.fields:
                self.gui.set_label_text(self.gui.post_parms_label, self.captions['C_APARMS'] + ':')
            if 'C_FEAT' in self.fields:
                self.gui.set_label_text(self.gui.feature_label, self.captions['C_FEAT'] + ':')
            self.gui.set_label_text(self.gui.b_save, self.captions['C_SAVE'])
            self.gui.set_label_text(self.gui.b_del, self.captions['C_DEL'])
            self.gui.resize_if_necessary()

    def populate_list(self, pos=0):
        """vullen van de lijst
        """
        self.gui.clear_list()

        items = self.data.items()
        if not items:  # if items is None or len(items) == 0:
            return

        for key, data in items:
            try:
                int(key)
            except ValueError:
                shared.log_exc()
                continue
            new_item = self.gui.build_listitem(key)
            for indx, col in enumerate(self.column_info):
                is_soort = col[2]
                try:
                    value = data[indx]
                except IndexError:
                    print(data)
                    raise
                if is_soort:
                    value = 'C_DFLT' if value == 'S' else 'C_RDEF'
                    value = self.captions[value]
                self.gui.set_listitemtext(new_item, indx, value)
            self.gui.add_listitem(new_item)
        self.gui.set_listselection(pos)

    def add_extra_attributes(self):
        """helper stuff for selected keydef, to make editing possible
        """
        self.init_origdata = []
        self.field_indexes = {}
        itemindex = 0
        for text in ('C_KEY', 'C_MODS', 'C_CNTXT', 'C_CMD',
                     'C_PARMS', 'C_CTRL', 'C_BPARMS', 'C_APARMS', 'C_FEAT'):
            if text == 'C_MODS':
                self.init_origdata += [False, False, False, False]
                self.field_indexes[text] = [itemindex, itemindex + 1, itemindex + 2, itemindex + 3]
                itemindex += 4
            else:
                self.init_origdata.append('')
                self.field_indexes[text] = itemindex
                itemindex += 1
            if text == 'C_KEY':
                self.keylist = (list(string.ascii_uppercase) + list(string.digits)
                                + [f"F{i}" for i in range(1, 13)] + named_keys
                                + ['.', ',', '+', '=', '-', '`', '[', ']', '\\', ';', "'", '/'])

        self.contextslist = self.commandslist = self.defkeys = []
        self.contextactionsdict = self.omsdict = self.descriptions = {}
        try:
            self.reader.add_extra_attributes(self)  # user exit
        except AttributeError:
            shared.log_exc()
        if self.keylist:
            self.keylist.sort()

    def set_title(self, modified=None):
        """set title and adapt to modified flag
        if modified flag is not supplied, use its current state
        """
        if modified is not None:
            self.modified = False
        title = self.title
        if self.modified:
            title += ' ' + self.captions["T_MOD"]
        self.gui.set_title(title)

    def exit(self):
        "ask if we can leave the page"
        if self.modified:
            ok, noexit = gui.ask_ync_question(self.gui, 'Q_SAVXIT')
            if ok:
                self.savekeys()
            if noexit:
                return False
        return True

    def on_text(self, *args):
        """on changing a text enty
        """
        if self.initializing_screen:
            return
        text = self.gui.get_widget_text(*args)
        self.defchanged = False
        if 'C_KEY' in self.fields:
            # if text == self._origdata[self.field_indexes['C_KEY']]:
            #     self.defchanged = True
            #     self.gui.enable_save(True)
            # elif text == self._origdata[self.field_indexes['C_KEY']]:
            #     self.defchanged = False
            #     self.gui.enable_save(False)
            state = text == self._origdata[self.field_indexes['C_KEY']]
            self.defchanged = state
            self.gui.enable_save(state)

    def on_combobox(self, *args):
        """callback op het gebruik van een combobox

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        if self.initializing_screen:
            return
        cb, text = self.gui.get_choice_value(*args)
        self.defchanged = False
        for attr in ('cmb_key', 'cmb_context', 'cmb_commando', 'cmb_controls'):
            if not hasattr(self.gui, attr):
                setattr(self.gui, attr, None)
        for field, control in (('C_KEY', self.gui.cmb_key),
                               ('C_CNTXT', self.gui.cmb_context),
                               ('C_CMD', self.gui.cmb_commando),
                               ('C_CTRL', self.gui.cmb_controls)):
            command_changed = self.gui.cmb_commando and self.gui.get_combobox_text(
                self.gui.cmb_commando) == self._origdata[self.field_indexes['C_CMD']]
            key_changed = self.gui.cmb_key and self.gui.get_combobox_text(
                self.gui.cmb_key) == self._origdata[self.field_indexes['C_KEY']]
            if field in self.fields and cb == control:
                fieldindex = self.field_indexes[field]
                if text != self._origdata[fieldindex]:
                    self._newdata[fieldindex] = text
                    if field == 'C_CNTXT':
                        self.gui.init_combobox(self.gui.cmb_commando,
                                               self.contextactionsdict[text] or self.commandslist)
                    elif field == 'C_CMD':
                        text_to_set = self.descriptions.get(text, self.captions['M_NODESC'])
                        self.gui.set_textfield_value(self.gui.txt_oms, text_to_set)
                    if not self.gui.initializing_keydef:
                        self.set_changed_indicators(True)
            elif field != 'C_CMD' and command_changed:
                self.set_changed_indicators(False)
            elif field == 'C_CMD' and key_changed:
                self.set_changed_indicators(False)

    def set_changed_indicators(self, value):
        "mark shortcut as user defined or not"
        self.defchanged = value
        if 'C_CMD' in self.fields:
            self.gui.enable_save(value)

    def on_checkbox(self, *args):
        """callback op het gebruik van een checkbox

        voorlopig alleen voor de modifiers
        """
        if self.initializing_screen:
            return
        cb, state = self.gui.get_check_value(*args)
        for win, indx in zip((self.gui.cb_shift, self.gui.cb_ctrl,
                              self.gui.cb_alt, self.gui.cb_win), self.field_indexes['C_MODS']):
            if cb == win and state != self._origdata[indx]:
                self._newdata[indx] = state
                if not self.gui.initializing_keydef:
                    self.defchanged = True
                    if 'C_CMD' in self.fields:
                        self.gui.enable_save(True)
                break
        else:
            states = [self.gui.get_checkbox_state(self.gui.cb_shift),
                      self.gui.get_checkbox_state(self.gui.cb_ctrl),
                      self.gui.get_checkbox_state(self.gui.cb_alt),
                      self.gui.get_checkbox_state(self.gui.cb_win)]
            if states == [self._origdata[x] for x in self.field_indexes['C_MODS']]:
                self.defchanged = False
                if 'C_CMD' in self.fields:
                    self.gui.enable_save(False)

    def refresh_extrascreen(self, selitem):
        """show new values after changing kb shortcut
        """
        if not selitem:  # bv. bij p0list.clear()
            return
        seli = self.gui.get_itemdata(selitem)
        keydefdata = dict(zip(self.fields, self.data[seli]))
        # print(keydefdata)
        if 'C_CMD' in self.fields:
            self.gui.enable_save(False)
            self.gui.enable_delete(False)
        self._origdata = self.init_origdata[:]
        # self._newdata = self.init_origdata[:]
        fieldnames = {'C_KEY': self.gui.cmb_key,
                      'C_CNTXT': getattr(self.gui, 'cmb_context', None),
                      'C_CMD': getattr(self.gui, 'cmb_commando', None),
                      'C_DESC': getattr(self.gui, 'txt_oms', None),
                      'C_PARMS': getattr(self.gui, 'txt_parms', None),
                      'C_CTRL': getattr(self.gui, 'cmb_controls', None),
                      'C_BPARMS': getattr(self.gui, 'pre_parms_text', None),
                      'C_APARMS': getattr(self.gui, 'post_parms_text', None),
                      'C_FEAT': getattr(self.gui, 'feature_select', None)}
        for text in ('C_KEY', 'C_MODS', 'C_TYPE', 'C_CNTXT', 'C_CMD', 'C_DESC',
                     'C_PARMS', 'C_CTRL', 'C_BPARMS', 'C_APARMS', 'C_FEAT'):
            if text not in keydefdata:
                continue
            if text == 'C_TYPE':
                if bool(int(self.settings[shared.SettType.RDEF.value])):
                    self.gui.enable_delete(keydefdata[text] == 'U')
            elif text == 'C_MODS':
                mods = keydefdata[text]
                checkboxes = self.gui.cb_shift, self.gui.cb_ctrl, self.gui.cb_alt, self.gui.cb_win
                # for cb in checkboxes:
                #     self.gui.set_checkbox_state(cb, False)
                for x, y, z in zip('SCAW', self.field_indexes['C_MODS'], checkboxes):
                    self._origdata[y] = x in mods
                    self.gui.set_checkbox_state(z, x in mods)
            else:
                if text != 'C_DESC':  # description is (vooralsnog) readonly bedoeld
                    self._origdata[self.field_indexes[text]] = keydefdata[text]
                if text == 'C_KEY' and self.keylist is None:
                    self.gui.set_textfield_value(self.gui.txt_key, keydefdata[text])
                elif text in ('C_KEY', 'C_CNTXT', 'C_CMD', 'C_CTRL', 'C_FEAT'):
                    valuelist = self.get_valuelist(text)
                    if valuelist:
                        self.gui.set_combobox_string(fieldnames[text], keydefdata[text], valuelist)
                else:
                    self.gui.set_textfield_value(fieldnames[text], keydefdata[text])
        self._newdata = self._origdata[:]

    def get_valuelist(self, text):
        "iget list of values for a specific category"
        if text == 'C_KEY':
            return self.keylist
        if text == 'C_CNTXT':
            return self.contextslist
        if text == 'C_CMD':
            if 'C_CNTXT' in self.fields:
                self.gui.init_combobox(self.gui.cmb_commando)
                context = self.gui.get_combobox_selection(self.gui.cmb_context)
                if self.contextactionsdict:
                    actionslist = self.contextactionsdict[context]
                else:
                    actionslist = self.commandslist
                self.gui.init_combobox(self.gui.cmb_commando, actionslist)
                return actionslist
            return self.commandslist
        if text == 'C_CTRL':
            return self.controlslist  # only defined in appropriate plugin
        if text == 'C_FEAT':
            return self.featurelist  # only defined in appropriate plugin
        return []

    def process_changed_selection(self, newitem, olditem):
        """bijwerken velden op het hoofdscherm na wijzigen van de selectie

        bevat een soort detectie of de definitie gewijzigd is die rekening probeert
        te houden met of een nieuwe keydef wordt aangemaakt die een kopie is van de
        oude voor een andere keycombo - alleen die triggert ook bij opbouwen van
        het scherm
        """
        self.gui.initializing_keydef = True
        # in de qt versie was deze controle op commentaar gezet
        # in de __init__ is het scherm editable afhankelijk van de setting
        # bool(int(self.settings['RedefineKeys']
        if bool(int(self.settings[shared.SettType.RDEF.value])):
            # eventuele wijzigingen in detailscherm checken
            if not self.initializing_screen:  # in de wx versie zat deze conditie niet
                # zoek naar wijzigingen in sleutelwaarden
                any_change, changedata = self.check_for_changes()
                # zoek de lijstentry behorende bij de nieuwe sleutelwaarden
                found, indx = self.check_for_selected_keydef(changedata)
                # vraag indien nodig of wijzigingen doorgevoerd moeten worden
                make_change = self.ask_what_to_do(any_change, found, newitem, olditem)
                if make_change:
                    newitem = self.apply_changes(found, indx, changedata)
        else:
            newitem = self.gui.get_selected_keydef()
        self.refresh_extrascreen(newitem)
        self.gui.initializing_keydef = False

    def check_for_changes(self):
        "find out what has been changed in the key columns"
        # other_item = other_cntxt = other_cmd = False
        # key = mods = cmnd = context = ''
        # if 'C_KEY' in self.fields:
        #     origkey = self._origdata[self.field_indexes['C_KEY']]
        #     key = self._newdata[self.field_indexes['C_KEY']]
        #     other_item = key != origkey
        # if 'C_MODS' in self.fields:
        #     origmods = ''.join([y for x, y in zip(self.field_indexes['C_MODS'], ('WCAS'))
        #                         if self._origdata[x]])
        #     mods = ''.join([y for x, y in zip(self.field_indexes['C_MODS'], ('WCAS'))
        #                     if self._newdata[x]])
        #     other_item = other_item or mods != origmods
        # # if 'C_CMD' in self.fields:
        # #     origcmd = self._origdata[self.field_indexes['C_CMD']]
        # #     cmnd = self._newdata[self.field_indexes['C_CMD']]
        # #     other_cmd = cmnd != origcmd
        # if 'C_CNTXT' in self.fields:
        #     origcntxt = self._origdata[self.field_indexes['C_CNTXT']]
        #     context = self._newdata[self.field_indexes['C_CNTXT']]
        #     other_cntxt = context != origcntxt
        # return ((other_item, other_cmd, other_cntxt), (key, mods, context))  # cmnd, context))
        changed, changes = [], []
        for text in ('C_KEY', 'C_MODS', 'C_CNTXT'):
            fieldindex = self.field_indexes[text]
            if text != 'C_MODS':
                oldvalue = self._origdata[fieldindex]
                newvalue = self._newdata[fieldindex]
            else:
                indexmap = dict(zip(self.field_indexes[text], ('SCAW')))
                oldvalue = [self._origdata[x] for x in fieldindex]
                newvalue = [self._newdata[x] for x in fieldindex]
            changed.append(newvalue == oldvalue)
            changes.append(newvalue)
        return changed, changes

    def check_for_selected_keydef(self, keydefdata):
        "find the keydef currently selected (if any)"
        # key, mods, cmnd, context = keydefdata
        # found, indx = False, -1
        # for number, item in self.data.items():
        #     keymatch = modmatch = cntxtmatch = True
        #     if 'C_KEY' in self.fields and item[0] != key:
        #         keymatch = False
        #     if 'C_MODS' in self.fields and item[1] != mods:
        #         modmatch = False
        #     if 'C_CNTXT' in self.fields and item[2] != context:
        #         cntxtmatch = False
        #     if keymatch and modmatch and cntxtmatch:
        #         found = True
        #         indx = number
        #         break
        for number, item in self.data.items():
            if all(('C_KEY' in self.fields and item[0] == keydefdata[0],
                    'C_MODS' in self.fields and item[1] == keydefdata[1],
                    'C_CNTXT' in self.fields and item[2] == keydefdata[2])):
                found, indx = True, number
                break
        else:
            found, indx = False, -1
        return found, indx

    def ask_what_to_do(self, changes, found, newitem, olditem):
        "get input on what to do next"
        cursor_moved = newitem != olditem and olditem is not None
        data_changed = self._newdata != self._origdata
        make_change = False
        if data_changed:  # any(changes):
            if cursor_moved:
                make_change = gui.ask_question(self.gui, "Q_SAVCHG")
            elif found:  # changes[0]:
                # if found:
                make_change = gui.ask_question(self.gui, "Q_DPLKEY")
                # else:
                #     make_change = True
            else:
                make_change = True
        return make_change

    def apply_changes(self, found, indx, keydefdata):
        "effectuate the changes as indicated in the gui"
        # key, mods, cmnd, context = keydefdata - we moeten kijken naar self._newdata (alles)
        item = self.gui.get_selected_keydef()
        pos = self.gui.get_keydef_position(item)
        if found:
            for fieldnum, field in self.fields:
                if field[0] == 'C_MODS':
                    self.data[indx][self.fields.index(field)] = keydefdata[1]  # samengevoegde mods
                else:
                    self.data[indx][self.fields.index(field)] = self._newdata[
                        self.field_indexes[field[0]]]
        else:
            # ordereddict opnieuw opbouwen
            newdata = list(self.data.values())
            # dit is heel typisch specifiek voor één bepaalde plugin:
            # newvalue = (key, mods, 'U', cmnd, self.omsdict[cmnd])
            newdata.append(self._newdata)   # newvalue)
            newdata.sort()
            self.data.clear()
            for x, y in enumerate(newdata):
                # if y == newvalue:  # is dit nodig?
                #     indx = x       # want waar gebruik ik die indx verder?
                self.data[x] = y
        self.modified = True
        self._origdata = self._newdata  # self.init_origdata
        # if 'C_KEY' in self.fields:
        #     self._origdata[self.field_indexes['C_KEY']] = key
        # if 'C_MODS' in self.fields:
        #     for mod, ix_mod in zip(('WCAS'), self.field_indexes['C_MODS']):
        #         self._origdata[ix_mod] = mod in mods
        # if 'C_CMD' in self.fields:
        #     self._origdata[self.field_indexes['C_CMD']] = cmnd
        # if 'C_CNTXT' in self.fields:
        #     self._origdata[self.field_indexes['C_CNTXT']] = context
        # # TODO: niet geïmplementeerd voor vikeys.py (is ook read only momenteel)
        # # de implementatie in dckeys.py is subtiel anders:
        # self._origdata[self.field_indexes['C_PARMS']] = newdata[self.field_indexes['C_PARMS']]
        # self._origdata[self.field_indexes['C_CTRL']] = newdata[self.field_indexes['C_CTRL']]
        # #
        newitem = self.gui.get_keydef_at_position(pos)
        self.populate_list(pos)    # refresh
        return newitem

    def apply_deletion(self):
        "remove the indicated keydef"
        item = self.gui.get_selected_keydef()
        pos = self.gui.get_keydef_position(item)
        indx = self.gui.get_itemdata(item)
        if self.captions["{indx:03}"] == 'C_TYPE':
            if self.data[indx][1] == "S":  # can't delete standard key
                gui.show_message(self.parent, 'I_STDDEF')
                return
        elif self.captions["{indx:03}"] == 'C_KEY':
            if self.data[indx][0] in self.defkeys:  # restore standard if any
                cmnd = self.defkeys[self.data[indx][0]]
                if cmnd in self.omsdict:
                    oms = self.omsdict[cmnd]
                else:
                    oms, cmnd = cmnd, ""
                key = self.data[indx][0]                 # is this correct?
                self.data[indx] = (key, 'S', cmnd, oms)  # key UNDEF
            else:
                del self.data[indx]
                ## pos -= 1
        self.gui.enable_save(False)
        self.gui.enable_deleted(False)
        self.set_title(modified=True)
        self.populate_list(pos)    # refresh


class ChoiceBook:
    """Het schermdeel dat de selector, zoekfunctie en de gegevenstabel toont
    """
    def __init__(self, parent):
        self.parent = parent
        self.page = None

        self.gui = gui.TabbedInterface(self.parent.gui, self)
        self.gui.setup_selector()
        self.gui.setup_search()

        for txt, loc in self.parent.ini['plugins']:
            if loc and not os.path.exists(loc):
                loc = str(BASE / loc)
            win = HotkeyPanel(self, loc)
            self.gui.add_subscreen(win)
            try:
                fl = win.settings[shared.SettType.PLG.value]
            except KeyError:
                shared.log_exc()
                fl = ''  # error is handled elsewhere
            self.parent.pluginfiles[txt] = fl
            self.gui.add_to_selector(txt)

        self.gui.format_screen()

    def on_page_changed(self, indx):
        """callback for change in tool page
        """
        # no use finishing this method if certain conditions aren't met
        if self.parent.book is None:        # leaving: not done setting up this object yet?
            # this can happen when the page_changed callback is set up during __init__
            return
        win = self.gui.get_panel()
        self.page = win.master              # change to new selection
        if win is None:                     # leaving: no page selected yet
            return
        if self.page.modified:
            ok = win.exit()
            if not ok:                       # leaving: can't exit modified page yet
                return
        self.parent.gui.statusbar_message(self.parent.captions["M_DESC"].format(
            self.gui.get_selected_tool()))
        self.gui.set_selected_panel(indx)
        win = self.gui.get_panel()
        self.page = win.master              # change to new selection
        self.parent.gui.setup_menu()
        if not all((self.page.settings, self.page.column_info, self.page.data)):
            return                          # leaving: page data incomplete (e.g. no keydefs)
        self.page.setcaptions()
        items = [self.parent.captions[x[0]] for x in self.page.column_info]
        self.gui.update_search(items)

    def on_text_changed(self, text):
        """callback for change in search text
        """
        page = self.page  # self.pnl.currentWidget()
        for ix, item in enumerate(self.page.column_info):
            if self.page.captions[item[0]] == self.gui.get_search_col():
                self.zoekcol = ix
                break
        self.items_found = self.gui.find_items(self.page, text)
        self.gui.init_search_buttons()
        if self.items_found:
            self.gui.set_selected_keydef_item(page, 0)
            self.founditem = 0
            if 1 < len(self.items_found) < len(self.page.data.items()):
                self.gui.enable_search_buttons(next=True, filter=True)
            message = self.parent.captions["I_#FOUND"].format(len(self.items_found))
        else:
            message = self.parent.captions["I_NOTFND"].format(text)
        self.parent.gui.statusbar_message(message)

    def find_next(self, event=None):
        """to next search result
        """
        self.gui.enable_search_buttons(prev=True)
        if self.founditem < len(self.items_found) - 1:
            self.founditem += 1
            self.gui.set_selected_keydef_item(self.page, self.founditem)
        else:
            self.parent.gui.statusbar_message(self.parent.captions["I_NONXT"])
            self.gui.enable_search_buttons(next=False)

    def find_prev(self, event=None):
        """to previous search result
        """
        self.gui.enable_search_buttons(next=True)
        if self.founditem == 0:
            self.parent.gui.statusbar_message(self.parent.captions["I_NOPRV"])
            self.gui.enable_search_buttons(prev=False)
        else:
            self.founditem -= 1
            self.gui.set_selected_keydef_item(self.page, self.founditem)

    def filter(self, event=None):
        """filter shown items according to search text
        """
        if not self.items_found:
            return
        state_text = self.gui.get_filter_state_text()
        text = self.gui.get_search_text()
        self.reposition = self.gui.get_found_keydef_position()
        if state_text == self.parent.captions['C_FILTER']:
            state_text = self.parent.captions['C_FLTOFF']
            self.filter_on = True
            self.page.filtertext = text
            self.page.olddata = self.page.data
            self.page.data = {ix: item for ix, item in enumerate(
                self.page.data.values()) if text.upper() in item[self.zoekcol].upper()}
            self.gui.enable_search_buttons(next=False, prev=False)
            self.gui.enable_search_text(False)
        else:       # self.filter_on == True
            state_text = self.parent.captions['C_FILTER']
            self.filter_on = False
            self.page.filtertext = ''
            self.page.data = self.page.olddata
            self.gui.enable_search_buttons(next=True, prev=True)
            self.gui.enable_search_text(True)
        self.page.populate_list()
        self.gui.set_found_keydef_position()
        self.gui.set_filter_state_text(state_text)
        if self.page.data == self.page.olddata:
            self.on_text_changed(text)  # reselect items_found after setting filter to off


class Editor:
    """Hoofdscherm van de applicatie
    """
    def __init__(self, args):
        shared.save_log()
        ini = args.conf or CONF
        self.ini = read_settings_json(ini)
        self.readcaptions(self.ini['lang'])
        startapp = args.start
        self.title = self.captions["T_MAIN"]
        self.pluginfiles = {}
        self.book = None
        self.gui = gui.Gui(self)
        if self.ini['plugins'] == []:
            self.show_empty_screen()
        else:
            self.gui.set_window_title(self.title)
            self.gui.statusbar_message(self.captions["T_HELLO"].format(self.captions["T_MAIN"]))
            self.book = ChoiceBook(self)
            self.gui.setup_tabs()
            start = 0
            if self.ini.get('title', ''):
                self.title = self.ini['title']
            if startapp:
                try:
                    start = [x for x, y in self.ini['plugins']].index(startapp) + 1
                except ValueError:
                    pass
            if not start and self.ini.get('initial', ''):
                start = [x for x, y in self.ini['plugins']].index(self.ini['initial']) + 1
            start -= 1
            self.book.gui.set_selected_tool(start)
            self.book.on_page_changed(start)
            self.setcaptions()
        self.gui.go()

    def show_empty_screen(self):
        """what to do when there's no data to show
        """
        message = self.captions["EMPTY_CONFIG_TEXT"]
        self.book = SimpleNamespace()
        self.book.gui = gui.DummyPage(self.gui, message)
        self.book.page = SimpleNamespace()
        self.book.page.gui = self.book.gui
        self.gui.resize_empty_screen(640, 80)

    def get_menudata(self):
        """provide the application's menu definition to the program
        """
        return (('M_APP', (('M_SETT', ((('M_LOC', (self.m_loc, 'Ctrl+F')),
                                        ('M_LANG', (self.m_lang, 'Ctrl+L')),
                                        ('M_PREF', (self.m_pref, ''))), '')),
                           ('M_EXIT', (self.m_exit, 'Ctrl+Q')), )),
                ('M_TOOL', (('M_SETT2', ((('M_COL', (self.m_col, '')),
                                          ('M_MISC', (self.m_tool, '')),
                                          ('M_ENTR', (self.m_entry, '')), ), '')),
                            ('M_READ', (self.m_read, 'Ctrl+R')),
                            ('M_RBLD', (self.m_rebuild, 'Ctrl+B')),
                            ('M_SAVE', (self.m_save, 'Ctrl+S')), )),
                ('M_HELP', (('M_ABOUT', (self.m_about, 'Ctrl+H')), )))

    # menu callbacks (event argument is for compatibility between gui toolkits)
    def m_read(self, event=None):
        """(menu) callback voor het lezen van de hotkeys

        vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
        zet de gelezen keys daarna ook in de gui
        """
        if not self.book.page.settings:
            gui.show_message(self.gui, 'I_ADDSET')
            return
        if not self.book.page.modified:
            if not gui.ask_question(self.gui, 'Q_NOCHG'):
                return
        self.book.page.readkeys()
        self.book.page.populate_list()

    def m_save(self, event=None):
        """(menu) callback voor het terugschrijven van de hotkeys

        vraagt eerst of het ok is om de hotkeys weg te schrijven
        vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
        """
        if not self.book.page.modified:
            if not gui.ask_question(self.gui, 'Q_NOCHG'):
                return
        try:
            self.book.page.savekeys()
        except AttributeError:
            shared.log_exc()
            gui.show_message(self.gui, 'I_DEFSAV')
            return
        gui.show_message(self.gui, 'I_RSTRT')

    def m_loc(self, event=None):
        """(menu) callback voor aanpassen van de bestandslocaties

        vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
        toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
        (met name of de opgegeven paden kloppen)
        """
        # self.ini["plugins"] bevat de lijst met tools en csv locaties
        current_programs = [x for x, y in self.ini["plugins"]]
        current_paths = [y for x, y in self.ini["plugins"]]

        self.last_added = None  # wordt in de hierna volgende dialoog ingesteld
        if gui.show_dialog(self, gui.FilesDialog):
            selection = self.book.gui.get_selected_index()
            write_settings_json(self.ini)  # modify_settings(self.ini)

            # update the screen(s)
            # clear the selector and the stackedwidget while pairing up programs and windows
            # that need to be kept or replaced
            hlpdict = {}
            self.book.gui.clear_selector()

            current_items = reversed(list(enumerate(current_programs)))
            new_programs = [x for x, y in self.ini["plugins"]]
            new_paths = [y for x, y in self.ini["plugins"]]
            for indx, program in current_items:  # we need to do this in reverse
                # NB niet alleen de Gui, ook het HotkeyPanel verwijderen
                test = self.book.gui.remove_tool(indx, program, new_programs)
                if test:
                    hlpdict[program] = test
                else:
                    self.pluginfiles.pop(program)

            # add new ones, modify existing or leave them alone
            for indx, program in enumerate(new_programs):
                if program in current_programs:
                    # compare the new and the existing path
                    old_loc = current_paths[current_programs.index(program)]
                    new_loc = new_paths[new_programs.index(program)]
                    if new_loc == old_loc:  # unchanged
                        win = hlpdict[program]
                    else:  # take data from different location
                        win = HotkeyPanel(self.book, new_loc)
                else:  # new entry
                    loc = new_paths[indx]
                    if not os.path.exists(loc):
                        loc = str(BASE / loc)
                    win = HotkeyPanel(self.book, loc)
                self.book.gui.add_tool(program, win)

            if self.last_added:
                selection = self.book.gui.get_new_selection(self.last_added)
            if selection > len(self.ini['plugins']) - 1:
                selection -= 1
            self.book.gui.set_selected_tool(selection)

    def accept_pathsettings(self, name_path_list, settingsdata, names_to_remove):
        """check and confirm input from FilesDialog
        """
        # last_added leegmaken als deze niet meer bestaat
        if self.last_added not in [x[0] for x in name_path_list]:
            self.last_added = ''

        # dit is verplaatst vanuit de `exit` methode omdat het me hier beter op z'n plaats leek
        # when setting is 'fixed', don't remember a startup tool that is removed from the config
        mode = self.ini.get("startup", '')
        pref = self.ini.get("initial", '')
        if mode == shared.mode_f and pref not in [x[0] for x in self.ini['plugins']]:
            oldmode, mode = mode, shared.mode_r
            self.ini['startup'] = mode
            write_settings_json(self.ini)  # self.change_setting('startup', oldmode, mode)
        #

        for ix, entry in enumerate(name_path_list):
            name, csvname = entry
            if name not in [x for x, y in self.ini['plugins']]:
                if not csvname:
                    gui.show_message(self.gui, text=self.captions['I_FILLALL'])
                    return False
                prgname = settingsdata[name][0]
                if not prgname:
                    # try to get the plugin name from the csv file
                    try:
                        if os.path.splitext(csvname)[1] == '.csv':
                            data = readcsv(csvname)
                        else:
                            data = readjson(csvname)
                    except (FileNotFoundError, IsADirectoryError, ValueError):
                        shared.log_exc()
                        gui.show_message(self.gui, text=self.captions['I_NOCSV'].format(csvname))
                        return False
                    try:
                        prgname = data[0][shared.SettType.PLG.value]
                    except KeyError:
                        shared.log_exc()
                        gui.show_message(self.gui, text=self.captions['I_NOPLNAM'].format(csvname))
                        return False
                if len(settingsdata[name]) == 1:  # existing plugin
                    try:
                        _ = importlib.import_module(prgname)
                    except ImportError:
                        shared.log_exc()
                        gui.show_message(self.gui, text=self.captions['I_NOPLREF'].format(csvname))
                        return False

                self.pluginfiles[name] = prgname
        for filename in names_to_remove:
            os.remove(filename)
        newpathdata = {name: entry for name, entry in settingsdata.items() if len(entry) > 1}
        self.ini["plugins"] = update_paths(name_path_list, newpathdata, self.ini["lang"])
        return True

    def m_rebuild(self, event=None):
        """rebuild csv data from (updated) settings
        """
        if not self.book.page.settings:
            gui.show_message(self.gui, 'I_ADDSET')
            return
        # if hasattr(self.reader, 'buildcsv'):
        if hasattr(self.book.page.reader, 'buildcsv'):
            try:
                newdata = self.book.page.reader.buildcsv(self.book.page)
            except FileNotFoundError as exception:
                gui.show_message(self.gui, 'I_ERRRBLD' + '\n({exception})')
                return
        else:
            gui.show_message(self.gui, 'I_DEFRBLD')
            return
        if newdata is None:  # afgebroken
            return
        if newdata[0]:
            self.book.page.data = newdata[0]
            self.book.page.otherstuff = newdata[1]
            if os.path.splitext(self.book.page.pad)[1] == '.csv':
                writecsv(self.book.page.pad, self.book.page.settings, self.book.page.column_info,
                         self.book.page.data, self.ini['lang'])
            else:
                writejson(self.book.page.pad, self.book.page.settings, self.book.page.column_info,
                          self.book.page.data, self.book.page.otherstuff)
            self.book.page.populate_list()
            mld = self.captions['I_RBLD']
        else:
            mld = self.captions['I_NODEFS']
            try:
                test = newdata[1]
            except IndexError:
                mld = self.captions['I_NOEXTRA']
            mld = self.captions['I_NORBLD'].format(self.captions['I_#FOUND'].format(mld))
        gui.show_message(self.gui, text=mld)

    def accept_csvsettings(self, cloc, ploc, title, rebuild, details, redef):
        """check and confirm input from SetupDialog
        """
        if cloc == "":
            gui.show_message(self.gui, 'I_NEEDNAME')
            return False
        cloc = os.path.abspath(cloc)
        if os.path.exists(cloc):
            gui.show_message(self.gui, 'I_GOTSETFIL', args=[cloc])
            return False
        if importlib.util.find_spec(ploc):
            gui.show_message(self.gui, 'I_GOTPLGFIL', args=[ploc])
            return False
        self.gui.loc = cloc
        self.gui.data = [ploc, title, int(rebuild), int(details), int(redef)]
        return True

    def m_tool(self, event=None):
        """define tool-specific settings
        """
        if not self.book.page.settings:
            self.book.page.settings = {x: '' for x in shared.csv_settingnames}
        old_redef = bool(int(self.book.page.settings[shared.SettType.RDEF.value]))
        if gui.show_dialog(self, gui.ExtraSettingsDialog):
            if os.path.splitext(self.book.page.pad)[1] == '.csv':
                writecsv(self.book.page.pad, self.book.page.settings, self.book.page.column_info,
                         self.book.page.data, self.ini['lang'])
            else:
                writejson(self.book.page.pad, self.book.page.settings, self.book.page.column_info,
                          self.book.page.column_info, self.book.page.data, self.book.page.otherstuff)
            test_redef = bool(int(self.book.page.settings[shared.SettType.RDEF.value]))
            test_dets = bool(int(self.book.page.settings[shared.SettType.DETS.value]))
            test_rbld = bool(int(self.book.page.settings[shared.SettType.RBLD.value]))
            self.gui.modify_menuitem('M_SAVE', test_redef)
            self.gui.modify_menuitem('M_RBLD', test_rbld)
            indx, win = self.book.gui.get_selected_panel()
            if test_dets != self.book.page.has_extrapanel:
                self.book.page.has_extrapanel = test_dets
                newwin = HotkeyPanel(self.book, self.ini["plugins"][indx][1]).gui
                self.book.gui.replace_panel(indx, win, newwin)
            elif test_redef != old_redef and test_dets:
                self.book.gui.set_panel_editable(test_redef)

    def accept_extrasettings(self, program, title, rebuild, showdet, redef, data):
        "check and confirm the input from ExtraSettingsDialog"
        if redef and not showdet:
            gui.show_message(self, "I_NODET")
            return False
        if showdet:
            try:
                test = self.book.page.reader.add_extra_attributes
            except AttributeError:
                shared.log_exc()
                gui.show_message(self.gui, "I_IMPLXTRA")
                return False
        self.book.page.settings[shared.SettType.PLG.value] = program
        self.book.page.settings[shared.SettType.PNL.value] = title
        if self.book.page.title != title:
            self.book.page.title = title
            self.book.page.set_title()
        self.book.page.settings[shared.SettType.RBLD.value] = '1' if rebuild else '0'
        self.book.page.settings[shared.SettType.DETS.value] = '1' if showdet else '0'
        self.book.page.settings[shared.SettType.RDEF.value] = '1' if redef else '0'

        settingsdict, settdescdict = {}, {}
        for name, value, desc in data:
            settingsdict[name] = value
            settdescdict[name] = desc
        todelete = []
        for setting in self.book.page.settings:
            if setting not in shared.csv_settingnames:
                todelete.append(setting)
        for setting in todelete:
            del self.book.page.settings[setting]
        self.book.page.settings.update(settingsdict)
        self.book.page.settings['extra'] = settdescdict
        return True

    def m_col(self, event=None):
        """define tool-specific settings: column properties
        """
        self.col_textids, self.col_names = read_columntitledata(self)
        if not self.book.page.settings:
            gui.show_message(self.gui, 'I_ADDSET')
            return
        oldcolcount = len(self.book.page.column_info)
        if not gui.show_dialog(self, gui.ColumnSettingsDialog):
            # strip off old colno and exit
            self.book.page.column_info = [x[:-1] for x in self.book.page.column_info]
            return
        if self.modified:
            new_pagedata = {}
            for key, value in self.book.page.data.items():
                newvalue = []
                for colinf in self.book.page.column_info:
                    test = colinf[-1]
                    if test == 'new':
                        newvalue.append('')
                    else:
                        newvalue.append(value[test])
                new_pagedata[key] = newvalue
            self.book.page.data = new_pagedata
        self.book.page.column_info = [x[:-1] for x in self.book.page.column_info]
        if not self.modified:
            gui.show_message(self.gui, 'I_NOCHG')
            return

        if os.path.splitext(self.book.page.pad)[1] == '.csv':
            writecsv(self.book.page.pad, self.book.page.settings, self.book.page.column_info,
                     self.book.page.data, self.ini['lang'])
        else:
            writejson(self.book.page.pad, self.book.page.settings, self.book.page.column_info,
                      self.book.page.column_info, self.book.page.data, self.book.page.otherstuff)
        headers = [self.captions[col[0]] for col in self.book.page.column_info]
        self.book.page.gui.update_columns(oldcolcount, len(headers))
        self.book.gui.refresh_locs(headers)
        self.book.page.gui.refresh_headers(headers)
        self.book.page.populate_list()

    def accept_columnsettings(self, data):
        "check and confirm input from columnsettings dialog"
        column_info, new_titles = [], []
        # checken op dubbele en vergeten namen
        test = [x[0] for x in data]
        if len(set(test)) != len(test):
            gui.show_message(self.gui, 'I_DPLNAM')
            return False, False  # not ok but continue with dialog
        if len([x for x in test if x]) != len(test):
            gui.show_message(self.gui, 'I_MISSNAM')
            return False, False  # not ok but continue with dialog
        # checken op dubbele kolomnummers
        test = [x[2] for x in data]
        if len(set(test)) != len(test):
            gui.show_message(self.gui, 'I_DPLCOL')
            return False, False  # not ok but continue with dialog
        # lastcol = -1
        for ix, value in enumerate(sorted(data, key=lambda x: x[2])):
            name, width, colno, flag, old_colno = value
            if name in self.col_names:
                name = self.col_textids[self.col_names.index(name)]
            else:
                new_titles.append((name))
            column_info.append([name, width, flag, old_colno])
        if new_titles:
            languages = [x.name for x in shared.HERELANG.iterdir() if x.suffix == ".lng"]
            for indx, name in enumerate(languages):
                if name == self.ini['lang']:
                    colno = indx + 1
                    break
            self.dialog_data = {'textid': 'C_XXX', 'new_titles': new_titles,
                                'languages': languages, 'colno': colno}
            if not gui.show_dialog(self, gui.NewColumnsDialog):
                # gui.show_message(self.gui, 'T_CANCLD')
                return False, True  # not ok, do not continue with dialog
            for item in column_info:
                for key, value in self.dialog_data[self.ini['lang']].items():
                    if item[0] == value:
                        item[0] = key
                        break
            add_columntitledata(self.dialog_data)
            for ix, item in enumerate(new_titles):
                for name, value in self.dialog_data[self.ini['lang']].items():
                    if value == item:
                        new_titles[ix] = (name, item)
                        break
        self.modified = self.book.page.column_info != column_info
        self.book.page.column_info = column_info
        for id_, name in new_titles:
            self.captions[id_] = name
            self.book.page.captions[id_] = name
        return True, False  # ok, done with dialog (but not canceled)

    def accept_newcolumns(self, entries):
        "check and confirm input from newcolumns dialog"
        languages = self.dialog_data['languages']
        modeltext = self.dialog_data['textid']
        # get all the symbols from a language file
        used_symbols = []
        with (shared.HERELANG / self.ini['lang']).open() as _in:
            for line in _in:
                if line.strip() and not line.startswith('#'):
                    used_symbols.append(line.split()[0])
        # check and process the information entered
        print('accepting', entries)
        self.dialog_data = collections.defaultdict(dict)
        for row in entries:
            for colno, col in enumerate(row):
                entered = col
                if not entered:
                    gui.show_message(self.gui, 'T_NOTALL')
                    return False
                if colno == 0:
                    if entered == modeltext:
                        gui.show_message(self.gui, 'T_CHGSTD')
                        return False
                    if entered in used_symbols:
                        gui.show_message(self.gui, 'T_NOTUNIQ', args=(entered,))
                        return False
                    used_symbols.append(entered)
            for ix, col in enumerate(row[1:]):
                # self.dialog_data[row[0]][self.languages[ix]] = col
                self.dialog_data[languages[ix]][row[0]] = col
        return True

    def m_entry(self, event=None):
        """manual entry of keyboard shortcuts
        """
        if not all((self.book.page.settings, self.book.page.column_info)):
            gui.show_message(self.gui, 'I_ADDCOL')
            return
        if gui.show_dialog(self, gui.EntryDialog):
            if self.book.page.data:
                if os.path.splitext(self.book.page.pad)[1] == '.csv':
                    writecsv(self.book.page.pad, self.book.page.settings,
                             self.book.page.column_info, self.book.page.data, self.ini['lang'])
                else:
                    writejson(self.book.page.pad, self.book.page.settings,
                              self.book.page.column_info, self.book.page.data, self.otherstuff)
                self.book.page.populate_list()

    def m_lang(self, event=None):
        """(menu) callback voor taalkeuze

        past de settings aan en leest het geselecteerde language file
        """
        # bepaal welke language files er beschikbaar zijn
        choices = [x.name for x in shared.HERELANG.iterdir() if x.suffix == ".lng"]
        # bepaal welke er momenteel geactiveerd is
        oldlang = self.ini['lang']
        indx = choices.index(oldlang) if oldlang in choices else 0
        lang, ok = gui.get_choice(self.gui, self.captions["P_SELLNG"], self.title, choices,
                                  current=indx)
        if ok:
            # self.change_setting('lang', oldlang, lang)
            self.ini['lang'] = lang
            write_settings_json(self.ini)
            self.readcaptions(lang)
            self.setcaptions()

    def m_about(self, event=None):
        """(menu) callback voor het tonen van de "about" dialoog
        """
        text = '\n'.join(self.captions['T_ABOUT'].format(self.captions['T_SHORT'], VRS, AUTH,
                                                         self.captions['T_LONG']).split(' / '))
        gui.show_message(self.gui, text=text)

    def m_pref(self, event=None):
        """mogelijkheid bieden om een tool op te geven dat default getoond wordt
        """
        oldpref = self.ini.get("initial", None)
        oldmode = self.ini.get("startup", None)
        self.prefs = oldmode, oldpref
        if gui.show_dialog(self, gui.InitialToolDialog):
            changed = False
            mode, pref = self.prefs
            if mode:
                self.ini['startup'] = mode
                changed = True  # self.change_setting('startup', oldmode, mode)
            if mode == 'Fixed':
                self.ini['initial'] = pref
                changed = True  # self.change_setting('initial', oldpref, pref)
            if changed:
                write_settings_json(self.ini)

    def accept_startupsettings(self, fix, remember, pref):
        """check and confirm input from initialToolDialog
        """
        if fix:
            mode = shared.mode_f
        elif remember:
            mode = shared.mode_r
        else:
            mode = None
        self.prefs = mode, pref

    def m_exit(self, event=None):
        """(menu) callback om het programma direct af te sluiten
        """
        self.exit()

    # other methods
    def exit(self, event=None):
        """quit the application - extra actions to perform on closing
        """
        if not self.book.page.exit():
            return
        mode = self.ini.get("startup", '')
        pref = self.ini.get("initial", '')
        # when setting is 'remember', set the remembered tool to the current one
        if mode == shared.mode_r:
            try:
                # oldpref, pref = pref, self.book.gui.get_selected_text()
                self.ini['initial'] = self.book.gui.get_selected_text()
            except AttributeError:  # selector bestaat niet als er geen tool pages zijn
                pass
            else:
                # self.change_setting('initial', oldpref, pref)
                write_settings_json(self.ini, nobackup=True)

        # super().close()
        self.gui.close()

    def change_setting(self, setting, old, new):
        "change a setting and write it immediately"
        setting = setting.upper()
        inifile = self.ini['filename']
        shutil.copyfile(inifile, inifile + '.bak')
        with open(inifile + '.bak') as _in:
            lines = _in.readlines()
        for ix, line in enumerate(lines):
            if setting is not None and line.startswith(setting):
                if not old:
                    lines[ix] = line.replace("''", "'{new}'")
                elif not new:
                    lines[ix] = line.replace("'{old}'", "''")
                    if setting == 'TITLE':
                        lines[ix - 2: ix + 1] = [lines[ix - 2]]
                else:
                    lines[ix] = line.replace(old, new)
                break
        else:
            lines.append("# {self.captions['C_' + setting]}\n")
            lines.append("{setting} = '{new}'\n")
        with open(inifile, 'w') as _out:
            _out.writelines(lines)

    def readcaptions(self, lang):
        """get captions from language file or settings
        """
        self.captions = readlang(lang)
        self.last_textid = ''

    def setcaptions(self):
        """propagate captions to other parts of the application
        """
        # self.set_title()
        self.gui.setcaptions()
        self.book.gui.setcaptions()
        self.book.page.setcaptions()
