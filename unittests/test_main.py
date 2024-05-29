"""unittests for ./editor/main.py
"""
import types
import pytest
import editor.main as testee


class MockSettType(testee.enum.Enum):
    """stub for shared.SettType
    """
    PLG = 'plg'
    PNL = 'pnl'
    RBLD = 'rbld'
    DETS = 'dets'
    RDEF = 'rdef'

class MockLineType(testee.enum.Enum):
    """stub for main.LineType
    """
    SETT = 'sett'
    CAPT = 'capt'
    WID = 'wid'
    ORIG = 'orig'
    KEY = 'key'

class MockSDI:
    """stub for gui.SingleDataInterface
    """
    def __init__(self, *args):
        print('called SingleDataInterface.__init__ with args', args)
    def setup_empty_screen(self, *args):
        """stub
        """
        print('called SDI.setup_empty_screen with args', args)
    def add_extra_fields(self):
        """stub
        """
        print('called SDI.add_extra_fields')
    def set_extrascreen_editable(self, *args):
        """stub
        """
        print('called SDI.set_extrascreen_editable with args', args)
    def setup_list(self):
        """stub
        """
        print('called SDI.setup_list')
    def getfirstitem(self):
        """stub
        """
        return 'first_item'

class MockReader:
    """stub for plugin program
    """

class MockReader2:
    """stub for plugin program
    """
    def build_data(self):
        pass


def test_readlang(monkeypatch, tmp_path):
    """unittest for main.readlang
    """
    mock_lang = tmp_path / 'hotkeys' / 'lang'
    monkeypatch.setattr(testee.shared, 'HERELANG', mock_lang)
    mock_lang.mkdir(parents=True)
    (mock_lang / 'en').write_text("#deze overslaan\n\ncode text\n\nalso a code with text\n")
    assert testee.readlang('en') == {'code': 'text', 'also': 'a code with text'}

