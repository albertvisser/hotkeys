"""unittests for ./editor/plugins/audacity_keys.py
"""
import types
import pathlib
from editor.plugins import audacity_keys as testee


def test_translate_keyname():
    """unittest for audacity_keys._translate_keyname
    """
    assert testee._translate_keyname('xxx') == "xxx"
    assert testee._translate_keyname('Escape') == "Esc"
    assert testee._translate_keyname('Delete') == "Del"
    assert testee._translate_keyname('Return') == "Enter"
    assert testee._translate_keyname('Page_up') == "PgUp"
    assert testee._translate_keyname('Page_down') == "PgDn"
    assert testee._translate_keyname('NUMPAD_ENTER') == "NumEnter"


def test_build_data(monkeypatch, capsys):
    """unittest for audacity_keys.build_data
    """
    def mock_show(*args, **kwargs):
        print('called show_cancel_message with args', args, kwargs)
        return False
    def mock_show_2(*args, **kwargs):
        print('called show_cancel_message with args', args, kwargs)
        return True
    def mock_get(*args, **kwargs):
        print('called get_file_to_open with args', args, kwargs)
        return ''
    def mock_get_2(*args, **kwargs):
        print('called get_file_to_open with args', args, kwargs)
        return 'kbfilename'
    def mock_parse(fname):
        print(f"called ET.parse with arg '{fname}'")
        return types.SimpleNamespace(getroot=lambda *x: 'xmlroot')
    def mock_build(root):
        print(f"called build_commandlist with arg '{root}'")
        return 'shortcuts', 'commands'
    monkeypatch.setattr(testee, 'show_cancel_message', mock_show)
    monkeypatch.setattr(testee, 'get_file_to_open', mock_get)
    monkeypatch.setattr(testee.ET, 'parse', mock_parse)
    monkeypatch.setattr(testee, 'build_commandlist', mock_build)
    monkeypatch.setattr(testee, 'INSTRUCTIONS', 'instructions')
    page = types.SimpleNamespace(settings={}, gui='pagegui')
    assert testee.build_data(page, showinfo=False) == ({}, {})
    assert capsys.readouterr().out == ("")
    assert testee.build_data(page, showinfo=True) == ({}, {})
    assert capsys.readouterr().out == (
            "called show_cancel_message with args ('pagegui',) {'text': 'instructions'}\n")
    page = types.SimpleNamespace(settings={'AC_KEYS': 'ac_keys'}, gui='pagegui')
    assert testee.build_data(page, showinfo=False) == ('shortcuts', {'commands': 'commands'})
    assert capsys.readouterr().out == ("called ET.parse with arg 'ac_keys'\n"
                                       "called build_commandlist with arg 'xmlroot'\n")
    assert testee.build_data(page, showinfo=True) == ({}, {})
    assert capsys.readouterr().out == (
            "called show_cancel_message with args ('pagegui',) {'text': 'instructions'}\n")

    monkeypatch.setattr(testee, 'show_cancel_message', mock_show_2)
    assert testee.build_data(page, showinfo=True) == ({}, {})
    assert capsys.readouterr().out == (
            "called show_cancel_message with args ('pagegui',) {'text': 'instructions'}\n"
            "called get_file_to_open with args"
            " ('pagegui',) {'extension': 'XML files (*.xml)', 'start': 'ac_keys'}\n")
    monkeypatch.setattr(testee, 'get_file_to_open', mock_get_2)
    assert testee.build_data(page, showinfo=True) == ('shortcuts', {'commands': 'commands'})
    assert capsys.readouterr().out == (
            "called show_cancel_message with args ('pagegui',) {'text': 'instructions'}\n"
            "called get_file_to_open with args"
            " ('pagegui',) {'extension': 'XML files (*.xml)', 'start': 'ac_keys'}\n"
            "called ET.parse with arg 'kbfilename'\n"
            "called build_commandlist with arg 'xmlroot'\n")


