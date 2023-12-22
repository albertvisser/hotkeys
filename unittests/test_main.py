"""Hotkeys unittests for main.py
"""
import types
import pytest
import editor.main as testee


def test_readlang(monkeypatch, capsys, tmp_path):
    mock_lang = tmp_path / 'hotkeys' / 'lang'
    monkeypatch.setattr(testee.shared, 'HERELANG', mock_lang)
    mock_lang.mkdir(parents=True)
    (mock_lang / 'en').write_text("#deze overslaan\n\ncode text\n\nalso a code with text\n")
    assert testee.readlang('en') == {'code': 'text', 'also': 'a code with text'}

class MockSettType(testee.enum.Enum):
    PLG = 'plg'
    PNL = 'pnl'
    RBLD = 'rbld'
    DETS = 'dets'
    RDEF = 'rdef'

class MockLineType(testee.enum.Enum):
    SETT = 'sett'
    CAPT = 'capt'
    WID = 'wid'
    ORIG = 'orig'
    KEY = 'key'

def test_get_csv_oms(monkeypatch, capsys):
    def mock_read(lang):
        print(f'called readlang with arg `{lang}`')
        return { 'T_NAMOF': '{} {} name', 'S_PLGNAM' : 'plugin', 'T_NOPY': 'module',
                'T_INSEL': '{} name', 'S_PNLNAM': 'panel', 'T_BOOL': '{} option',
                'S_RBLD': 'rebuild', 'S_DETS': 'details', 'S_RSAV': 'resave', 'T_COLTTL': 'coltitle',
                'T_COLWID': 'colwidth', 'T_COLIND': 'colind'}
    monkeypatch.setattr(testee, 'readlang', mock_read)
    monkeypatch.setattr(testee.shared, 'SettType', MockSettType)
    monkeypatch.setattr(testee, 'LineType', MockLineType)
    assert testee.get_csv_oms('x') == {'plg': 'plugin module name', 'pnl': 'panel name',
                                       'rbld': 'rebuild option', 'dets': 'details option',
                                       'rdef': 'resave option', 'capt': 'coltitle',
                                       'wid': 'colwidth', 'orig': 'colind option'}
    assert capsys.readouterr().out == 'called readlang with arg `x`\n'

# niet meer nodig als ik alleen nog maar met json werk
def test_build_csv_sample_data(monkeypatch, capsys):
    def mock_get(lang):
        print(f'called get_csv_oms with arg `{lang}`')
        return {'plg': 'plugin module name', 'pnl': 'panel name', 'rbld': 'rebuild option',
                'dets': 'details option', 'rdef': 'resave option', 'capt': 'coltitle',
                'wid': 'colwidth', 'orig': 'colind option'}
    monkeypatch.setattr(testee, 'get_csv_oms', mock_get)
    monkeypatch.setattr(testee.shared, 'SettType', MockSettType)
    monkeypatch.setattr(testee, 'LineType', MockLineType)
    assert testee.build_csv_sample_data('en') == [['capt', 'C_KEY', 'C_MODS', 'C_DESC', 'coltitle'],
                                                  ['wid', 120, 90, 292, 'colwidth'],
                                                  ['orig', 0, 0, 0, 'colind option']]
    assert capsys.readouterr().out == 'called get_csv_oms with arg `en`\n'

# wordt niet (meer) gebruikt
def _test_get_pluginname(monkeypatch, capsys):
    testee.get_pluginname(csvname)

