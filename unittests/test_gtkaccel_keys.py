"""unittests for ./editor/plugins/gtkaccel_keys.py
"""
import types
from editor.plugins import gtkaccel_keys as testee
import pytest


def test_read_keydefs_and_stuff(monkeypatch, capsys):
    """unittest for gtkaccel_keys.read_keydefs_and_stuff
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
    """unittest for gtkaccel_keys.readfile
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
    """unittest for gtkaccel_keys.parse_actiondef
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
    """unittest for gtkaccel_keys.expand_actions
    """
    with pytest.raises(ValueError):
        testee.expand_actions({1: 'copy'})
    assert testee.expand_actions({2: 'edit/paste'}) == ({2: ('edit', 'paste')}, {'edit': ['paste']},
                                                        {2: ''})
    assert testee.expand_actions({1: '/edit/edit-copy', 2: '/edit/edit-paste'}) == (
           {1: ('edit', 'edit-copy'), 2: ('edit', 'edit-paste')},
           {'edit': ['edit-copy', 'edit-paste']}, {1: '', 2: ''})


def test_expand_others():
    """unittest for gtkaccel_keys.expand_others
    """
    assert testee.expand_others([('x/y', 'yz'), ('/x/a', 'yb'), ('/q/r/s', '')]) == (
            {1: ('x', 'y'), 2: ('x', 'a'), 3: ('q', 'r/s')}, {'x': ['y', 'a'], 'q': ['r/s']},
            [('yz', 1), ('yb', 2)])


def test_translate_keyname():
    """unittest for gtkaccel_keys._translate_keyname
    """
    for original, converted in [('x', 'x'), ('Equal', '='), ('Escape', 'Esc'), ('Delete', 'Del'),
                                ('Return', 'Enter'), ('Page_up', 'PgUp'), ('Page_down', 'PgDn')]:
        assert testee._translate_keyname(original) == converted


def test_build_data(monkeypatch, capsys):
    """unittest for gtkaccel_keys.build_data
    """
    def mock_names(*args):
        print('called names2filenames with args', args)
        return '', ''
    def mock_names_2(*args):
        print('called names2filenames with args', args)
        return '', 'fnamedesc'
    def mock_names_3(*args):
        print('called names2filenames with args', args)
        return 'fnamekb', ''
    def mock_names_4(*args):
        print('called names2filenames with args', args)
        return 'fnamekb', 'fnamedesc'
    def mock_read(*args):
        print('called read_keydefs_and_stuff with args', args)
        return {'keydefs': [], 'actions': {}, 'descriptions': {}}
    def mock_read_2(*args):
        print('called read_keydefs_and_stuff with args', args)
        return {'keydefs': [('x', '', 'xxx'), ('y', 'C', 'yyy')],
                'actions': {'xxx': ['ccc', 'aaa'], 'yyy': ['ddd', 'bbb']},
                'descriptions': {'xxx': '', 'yyy': 'descy'}}
    def mock_translate(key):
        print(f'called _translate_keyname with arg {key}')
        return key
    settnames = 'settnames'
    page = types.SimpleNamespace(otherstuff={'descriptions': {'x': 'y'}})
    monkeypatch.setattr(testee, 'names2filenames', mock_names)
    monkeypatch.setattr(testee, 'read_keydefs_and_stuff', mock_read)
    monkeypatch.setattr(testee, '_translate_keyname', mock_translate)
    assert testee.build_data(settnames, page) == ({}, {})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n")
    monkeypatch.setattr(testee, 'names2filenames', mock_names_2)
    assert testee.build_data(settnames, page) == ({}, {'actions': {}, 'descriptions': {},
                                                       'olddescs': {'x': 'y'}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n"
            "called read_keydefs_and_stuff with args ('',)\n")
    monkeypatch.setattr(testee, 'names2filenames', mock_names_3)
    assert testee.build_data(settnames, page) == ({}, {'actions': {}, 'descriptions': {},
                                                       'olddescs': {'x': 'y'}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n"
            "called read_keydefs_and_stuff with args ('fnamekb',)\n")
    monkeypatch.setattr(testee, 'names2filenames', mock_names_4)
    assert testee.build_data(settnames, page) == ({}, {'actions': {}, 'descriptions': {},
                                                       'olddescs': {'x': 'y'}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n"
            "called read_keydefs_and_stuff with args ('fnamekb',)\n")
    monkeypatch.setattr(testee, 'read_keydefs_and_stuff', mock_read_2)
    assert testee.build_data(settnames, page) == (
            {1: ('x', '', 'ccc', 'aaa', ''), 2: ('y', 'C', 'ddd', 'bbb', 'descy')},
            {'actions': {'xxx': ['ccc', 'aaa'], 'yyy': ['ddd', 'bbb']},
             'descriptions': {'xxx': '', 'yyy': 'descy'}, 'olddescs': {'x': 'y'}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n"
            "called read_keydefs_and_stuff with args ('fnamekb',)\n"
            "called _translate_keyname with arg x\n"
            "called _translate_keyname with arg y\n")
    return
    # de showinfo parameter is vervallenO
    # assert testee.build_data(settnames, page, showinfo=False) == (
    #         {1: ('x', '', 'ccc', 'aaa', ''), 2: ('y', 'C', 'ddd', 'bbb', 'descy')},
    #         {'actions': {'xxx': ['ccc', 'aaa'], 'yyy': ['ddd', 'bbb']},
    #          'descriptions': {'xxx': '', 'yyy': 'descy'},
    #                                                    'olddescs': {'x': 'y'}})
    # assert capsys.readouterr().out == (
    #         f"called names2filenames with args ('settnames', {page}, False)\n"
    #         "called read_keydefs_and_stuff with args ('fnamekb',)\n"
    #         "called dml.read_data with args ('fnamedesc', {'xxx': '', 'yyy': 'descy'})\n"
    #         "called _translate_keyname with arg x\n"
    #         "called _translate_keyname with arg y\n")
    # evenals het tonen van de CompletDialog
    # assert testee.build_data(settnames, page) == (
    #         {1: ('x', '', 'ccc', 'aaa', ''), 2: ('y', 'C', 'ddd', 'bbb', 'descy')},
    #         {'actions': {'xxx': ['ccc', 'aaa'], 'yyy': ['ddd', 'bbb']},
    #          'descriptions': {'xxx': '', 'yyy': 'descy'}})
    # assert page.dialog_data == {'desc': 'dict'}
    # # stand van page vóór de aanroep van de dialoog terugzetten t,b.v. assert statement
    # page = types.SimpleNamespace(dialog_data={'descdict': {'desc': 'dict'},
    #                                           'actions': {'xxx': ['ccc', 'aaa'],
    #                                                       'yyy': ['ddd', 'bbb']},
    #                                                    'olddescs': {'x': 'y'}})
    # assert capsys.readouterr().out == (
    #         f"called names2filenames with args ('settnames', namespace(), True)\n"
    #         "called read_keydefs_and_stuff with args ('fnamekb',)\n"
    #         "called dml.read_data with args ('fnamedesc', {'xxx': '', 'yyy': 'descy'})\n"
    #         f"called gui.show_dialog with args ({page}, {testee.AccelCompleteDialog})\n"
    #         "called _translate_keyname with arg x\n"
    #         "called _translate_keyname with arg y\n")
    # monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
    # assert testee.build_data(settnames, page) == (
    #         {1: ('x', '', 'ccc', 'aaa', ''), 2: ('y', 'C', 'ddd', 'bbb', 'descy')},
    #         {'actions': {'xxx': ['ccc', 'aaa'], 'yyy': ['ddd', 'bbb']},
    #          'descriptions': {'xxx': '', 'yyy': 'descy'},
    #                                                    'olddescs': {'x': 'y'}})
    # assert page.dialog_data == {'desc': 'dict'}
    # # stand van page vóór de aanroep van de dialoog terugzetten t,b.v. assert statement
    # page = types.SimpleNamespace(dialog_data={'descdict': {'desc': 'dict'},
    #                                           'actions': {'xxx': ['ccc', 'aaa'],
    #                                                       'yyy': ['ddd', 'bbb']},
    #                                                    'olddescs': {'x': 'y'}})
    # assert capsys.readouterr().out == (
    #         f"called names2filenames with args ('settnames', {page}, True)\n"
    #         "called read_keydefs_and_stuff with args ('fnamekb',)\n"
    #         "called dml.read_data with args ('fnamedesc', {'xxx': '', 'yyy': 'descy'})\n"
    #         f"called gui.show_dialog with args ({page}, {testee.AccelCompleteDialog})\n"
    #         "called _translate_keyname with arg x\n"
    #         "called _translate_keyname with arg y\n")
    # monkeypatch.setattr(testee, 'show_dialog', mock_show_3)
    # assert testee.build_data(settnames, page) == (
    #         {1: ('x', '', 'ccc', 'aaa', 'descx'), 2: ('y', 'C', 'ddd', 'bbb', 'descy')},
    #         {'actions': {'xxx': ['ccc', 'aaa'], 'yyy': ['ddd', 'bbb']},
    #          'descriptions': {'xxx': 'descx', 'yyy': 'descy'},
    #                                                    'olddescs': {'x': 'y'}})
    # assert page.dialog_data == {'ccc/aaa': 'descx'}
    # # stand van page vóór de aanroep van de dialoog terugzetten t,b.v. assert statement
    # page = types.SimpleNamespace(dialog_data={'descdict': {'desc': 'dict'},
    #                                           'actions': {'xxx': ['ccc', 'aaa'],
    #                                                       'yyy': ['ddd', 'bbb']}})
    # assert capsys.readouterr().out == (
    #         f"called names2filenames with args ('settnames', {page}, True)\n"
    #         "called read_keydefs_and_stuff with args ('fnamekb',)\n"
    #         "called dml.read_data with args ('fnamedesc', {'xxx': '', 'yyy': 'descy'})\n"
    #         f"called gui.show_dialog with args ({page}, {testee.AccelCompleteDialog})\n"
    #         "called dml.write_data with args ('fnamedesc', {'xxx': 'descx', 'yyy': 'descy'})\n"
    #         "called _translate_keyname with arg x\n"
    #         "called _translate_keyname with arg y\n")


def test_compare_descriptions():
    """unittest for gtkaccel_keys.compare_descriptions
    """
    cmddict = {'x': 'y', 'a': 'b', 'p': '', 'g': 'h'}
    olddescs = {'x': 'y', 'a': 'c', 'p':'q'}
    testee.compare_descriptions(cmddict, olddescs) == ({'x': 'y', 'a': 'b', 'p': 'q', 'g': 'h'},
                                                       {'a': 'c'})


def test_names2filenames(monkeypatch, capsys):
    """unittest for gtkaccel_keys.names2filenames
    """
    def mock_get_file_to_save(*args, **kwargs):
        print('called testee.gui.get_file_to_save with args', args, kwargs)
        return ''
    def mock_get_file_to_open(*args, **kwargs):
        print('called testee.gui.get_file_to_open with args', args, kwargs)
        return ''
    def mock_get_file_to_open_2(*args, **kwargs):
        print('called testee.gui.get_file_to_open with args', args, kwargs)
        return 'xxx.json'
    monkeypatch.setattr(testee, 'get_file_to_save', mock_get_file_to_save)
    monkeypatch.setattr(testee, 'get_file_to_open', mock_get_file_to_open)
    monkeypatch.setattr(testee, 'FDESC', ("kbfile", "descfile"))
    monkeypatch.setattr(testee.os.path, 'dirname', lambda *x: 'fileroot')
    settnames = ('kbfname', 'descfname')
    page = types.SimpleNamespace(gui='gui', settings={'extra': {}}, captions={'C_SELFIL': 'selfil'})
    assert testee.names2filenames(settnames, page, False) == ('', '')
    assert capsys.readouterr().out == ""
    assert testee.names2filenames(settnames, page, True) == ('', '')
    assert capsys.readouterr().out == ("called testee.gui.get_file_to_save with args ('gui',)"
                                       " {'oms': 'selfil - kbfile', 'start': 'fileroot'}\n")
    page.settings = {'descfname': 'descfpath', 'extra': {}}
    assert testee.names2filenames(settnames, page, False) == ('', '')
    assert capsys.readouterr().out == ""
    assert testee.names2filenames(settnames, page, True) == ('', '')
    assert capsys.readouterr().out == ("called testee.gui.get_file_to_save with args ('gui',)"
                                       " {'oms': 'selfil - kbfile', 'start': 'fileroot'}\n")
    page.settings = {'kbfname': 'kbfpath', 'extra': {}}
    assert testee.names2filenames(settnames, page, False) == ('kbfpath', '')
    assert capsys.readouterr().out == ""
    assert testee.names2filenames(settnames, page, True) == ('', '')
    assert capsys.readouterr().out == ("called testee.gui.get_file_to_open with args ('gui',)"
                                       " {'oms': 'selfil - kbfile', 'start': 'kbfpath'}\n")
    page.settings = {'kbfname': 'kbfpath', 'descfname': 'descfpath', 'extra': {}}
    assert testee.names2filenames(settnames, page, False) == ('kbfpath', 'descfpath')
    assert capsys.readouterr().out == ""
    assert testee.names2filenames(settnames, page, True) == ('', '')
    assert capsys.readouterr().out == ("called testee.gui.get_file_to_open with args ('gui',)"
                                       " {'oms': 'selfil - kbfile', 'start': 'kbfpath'}\n")

    monkeypatch.setattr(testee, 'get_file_to_open', mock_get_file_to_open_2)
    page.settings = {'extra': {}}
    assert testee.names2filenames(settnames, page, False) == ('', '')
    assert capsys.readouterr().out == ""
    assert testee.names2filenames(settnames, page, True) == ('', '')
    assert capsys.readouterr().out == ("called testee.gui.get_file_to_save with args ('gui',)"
                                       " {'oms': 'selfil - kbfile', 'start': 'fileroot'}\n")
    page.settings = {'descfname': 'descfpath', 'extra': {}}
    assert testee.names2filenames(settnames, page, False) == ('', '')
    assert capsys.readouterr().out == ""
    assert testee.names2filenames(settnames, page, True) == ('', '')
    assert capsys.readouterr().out == ("called testee.gui.get_file_to_save with args ('gui',)"
                                       " {'oms': 'selfil - kbfile', 'start': 'fileroot'}\n")
    page.settings = {'kbfname': 'kbfpath', 'extra': {}}
    assert testee.names2filenames(settnames, page, False) == ('kbfpath', '')
    assert capsys.readouterr().out == ""
    assert testee.names2filenames(settnames, page, True) == ('xxx.json', '')
    assert capsys.readouterr().out == ("called testee.gui.get_file_to_open with args ('gui',)"
                                       " {'oms': 'selfil - kbfile', 'start': 'kbfpath'}\n"
                                       "called testee.gui.get_file_to_save with args ('gui',)"
                                       " {'oms': 'selfil - descfile', 'start': 'fileroot'}\n")
    page.settings = {'kbfname': 'kbfpath', 'descfname': 'descfpath', 'extra': {}}
    assert testee.names2filenames(settnames, page, False) == ('kbfpath', 'descfpath')
    assert capsys.readouterr().out == ""
    assert testee.names2filenames(settnames, page, True) == ('xxx.json', 'xxx.json')
    assert capsys.readouterr().out == ("called testee.gui.get_file_to_open with args ('gui',)"
                                       " {'oms': 'selfil - kbfile', 'start': 'kbfpath'}\n"
                                       "called testee.gui.get_file_to_open with args ('gui',)"
                                       " {'oms': 'selfil - descfile', 'start': 'descfpath'}\n")


def test_add_extra_attributes():
    """unittest for gtkaccel_keys.add_extra_attributes
    """
    win = types.SimpleNamespace(keylist=[],
                                otherstuff={'contexts': 'clist', 'actionscontext': 'adict',
                                            'actions': 'alist', 'descriptions': 'descs',
                                            'othercontext': 'odict', 'otherkeys': 'okeys'})
    testee.add_extra_attributes(win)
    assert win.keylist == ['Num0', 'Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Num6', 'Num7', 'Num8',
                           'Num9', '>', '<']
    assert win.contextslist == 'clist'
    assert win.contextactionsdict == 'adict'
    assert win.actionslist == 'alist'
    assert win.descriptions == 'descs'
    assert not hasattr(win, 'otherslist')
    assert not hasattr(win, 'othersdict')
    assert not hasattr(win, 'otherskeys')

    win = types.SimpleNamespace(keylist=[],
                                otherstuff={'contexts': 'clist', 'actionscontext': 'adict',
                                            'actions': 'alist', 'descriptions': 'descs',
                                            'others': 'olist',
                                            'othercontext': 'odict', 'otherkeys': 'okeys'})
    testee.add_extra_attributes(win)
    assert win.keylist == ['Num0', 'Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Num6', 'Num7', 'Num8',
                           'Num9', '>', '<']
    assert win.contextslist == 'clist'
    assert win.contextactionsdict == 'adict'
    assert win.actionslist == 'alist'
    assert win.descriptions == 'descs'
    assert win.otherslist == 'olist'
    assert win.othersdict == 'odict'
    assert win.otherskeys == 'okeys'
