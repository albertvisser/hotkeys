"""unittests for ./editor/plugins/read_gtkaccel.py
"""
from editor.plugins import read_gtkaccel as testee
import pytest


def test_read_keydefs_and_stuff(monkeypatch, capsys):
    """unittest for read_gtkaccel.read_keydefs_and_stuff
    """
    def mock_read(filename):
        print(f'called readfile with arg {filename}')
        return {'key': 'defs'}, {'actions': 'dict'}, {}
    def mock_read_2(filename):
        print(f'called readfile with arg {filename}')
        return {'key': 'defs'}, {'actions': 'dict'}, {'others': 'dict'}
    def mock_actions(arg):
        print(f'called expand_actions with arg {arg}')
        return {'act': 'ions'}, {'action': 'dict'}, {'desc': 'riptions'}
    def mock_others(arg):
        print(f'called expand_others with arg {arg}')
        return {'other': 'actions'}, {'others': 'dict'}, {'other': 'keys'}
    monkeypatch.setattr(testee, 'readfile', mock_read)
    monkeypatch.setattr(testee, 'expand_actions', mock_actions)
    monkeypatch.setattr(testee, 'expand_others', mock_others)
    assert testee.read_keydefs_and_stuff('filename') == {
            'keydefs': {'key': 'defs'}, 'actions': {'act': 'ions'},
            'actionscontext': {'action': 'dict'}, 'contexts': ['action'],
            'descriptions': {'desc': 'riptions'}}
    assert capsys.readouterr().out == ("called readfile with arg filename\n"
                                       "called expand_actions with arg {'actions': 'dict'}\n")
    monkeypatch.setattr(testee, 'readfile', mock_read_2)
    assert testee.read_keydefs_and_stuff('filename') == {
            'keydefs': {'key': 'defs'}, 'actions': {'act': 'ions'},
            'actionscontext': {'action': 'dict'}, 'contexts': ['action'],
            'descriptions': {'desc': 'riptions'},
            'others': {'other': 'actions'}, 'othercontext': {'others': 'dict'},
            'otherkeys': {'other': 'keys'}}
    assert capsys.readouterr().out == ("called readfile with arg filename\n"
                                       "called expand_actions with arg {'actions': 'dict'}\n"
                                       "called expand_others with arg {'others': 'dict'}\n")


def test_readfile(monkeypatch, capsys, tmp_path):
    """unittest for read_gtkaccel.readfile
    """
    monkeypatch.setattr(testee, 'KEYDEF', 'KEYDEF')
    path = tmp_path / 'keydefs'
    with pytest.raises(FileNotFoundError):
        testee.readfile(str(path))
    path.touch()
    assert testee.readfile(str(path)) == ([], {}, [])
    assert capsys.readouterr().out == ("")
    path.write_text("KEYDEF\n  \n")
    assert testee.readfile(str(path)) == ([], {}, [])
    assert capsys.readouterr().out == ("KEYDEF\n\ncontains more/less that 2 items, what to do?\n")
    path.write_text('KEYDEF xxx yyy zzz)\n  \n')
    assert testee.readfile(str(path)) == ([], {}, [])
    assert capsys.readouterr().out == ('KEYDEF xxx yyy zzz)\n\n'
                                       'contains more/less that 2 items, what to do?\n')
    path.write_text('KEYDEF "x" "y" "z")\n  \n')
    assert testee.readfile(str(path)) == ([], {}, [])
    assert capsys.readouterr().out == ('KEYDEF "x" "y" "z")\n\n'
                                       'contains more/less that 2 items, what to do?\n')
    path.write_text('KEYDEF xxx yyy)')
    assert testee.readfile(str(path)) == ([], {}, [])
    assert capsys.readouterr().out == ('KEYDEF xxx yyy)\n'
                                       'contains more/less that 2 items, what to do?\n')
    path.write_text('KEYDEF "x" "y")')
    assert testee.readfile(str(path)) == ([], {}, [('x', 'y')])
    assert capsys.readouterr().out == ""
    path.write_text('; (KEYDEF "<Actions>/edit/edit-copy" "<Primary>c")\n'
                    '; (KEYDEF "<Actions>/edit/edit-paste" "")\n')
    assert testee.readfile(str(path)) == ([('C', 'C', 1)],
                                          {1: '/edit/edit-copy', 2: '/edit/edit-paste'}, [])
    assert capsys.readouterr().out == ("")


def test_parse_actiondef(monkeypatch):
    """unittest for read_gtkaccel.parse_actiondef
    """
    monkeypatch.setattr(testee, 'conversion_map', (('xxx', 'x'),))
    assert testee.parse_actiondef("it's>the xxx key") == ('The x key', '')
    assert testee.parse_actiondef("") == ('', '')
    assert testee.parse_actiondef("zzz") == ('Zzz', '')
    assert testee.parse_actiondef("<Primary>A bladibla") == ('A bladibla', 'C')
    assert testee.parse_actiondef("<Alt>b") == ('B', 'A')
    assert testee.parse_actiondef("<Shift>c") == ('C', 'S')
    assert testee.parse_actiondef("<Shift><Alt><Primary>") == ('', 'CAS')


def test_expand_actions():
    """unittest for read_gtkaccel.expand_actions
    """
    with pytest.raises(ValueError):
        testee.expand_actions({1: 'copy'})
    assert testee.expand_actions({2: 'edit/paste'}) == ({2: ('edit', 'paste')}, {'edit': ['paste']},
                                                        {2: ''})
    assert testee.expand_actions({1: '/edit/edit-copy', 2: '/edit/edit-paste'}) == (
           {1: ('edit', 'edit-copy'), 2: ('edit', 'edit-paste')},
           {'edit': ['edit-copy', 'edit-paste']}, {1: '', 2: ''})


def test_expand_others():
    """unittest for read_gtkaccel.expand_others
    """
    assert testee.expand_others([('x/y', 'yz'), ('/x/a', 'yb'), ('/q/r/s', '')]) == (
            {1: ('x', 'y'), 2: ('x', 'a'), 3: ('q', 'r/s')}, {'x': ['y', 'a'], 'q': ['r/s']},
            [('yz', 1), ('yb', 2)])