# te vervangen door de hierna volgende
def _test_read_settings(monkeypatch, capsys):
    # zolang ik dit met een python module doe moet ik dit importeren
    # en kan ik het niet testen met behulp van tmp_path
    def mock_log_exc():
        print('called shared.log_exc')
    monkeypatch.setattr(testee.shared, 'log_exc', mock_log_exc)
    with open('fake_module.py', 'w') as f:
        f.write('"""settings for hotkeys\n"""\n')
    assert testee.read_settings('fake_module') == {
            'filename': '/home/albert/projects/hotkeys/fake_module.py',
            'plugins': [], 'lang': 'english.lng'}
    assert capsys.readouterr().out == ''
    with open('fake_module_2.py', 'w') as f:
        f.write('"""settings for hotkeys\n"""\nPLUGINS = ["x", "y"]\nLANG = "z"\n'
                'INITIAL = "a"\nSTARTUP = "b"\n')
    # breakpoint()
    assert testee.read_settings('fake_module_2') == {
            'filename': '/home/albert/projects/hotkeys/fake_module_2.py',
            'plugins': ['x', 'y'], 'lang': 'z', 'initial': 'a', 'startup': 'b'}
    assert capsys.readouterr().out == ''
    assert testee.read_settings('fake_module_3') == {'plugins': [], 'lang': 'english.lng'}
    assert capsys.readouterr().out == 'called shared.log_exc\n'
    testee.os.remove('fake_module.py')
    testee.os.remove('fake_module_2.py')