def test_get_csv_oms(monkeypatch, capsys):
    """unittest for main.get_csv_oms
    """
    def mock_read(lang):
        """stub
        """
        print(f'called readlang with arg `{lang}`')
        return {'T_NAMOF': '{} {} name', 'S_PLGNAM': 'plugin', 'T_NOPY': 'module',
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
    """unittest for main.build_csv_sample_data
    """
    def mock_get(lang):
        """stub
        """
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
# def _test_get_pluginname(monkeypatch, capsys):
#     """unittest for main.get_pluginname
#     """
#     testee.get_pluginname('csvname')

# te vervangen door de hierna volgende
def _test_read_settings(monkeypatch, capsys, tmp_path):
    """unittest for main.read_settings
    """
    # zolang ik dit met een python module doe moet ik dit importeren
    # ik kan het dan niet testen met behulp van tmp_path omdat die niet in het zoekpad zit
    # het probleem is dat deze bij opnieuw proberen om en om failt en niet failt
    # zolang dat niet gefikst is deze test maar uitgeschakeld
    def mock_log_exc():
        """stub
        """
        print('called shared.log_exc')
    monkeypatch.setattr(testee.shared, 'log_exc', mock_log_exc)
    with open('fake_module.py', 'w') as f:
        f.write('"""settings for hotkeys\n"""\n')
    assert testee.read_settings('fake_module') == {
            'filename': '/home/albert/projects/hotkeys/fake_module.py',
            'plugins': [], 'lang': 'english.lng'}

    with open('fake_module_2.py', 'w') as f:
        f.write('"""settings for hotkeys\n"""\nPLUGINS = ["x", "y"]\nLANG = "z"\n'
                'INITIAL = "a"\nSTARTUP = "b"\n')
    # breakpoint()
    assert testee.read_settings('fake_module_2') == {
            'filename': '/home/albert/projects/hotkeys/fake_module_2.py',
            'plugins': ['x', 'y'], 'lang': 'z', 'initial': 'a', 'startup': 'b'}

    assert testee.read_settings('fake_module_3') == {'plugins': [], 'lang': 'english.lng'}

    testee.os.remove('fake_module.py')
    testee.os.remove('fake_module_2.py')

def test_read_settings_json(monkeypatch, tmp_path):
    """unittest for main.read_settings_json
    """
    monkeypatch.setattr(testee, 'initial_settings', {'x': '', 'a': ''})
    ini = tmp_path / 'settingsfile'
    ini.write_text('{"a": "b", "q": "r"}\n')
    assert testee.read_settings_json(ini) == {'a': 'b', 'filename': ini, 'x': ''}

def test_write_settings_json(monkeypatch, capsys, tmp_path):
    """unittest for main.write_settings_json
    """
    def mock_copy(*args):
        """stub
        """
        print('called shutil.copyfile with args', args)
    def mock_dump(*args):
        """stub
        """
        print('called json.dump with arg', args[0])
    monkeypatch.setattr(testee.json, 'dump', mock_dump)
    monkeypatch.setattr(testee.shared.pathlib.Path, 'exists', lambda *x: False)
    monkeypatch.setattr(testee, 'initial_settings', {'x': '', 'a': ''})
    ini = tmp_path / 'settingsfile'
    testee.write_settings_json(settings={'a': 'b', 'filename': ini, 'x': 'y'})
    assert capsys.readouterr().out == "called json.dump with arg {'a': 'b', 'x': 'y'}\n"
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
    monkeypatch.setattr(testee.shared.pathlib.Path, 'exists', lambda *x: True)
    testee.write_settings_json(settings={'a': 'b', 'filename': ini, 'x': 'y'})
    assert capsys.readouterr().out == (f"called shutil.copyfile with args ('{ini}',"
                                       f" '{str(ini) + '~'}')\n"
                                       "called json.dump with arg {'a': 'b', 'x': 'y'}\n")
    testee.write_settings_json(settings={'a': 'b', 'filename': ini, 'x': 'y'}, nobackup=True)
    assert capsys.readouterr().out == "called json.dump with arg {'a': 'b', 'x': 'y'}\n"

def test_modify_settings(tmp_path):
    """unittest for main.modify_settings
    """
    ini = {'filename': str(tmp_path / 'settings'), 'plugins': [('x', 'y'), ('a', 'b')]}
    (tmp_path / 'settings').write_text('ppp\n\nPLUGINS\nqqq\n  ]  \nrrr\nsss\n')
    testee.modify_settings(ini)
    assert (tmp_path / 'settings.bak').read_text() == 'ppp\n\nPLUGINS\nqqq\n  ]  \nrrr\nsss\n'
    assert (tmp_path / 'settings').read_text() == ('ppp\n\nPLUGINS\n    ("x", "y"),\n'
                                                   '    ("a", "b"),\n  ]  \nrrr\nsss\n')

def test_read_columntitledata(monkeypatch, capsys, tmp_path):
    """unittest for main.read_columntitledata
    """
    def mock_log(*args, **kwargs):
        """stub
        """
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

def test_add_columntitledata(monkeypatch, tmp_path):
    """unittest for main.add_columntitledata
    """
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
    """unittest for main.update_paths
    """
    def mock_write(*args):
        """stub
        """
        print('called path.write with args', args)
    def mock_initcsv(*args):
        """stub
        """
        print('called initcsv with args', args)
    def mock_initjson(*args):
        """stub
        """
        print('called initjson with args', args)
    monkeypatch.setattr(testee.shared.pathlib.Path, 'write_text', mock_write)
    monkeypatch.setattr(testee, 'initcsv', mock_initcsv)
    monkeypatch.setattr(testee, 'initjson', mock_initjson)
    paths = (('xx', 'yy.csv'), ('aa', 'bb.json'))
    pathdata = {'xx': ['xx.yy.zz', 'xxx', 1, 0, 0], 'aa': ['.bb.cc', 'aaa', 1, 1, 1]}
    assert testee.update_paths(paths, pathdata, 'en') == [('xx', 'yy.csv'), ('aa', 'bb.json')]

# niet meer nodig als ik alleen nog maar met json werk
def test_initcsv(monkeypatch, capsys, tmp_path):
    """unittest for main.initcsv
    """
    def mock_get_oms(lang):
        print(f"called get_csv_oms with arg '{lang}'")
        return {'sett1': 'first setting', 'sett2': 'second setting', 'sett3': 'third setting'}
    def mock_build(lang):
        print(f"called build_csv_sample_data with arg '{lang}'")
        return [('sample', 'line', '1'), ('sample', 'line', '2')]
    monkeypatch.setattr(testee, 'get_csv_oms', mock_get_oms)
    monkeypatch.setattr(testee, 'build_csv_sample_data', mock_build)
    monkeypatch.setattr(testee.shared, 'csv_settingnames', ['sett1', 'sett2', 'sett3'])
    loc = tmp_path / 'mock_init.csv'
    data = ['value1', 'value2', 'value3']
    testee.initcsv(loc, data, 'nl')
    assert loc.read_text() == ("Setting,sett1,value1,first setting\n"
                               "Setting,sett2,value2,second setting\n"
                               "Setting,sett3,value3,third setting\n"
                               "sample,line,1\n"
                               "sample,line,2\n")
    assert capsys.readouterr().out == ("called get_csv_oms with arg 'nl'\n"
                                       "called build_csv_sample_data with arg 'nl'\n")

def test_initjson(monkeypatch, capsys):
    """unittest for main.initjson
    """
    def mock_write(*args):
        """stub
        """
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
    """unittest for main.readcsv
    """
    testee.readcsv('pad')

def _test_readjson(monkeypatch, capsys, tmp_path):
    """unittest for main.readjson
    """
    (tmp_path / 'test' / 'plugin.json').write_text(
         '{"settings": {"settings": "dict"}, "column_info": [["column", "info"]],'
         ' "keydata": {"keycombo": "dict"}, "otherstuff": {}')
    testee.readjson('test/plugin.json')

# niet meer nodig als ik alleen nog maar met json werk
def _test_writecsv(monkeypatch, capsys):
    """unittest for main.writecsv
    """
    class MockWriter:
        """stub for csv.writer
        """
        def __init__(self, *args):
            print('called csv.writer with args', args)
        def writerow(self, line):
            print('called csv.writer.writerow with arg', arg)
    testee.writecsv('pad', 'settings', 'coldata', 'data', 'lang')

def _test_writejson(monkeypatch, capsys):
    """unittest for main.writejson
    """
    testee.writejson('pad', 'settings', 'coldata', 'data', 'otherstuff')

def test_quick_check(monkeypatch, capsys):
    """unittest for main.quick_check
    """
    def mock_log_exc():
        """stub
        """
        print('called shared.log_exc')
    def mock_readcsv(arg):
        """stub
        """
        print(f'called readcsv with arg `{arg}`')
        return {}, [[], []], {1: ['x', 'y'], 2: ['a', 'b']}
    def mock_readjson(arg):
        """stub
        """
        print(f'called readjson with arg `{arg}`')
        return {}, [[], []], {}, {}
    def mock_readjson_2(arg):
        """stub
        """
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

def test_hotkeypanel_init(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.init
    """
    def mock_log(text):
        """stub
        """
        print(f'called shared.log with arg `{text}`')
    def mock_log_exc():
        """stub
        """
        print('called shared.log_exc')
    def mock_readcsv(arg):
        """stub
        """
        print(f'called readcsv with arg `{arg}`')
        return {'x': 'y'}, [], {1: ['x', 'y'], 2: ['a', 'b']}
    def mock_readcsv_2(arg):
        """stub
        """
        print(f'called readcsv with arg `{arg}`')
        return ({'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '0'}, ['qq', 'rr'],
                {1: ['x', 'y'], 2: ['a', 'b']})
    def mock_readjson_exc_1(arg):
        """stub
        """
        raise ValueError('A ValueError')
    def mock_readjson_exc_2(arg):
        """stub
        """
        raise FileNotFoundError('A FileNotFoundError')
    def mock_readjson(arg):
        """stub
        """
        print(f'called readjson with arg `{arg}`')
        return {'x': 'y'}, [[], []], {}, {}
    def mock_readjson_2(arg):
        """stub
        """
        print(f'called readjson with arg `{arg}`')
        return {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '0'}, [[], []], {}, {}
    def mock_readjson_3(arg):
        """stub
        """
        print(f'called readjson with arg `{arg}`')
        return ({'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '1',
                 'RedefineKeys': '0'}, [['x', 0], ['y', 1]], {}, {})
    def mock_import_nok(*args):
        """stub
        """
        print('called importlib.import_module with args', args)
        raise ImportError
    def mock_import_ok(*args):
        """stub
        """
        print('called importlib.import_module with args', args)
        return MockReader()
    def mock_import_ok_2(*args):
        """stub
        """
        print('called importlib.import_module with args', args)
        return MockReader2()
    def mock_add(self):
        """stub
        """
        print('called HotkeyPanel.add_extra_attributes')
    def mock_refresh(self, arg):
        """stub
        """
        print(f'called HotkeyPanel.refresh_extrascreen with arg {arg}')
    def mock_build(self, *args, **kwargs):
        print('called Reader.build_data with args', args, kwargs)
        return 'x', 'otherstuff'
    def mock_build_2(self, *args, **kwargs):
        print('called Reader.build_data with args', args, kwargs)
        raise FileNotFoundError('zzz')
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
    assert (testobj.settings, testobj.column_info, testobj.data) == ({'x': 'y'}, [],
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

    monkeypatch.setattr(testee, 'readcsv', mock_readcsv_2)
    testobj = testee.HotkeyPanel(parent, 'plugin.csv')
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.csv`\n'
                                       'called readcsv with arg `plugin.csv`\n'
                                       "called importlib.import_module with args ('plugin',)\n"
                                       "called SDI.setup_list\n")

    monkeypatch.setattr(MockReader2, 'build_data', mock_build)
    monkeypatch.setattr(testee.importlib, 'import_module', mock_import_ok_2)
    testobj = testee.HotkeyPanel(parent, 'plugin.csv')
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.csv`\n'
                                       'called readcsv with arg `plugin.csv`\n'
                                       "called importlib.import_module with args ('plugin',)\n"
                                       f"called Reader.build_data with args ({testobj},)"
                                       " {'showinfo': False}\n"
                                       "called SDI.setup_list\n")

    monkeypatch.setattr(MockReader2, 'build_data', mock_build_2)
    testobj = testee.HotkeyPanel(parent, 'plugin.csv')
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.csv`\n'
                                       'called readcsv with arg `plugin.csv`\n'
                                       "called importlib.import_module with args ('plugin',)\n"
                                       f"called Reader.build_data with args ({testobj},)"
                                       " {'showinfo': False}\n"
                                       'called SDI.setup_empty_screen with args'
                                       " ('plugin no settings\\nzzz', 'A title')\n")

def setup_hotkeypanel(monkeypatch, capsys):
    """stub for initializing main.HotKeyPanel when needed
    """
    def mock_init(self, *args):
        """stub
        """
        print('called HotkeyPanel.__init__ with args', args)
    monkeypatch.setattr(testee.HotkeyPanel, '__init__', mock_init)
    testobj = testee.HotkeyPanel()
    assert capsys.readouterr().out == 'called HotkeyPanel.__init__ with args ()\n'
    testobj.parent = types.SimpleNamespace(parent=types.SimpleNamespace())
    testobj.gui = types.SimpleNamespace()
    testobj.reader = types.SimpleNamespace()
    return testobj

def test_hotkeypanel_readkeys(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.readkeys
    """
    def mock_readcsv(arg):
        """stub
        """
        print(f'called readcsv with arg `{arg}`')
        return {}, [], 'csvdata'
    def mock_readjson(arg):
        """stub
        """
        print(f'called readjson with arg `{arg}`')
        return {}, [], 'jsondata', {}
    monkeypatch.setattr(testee, 'readcsv', mock_readcsv)
    monkeypatch.setattr(testee, 'readjson', mock_readjson)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.pad = 'plugin.csv'
    testobj.readkeys()
    assert testobj.data == 'csvdata'
    assert capsys.readouterr().out == 'called readcsv with arg `plugin.csv`\n'
    testobj.pad = 'plugin.json'
    testobj.readkeys()
    assert testobj.data == 'jsondata'
    assert capsys.readouterr().out == 'called readjson with arg `plugin.json`\n'

def test_hotkeypanel_savekeys(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.savekeys
    """
    def mock_logexc():
        print('called shared.log_exc')
    def mock_writecsv(*args):
        print('called writecsv with args', args)
    def mock_writejson(*args):
        print('called writejson with args', args)
    def mock_savekeys(arg):
        print('called Reader.savekeys with arg', arg)
        raise AttributeError
    def mock_savekeys_2(arg):
        print('called Reader.savekeys with arg', arg)
    def mock_set_title(**kwargs):
        print('called HotkeyPanel.set_title with args', kwargs)
    monkeypatch.setattr(testee.shared, 'log_exc', mock_logexc)
    monkeypatch.setattr(testee, 'writecsv', mock_writecsv)
    monkeypatch.setattr(testee, 'writejson', mock_writejson)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.reader.savekeys = mock_savekeys
    testobj.pad = 'xxxx.csv'
    testobj.settings = ['settings']
    testobj.column_info = ['column', 'info']
    testobj.data = ['data']
    testobj.otherstuff = ['other', 'stuff']
    testobj.set_title = mock_set_title
    testobj.parent.parent.ini = {'lang': 'en'}
    testobj.savekeys()
    assert capsys.readouterr().out == (f"called Reader.savekeys with arg {testobj}\n"
                                       "called shared.log_exc\n"
                                       "called writecsv with args ('xxxx.csv',"
                                       " ['settings'], ['column', 'info'], ['data'], 'en')\n"
                                       "called HotkeyPanel.set_title with args {'modified': False}\n")

    testobj.reader.savekeys = mock_savekeys_2
    testobj.savekeys()
    assert capsys.readouterr().out == (f"called Reader.savekeys with arg {testobj}\n"
                                       "called writecsv with args ('xxxx.csv',"
                                       " ['settings'], ['column', 'info'], ['data'], 'en')\n"
                                       "called HotkeyPanel.set_title with args {'modified': False}\n")

    testobj.pad = 'xxxx.json'
    testobj.savekeys()
    assert capsys.readouterr().out == (f"called Reader.savekeys with arg {testobj}\n"
                                       "called writejson with args ('xxxx.json', ['settings'],"
                                       " ['column', 'info'], ['data'], ['other', 'stuff'])\n"
                                       "called HotkeyPanel.set_title with args {'modified': False}\n")

def test_hotkeypanel_setcaptions(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.setcaptions
    """
    class MockWidget:
        "stub for getting just a reference to a widget"
    def mock_title():
        print('called HotKeyPanel.set_title')
    def mock_labeltext(*args):
        print('called HotkeyPanelGui.set_label_text with args', args)
    def mock_resize():
        print('called HotkeyPanelGui.resize_if_necessary')
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.parent.parent.captions = {'C_KTXT': 'key', 'M_WIN': 'win', 'M_CTRL': 'ctrl',
                                      'M_ALT': 'alt', 'M_SHFT': 'shift', 'C_CNTXT': 'context',
                                      'C_CMD': 'command', 'C_PARMS': 'parms', 'C_CTRL': 'control',
                                      'C_BPARMS': 'bparms', 'C_APARMS': 'aparms',
                                      'C_FEAT': 'feature', 'C_SAVE': 'save', 'C_DEL': 'delete'}
    testobj.set_title = mock_title
    testobj.gui.set_label_text = mock_labeltext
    testobj.gui.resize_if_necessary = mock_resize
    testobj.gui.lbl_key = MockWidget()
    testobj.gui.cb_win = MockWidget()
    testobj.gui.cb_ctrl = MockWidget()
    testobj.gui.cb_alt = MockWidget()
    testobj.gui.cb_shift = MockWidget()
    testobj.gui.lbl_context = MockWidget()
    testobj.gui.txt_cmd = MockWidget()
    testobj.gui.lbl_parms = MockWidget()
    testobj.gui.lbl_controls = MockWidget()
    testobj.gui.pre_parms_label = MockWidget()
    testobj.gui.post_parms_label = MockWidget()
    testobj.gui.feature_label = MockWidget()
    testobj.gui.b_save = MockWidget()
    testobj.gui.b_del = MockWidget()
    testobj.fields = ['C_KEY']
    testobj.has_extrapanel = False
    testobj.setcaptions()
    assert capsys.readouterr().out == ("called HotKeyPanel.set_title\n")
    testobj.fields = []
    testobj.has_extrapanel = True
    testobj.setcaptions()
    assert capsys.readouterr().out == (
            "called HotKeyPanel.set_title\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.b_save}, 'save')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.b_del}, 'delete')\n"
            "called HotkeyPanelGui.resize_if_necessary\n")
    testobj.fields = ['C_KEY', 'C_MODS', 'C_CNTXT', 'C_CMD', 'C_PARMS', 'C_CTRL', 'C_BPARMS',
                      'C_APARMS', 'C_FEAT']
    testobj.setcaptions()
    assert capsys.readouterr().out == (
            "called HotKeyPanel.set_title\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.lbl_key}, 'key')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.cb_win}, '+win  ')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.cb_ctrl}, '+ctrl  ')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.cb_alt}, '+alt  ')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.cb_shift}, '+shift  ')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.lbl_context},"
            " 'context:')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.txt_cmd}, 'command')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.lbl_parms}, 'parms')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.lbl_controls},"
            " 'control')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.pre_parms_label},"
            " 'bparms:')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.post_parms_label},"
            " 'aparms:')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.feature_label},"
            " 'feature:')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.b_save}, 'save')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.b_del}, 'delete')\n"
            "called HotkeyPanelGui.resize_if_necessary\n")

def test_hotkeypanel_populate_list(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.populate_list
    """
    def mock_logexc():
        print('called shared.log_exc')
    def mock_clear():
        print('called HotkeyPanelGui.clear_list')
    def mock_build(key):
        print(f"called HotkeyPanelGui.build_listitem with arg '{key}'")
        return f'item-{key}'
    def mock_set_text(*args):
        print('called HotkeyPanelGui.set_listitemtext with args', args)
    def mock_add(item):
        print(f'called HotkeyPanelGui.add_listitem with arg {item}')
    def mock_select(pos):
        print(f'called HotkeyPanelGui.set_listselection with arg {pos}')
    monkeypatch.setattr(testee.shared, 'log_exc', mock_logexc)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.captions = {'C_DFLT': 'default', 'C_RDEF': 'custom'}
    testobj.gui.clear_list = mock_clear
    testobj.gui.build_listitem = mock_build
    testobj.gui.set_listitemtext = mock_set_text
    testobj.gui.add_listitem = mock_add
    testobj.gui.set_listselection = mock_select
    testobj.data = {}
    testobj.populate_list()
    assert capsys.readouterr().out == "called HotkeyPanelGui.clear_list\n"
    testobj.column_info = [('xxx', 10, False), ('yyy', 20, False), ('zzz', 5, True)]
    testobj.data = {'a': 'key error', '1': ['aaa', 'bbb', 'S'], 2: ['ppp', 'qqq', 'rrr']}
    testobj.populate_list()
    assert capsys.readouterr().out == (
            "called HotkeyPanelGui.clear_list\n"
            "called shared.log_exc\n"
            "called HotkeyPanelGui.build_listitem with arg '1'\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-1', 0, 'aaa')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-1', 1, 'bbb')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-1', 2, 'default')\n"
            "called HotkeyPanelGui.add_listitem with arg item-1\n"
            "called HotkeyPanelGui.build_listitem with arg '2'\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-2', 0, 'ppp')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-2', 1, 'qqq')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-2', 2, 'custom')\n"
            "called HotkeyPanelGui.add_listitem with arg item-2\n"
            "called HotkeyPanelGui.set_listselection with arg 0\n")
    testobj.data = {3: ['ppp', 'qqq']}  # te weinig kolommen in data
    with pytest.raises(IndexError) as exc:
        testobj.populate_list()
    assert str(exc.value) == 'list index out of range'
    assert capsys.readouterr().out == (
            "called HotkeyPanelGui.clear_list\n"
            "called HotkeyPanelGui.build_listitem with arg '3'\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-3', 0, 'ppp')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-3', 1, 'qqq')\n"
            "['ppp', 'qqq']\n")
    testobj.data = {3: ['ppp', 'qqq', 'R', 'sss']}  # te veel kolommen
    testobj.populate_list()
    assert capsys.readouterr().out == (
            "called HotkeyPanelGui.clear_list\n"
            "called HotkeyPanelGui.build_listitem with arg '3'\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-3', 0, 'ppp')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-3', 1, 'qqq')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-3', 2, 'custom')\n"
            "called HotkeyPanelGui.add_listitem with arg item-3\n"
            "called HotkeyPanelGui.set_listselection with arg 0\n")

def _test_hotkeypanel_add_extra_attributes(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.add_extra_attributes
    """
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.add_extra_attributes()

def test_hotkeypanel_set_title(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.set_title
    """
    def mock_set(value):
        print(f"called HotkeyPanelGui.set_title with arg '{value}'")
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.captions = {"T_MOD": '(*)'}
    testobj.gui.set_title = mock_set
    testobj.modified = True
    testobj.title = 'xxxx'
    testobj.set_title()
    assert capsys.readouterr().out == ("called HotkeyPanelGui.set_title with arg 'xxxx (*)'\n")
    testobj.modified = False
    testobj.set_title()
    assert capsys.readouterr().out == ("called HotkeyPanelGui.set_title with arg 'xxxx'\n")
    testobj.modified = False
    testobj.set_title(modified=True)
    assert capsys.readouterr().out == ("called HotkeyPanelGui.set_title with arg 'xxxx (*)'\n")
    testobj.modified = True
    testobj.set_title(modified=False)
    assert capsys.readouterr().out == ("called HotkeyPanelGui.set_title with arg 'xxxx'\n")

def test_hotkeypanel_exit(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.exit
    """
    def mock_ask(*args):
        print('called gui.ask_ync_question with args', args)
        return True, None
    def mock_ask_2(*args):
        print('called gui.ask_ync_question with args', args)
        return False, True
    def mock_ask_3(*args):
        print('called gui.ask_ync_question with args', args)
        return False, False
    def mock_save():
        print('called HotkeyPanel.savekeys')
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testee.gui.ask_ync_question = mock_ask
    testobj.savekeys = mock_save
    testobj.modified = False
    assert testobj.exit()
    assert capsys.readouterr().out == ""

    testobj.modified = True
    assert testobj.exit()
    assert capsys.readouterr().out == (
            f"called gui.ask_ync_question with args ({testobj.gui}, 'Q_SAVXIT')\n"
            "called HotkeyPanel.savekeys\n")

    testee.gui.ask_ync_question = mock_ask_2
    assert not testobj.exit()
    assert capsys.readouterr().out == (
            f"called gui.ask_ync_question with args ({testobj.gui}, 'Q_SAVXIT')\n")

    testee.gui.ask_ync_question = mock_ask_3
    assert testobj.exit()
    assert capsys.readouterr().out == (
            f"called gui.ask_ync_question with args ({testobj.gui}, 'Q_SAVXIT')\n")

def test_hotkeypanel_on_text(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.on_text
    """
    def mock_get(*args):
        print("called HotkeyPanelGui.get_widget_text with args", args)
        return 'snark'
    def mock_enable(state):
        print(f'called HotkeyPanelGui.enable_save with arg {state}')
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.gui.get_widget_text = mock_get
    testobj.gui.enable_save = mock_enable
    testobj.field_indexes = {'C_KEY': 1}
    testobj._origdata = ['', 'snork']
    testobj.initializing_screen = True
    testobj.fields = []
    testobj.defchanged = True
    testobj.on_text('x')
    assert testobj.defchanged
    assert capsys.readouterr().out == ""
    testobj.initializing_screen = False
    testobj.defchanged = True
    testobj.on_text('xx')
    assert not testobj.defchanged
    assert capsys.readouterr().out == "called HotkeyPanelGui.get_widget_text with args ('xx',)\n"
    testobj.fields = ['C_KEY']
    # breakpoint()
    testobj.on_text('xx')
    assert testobj.defchanged
    assert capsys.readouterr().out == ("called HotkeyPanelGui.get_widget_text with args ('xx',)\n"
                                       "called HotkeyPanelGui.enable_save with arg True\n")
    testobj._origdata = ['', 'snark']
    testobj.on_text('xx')
    assert not testobj.defchanged
    assert capsys.readouterr().out == ("called HotkeyPanelGui.get_widget_text with args ('xx',)\n"
                                       "called HotkeyPanelGui.enable_save with arg False\n")

def _test_hotkeypanel_on_combobox(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.on_combobox
    """
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.on_combobox(*args)

def test_hotkeypanel_set_changed_indicators(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.set_changed_indicators
    """
    def mock_enable(value):
        print(f"called HotkeyPanelGui.enable_save with arg '{value}')")
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.gui.enable_save = mock_enable
    testobj.defchanged = False
    testobj.fields = []
    testobj.set_changed_indicators(True)
    assert testobj.defchanged
    assert capsys.readouterr().out == ""
    testobj.defchanged = True
    testobj.fields = ['C_CMD']
    testobj.set_changed_indicators(False)
    assert not testobj.defchanged
    assert capsys.readouterr().out == "called HotkeyPanelGui.enable_save with arg 'False')\n"

def _test_hotkeypanel_on_checkbox(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.on_checkbox
    """
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.on_checkbox(*args)

def _test_hotkeypanel_refresh_extrascreen(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.refresh_extrascreen
    """
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.refresh_extrascreen(selitem)

def test_hotkeypanel_get_valuelist(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.get_valuelist
    """
    def mock_init(*args):
        print('called HotkeyPanelGui.init_combobox with arg', args)
    def mock_get(arg):
        print(f"called HotkeyPanelGui.get_combobox_selection with arg '{arg}'")
        return 'xxx'
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.keylist = ['a']
    testobj.contextslist = ['b']
    testobj.fields = ['C_CNTXT']
    testobj.contextactionsdict = {'xxx': ['c']}
    testobj.commandslist = ['d']
    testobj.controlslist = ['e']
    testobj.featurelist = ['f']
    testobj.gui.cmb_commando = 'xx'
    testobj.gui.init_combobox = mock_init
    testobj.gui.cmb_context = 'yy'
    testobj.gui.get_combobox_selection = mock_get

    assert testobj.get_valuelist('xx') == []
    assert capsys.readouterr().out == ""
    assert testobj.get_valuelist('C_KEY') == ['a']
    assert capsys.readouterr().out == ""
    assert testobj.get_valuelist('C_CNTXT') == ['b']
    assert capsys.readouterr().out == ""
    assert testobj.get_valuelist('C_CMD') == ['c']
    assert capsys.readouterr().out == (
            "called HotkeyPanelGui.init_combobox with arg ('xx',)\n"
            "called HotkeyPanelGui.get_combobox_selection with arg 'yy'\n"
            "called HotkeyPanelGui.init_combobox with arg ('xx', ['c'])\n")
    testobj.contextactionsdict = {}
    assert testobj.get_valuelist('C_CMD') == ['d']
    assert capsys.readouterr().out == (
            "called HotkeyPanelGui.init_combobox with arg ('xx',)\n"
            "called HotkeyPanelGui.get_combobox_selection with arg 'yy'\n"
            "called HotkeyPanelGui.init_combobox with arg ('xx', ['d'])\n")
    testobj.fields = []
    assert testobj.get_valuelist('C_CMD') == ['d']
    assert capsys.readouterr().out == ""
    assert testobj.get_valuelist('C_CTRL') == ['e']
    assert capsys.readouterr().out == ""
    assert testobj.get_valuelist('C_FEAT') == ['f']
    assert capsys.readouterr().out == ""

def test_hotkeypanel_process_changed_selection(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.process_changed_selection
    """
    def mock_check():
        print("called HotKeyPanel.check_for_changes")
        return 'xxx', 'yyy'
    def mock_check_keydef(arg):
        print(f"called HotKeyPanel.check_for_selected_keydef with arg '{arg}'")
        return True, 1
    def mock_ask(*args):
        print("called HotKeyPanel.ask_what_to_do with args", args)
        return False
    def mock_ask_2(*args):
        print("called HotKeyPanel.ask_what_to_do with args", args)
        return True
    def mock_apply(*args):
        print("called HotKeyPanel.apply_changes with args", args)
        return 'item a'
    def mock_get():
        print("called HotKeyPanel.get_selected_keydef")
        return 'item b'
    def mock_refresh(arg):
        print(f"called HotKeyPanel.refresh_extrascreen with arg '{arg}'")
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.check_for_changes = mock_check
    testobj.check_for_selected_keydef = mock_check_keydef
    testobj.ask_what_to_do = mock_ask
    testobj.apply_changes = mock_apply
    testobj.gui.get_selected_keydef = mock_get
    testobj.refresh_extrascreen = mock_refresh
    testobj.settings = {testee.shared.SettType.RDEF.value: '0'}
    testobj.initializing_screen = True
    testobj.process_changed_selection('newitem', 'olditem')
    assert capsys.readouterr().out == ("called HotKeyPanel.get_selected_keydef\n"
                                       "called HotKeyPanel.refresh_extrascreen with arg 'item b'\n")
    testobj.settings = {testee.shared.SettType.RDEF.value: '1'}
    testobj.process_changed_selection('newitem', 'olditem')
    assert capsys.readouterr().out == "called HotKeyPanel.refresh_extrascreen with arg 'newitem'\n"
    testobj.initializing_screen = False
    testobj.process_changed_selection('newitem', 'olditem')
    assert capsys.readouterr().out == (
            "called HotKeyPanel.check_for_changes\n"
            "called HotKeyPanel.check_for_selected_keydef with arg 'yyy'\n"
            "called HotKeyPanel.ask_what_to_do with args (True, 'newitem', 'olditem')\n"
            "called HotKeyPanel.refresh_extrascreen with arg 'newitem'\n")
    testobj.ask_what_to_do = mock_ask_2
    testobj.process_changed_selection('newitem', 'olditem')
    assert capsys.readouterr().out == (
            "called HotKeyPanel.check_for_changes\n"
            "called HotKeyPanel.check_for_selected_keydef with arg 'yyy'\n"
            "called HotKeyPanel.ask_what_to_do with args (True, 'newitem', 'olditem')\n"
            "called HotKeyPanel.apply_changes with args (True, 1, 'yyy')\n"
            "called HotKeyPanel.refresh_extrascreen with arg 'item a'\n")

def test_hotkeypanel_check_for_changes(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.check_for_changes
    """
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.field_indexes = {'C_KEY': 0, 'C_MODS': [1, 2, 3, 4], 'C_CNTXT': 5}
    testobj._origdata = ['x', True, False, True, False, 'zzz']
    testobj._newdata = ['x', True, False, True, False, 'zzz']
    assert testobj.check_for_changes() == ([False, False, False],
                                           ['x', [True, False, True, False], 'zzz'])
    testobj._newdata = ['y', False, True, False, True, 'zzzz']
    assert testobj.check_for_changes() == ([True, True, True],
                                           ['y', [False, True, False, True], 'zzzz'])

def test_hotkeypanel_check_for_selected_keydef(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.check_for_selected_keydef
    """
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.fields = ['C_KEY', 'C_MODS', 'C_CNTXT']
    testobj.data = {1: ['x', 'y', 'z', 'aaaaaaa'], 2: ['p', 'q', 'r', 'bbbbbb']}
    assert testobj.check_for_selected_keydef(['x', 'y', 'z']) == (True, 1)
    assert testobj.check_for_selected_keydef(['k', 'l', 'm']) == (False, -1)

def test_hotkeypanel_ask_what_to_do(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.ask_what_to_do
    """
    def mock_ask(*args):
        print('called gui.ask_question with args', args)
        return 'answered'
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj._newdata = ['x', 'y', 'z']
    testobj._origdata = ['x', 'y', 'z']
    assert not testobj.ask_what_to_do(True, 'newitem', 'olditem')
    assert capsys.readouterr().out == ""
    testobj._origdata = ['x', 'y', 'w']
    assert testobj.ask_what_to_do(True, 'newitem', 'olditem') == 'answered'
    assert capsys.readouterr().out == "called gui.ask_question with args (namespace(), 'Q_SAVCHG')\n"
    assert testobj.ask_what_to_do(True, 'newitem', None) == 'answered'
    assert capsys.readouterr().out == "called gui.ask_question with args (namespace(), 'Q_DPLKEY')\n"
    assert testobj.ask_what_to_do(False, 'newitem', 'olditem') == 'answered'
    assert capsys.readouterr().out == "called gui.ask_question with args (namespace(), 'Q_SAVCHG')\n"
    assert testobj.ask_what_to_do(False, 'newitem', None)
    assert capsys.readouterr().out == ""

def _test_hotkeypanel_apply_changes(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.apply_changes
    """
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.apply_changes(found, indx, keydefdata)

def _test_hotkeypanel_apply_deletion(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.apply_deletion
    """
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.apply_deletion()


class MockEditor:
    """stub for main.Editor (and its gui component)
    """
    def __init__(self):
        def mock_message(text):
            print(f"called EditorGui.statusbar_message with arg '{text}'")
        print('called Editor.__init__')
        self.gui = types.SimpleNamespace(statusbar_message=mock_message)
        self.pluginfiles = {}


class MockTabGui:
    """stub for gui.TabbedInterface
    """
    def __init__(self, *args):
        print('called TabbedInterface.__init__ with args', args)
    def setup_selector(self):
        print('called TabbedInterface.setup_selector')
    def setup_search(self):
        print('called TabbedInterface.setup_search')
    def add_subscreen(self, win):
        print(f'called TabbedInterface.add_subscreen with arg of type {type(win)}')
    def add_to_selector(self, txt):
        print(f"called TabbedInterface.add_to_selector with arg '{txt}'")
    def format_screen(self):
        print("called TabbedInterface.format_screen")
    def update_search(self, arg):
        print("called TabbedInterface.update_search with arg", arg)
    def init_search_buttons(self):
        print("called TabbedInterface.init_search_buttons")
    def set_selected_tool(self, arg):
        print(f"called TabbedInterface.set_selected_tool with arg '{arg}'")
    def set_selected_panel(self, *args):
        print("called TabbedInterface.set_selected_panel with args", args)
    def set_selected_keydef_item(self, *args):
        print("called TabbedInterface.set_selected_keydef_item with args", args)
    def enable_search_buttons(self, **kwargs):
        print("called TabbedInterface.enable_search_buttons with args", kwargs)
    def enable_search_text(self, state):
        print(f"called TabbedInterface.enable_search_text with arg {state}")
    def set_found_keydef_position(self, *args):
        print("called TabbedInterface.set_found_keydef_position with args", args)
    def set_filter_state_text(self, text):
        print(f"called TabbedInterface.set_filter_state_text with arg {text}")


class MockHotkeyPanel:
    """stub for main.HotkeyPanel
    """
    def __init__(self, *args):
        print('called HotkeyPanel.__init__ with args', args)
        self.settings = {}
        if testee.os.path.basename(args[1]) == 'itsnotthere':
            self.settings[testee.shared.SettType.PLG.value] = 'xxx'
    def readkeys(self):
        print('called HotkeyPanel.readkeys')
    def populate_list(self):
        print('called HotkeyPanel.populate_list')
    def setcaptions(self):
        print('called HotkeyPanel.setcaptions')


def test_choicebook_init(monkeypatch, capsys, tmp_path):
    """unittest for main.ChoiceBook.init
    """
    def mock_log():
        print('called shared.log_exc')
    monkeypatch.setattr(testee.shared, 'log_exc', mock_log)
    plgfile = tmp_path / 'isthere'
    plgfile.touch()
    monkeypatch.setattr(testee.gui, 'TabbedInterface', MockTabGui)
    monkeypatch.setattr(testee, 'HotkeyPanel', MockHotkeyPanel)
    parent = MockEditor()
    parent.ini = {'plugins': [('xxx', str(plgfile)), ('yyy', 'itsnotthere')]}
    # breakpoint()
    testobj = testee.ChoiceBook(parent)
    assert testobj.parent == parent
    assert testobj.page is None
    assert isinstance(testobj.gui, testee.gui.TabbedInterface)
    assert testobj.parent.pluginfiles == {'xxx': '', 'yyy': 'xxx'}
    assert capsys.readouterr().out == (
            "called Editor.__init__\n"
            f"called TabbedInterface.__init__ with args ({testobj.parent.gui}, {testobj})\n"
            "called TabbedInterface.setup_selector\n"
            "called TabbedInterface.setup_search\n"
            f"called HotkeyPanel.__init__ with args ({testobj}, '{plgfile}')\n"
            "called TabbedInterface.add_subscreen with arg of type"
            " <class 'test_main.MockHotkeyPanel'>\n"
            "called shared.log_exc\n"
            "called TabbedInterface.add_to_selector with arg 'xxx'\n"
            f"called HotkeyPanel.__init__ with args ({testobj}, '{testee.BASE}/itsnotthere')\n"
            "called TabbedInterface.add_subscreen with arg of type"
            " <class 'test_main.MockHotkeyPanel'>\n"
            "called TabbedInterface.add_to_selector with arg 'yyy'\n"
            "called TabbedInterface.format_screen\n")

def setup_choicebook(monkeypatch, capsys):
    """stub for main.Editor.book
    """
    def mock_init(self):
        print('called ChoiceBook.__init__')
    monkeypatch.setattr(testee.ChoiceBook, '__init__', mock_init)
    testobj = testee.ChoiceBook()
    testobj.parent = MockEditor()
    testobj.gui = MockTabGui()
    assert capsys.readouterr().out == ('called ChoiceBook.__init__\n'
                                       "called Editor.__init__\n"
                                       "called TabbedInterface.__init__ with args ()\n")
    return testobj

def test_choicebook_on_page_changed(monkeypatch, capsys):
    """unittest for main.ChoiceBook.on_page_changed
    """
    win = MockSDI()
    assert capsys.readouterr().out == 'called SingleDataInterface.__init__ with args ()\n'
    def mock_get():
        print('called TabbedInterface.get_panel')
        return None
    def mock_get_2():
        print('called TabbedInterface.get_panel')
        return win
    def mock_exit():
        print('called SingleDataInterface.exit')
        return False
    def mock_exit_2():
        print('called SingleDataInterface.exit')
        return True
    def mock_get_tool():
        print('called TabbedInterface.get_selected_tool')
        return
    def mock_setup():
        print('called EditorGui.setup_menu')
    win.master = MockHotkeyPanel('testobj', '')
    assert capsys.readouterr().out == "called HotkeyPanel.__init__ with args ('testobj', '')\n"
    win.master.modified = True
    win.master.column_info = [('x', 1)]
    win.master.data = {1: 'y'}
    win.exit = mock_exit
    testobj = setup_choicebook(monkeypatch, capsys)
    testobj.parent.captions = {'M_DESC': "it's {}", 'x': 'column'}
    testobj.gui.get_selected_tool = mock_get_tool
    testobj.gui.get_panel = mock_get
    testobj.parent.gui.setup_menu = mock_setup

    testobj.parent.book = None
    testobj.on_page_changed(1)
    assert capsys.readouterr().out == ""

    testobj.parent.book = testobj
    testobj.on_page_changed(1)
    assert capsys.readouterr().out == "called TabbedInterface.get_panel\n"

    testobj.gui.get_panel = mock_get_2
    testobj.on_page_changed(1)
    assert capsys.readouterr().out == ("called TabbedInterface.get_panel\n"
                                       "called SingleDataInterface.exit\n")

    win.exit = mock_exit_2
    testobj.on_page_changed(1)
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_panel\n"
            "called SingleDataInterface.exit\n"
            "called TabbedInterface.get_selected_tool\n"
            "called EditorGui.statusbar_message with arg 'it's None'\n"
            "called TabbedInterface.set_selected_panel with args (1,)\n"
            "called TabbedInterface.get_panel\n"
            "called EditorGui.setup_menu\n")

    win.master.settings = {'a': 'b'}
    testobj.on_page_changed(1)
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_panel\n"
            "called SingleDataInterface.exit\n"
            "called TabbedInterface.get_selected_tool\n"
            "called EditorGui.statusbar_message with arg 'it's None'\n"
            "called TabbedInterface.set_selected_panel with args (1,)\n"
            "called TabbedInterface.get_panel\n"
            "called EditorGui.setup_menu\n"
            "called HotkeyPanel.setcaptions\n"
            "called TabbedInterface.update_search with arg ['column']\n")

def test_choicebook_on_text_changed(monkeypatch, capsys):
    """unittest for main.ChoiceBook.on_text_changed
    """
    def mock_get():
        print("called TabbedInterface.get_search_col")
        return "yyy"
    def mock_find(*args):
        print("called TabbedInterface.find_items with args", args)
        return []
    def mock_find_2(*args):
        print("called TabbedInterface.find_items with args", args)
        return ['item-1', 'item-2']
    testobj = setup_choicebook(monkeypatch, capsys)
    testobj.parent.captions = {"I_#FOUND": "{} found", "I_NOTFND": "no {}"}
    testobj.page = MockHotkeyPanel(testobj, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
    testobj.page.column_info = [('x', 0), ('y', 1)]
    testobj.page.captions = {'x': 'xxx', 'y': 'yyy'}
    testobj.page.data = {1: 'a', 2: 'b'}
    testobj.gui.get_search_col = mock_get
    testobj.gui.find_items = mock_find
    testobj.on_text_changed('qq')
    assert testobj.zoekcol == 1
    assert testobj.items_found == []
    assert not hasattr(testobj, 'founditem')
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_search_col\n"
            "called TabbedInterface.get_search_col\n"
            f"called TabbedInterface.find_items with args ({testobj.page}, 'qq')\n"
            "called TabbedInterface.init_search_buttons\n"
            "called EditorGui.statusbar_message with arg 'no qq'\n")

    testobj.gui.find_items = mock_find_2
    testobj.on_text_changed('qq')
    assert testobj.zoekcol == 1
    assert testobj.items_found == ['item-1', 'item-2']
    assert testobj.founditem == 0
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_search_col\n"
            "called TabbedInterface.get_search_col\n"
            f"called TabbedInterface.find_items with args ({testobj.page}, 'qq')\n"
            "called TabbedInterface.init_search_buttons\n"
            f"called TabbedInterface.set_selected_keydef_item with args ({testobj.page}, 0)\n"
            "called EditorGui.statusbar_message with arg '2 found'\n")

    testobj.page.data = {1: 'a', 2: 'b', 3: 'c'}
    testobj.on_text_changed('qq')
    assert testobj.zoekcol == 1
    assert testobj.items_found == ['item-1', 'item-2']
    assert testobj.founditem == 0
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_search_col\n"
            "called TabbedInterface.get_search_col\n"
            f"called TabbedInterface.find_items with args ({testobj.page}, 'qq')\n"
            "called TabbedInterface.init_search_buttons\n"
            f"called TabbedInterface.set_selected_keydef_item with args ({testobj.page}, 0)\n"
            "called TabbedInterface.enable_search_buttons with args {'next': True, 'filter': True}\n"
            "called EditorGui.statusbar_message with arg '2 found'\n")

    testobj.page.captions = {'x': 'xxx', 'y': 'zzz'}
    testobj.gui.find_items = mock_find
    testobj.on_text_changed('qq')
    assert testobj.zoekcol == -1
    assert testobj.items_found == []
    assert testobj.founditem == 0
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_search_col\n"
            "called TabbedInterface.get_search_col\n"
            f"called TabbedInterface.find_items with args ({testobj.page}, 'qq')\n"
            "called TabbedInterface.init_search_buttons\n"
            "called EditorGui.statusbar_message with arg 'no qq'\n")

def test_choicebook_find_next(monkeypatch, capsys):
    """unittest for main.ChoiceBook.find_next
    """
    testobj = setup_choicebook(monkeypatch, capsys)
    testobj.page = MockHotkeyPanel(testobj, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
    testobj.parent.captions = {'I_NONXT': 'xxx'}
    testobj.items_found = ['x', 'y']
    testobj.founditem = 1
    testobj.find_next()
    assert testobj.founditem == 1
    assert capsys.readouterr().out == (
            "called TabbedInterface.enable_search_buttons with args {'prev': True}\n"
            "called EditorGui.statusbar_message with arg 'xxx'\n"
            "called TabbedInterface.enable_search_buttons with args {'next': False}\n")
    testobj.founditem = 0
    testobj.find_next()
    assert testobj.founditem == 1
    assert capsys.readouterr().out == (
            "called TabbedInterface.enable_search_buttons with args {'prev': True}\n"
            f"called TabbedInterface.set_selected_keydef_item with args ({testobj.page}, 1)\n")

def test_choicebook_find_prev(monkeypatch, capsys):
    """unittest for main.ChoiceBook.find_prev
    """
    testobj = setup_choicebook(monkeypatch, capsys)
    testobj.page = MockHotkeyPanel(testobj, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
    testobj.parent.captions = {'I_NOPRV': 'uuu'}
    testobj.items_found = ['x', 'y']
    testobj.founditem = 1
    testobj.find_prev()
    assert testobj.founditem == 0
    assert capsys.readouterr().out == (
            "called TabbedInterface.enable_search_buttons with args {'next': True}\n"
            f"called TabbedInterface.set_selected_keydef_item with args ({testobj.page}, 0)\n")
    testobj.founditem = 0
    testobj.find_prev()
    assert testobj.founditem == 0
    assert capsys.readouterr().out == (
            "called TabbedInterface.enable_search_buttons with args {'next': True}\n"
            "called EditorGui.statusbar_message with arg 'uuu'\n"
            "called TabbedInterface.enable_search_buttons with args {'prev': False}\n")

def test_choicebook_filter(monkeypatch, capsys):
    """unittest for main.ChoiceBook.filter
    """
    def mock_get_filter_text():
        print("called TabbedInterface.get_filter_state_text")
        return 'on'
    def mock_get_filter_text_2():
        print("called TabbedInterface.get_filter_state_text")
        return 'off'
    def mock_get_search_text():
        print("called TabbedInterface.get_search_text")
        return 'this'
    def mock_get_pos():
        print("called TabbedInterface.get_found_keydef_position")
        return 2
    def mock_on_text(text):
        print(f"called ChoiceBook.on_text_changed with arg '{text}'")
    testobj = setup_choicebook(monkeypatch, capsys)
    testobj.page = MockHotkeyPanel(testobj, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
    testobj.parent.captions = {'C_FILTER': 'on', 'C_FLTOFF': 'off'}
    testobj.gui.get_filter_state_text = mock_get_filter_text
    testobj.gui.get_search_text = mock_get_search_text
    testobj.gui.get_found_keydef_position = mock_get_pos
    testobj.on_text_changed = mock_on_text
    testobj.zoekcol = 1
    testobj.page.data = {1: ['x', 'that'], 2: ['y', 'this'], 3: ['z', ''], 4: ['q', 'and this']}
    testobj.items_found = []
    testobj.filter()
    assert capsys.readouterr().out == ""
    testobj.items_found = ['x', 'y']
    testobj.filter()
    assert testobj.reposition == 2
    assert testobj.filter_on
    assert testobj.page.filtertext == 'this'
    assert testobj.page.olddata == {1: ['x', 'that'], 2: ['y', 'this'], 3: ['z', ''],
                                    4: ['q', 'and this']}
    assert testobj.page.data == {1: ['y', 'this'], 3: ['q', 'and this']}
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_filter_state_text\n"
            "called TabbedInterface.get_search_text\n"
            "called TabbedInterface.get_found_keydef_position\n"
            "called TabbedInterface.enable_search_buttons with args {'next': False, 'prev': False}\n"
            "called TabbedInterface.enable_search_text with arg False\n"
            "called HotkeyPanel.populate_list\n"
            "called TabbedInterface.set_found_keydef_position with args ()\n"
            "called TabbedInterface.set_filter_state_text with arg off\n")
    testobj.gui.get_filter_state_text = mock_get_filter_text_2
    testobj.filter()
    assert testobj.reposition == 2
    assert not testobj.filter_on
    assert testobj.page.filtertext == ''
    assert testobj.page.olddata == {1: ['x', 'that'], 2: ['y', 'this'], 3: ['z', ''],
                                    4: ['q', 'and this']}
    assert testobj.page.data == {1: ['x', 'that'], 2: ['y', 'this'], 3: ['z', ''],
                                 4: ['q', 'and this']}
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_filter_state_text\n"
            "called TabbedInterface.get_search_text\n"
            "called TabbedInterface.get_found_keydef_position\n"
            "called TabbedInterface.enable_search_buttons with args {'next': True, 'prev': True}\n"
            "called TabbedInterface.enable_search_text with arg True\n"
            "called HotkeyPanel.populate_list\n"
            "called TabbedInterface.set_found_keydef_position with args ()\n"
            "called TabbedInterface.set_filter_state_text with arg on\n"
            "called ChoiceBook.on_text_changed with arg 'this'\n")


class MockGui:
    "stub for gui.Gui"
    def __init__(self, arg):
        print(f'called Gui.__init__ with arg {arg}')
    def set_window_title(self, text):
        print(f"called Gui.set_window_title with arg '{text}'")
    def statusbar_message(self, *args):
        print('called Gui.statusbar_message with args', args)
    def setup_tabs(self):
        print('called Gui.setup_tabs')
    def go(self):
        print('called Gui.go')
    def resize_empty_screen(self, *args):
        print('called Gui.resize_empty_screen with args', args)
    def close(self):
        print('called Gui.close')


class MockChoiceBook:
    "stub for main.ChoiceBook"
    def __init__(self, arg):
        print(f"called ChoiceBook.__init__ with arg '{arg}'")
        self.gui = MockTabGui()
    def on_page_changed(self, start):
        print(f"called ChoiceBook.on_page_changed with arg '{start}'")


def test_editor_init(monkeypatch, capsys):
    """unittest for main.Editor.init
    """
    def mock_save_log():
        print('called shared.save_log')
    def mock_read(arg):
        print(f"called read_settings_json with arg '{arg}'")
        return {'lang': 'en', 'title': '', 'initial': '', 'plugins': []}
    def mock_read_2(arg):
        print(f"called read_settings_json with arg '{arg}'")
        return {'lang': 'en', 'title': '', 'initial': 'y', 'plugins': [('x', 'xxx'), ('y', 'yyy')]}
    def mock_read_3(arg):
        print(f"called read_settings_json with arg '{arg}'")
        return {'lang': 'en', 'title': 'qqq', 'initial': 'x', 'plugins': [('x', 'xxx')]}
    def mock_readcaptions(self, arg):
        print(f"called Editor.readcaptions with arg '{arg}'")
        self.captions = {'T_MAIN': 'maintitle', 'T_HELLO': 'hello from {}'}
    def mock_show(self):
        print('called Editor.show_empty_screen')
    def mock_set(self):
        print('called Editor.setcaptions')
    monkeypatch.setattr(testee.shared, 'save_log', mock_save_log)
    monkeypatch.setattr(testee, 'read_settings_json', mock_read)
    monkeypatch.setattr(testee.Editor, 'show_empty_screen', mock_show)
    monkeypatch.setattr(testee.Editor, 'readcaptions', mock_readcaptions)
    monkeypatch.setattr(testee.gui, 'Gui', MockGui)
    monkeypatch.setattr(testee, 'ChoiceBook', MockChoiceBook)
    monkeypatch.setattr(testee.Editor, 'setcaptions', mock_set)
    monkeypatch.setattr(testee, 'CONF', 'mock_conf')
    monkeypatch.setattr(testee, 'BASE', testee.pathlib.Path('/confbase'))
    args = types.SimpleNamespace(conf='', start='')
    testobj = testee.Editor(args)
    assert testobj.ini == {'initial': '', 'lang': 'en', 'plugins': [], 'title': ''}
    assert testobj.pluginfiles == {}
    assert testobj.book is None
    assert isinstance(testobj.gui, testee.gui.Gui)
    assert capsys.readouterr().out == ("called shared.save_log\n"
                                       "called read_settings_json with arg 'mock_conf'\n"
                                       "called Editor.readcaptions with arg 'en'\n"
                                       f"called Gui.__init__ with arg {testobj}\n"
                                       "called Editor.show_empty_screen\n"
                                       "called Gui.go\n")
    monkeypatch.setattr(testee, 'read_settings_json', mock_read_2)
    args = types.SimpleNamespace(conf='other_conf', start='y')
    testobj = testee.Editor(args)
    assert testobj.ini == {'initial': 'y', 'lang': 'en', 'title': '', 'plugins': [('x', 'xxx'),
                                                                                  ('y', 'yyy')]}
    assert testobj.pluginfiles == {}
    assert isinstance(testobj.gui, testee.gui.Gui)
    assert isinstance(testobj.book, testee.ChoiceBook)
    assert capsys.readouterr().out == (
            "called shared.save_log\n"
            "called read_settings_json with arg '/confbase/other_conf'\n"
            "called Editor.readcaptions with arg 'en'\n"
            f"called Gui.__init__ with arg {testobj}\n"
            "called Gui.set_window_title with arg 'maintitle'\n"
            "called Gui.statusbar_message with args ('hello from maintitle',)\n"
            f"called ChoiceBook.__init__ with arg '{testobj}'\n"
            "called TabbedInterface.__init__ with args ()\n"
            "called Gui.setup_tabs\n"
            "called TabbedInterface.set_selected_tool with arg '1'\n"
            "called ChoiceBook.on_page_changed with arg '1'\n"
            "called Editor.setcaptions\n"
            "called Gui.go\n")
    monkeypatch.setattr(testee, 'read_settings_json', mock_read_3)
    args = types.SimpleNamespace(conf='/yet/another/conf', start='')
    testobj = testee.Editor(args)
    assert testobj.ini == {'initial': 'x', 'lang': 'en', 'title': 'qqq', 'plugins': [('x', 'xxx')]}
    assert testobj.pluginfiles == {}
    assert isinstance(testobj.gui, testee.gui.Gui)
    assert isinstance(testobj.book, testee.ChoiceBook)
    assert capsys.readouterr().out == (
            "called shared.save_log\n"
            "called read_settings_json with arg '/yet/another/conf'\n"
            "called Editor.readcaptions with arg 'en'\n"
            f"called Gui.__init__ with arg {testobj}\n"
            "called Gui.set_window_title with arg 'maintitle'\n"
            "called Gui.statusbar_message with args ('hello from maintitle',)\n"
            f"called ChoiceBook.__init__ with arg '{testobj}'\n"
            "called TabbedInterface.__init__ with args ()\n"
            "called Gui.setup_tabs\n"
            "called TabbedInterface.set_selected_tool with arg '0'\n"
            "called ChoiceBook.on_page_changed with arg '0'\n"
            "called Editor.setcaptions\n"
            "called Gui.go\n")

def setup_editor(monkeypatch, capsys):
    """stub for main.Editor
    """
    def mock_init(self):
        print('called Editor.__init__')
    monkeypatch.setattr(testee.Editor, '__init__', mock_init)
    testobj = testee.Editor()
    testobj.book = MockChoiceBook(testobj)
    testobj.gui = MockGui(testobj)
    assert capsys.readouterr().out == ('called Editor.__init__\n'
                                       f"called ChoiceBook.__init__ with arg '{testobj}'\n"
                                       'called TabbedInterface.__init__ with args ()\n'
                                       f'called Gui.__init__ with arg {testobj}\n')
    return testobj

def test_editor_show_empty_screen(monkeypatch, capsys):
    """unittest for main.Editor.show_empty_screen
    """
    class MockDummy:
        "stub for gui.DummyPage"
        def __init__(self, *args):
            print('called gui.DummyPage.__init__ with args', args)
    def mock_init(self):
        print('called Editor.__init__')
    monkeypatch.setattr(testee.Editor, '__init__', mock_init)
    monkeypatch.setattr(testee.gui, 'DummyPage', MockDummy)
    testobj = testee.Editor()
    testobj.gui = MockGui(testobj)
    assert capsys.readouterr().out == ('called Editor.__init__\n'
                                       f'called Gui.__init__ with arg {testobj}\n')
    testobj.captions = {'EMPTY_CONFIG_TEXT': 'Empty'}
    testobj.show_empty_screen()
    assert isinstance(testobj.book, testee.SimpleNamespace)
    assert isinstance(testobj.book.gui, testee.gui.DummyPage)
    assert isinstance(testobj.book.page, testee.SimpleNamespace)
    assert testobj.book.page.gui == testobj.book.gui
    assert capsys.readouterr().out == (
            f"called gui.DummyPage.__init__ with args ({testobj.gui}, 'Empty')\n"
            "called Gui.resize_empty_screen with args (640, 80)\n")

def _test_editor_get_menudata(monkeypatch, capsys):
    """unittest for main.Editor.get_menudata
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.get_menudata()

def test_editor_m_read(monkeypatch, capsys):
    """unittest for main.Editor.m_read
    """
    def mock_show(*args):
        print('called gui.show_message with args', args)
    def mock_ask(*args):
        print('called gui.ask_question with args', args)
        return False
    def mock_ask_2(*args):
        print('called gui.ask_question with args', args)
        return True
    monkeypatch.setattr(testee.gui, 'show_message', mock_show)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.book.page = MockHotkeyPanel(testobj.book, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n")
    testobj.book.page.settings = []
    testobj.m_read()
    assert capsys.readouterr().out == (
            f"called gui.show_message with args ({testobj.gui}, 'I_ADDSET')\n")
    testobj.book.page.settings = ['x']
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask)
    testobj.book.page.modified = False
    testobj.m_read()
    assert capsys.readouterr().out == (
            f"called gui.ask_question with args ({testobj.gui}, 'Q_NOCHG')\n")
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask_2)
    testobj.m_read()
    assert capsys.readouterr().out == (
            f"called gui.ask_question with args ({testobj.gui}, 'Q_NOCHG')\n"
            "called HotkeyPanel.readkeys\n"
            "called HotkeyPanel.populate_list\n")
    testobj.book.page.modified = True
    testobj.m_read()
    assert capsys.readouterr().out == ("called HotkeyPanel.readkeys\n"
                                       "called HotkeyPanel.populate_list\n")
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask_2)
    testobj.m_read()
    assert capsys.readouterr().out == ("called HotkeyPanel.readkeys\n"
                                       "called HotkeyPanel.populate_list\n")

def test_editor_m_save(monkeypatch, capsys):
    """unittest for main.Editor.m_save
    """
    def mock_ask(*args):
        print('called gui.ask_question with args', args)
        return False
    def mock_ask_2(*args):
        print('called gui.ask_question with args', args)
        return True
    def mock_show(*args):
        print('called gui.show_message with args', args)
    def mock_log():
        print('called shared.log_exc')
    def mock_savekeys():
        print('called HotkeyPanel.savekeys')
    monkeypatch.setattr(testee.shared, 'log_exc', mock_log)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.book.page = MockHotkeyPanel(testobj.book, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n")
    testobj.book.page.modified = False
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask)
    testobj.m_save(event=None)
    assert capsys.readouterr().out == (
            f"called gui.ask_question with args ({testobj.gui}, 'Q_NOCHG')\n")
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask_2)
    testobj.m_save(event=None)
    assert capsys.readouterr().out == (
            f"called gui.ask_question with args ({testobj.gui}, 'Q_NOCHG')\n"
            "called shared.log_exc\n"
            f"called gui.show_message with args ({testobj.gui}, 'I_DEFSAV')\n")
    testobj.book.page.modified = True
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask)
    testobj.m_save(event=None)
    assert capsys.readouterr().out == (
            "called shared.log_exc\n"
            f"called gui.show_message with args ({testobj.gui}, 'I_DEFSAV')\n")
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask_2)
    testobj.m_save(event=None)
    assert capsys.readouterr().out == (
            "called shared.log_exc\n"
            f"called gui.show_message with args ({testobj.gui}, 'I_DEFSAV')\n")
    testobj.book.page.savekeys = mock_savekeys
    testobj.m_save(event=None)
    assert capsys.readouterr().out == (
            "called HotkeyPanel.savekeys\n"
            f"called gui.show_message with args ({testobj.gui}, 'I_RSTRT')\n")

def _test_editor_m_loc(monkeypatch, capsys):
    """unittest for main.Editor.m_loc
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.m_loc(event=None)

def _test_editor_accept_pathsettings(monkeypatch, capsys):
    """unittest for main.Editor.accept_pathsettings
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.accept_pathsettings(name_path_list, settingsdata, names_to_remove)

def _test_editor_m_rebuild(monkeypatch, capsys):
    """unittest for main.Editor.m_rebuild
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.m_rebuild(event=None)

def _test_editor_accept_csvsettings(monkeypatch, capsys):
    """unittest for main.Editor.accept_csvsettings
    """
    def mock_show(*args):
        print('called gui.show_message with args', args)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.accept_csvsettings(cloc, ploc, title, rebuild, details, redef)

def _test_editor_m_tool(monkeypatch, capsys):
    """unittest for main.Editor.m_tool
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.m_tool(event=None)

def _test_editor_accept_extrasettings(monkeypatch, capsys):
    """unittest for main.Editor.accept_extrasettings
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.accept_extrasettings(program, title, rebuild, showdet, redef, data)

def _test_editor_m_col(monkeypatch, capsys):
    """unittest for main.Editor.m_col
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.m_col(event=None)

def _test_editor_accept_columnsettings(monkeypatch, capsys):
    """unittest for main.Editor.accept_columnsettings
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.accept_columnsettings(data)

def _test_editor_accept_newcolumns(monkeypatch, capsys):
    """unittest for main.Editor.accept_newcolumns
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.accept_newcolumns(entries)

def test_editor_m_entry(monkeypatch, capsys):
    """unittest for main.Editor.m_entry
    """
    def mock_show(*args):
        print('called gui.show_message with args', args)
    def mock_dialog(*args):
        print('called gui.show_dialog with args', args)
        return False
    def mock_dialog_2(*args):
        print('called gui.show_dialog with args', args)
        return True
    def mock_writecsv(*args):
        print('called writecsv with args', args)
    def mock_writejson(*args):
        print('called writejson with args', args)
    monkeypatch.setattr(testee, 'writejson', mock_writejson)
    monkeypatch.setattr(testee, 'writecsv', mock_writecsv)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show)
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.ini = {'lang': 'en'}
    testobj.book.page = MockHotkeyPanel(testobj.book, 'xxx')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj.book}, 'xxx')\n")
    testobj.book.page.settings = {}
    testobj.book.page.column_info = [('column', 'info')]
    testobj.book.page.data = {}
    testobj.otherstuff = {'other': 'stuff'}
    testobj.book.page.pad = 'settings.json'
    testobj.m_entry()
    assert capsys.readouterr().out == (
            f"called gui.show_message with args ({testobj.gui}, 'I_ADDCOL')\n")

    testobj.book.page.settings = {'x': 'y'}
    testobj.book.page.colums_info = []
    testobj.m_entry()
    assert capsys.readouterr().out == (f"called gui.show_dialog with args ({testobj},"
                                       " <class 'editor.dialogs_qt.EntryDialog'>)\n")

    testobj.book.page.settings = {'x': 'y'}
    testobj.book.page.colums_info = [('column', 'info')]
    testobj.m_entry()
    assert capsys.readouterr().out == (f"called gui.show_dialog with args ({testobj},"
                                       " <class 'editor.dialogs_qt.EntryDialog'>)\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_2)
    testobj.m_entry()
    assert capsys.readouterr().out == (f"called gui.show_dialog with args ({testobj},"
                                       " <class 'editor.dialogs_qt.EntryDialog'>)\n")

    testobj.book.page.data = {'a': 'b'}
    testobj.m_entry()
    assert capsys.readouterr().out == (f"called gui.show_dialog with args ({testobj},"
                                       " <class 'editor.dialogs_qt.EntryDialog'>)\n"
                                       "called writejson with args ('settings.json',"
                                       " {'x': 'y'}, [('column', 'info')], {'a': 'b'},"
                                       " {'other': 'stuff'})\n"
                                       "called HotkeyPanel.populate_list\n")

    testobj.book.page.pad = 'settings.csv'
    testobj.m_entry()
    assert capsys.readouterr().out == (f"called gui.show_dialog with args ({testobj},"
                                       " <class 'editor.dialogs_qt.EntryDialog'>)\n"
                                       "called writecsv with args ('settings.csv',"
                                       " {'x': 'y'}, [('column', 'info')], {'a': 'b'}, 'en')\n"
                                       "called HotkeyPanel.populate_list\n")

def test_editor_m_lang(monkeypatch, capsys, tmp_path):
    """unittest for main.Editor.m_lang
    """
    def mock_choice(*args, **kwargs):
        print('called gui.get_choice with args', args, kwargs)
        return '', False
    def mock_choice_2(*args, **kwargs):
        print('called gui.get_choice with args', args, kwargs)
        return 'xx', True
    def mock_write(arg):
        print(f"called write_settings_json with arg '{arg}'")
    def mock_read(arg):
        print(f"called Editor.readcaptions with arg '{arg}'")
    def mock_set():
        print("called Editor.setcaptions")
    monkeypatch.setattr(testee, 'write_settings_json', mock_write)
    monkeypatch.setattr(testee.gui, 'get_choice', mock_choice)
    langdir = tmp_path
    (langdir / 'en.lng').touch()
    (langdir / 'nl.lng').touch()
    monkeypatch.setattr(testee.shared, 'HERELANG', langdir)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.title = 'hello'
    testobj.captions = {'P_SELLNG': 'xxx'}
    testobj.readcaptions = mock_read
    testobj.setcaptions = mock_set
    testobj.ini = {'lang': 'du.lng'}
    testobj.m_lang()
    assert testobj.ini['lang'] == 'du.lng'
    assert capsys.readouterr().out == (
            "called gui.get_choice with args"
            f" ({testobj.gui}, 'xxx', 'hello', ['en.lng', 'nl.lng']) {{'current': 0}}\n")

    testobj.ini = {'lang': 'nl.lng'}
    testobj.m_lang()
    assert testobj.ini['lang'] == 'nl.lng'
    assert capsys.readouterr().out == (
            "called gui.get_choice with args"
            f" ({testobj.gui}, 'xxx', 'hello', ['en.lng', 'nl.lng']) {{'current': 1}}\n")

    monkeypatch.setattr(testee.gui, 'get_choice', mock_choice_2)
    testobj.m_lang()
    assert testobj.ini['lang'] == 'xx'
    assert capsys.readouterr().out == (
            "called gui.get_choice with args"
            f" ({testobj.gui}, 'xxx', 'hello', ['en.lng', 'nl.lng']) {{'current': 1}}\n"
            "called write_settings_json with arg '{'lang': 'xx'}'\n"
            "called Editor.readcaptions with arg 'xx'\n"
            "called Editor.setcaptions\n")

def test_editor_m_about(monkeypatch, capsys):
    """unittest for main.Editor.m_about
    """
    def mock_show(*args, **kwargs):
        print('called gui.show_message with args', args, kwargs)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show)
    monkeypatch.setattr(testee, 'VRS', 'xxx')
    monkeypatch.setattr(testee, 'AUTH', 'yyy')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.captions = {'T_ABOUT': '{} / versie {} / {} / {}', 'T_SHORT': 'this',
                        'T_LONG': 'more text'}
    testobj.m_about()
    assert capsys.readouterr().out == (
            "called gui.show_message with args"
            f" ({testobj.gui},) {{'text': 'this\\nversie xxx\\nyyy\\nmore text'}}\n")

def test_editor_m_pref(monkeypatch, capsys):
    """unittest for main.Editor.m_pref
    """
    def mock_dialog(*args):
        print('called gui.show_dialog with args', args)
        return False
    def mock_dialog_2(*args):
        print('called gui.show_dialog with args', args)
        args[0].prefs = ('Remember', 'unchanged')
        return True
    def mock_dialog_3(*args):
        print('called gui.show_dialog with args', args)
        args[0].prefs = ('Fixed', 'unchanged')
        return True
    def mock_dialog_4(*args):
        print('called gui.show_dialog with args', args)
        args[0].prefs = ('Remember', 'changed')
        return True
    def mock_dialog_5(*args):
        print('called gui.show_dialog with args', args)
        args[0].prefs = ('Fixed', 'changed')
        return True
    def mock_write(arg):
        print(f"called write_settings_json with arg '{arg}'")
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog)
    monkeypatch.setattr(testee, 'write_settings_json', mock_write)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Fixed'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_2)
    # testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Remember'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings_json with arg"
            " '{'startup': 'Remember', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_3)
    testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Fixed'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings_json with arg"
            " '{'startup': 'Fixed', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_4)
    testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Remember'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings_json with arg"
            " '{'startup': 'Remember', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_5)
    testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Fixed'
    assert testobj.ini['initial'] == 'changed'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings_json with arg"
            " '{'startup': 'Fixed', 'initial': 'changed'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_2)
    testobj.ini = {'startup': 'Remember', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Remember'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings_json with arg"
            " '{'startup': 'Remember', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_3)
    testobj.ini = {'startup': 'Remember', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Fixed'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings_json with arg"
            " '{'startup': 'Fixed', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_4)
    testobj.ini = {'startup': 'Remember', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Remember'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings_json with arg"
            " '{'startup': 'Remember', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_5)
    testobj.ini = {'startup': 'Remember', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Fixed'
    assert testobj.ini['initial'] == 'changed'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings_json with arg"
            " '{'startup': 'Fixed', 'initial': 'changed'}'\n")

def test_editor_accept_startupsettings(monkeypatch, capsys):
    """unittest for main.Editor.accept_startupsettings
    """
    monkeypatch.setattr(testee.shared, 'mode_f', 'fixed')
    monkeypatch.setattr(testee.shared, 'mode_r', 'remember')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.accept_startupsettings(True, False, 'xxx')
    assert testobj.prefs == ('fixed', 'xxx')
    testobj.accept_startupsettings(False, True, 'yyy')
    assert testobj.prefs == ('remember', 'yyy')
    testobj.accept_startupsettings(True, True, 'zzz')
    assert testobj.prefs == ('fixed', 'zzz')
    testobj.accept_startupsettings(False, False, 'qqq')
    assert testobj.prefs == (None, 'qqq')

def test_editor_m_exit(monkeypatch, capsys):
    """unittest for main.Editor.m_exit
    """
    def mock_exit():
        print('called Editor.exit')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.exit = mock_exit
    testobj.m_exit()
    assert capsys.readouterr().out == 'called Editor.exit\n'

def test_editor_exit(monkeypatch, capsys):
    """unittest for main.Editor.exit
    """
    def mock_exit():
        print('called HotkeyPanel.exit')
        return False
    def mock_exit_2():
        print('called HotkeyPanel.exit')
        return True
    def mock_write(*args, **kwargs):
        print('called write_settings_json with args', args, kwargs)
    def mock_get():
        print('called SingledataInterface.get_selected_text')
        return 'xxx'
    monkeypatch.setattr(testee.shared, 'mode_f', 'fixed')
    monkeypatch.setattr(testee.shared, 'mode_r', 'remember')
    monkeypatch.setattr(testee, 'write_settings_json', mock_write)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.book.page = types.SimpleNamespace(exit=mock_exit)
    testobj.ini = {}
    testobj.exit()
    assert testobj.ini == {}
    assert capsys.readouterr().out == ("called HotkeyPanel.exit\n")
    testobj.book.page = types.SimpleNamespace(exit=mock_exit_2)
    testobj.exit()
    assert testobj.ini == {}
    assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                       "called Gui.close\n")
    testobj.ini = {'startup': 'remember'}
    testobj.book.gui.get_selected_text = mock_get
    testobj.exit()
    assert testobj.ini['initial'] == 'xxx'
    assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                       "called SingledataInterface.get_selected_text\n"
                                       "called write_settings_json with args"
                                       " ({'startup': 'remember', 'initial': 'xxx'},)"
                                       " {'nobackup': True}\n"
                                       "called Gui.close\n")
    testobj.ini = {'startup': 'remember', 'initial': 'yyy'}
    testobj.book.gui.get_selected_text = mock_get
    testobj.exit()
    assert testobj.ini['initial'] == 'xxx'
    assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                       "called SingledataInterface.get_selected_text\n"
                                       "called write_settings_json with args"
                                       " ({'startup': 'remember', 'initial': 'xxx'},)"
                                       " {'nobackup': True}\n"
                                       "called Gui.close\n")
    testobj.ini = {'startup': 'remember', 'initial': 'yyy'}
    testobj.book.gui = MockTabGui()
    assert capsys.readouterr().out == "called TabbedInterface.__init__ with args ()\n"
    testobj.exit()
    assert testobj.ini['initial'] == 'yyy'
    assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                       "called Gui.close\n")
    testobj.ini = {'startup': 'fixed'}
    testobj.exit()
    assert testobj.ini == {'startup': 'fixed'}
    assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                       "called Gui.close\n")

def test_editor_change_setting(monkeypatch, capsys, tmp_path):
    """unittest for main.Editor.change_setting
    """
    ininame = tmp_path / 'mock_ini'
    ininame.touch()
    bakname = ininame.with_suffix('.bak')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.captions = {'C_SETT': 'setting', 'C_TITLE': 'xxxxx'}
    testobj.ini = {'filename': str(ininame)}
    testobj.change_setting('sett', 'was', 'is')
    assert bakname.read_text() == ''
    assert ininame.read_text() == "# setting\nSETT = 'is'\n"

    testobj.change_setting('sett', 'is', '')
    assert bakname.read_text() == "# setting\nSETT = 'is'\n"
    assert ininame.read_text() == "# setting\nSETT = ''\n"

    testobj.change_setting('sett', '', 'was')
    assert bakname.read_text() == "# setting\nSETT = ''\n"
    assert ininame.read_text() == "# setting\nSETT = 'was'\n"

    testobj.change_setting('sett', 'was', 'is')
    assert bakname.read_text() == "# setting\nSETT = 'was'\n"
    assert ininame.read_text() == "# setting\nSETT = 'is'\n"

    testobj.change_setting('title', '', 'tata')
    assert bakname.read_text() == "# setting\nSETT = 'is'\n"
    assert ininame.read_text() == "# setting\nSETT = 'is'\n# xxxxx\nTITLE = 'tata'\n"

    testobj.change_setting('title', 'tata', '')
    assert bakname.read_text() == "# setting\nSETT = 'is'\n# xxxxx\nTITLE = 'tata'\n"
    assert ininame.read_text() == "# setting\nSETT = 'is'\n"


def test_editor_readcaptions(monkeypatch, capsys):
    """unittest for main.Editor.readcaptions
    """
    def mock_read(lang):
        print(f"called readlang with arg '{lang}'")
        return {'captions': 'dict'}
    monkeypatch.setattr(testee, 'readlang', mock_read)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.readcaptions('en')
    assert testobj.captions == {'captions': 'dict'}
    assert testobj.last_textid == ''


def test_editor_setcaptions(monkeypatch, capsys):
    """unittest for main.Editor.setcaptions
    """
    def mock_set():
        print('called EditorGui.setcaptions')
    def mock_set2():
        print('called TabbedInterface.setcaptions')
    def mock_set3():
        print('called HotkeyPanel.setcaptions')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.setcaptions = mock_set
    testobj.book.gui.setcaptions = mock_set2
    testobj.book.page = types.SimpleNamespace(setcaptions=mock_set3)
    testobj.setcaptions()
    assert capsys.readouterr().out == ("called EditorGui.setcaptions\n"
                                       "called TabbedInterface.setcaptions\n"
                                       "called HotkeyPanel.setcaptions\n")
