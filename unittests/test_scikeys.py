"""test new dc_keys plugin
"""
import types
import pytest
import editor.plugins.scikeys as testee


def test_translate_keyname(monkeypatch, capsys):
    convert = {'Equal': '=', 'Escape': 'Esc', 'Delete': 'Del', 'Return': 'Enter',
               'BackSpace': 'Backspace', 'PageUp': 'PgUp', 'PageDown': 'PgDn', 'space': 'Space',
               'Keypad*': 'Num*', 'Keypad+': 'Num+', 'Keypad-': 'Num-', 'Keypad/': 'Num/', }
    for x, y in convert.items():
        assert testee._translate_keyname(x) == y

def test_nicefy_props(monkeypatch, capsys):
    assert testee.nicefy_props('Ctrl+Alt+Shift+Anything') == ('Anything', 'CAS')
    assert testee.nicefy_props('Shift+Alt+Ctrl+KeypadPlus') == ('Keypad+', 'CAS')

def test_nicefy_source(monkeypatch, capsys):
    assert testee.nicefy_source('<control><alt><shift>Anything') == ('Anything', 'CAS')
    assert testee.nicefy_source('<shift><alt><control>Anything') == ('Anything', 'CAS')

def _test_read_commands(monkeypatch, capsys):
    testee.read_commands(path)

def _test_read_docs(monkeypatch, capsys):
    testee.read_docs(path)

def _test_read_symbols(monkeypatch, capsys):
    testee.read_symbols(fname)

def _test_read_menu_gtk(monkeypatch, capsys):
    testee.read_menu_gtk(fname)

def test_read_menu_win(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(testee, 'nicefy_props', lambda *x: ('qq', 'rr'))
    temp_fname = tmp_path / 'winmenufile'
    with temp_fname.open('w') as f:
        f.write('\n xxx\nMENUITEM  "xxx"  yyy\n MENUITEM SEPARATOR  \n'
                '   MENUITEM  "aaa\tbbb"   ccc\n')
    assert testee.read_menu_win(temp_fname) == [('qq', 'rr', 'ccc')]