def test_build_commandlist(capsys):
    """unittest for audacity_keys.build_commandlist
    """
    class MockElement:
        "stub for ElementTree.Element"
        def __init__(self, key, name, label):
            if key:
                self.key = key
            if name:
                self.name = name
            if label:
                self.label = label
        def get(self, arg, default=None):
            try:
                return getattr(self, arg)
                # if arg == 'key':
                #     return self.key
                # elif arg == 'name':
                #     return self.name
                # elif arg == 'label':
                #     return self.label
            except AttributeError:
                return default
    def mock_find(*args):
        print('called root.findall with args', args)
        return []
    def mock_find_2(*args):
        print('called root.findall with args', args)
        return [MockElement('C++', 'cmd1', 'desc1'), MockElement('+', 'cmd2', 'desc2'),
                MockElement('A+Num+', 'cmd3', 'desc3'), MockElement('A+S+X', 'cmd4', 'desc4'),
                MockElement('', '', ''), MockElement('A', 'cmd5', 'desc5')]
    root = types.SimpleNamespace(findall=mock_find)
    assert testee.build_commandlist(root) == ({}, {})
    assert capsys.readouterr().out == ("called root.findall with args ('command',)\n")
    root = types.SimpleNamespace(findall=mock_find_2)
    assert testee.build_commandlist(root) == (
        {1: ('+', 'C', 'cmd1', 'desc1'), 2: ('+', '', 'cmd2', 'desc2'),
         3: ('Num+', 'A', 'cmd3', 'desc3'), 4: ('X', 'AS', 'cmd4', 'desc4'),
         5: ('A', '', 'cmd5', 'desc5')},
        {'cmd1': 'desc1', 'cmd2': 'desc2', 'cmd3': 'desc3', 'cmd4': 'desc4', None: None,
         'cmd5': 'desc5'})
    assert capsys.readouterr().out == ("called root.findall with args ('command',)\n")


def test_savekeys(monkeypatch, capsys, tmp_path):
    """unittest for audacity_keys.savekeys
    """
    def mock_show(*args, **kwargs):
        print('called show_cancel_message with args', args, kwargs)
        return False
    def mock_show_2(*args, **kwargs):
        print('called show_cancel_message with args', args, kwargs)
        return True
    def mock_get(*args, **kwargs):
        print('called get_file_to_save with args', args, kwargs)
        return str(mockpath)
    def mock_copy(*args):
        print('called shutil.copyfile with args', args)
    mockpath = tmp_path / 'audakeys.xml'
    mockbakpath = tmp_path / 'audakeys.xml.bak'
    monkeypatch.setattr(testee, 'how_to_save', 'howto')
    monkeypatch.setattr(testee, 'show_cancel_message', mock_show)
    monkeypatch.setattr(testee, 'get_file_to_save', mock_get)
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
    parent = types.SimpleNamespace(settings={}, data={})
    testee.savekeys(parent)
    assert capsys.readouterr().out == (
            f"called show_cancel_message with args ({parent},) {{'text': 'howto'}}\n")

    # hier is een verschil gekomen door de laatste aanpaasing waarbij ik
    # a) de AC_KEYS setting van de parent instel als die er nog niet was
    # b) het aangegeven file alleen backup als het al bestaat
    monkeypatch.setattr(testee, 'show_cancel_message', mock_show_2)
    testee.savekeys(parent)
    parent.settings = {}    # side effect op parent ongedaan maken t.b.v. testoutput
    assert mockpath.read_text() == '<audacitykeyboard audacityversion="2.0.5" />'
    assert capsys.readouterr().out == (
            f"called show_cancel_message with args ({parent},) {{'text': 'howto'}}\n"
            f"called get_file_to_save with args ({parent},) {{'extension': 'XML files (*.xml)',"
            f" 'start': '{pathlib.Path('~/.config/Audacity-keys.xml').expanduser()}'}}\n")
    # mockpath.unlink()

    parent.settings = {'AC_KEYS': str(mockpath)}
    parent.data = {1: ('A', 'S', 'name1', 'label1'), 2: ('B', 'A', 'name2', 'label2'),
                   3: ('C', 'C', 'name3', 'label3'), 4: ('D', '', 'name4', 'label4'),
                   5: ('E', 'CAS', 'name5', 'label5')}
    testee.savekeys(parent)
    assert mockpath.read_text() == (
            '<audacitykeyboard audacityversion="2.0.5">'
            '<command name="name1" label="label1" key="Shift+A" />'
            '<command name="name2" label="label2" key="Alt+B" />'
            '<command name="name3" label="label3" key="Ctrl+C" />'
            '<command name="name4" label="label4" key="D" />'
            '<command name="name5" label="label5" key="Ctrl+Alt+Shift+E" />'
            '</audacitykeyboard>')
    assert capsys.readouterr().out == (
            f"called show_cancel_message with args ({parent},) {{'text': 'howto'}}\n"
            f"called shutil.copyfile with args ('{mockpath}', '{mockbakpath}')\n")
    mockpath.unlink()


def test_add_extra_attributes():
    """unittest for audacity_keys.add_extra_attributes
    """
    win = types.SimpleNamespace(keylist=[], otherstuff={'commands': {'x': 'xx', 'y': 'yy'}})
    testee.add_extra_attributes(win)
    assert win.keylist == ['NumEnter']
    assert win.descriptions == {'x': 'xx', 'y': 'yy'}
    assert win.commandslist == ['x', 'y']