def test_read_settings_json(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(testee, 'initial_settings', {'x': '', 'a': ''})
    ini = tmp_path / 'settingsfile'
    ini.write_text('{"a": "b", "q": "r"}\n')
    assert testee.read_settings_json(ini) == {'a': 'b', 'filename': ini, 'x': ''}

def test_write_settings_json(monkeypatch, capsys, tmp_path):
    def mock_copy(*args):
        print('called shutil.copyfile with args', args)
    def mock_dump(*args):
        print('called json.dump with arg', args[0])
    monkeypatch.setattr(testee.json, 'dump', mock_dump)
    monkeypatch.setattr(testee.shared.pathlib.Path, 'exists', lambda *x: False)
    monkeypatch.setattr(testee, 'initial_settings', {'x': '', 'a': ''})
    ini = tmp_path / 'settingsfile'
    testee.write_settings_json(settings = {'a': 'b', 'filename': ini, 'x': 'y'})
    assert capsys.readouterr().out == "called json.dump with arg {'a': 'b', 'x': 'y'}\n"
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
    monkeypatch.setattr(testee.shared.pathlib.Path, 'exists', lambda *x: True)
    testee.write_settings_json(settings = {'a': 'b', 'filename': ini, 'x': 'y'})
    assert capsys.readouterr().out == (f"called shutil.copyfile with args ('{ini}',"
                                       f" '{str(ini) + '~'}')\n"
                                       "called json.dump with arg {'a': 'b', 'x': 'y'}\n")
    testee.write_settings_json(settings = {'a': 'b', 'filename': ini, 'x': 'y'}, nobackup=True)
    assert capsys.readouterr().out == "called json.dump with arg {'a': 'b', 'x': 'y'}\n"

def test_modify_settings(monkeypatch, capsys, tmp_path):
    ini = {'filename': str(tmp_path / 'settings'), 'plugins': [('x', 'y'), ('a', 'b')]}
    (tmp_path / 'settings').write_text('ppp\n\nPLUGINS\nqqq\n  ]  \nrrr\nsss\n')
    testee.modify_settings(ini)
    assert (tmp_path / 'settings.bak').read_text() == 'ppp\n\nPLUGINS\nqqq\n  ]  \nrrr\nsss\n'
    assert (tmp_path / 'settings').read_text() == ('ppp\n\nPLUGINS\n    ("x", "y"),\n'
                                                   '    ("a", "b"),\n  ]  \nrrr\nsss\n')

def test_read_columntitledata(monkeypatch, capsys, tmp_path):
    def mock_log(*args, **kwargs):
        print('called shared.log with args', args, kwargs)
    monkeypatch.setattr(testee.shared, 'log', mock_log)
    monkeypatch.setattr(testee.shared, 'HERELANG', tmp_path / 'languages')
    editor = types.SimpleNamespace(ini={'lang': 'en.lng'})
    (tmp_path / 'languages').mkdir()
    (tmp_path / 'languages' / 'en.lng').write_text(
            'aaa\nbbb\n\n# Keyboard mapping\nID1 text1\nID2 text 2\n#end\nID3 text3\n')
    assert testee.read_columntitledata(editor) == (['ID1', 'ID2'], ['text1', 'text 2'])
    assert capsys.readouterr().out == (
            "called shared.log with args (['aaa'],) {'always': True}\n"
            "called shared.log with args (['bbb'],) {'always': True}\n"
            "called shared.log with args (['ID1', 'text1'],) {'always': True}\n"
            "called shared.log with args (['ID2', 'text 2'],) {'always': True}\n"
            "called shared.log with args (['ID3', 'text3'],) {'always': True}\n")

def test_add_columntitledata(monkeypatch, capsys, tmp_path):
    mock_lang = tmp_path / 'hotkeys' / 'lang'
    monkeypatch.setattr(testee.shared, 'HERELANG', mock_lang)
    mock_lang.mkdir(parents=True)
    oldtext_start = 'aa bb\ncc dd\n\n# Keyboard mapping...\npp rr\n'
    oldtext_end = '\nss tt\n'
    (mock_lang / 'en').write_text(oldtext_start + oldtext_end)
    (mock_lang / 'nl').write_text(oldtext_start + oldtext_end)
    newdata = {'en': {'a': 'b'}, 'nl': {'x': 'y'}}
    testee.add_columntitledata(newdata)
    assert (mock_lang / 'en~').read_text() == oldtext_start + oldtext_end
    assert (mock_lang / 'nl~').read_text() == oldtext_start + oldtext_end
    assert (mock_lang / 'en').read_text() == oldtext_start + 'a b\n' + oldtext_end
    assert (mock_lang / 'nl').read_text() == oldtext_start + 'x y\n' + oldtext_end

def test_update_paths(monkeypatch, capsys):
    def mock_write(*args):
        print('called path.write with args', args)
    def mock_initcsv(*args):
        print('called initcsv with args', args)
    def mock_initjson(*args):
        print('called initjson with args', args)
    monkeypatch.setattr(testee.shared.pathlib.Path, 'write_text', mock_write)
    monkeypatch.setattr(testee, 'initcsv', mock_initcsv)
    monkeypatch.setattr(testee, 'initjson', mock_initjson)
    paths = (('xx', 'yy.csv'), ('aa', 'bb.json'))
    pathdata = {'xx': ['xx.yy.zz', 'xxx', 1, 0, 0], 'aa': ['.bb.cc', 'aaa', 1, 1, 1]}
    assert testee.update_paths(paths, pathdata, 'en') == [('xx', 'yy.csv'), ('aa', 'bb.json')]

# niet meer nodig als ik alleen nog maar met json werk
def _test_initcsv(monkeypatch, capsys):
    testee.initcsv(loc, data, lang)

def test_initjson(monkeypatch, capsys):
    def mock_write(*args):
        print('called writejson with args', args)
    monkeypatch.setattr(testee, 'writejson', mock_write)
    monkeypatch.setattr(testee.shared, 'csv_settingnames', ['x', 'y'])
    monkeypatch.setattr(testee, 'initial_columns', (('a', 1, True), 'b', 2, False))
    testee.initjson('settfile', ['xxx', 'yyy'])
    assert capsys.readouterr().out == ("called writejson with args"
                                       " ('settfile', {'x': 'xxx', 'y': 'yyy'},"
                                       " [(('a', 1, True), 'b', 2, False)], {}, {})\n")

# niet meer nodig als ik alleen nog maar met json werk
def _test_readcsv(monkeypatch, capsys):
    testee.readcsv(pad)

def _test_readjson(monkeypatch, capsys, tmp_path):
    (tmp_path / 'test' / 'plugin.json').write_text(
         '{"settings": {"settings": "dict"}, "column_info": [["column", "info"]],'
         ' "keydata": {"keycombo": "dict"}, "otherstuff": {}')
    testee.readjson('test/plugin.json')

# niet meer nodig als ik alleen nog maar met json werk
def _test_writecsv(monkeypatch, capsys):
    testee.writecsv(pad, settings, coldata, data, lang)

def _test_writejson(monkeypatch, capsys):
    testee.writejson(pad, settings, coldata, data, otherstuff)

def test_quick_check(monkeypatch, capsys):
    def mock_log_exc():
        print('called shared.log_exc')
    def mock_readcsv(arg):
        print(f'called readcsv with arg `{arg}`')
        return {}, [[], []], {1: ['x', 'y'], 2: ['a', 'b']}
    def mock_readjson(arg):
        print(f'called readjson with arg `{arg}`')
        return {}, [[], []], {}, {}
    def mock_readjson_2(arg):
        print(f'called readjson with arg `{arg}`')
        return {}, [[], []], {1: [], 2: []}, {}
    monkeypatch.setattr(testee.shared, 'log_exc', mock_log_exc)
    monkeypatch.setattr(testee, 'readcsv', mock_readcsv)
    monkeypatch.setattr(testee, 'readjson', mock_readjson)
    testee.quick_check('plugin.csv')
    assert capsys.readouterr().out == ('called readcsv with arg `plugin.csv`\n'
                                       'plugin.csv: No errors found\n')
    testee.quick_check('plugin.json')
    assert capsys.readouterr().out == ('called readjson with arg `plugin.json`\n'
                                       'plugin.json: No keydefs found in this file\n')
    monkeypatch.setattr(testee, 'readjson', mock_readjson_2)
    testee.quick_check('plugin.json')
    assert capsys.readouterr().out == ('called readjson with arg `plugin.json`\n'
                                       'inconsistent item lengths in plugin.json\n'
                                       '1 []\n')

class MockSDI:
    def __init__(self, *args):
        print('called SingleDataInterface.__init__ with args', args)
    def setup_empty_screen(self, *args):
        print('called SDI.setup_empty_screen with args', args)
    def add_extra_fields(self):
        print('called SDI.add_extra_fields')
    def set_extrascreen_editable(self, *args):
        print('called SDI.set_extrascreen_editable with args', args)
    def setup_list(self):
        print('called SDI.setup_list')
    def getfirstitem(self):
        return 'first_item'

class MockReader:
    pass

def test_hotkeypanel_init(monkeypatch, capsys):
    def mock_log(text):
        print(f'called shared.log with arg `{text}`')
    def mock_log_exc():
        print('called shared.log_exc')
    def mock_readcsv(arg):
        print(f'called readcsv with arg `{arg}`')
        return {'x': 'y'}, [], {1: ['x', 'y'], 2: ['a', 'b']}
    def mock_readjson_exc_1(arg):
        raise ValueError('A ValueError')
    def mock_readjson_exc_2(arg):
        raise FileNotFoundError('A FileNotFoundError')
    def mock_readjson(arg):
        print(f'called readjson with arg `{arg}`')
        return {'x': 'y'}, [[], []], {}, {}
    def mock_readjson_2(arg):
        print(f'called readjson with arg `{arg}`')
        return {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '0'}, [[], []], {}, {}
    def mock_readjson_3(arg):
        print(f'called readjson with arg `{arg}`')
        return ({'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '1',
                 'RedefineKeys': '0'}, [['x', 0], ['y', 1]], {}, {})
    def mock_import_nok(*args):
        print('called importlib.import_module with args', args)
        raise ImportError
    def mock_import_ok(*args):
        print('called importlib.import_module with args', args)
        return MockReader()
    def mock_add(self):
        print('called HotkeyPanel.add_extra_attributes')
    def mock_refresh(self, arg):
        print(f'called HotkeyPanel.refresh_extrascreen with arg {arg}')
    pad = 'NO_PATH'
    parent = types.SimpleNamespace(parent=types.SimpleNamespace(title='A title',
                                                                captions={'I_NOPATH': 'no path',
                                                                    'I_NOSET': '{}',
                                                                    'I_NOSETFIL': '{} not found',
                                                                    'I_NOSETT': '{} no settings',
                                                                    'I_NODATA': 'no data'}),
                                   gui='parent gui')
    monkeypatch.setattr(testee.gui, 'SingleDataInterface', MockSDI)
    monkeypatch.setattr(testee.shared, 'log_exc', mock_log_exc)
    monkeypatch.setattr(testee.shared, 'log', mock_log)
    monkeypatch.setattr(testee, 'readcsv', mock_readcsv)
    testobj = testee.HotkeyPanel(parent, pad)
    assert testobj.pad == pad
    assert testobj.parent == parent
    assert testobj.initializing_screen
    assert not testobj.modified
    assert testobj.title == 'A title'
    assert testobj.captions == parent.parent.captions
    assert testobj.filtertext == ''
    assert not testobj.has_extrapanel
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `NO_PATH`\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no path', 'A title')\n")

    monkeypatch.setattr(testee, 'readjson', mock_readjson)
    testobj = testee.HotkeyPanel(parent, '')
    assert (testobj.settings, testobj.column_info, testobj.data) == ({}, [], {})
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg ``\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no data:\\n\\nempty filename', 'A title')\n")

    monkeypatch.setattr(testee, 'readjson', mock_readjson_exc_1)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == ({}, [], {})
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.json`\n'
                                       'called shared.log_exc\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no data:\\n\\nA ValueError', 'A title')\n")

    monkeypatch.setattr(testee, 'readjson', mock_readjson_exc_2)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == ({}, [], {})
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.json`\n'
                                       'called shared.log_exc\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no data:\\n\\nplugin.json not found', 'A title')\n")

    testobj = testee.HotkeyPanel(parent, 'plugin.csv')
    assert (testobj.settings, testobj.column_info, testobj.data) == ( {'x': 'y'}, [],
                                                                     {1: ['x', 'y'], 2: ['a', 'b']})
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.csv`\n'
                                       'called readcsv with arg `plugin.csv`\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no data', 'A title')\n")

    monkeypatch.setattr(testee, 'readjson', mock_readjson)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == ({'x': 'y'}, [[], []], {})
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.json`\n'
                                       'called readjson with arg `plugin.json`\n'
                                       'called shared.log_exc\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no plugin code', 'A title')\n")

    monkeypatch.setattr(testee, 'readjson', mock_readjson_2)
    monkeypatch.setattr(testee.importlib, 'import_module', mock_import_nok)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == (
            {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '0'}, [[], []], {})
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.json`\n'
                                       'called readjson with arg `plugin.json`\n'
                                       "called importlib.import_module with args ('plugin',)\n"
                                       'called shared.log_exc\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no plugin code', 'A title')\n")
    # eigenlijk nog 2 of 3 pogingen met csv voor aanroepen van buildcsv
    # omdat ik dat weg ga gooien laat ik het even zitten
    monkeypatch.setattr(testee.importlib, 'import_module', mock_import_ok)
    monkeypatch.setattr(testee.HotkeyPanel, 'add_extra_attributes', mock_add)
    monkeypatch.setattr(testee.HotkeyPanel, 'refresh_extrascreen', mock_refresh)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == (
            {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '0'}, [[], []], {})
    assert not testobj.has_extrapanel
    assert testobj.title == 'A Panel'
    assert not testobj.initializing_screen
    assert capsys.readouterr().out == ("called SingleDataInterface.__init__ with args"
                                       f" ('parent gui', {testobj})\n"
                                       "called shared.log with arg `plugin.json`\n"
                                       "called readjson with arg `plugin.json`\n"
                                       "called importlib.import_module with args ('plugin',)\n"
                                       "called SDI.setup_list\n")

    monkeypatch.setattr(testee, 'readjson', mock_readjson_3)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == (
            {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '1', 'RedefineKeys': '0'},
            [['x', 0], ['y', 1]], {})
    assert testobj.has_extrapanel
    assert testobj.title == 'A Panel'
    assert not testobj.initializing_screen
    assert capsys.readouterr().out == ("called SingleDataInterface.__init__ with args"
                                       f" ('parent gui', {testobj})\n"
                                       "called shared.log with arg `plugin.json`\n"
                                       "called readjson with arg `plugin.json`\n"
                                       "called importlib.import_module with args ('plugin',)\n"
                                       "called HotkeyPanel.add_extra_attributes\n"
                                       "called SDI.add_extra_fields\n"
                                       "called SDI.set_extrascreen_editable with args (False,)\n"
                                       "called SDI.setup_list\n"
                                       "called HotkeyPanel.refresh_extrascreen with arg first_item\n")

def setup_hotkeypanel(monkeypatch, capsys):
    def mock_init(self, *args):
        self.parent = types.SimpleNamespace(parent=types.SimpleNamespace)
        self.gui = types.SimpleNamespace()
        print('called HotkeyPanel.__init__ with args', args)
    monkeypatch.setattr(testee.HotkeyPanel, '__init__', mock_init)
    return testee.HotkeyPanel()

def test_hotkeypanel_readkeys(monkeypatch, capsys):
    def mock_readcsv(arg):
        print(f'called readcsv with arg `{arg}`')
        return {}, [], 'csvdata'
    def mock_readjson(arg):
        print(f'called readjson with arg `{arg}`')
        return {}, [], 'jsondata', {}
    monkeypatch.setattr(testee, 'readcsv', mock_readcsv)
    monkeypatch.setattr(testee, 'readjson', mock_readjson)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    assert capsys.readouterr().out == 'called HotkeyPanel.__init__ with args ()\n'
    testobj.pad = 'plugin.csv'
    testobj.readkeys()
    assert testobj.data == 'csvdata'
    assert capsys.readouterr().out == 'called readcsv with arg `plugin.csv`\n'
    testobj.pad = 'plugin.json'
    testobj.readkeys()
    assert testobj.data == 'jsondata'
    assert capsys.readouterr().out == 'called readjson with arg `plugin.json`\n'

def _test_hotkeypanel_savekeys(monkeypatch, capsys):
    testobj.savekeys()

def _test_hotkeypanel_setcaptions(monkeypatch, capsys):
    testobj.setcaptions()

def _test_hotkeypanel_populate_list(monkeypatch, capsys):
    testobj.populate_list(pos=0)

def _test_hotkeypanel_add_extra_attributes(monkeypatch, capsys):
    testobj.add_extra_attributes()

def _test_hotkeypanel_set_title(monkeypatch, capsys):
    testobj.set_title(modified=None)

def _test_hotkeypanel_exit(monkeypatch, capsys):
    testobj.exit()

def _test_hotkeypanel_on_text(monkeypatch, capsys):
    testobj.on_text(*args)

def _test_hotkeypanel_on_combobox(monkeypatch, capsys):
    testobj.on_combobox(*args)

def _test_hotkeypanel_set_changed_indicators(monkeypatch, capsys):
    testobj.set_changed_indicators(value)

def _test_hotkeypanel_on_checkbox(monkeypatch, capsys):
    testobj.on_checkbox(*args)

def _test_hotkeypanel_refresh_extrascreen(monkeypatch, capsys):
    testobj.refresh_extrascreen(selitem)

def _test_hotkeypanel_get_valuelist(monkeypatch, capsys):
    testobj.get_valuelist(text)

def _test_hotkeypanel_process_changed_selection(monkeypatch, capsys):
    testobj.process_changed_selection(newitem, olditem)

def _test_hotkeypanel_check_for_changes(monkeypatch, capsys):
    testobj.check_for_changes()

def _test_hotkeypanel_check_for_selected_keydef(monkeypatch, capsys):
    testobj.check_for_selected_keydef(keydefdata)

def _test_hotkeypanel_ask_what_to_do(monkeypatch, capsys):
    testobj.ask_what_to_do(changes, found, newitem, olditem)

def _test_hotkeypanel_apply_changes(monkeypatch, capsys):
    testobj.apply_changes(found, indx, keydefdata)

def _test_hotkeypanel_apply_deletion(monkeypatch, capsys):
    testobj.apply_deletion()

def _test_choicebook_init(monkeypatch, capsys):
    testobj = testee.ChoiceBook()

def _test_choicebook_on_page_changed(monkeypatch, capsys):
    testobj.on_page_changed(indx)

def _test_choicebook_on_text_changed(monkeypatch, capsys):
    testobj.on_text_changed(text)

def _test_choicebook_find_next(monkeypatch, capsys):
    testobj.find_next(event=None)

def _test_choicebook_find_prev(monkeypatch, capsys):
    testobj.find_prev(event=None)

def _test_choicebook_filter(monkeypatch, capsys):
    testobj.filter(event=None)

def _test_editor_init(monkeypatch, capsys):
    testobj = testee.Editor(args)

def _test_editor_show_empty_screen(monkeypatch, capsys):
    testobj.show_empty_screen()

def _test_editor_get_menudata(monkeypatch, capsys):
    testobj.get_menudata()

def _test_editor_m_read(monkeypatch, capsys):
    testobj.m_read(event=None)

def _test_editor_m_save(monkeypatch, capsys):
    testobj.m_save(event=None)

def _test_editor_m_loc(monkeypatch, capsys):
    testobj.m_loc(event=None)

def _test_editor_accept_pathsettings(monkeypatch, capsys):
    testobj.accept_pathsettings(name_path_list, settingsdata, names_to_remove)

def _test_editor_m_rebuild(monkeypatch, capsys):
    testobj.m_rebuild(event=None)

def _test_editor_accept_csvsettings(monkeypatch, capsys):
    testobj.accept_csvsettings(cloc, ploc, title, rebuild, details, redef)

def _test_editor_m_tool(monkeypatch, capsys):
    testobj.m_tool(event=None)

def _test_editor_accept_extrasettings(monkeypatch, capsys):
    testobj.accept_extrasettings(program, title, rebuild, showdet, redef, data)

def _test_editor_m_col(monkeypatch, capsys):
    testobj.m_col(event=None)

def _test_editor_accept_columnsettings(monkeypatch, capsys):
    testobj.accept_columnsettings(data)

def _test_editor_accept_newcolumns(monkeypatch, capsys):
    testobj.accept_newcolumns(entries)

def _test_editor_m_entry(monkeypatch, capsys):
    testobj.m_entry(event=None)

def _test_editor_m_lang(monkeypatch, capsys):
    testobj.m_lang(event=None)

def _test_editor_m_about(monkeypatch, capsys):
    testobj.m_about(event=None)

def _test_editor_m_pref(monkeypatch, capsys):
    testobj.m_pref(event=None)

def _test_editor_accept_startupsettings(monkeypatch, capsys):
    testobj.accept_startupsettings(fix, remember, pref)

def _test_editor_m_exit(monkeypatch, capsys):
    testobj.m_exit(event=None)

def _test_editor_exit(monkeypatch, capsys):
    testobj.exit(event=None)

def _test_editor_change_setting(monkeypatch, capsys):
    testobj.change_setting(setting, old, new)

def _test_editor_readcaptions(monkeypatch, capsys):
    testobj.readcaptions(lang)

def _test_editor_setcaptions(monkeypatch, capsys):
    testobj.setcaptions()
