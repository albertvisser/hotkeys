"""unittests for ./editor/plugins/opkeys.py
"""
from editor.plugins import opkeys as testee


def test_get_keydefs():
    """unittest for opkeys.get_keydefs
    """
    doc = []
    assert testee.get_keydefs(doc, 'soort') == {}

    doc = ['', '[InFo]', 'yyyy', '[Version]', '12.0', ';\n', '[x]', 'a hello', '#---']
    keydefs = {'x': 'xxx'}
    assert testee.get_keydefs(doc, 'soort2', keydefs) == {'x': 'xxx'}

    doc = ['[x]', '[y]', 'keydata=definition', 'extra,key"data=de"fi=nition',
           'platform xxx feature yyy,keydata=definition',
           'PlatForm xxx Feature yyy,keydata=definition', '[z]']
    keydefs = {'x': 'xxx', 'z': 'zzz'}
    assert testee.get_keydefs(doc, 'soort2', keydefs) == {
            'x': 'xxx', 'z': 'zzz', 'y': [['', '', 'keydata', 'soort2', 'definition'],
                                          ['', '', 'key data=de fi', 'soort2', 'nition'],
                                          ['xxx', 'yyy', 'keydata', 'soort2', 'definition'],
                                          ['xxx', 'yyy', 'keydata', 'soort2', 'definition']]}


def get_tmp_path():
    "helper function to get temporary basepath"
    return temp_path


class MockSettings:
    "stub voor opkeys.Settings object"
    def __init__(self, arg):
        print('called Settings.__init__ with arg', arg)
        self.csv = get_tmp_path() / 'inipath'
        self.user = get_tmp_path() / 'userdefs'
        self.std = get_tmp_path() / 'stddefs'


class MockWriter:
    "stub for csv writer object"
    def __init__(self, stream):
        print('called csv.writer.__init__ with arg', stream)
        self._stream = stream
    def writerow(self, data):
        print('called csv.writer.writerow with arg', data)


def test_write_data(monkeypatch, capsys, tmp_path):
    """unittest for opkeys.write_data
    """
    global temp_path
    temp_path = tmp_path
    def mock_copy(*args):
        print('called shutil.copyfile with args', args)
    def mock_get(*args):
        print('called get_keydefs with args', args)
        return {args[1]: [['key'], ['defs']]}
    (tmp_path / 'inipath').mkdir()
    (tmp_path / 'userdefs').touch()
    (tmp_path / 'stddefs').touch()
    monkeypatch.setattr(testee, 'Settings', MockSettings)
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
    monkeypatch.setattr(testee.csv, 'writer', MockWriter)
    monkeypatch.setattr(testee, 'get_keydefs', mock_get)
    testee.write_data()
    assert capsys.readouterr().out == (
            f"called Settings.__init__ with arg /home/albert/tcmdrkeys/tcmdrkeys/opkey_config.py\n"
            f"called get_keydefs with args (<_io.TextIOWrapper name='{tmp_path / 'userdefs'}'"
            " mode='r' encoding='UTF-8'>, 'R')\n"
            f"called get_keydefs with args (<_io.TextIOWrapper name='{tmp_path / 'stddefs'}'"
            " mode='r' encoding='UTF-8'>, 'S', {'R': [['key'], ['defs']]})\n"
            "called csv.writer.__init__ with arg"
            f" <_io.TextIOWrapper name='{tmp_path / 'inipath' / 'Opera_hotkeys.csv'}'"
            " mode='w' encoding='UTF-8'>\n"
            "called csv.writer.writerow with arg ['S', 'key']\n"
            "called csv.writer.writerow with arg ['S', 'defs']\n")
    (tmp_path / 'inipath' / 'Opera_hotkeys.csv').touch()
    testee.write_data()
    assert capsys.readouterr().out == (
            f"called Settings.__init__ with arg /home/albert/tcmdrkeys/tcmdrkeys/opkey_config.py\n"
            f"called shutil.copyfile with args ('{tmp_path / 'inipath' / 'Opera_hotkeys.csv'}',"
            f" '{tmp_path / 'inipath' / 'Opera_hotkeys.csv.backup'}')\n"
            f"called get_keydefs with args (<_io.TextIOWrapper name='{tmp_path / 'userdefs'}'"
            " mode='r' encoding='UTF-8'>, 'R')\n"
            f"called get_keydefs with args (<_io.TextIOWrapper name='{tmp_path / 'stddefs'}'"
            " mode='r' encoding='UTF-8'>, 'S', {'R': [['key'], ['defs']]})\n"
            "called csv.writer.__init__ with arg"
            f" <_io.TextIOWrapper name='{tmp_path / 'inipath' / 'Opera_hotkeys.csv'}'"
            " mode='w' encoding='UTF-8'>\n"
            "called csv.writer.writerow with arg ['S', 'key']\n"
            "called csv.writer.writerow with arg ['S', 'defs']\n")


def _test_savekeys():
    """unittest for opkeys.savekeys - niet geïmplementeerd
    """


class TestSettings:
    """unittest for opkeys.Settings
    """
    def setup_testobj(self, monkeypatch, capsys, fnaam):
        """stub for opkeys.Settings object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Settings.__init__ with args', args)
        monkeypatch.setattr(testee.Settings, '__init__', mock_init)
        testobj = testee.Settings(fnaam)
        testobj.fnaam = fnaam
        testobj.namen = ['OP_STD', 'OP_USER', 'OP_CSV', 'LANG']
        assert capsys.readouterr().out == f"called Settings.__init__ with args ('{fnaam}',)\n"
        return testobj

    def test_init(self, tmp_path):
        """unittest for Settings.__init__
        """
        fnaam = tmp_path / 'testfile'
        testobj = testee.Settings(fnaam)
        assert testobj.fnaam == fnaam
        assert testobj.namen == ['OP_STD', 'OP_USER', 'OP_CSV', 'LANG']
        assert testobj.pad == ''
        assert testobj.lang == ''
        assert not hasattr(testobj, 'std')
        assert not hasattr(testobj, 'user')
        assert not hasattr(testobj, 'csv')
        fnaam.write_text('\n# comment\nOP_STD=xxx\nOP_USER=yyy\nOP_CSV=zzz\nLANG=en\nqqq=rrr\nst')
        testobj = testee.Settings(fnaam)
        assert testobj.fnaam == fnaam
        assert testobj.namen == ['OP_STD', 'OP_USER', 'OP_CSV', 'LANG']
        assert testobj.pad == ''
        assert testobj.lang == ''
        assert testobj.std == 'xxx'
        assert testobj.user == 'yyy'
        assert testobj.csv == 'zzz'

    def test_write(self, monkeypatch, capsys, tmp_path):
        """unittest for Settings.write
        """
        fnaam = tmp_path / 'testfile'
        fnaam_o = tmp_path / 'testfile.bak'
        fnaam.write_text('\n# comment\nOP_STD=xxx\nOP_USER=yyy\nOP_CSV=zzz\nLANG=en\nqqq=rrr\nst')
        testobj = self.setup_testobj(monkeypatch, capsys, str(fnaam))
        testobj.std = 'aaa'
        testobj.user = 'bbb'
        testobj.csv = 'ddd'
        testobj.write()
        assert fnaam.read_text() == (
                '\n# comment\nOP_STD=aaa\nOP_USER=bbb\nOP_CSV=ddd\nLANG=en\nqqq=rrr\nst')
        assert capsys.readouterr().out == ""
