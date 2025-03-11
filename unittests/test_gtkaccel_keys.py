"""unittests for ./editor/plugins/gtkaccel_keys.py
"""
import types
from editor.plugins import gtkaccel_keys as testee


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
    def mock_read_data(*args):
        print('called dml.read_data with args', args)
        return 'message from read_data', {}
    def mock_read_data_2(*args):
        print('called dml.read_data with args', args)
        return '', {'desc': 'dict'}
    def mock_show(*args):
        print('called gui.show_dialog with args', args)
        args[0].dialog_data = {'desc': 'dict'}
        return False
    def mock_show_2(*args):
        print('called gui.show_dialog with args', args)
        args[0].dialog_data = {'desc': 'dict'}
        return True
    def mock_show_3(*args):
        print('called gui.show_dialog with args', args)
        args[0].dialog_data = {'ccc/aaa': 'descx'}
        return True
    def mock_write_data(*args):
        print('called dml.write_data with args', args)
    def mock_translate(key):
        print(f'called _translate_keyname with arg {key}')
        return key
    settnames = 'settnames'
    page = types.SimpleNamespace()
    monkeypatch.setattr(testee, 'names2filenames', mock_names)
    monkeypatch.setattr(testee, 'read_keydefs_and_stuff', mock_read)
    monkeypatch.setattr(testee.dml, 'read_data', mock_read_data)
    monkeypatch.setattr(testee, 'show_dialog', mock_show)
    monkeypatch.setattr(testee.dml, 'write_data', mock_write_data)
    monkeypatch.setattr(testee, '_translate_keyname', mock_translate)
    assert testee.build_data(settnames, page) == ({}, {})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n")
    monkeypatch.setattr(testee, 'names2filenames', mock_names_2)
    assert testee.build_data(settnames, page) == ({}, {'actions': {}, 'descriptions': {}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n"
            "called read_keydefs_and_stuff with args ('',)\n"
            "called dml.read_data with args ('fnamedesc', {})\n"
            "message from read_data\n")
    monkeypatch.setattr(testee, 'names2filenames', mock_names_3)
    assert testee.build_data(settnames, page) == ({}, {'actions': {}, 'descriptions': {}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n"
            "called read_keydefs_and_stuff with args ('fnamekb',)\n")
    monkeypatch.setattr(testee, 'names2filenames', mock_names_4)
    assert testee.build_data(settnames, page) == ({}, {'actions': {}, 'descriptions': {}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n"
            "called read_keydefs_and_stuff with args ('fnamekb',)\n"
            "called dml.read_data with args ('fnamedesc', {})\n"
            "message from read_data\n")
    monkeypatch.setattr(testee, 'read_keydefs_and_stuff', mock_read_2)
    assert testee.build_data(settnames, page) == (
            {1: ('x', '', 'ccc', 'aaa', ''), 2: ('y', 'C', 'ddd', 'bbb', 'descy')},
            {'actions': {'xxx': ['ccc', 'aaa'], 'yyy': ['ddd', 'bbb']},
             'descriptions': {'xxx': '', 'yyy': 'descy'}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n"
            "called read_keydefs_and_stuff with args ('fnamekb',)\n"
            "called dml.read_data with args ('fnamedesc', {'xxx': '', 'yyy': 'descy'})\n"
            "message from read_data\n"
            "called _translate_keyname with arg x\n"
            "called _translate_keyname with arg y\n")
    monkeypatch.setattr(testee.dml, 'read_data', mock_read_data_2)
    assert testee.build_data(settnames, page, showinfo=False) == (
            {1: ('x', '', 'ccc', 'aaa', ''), 2: ('y', 'C', 'ddd', 'bbb', 'descy')},
            {'actions': {'xxx': ['ccc', 'aaa'], 'yyy': ['ddd', 'bbb']},
             'descriptions': {'xxx': '', 'yyy': 'descy'}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, False)\n"
            "called read_keydefs_and_stuff with args ('fnamekb',)\n"
            "called dml.read_data with args ('fnamedesc', {'xxx': '', 'yyy': 'descy'})\n"
            "called _translate_keyname with arg x\n"
            "called _translate_keyname with arg y\n")
    assert testee.build_data(settnames, page) == (
            {1: ('x', '', 'ccc', 'aaa', ''), 2: ('y', 'C', 'ddd', 'bbb', 'descy')},
            {'actions': {'xxx': ['ccc', 'aaa'], 'yyy': ['ddd', 'bbb']},
             'descriptions': {'xxx': '', 'yyy': 'descy'}})
    assert page.dialog_data == {'desc': 'dict'}
    # stand van page vóór de aanroep van de dialoog terugzetten t,b.v. assert statement
    page = types.SimpleNamespace(dialog_data={'descdict': {'desc': 'dict'},
                                              'actions': {'xxx': ['ccc', 'aaa'],
                                                          'yyy': ['ddd', 'bbb']}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', namespace(), True)\n"
            "called read_keydefs_and_stuff with args ('fnamekb',)\n"
            "called dml.read_data with args ('fnamedesc', {'xxx': '', 'yyy': 'descy'})\n"
            f"called gui.show_dialog with args ({page}, {testee.AccelCompleteDialog})\n"
            "called _translate_keyname with arg x\n"
            "called _translate_keyname with arg y\n")
    monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
    assert testee.build_data(settnames, page) == (
            {1: ('x', '', 'ccc', 'aaa', ''), 2: ('y', 'C', 'ddd', 'bbb', 'descy')},
            {'actions': {'xxx': ['ccc', 'aaa'], 'yyy': ['ddd', 'bbb']},
             'descriptions': {'xxx': '', 'yyy': 'descy'}})
    assert page.dialog_data == {'desc': 'dict'}
    # stand van page vóór de aanroep van de dialoog terugzetten t,b.v. assert statement
    page = types.SimpleNamespace(dialog_data={'descdict': {'desc': 'dict'},
                                              'actions': {'xxx': ['ccc', 'aaa'],
                                                          'yyy': ['ddd', 'bbb']}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n"
            "called read_keydefs_and_stuff with args ('fnamekb',)\n"
            "called dml.read_data with args ('fnamedesc', {'xxx': '', 'yyy': 'descy'})\n"
            f"called gui.show_dialog with args ({page}, {testee.AccelCompleteDialog})\n"
            "called _translate_keyname with arg x\n"
            "called _translate_keyname with arg y\n")
    monkeypatch.setattr(testee, 'show_dialog', mock_show_3)
    assert testee.build_data(settnames, page) == (
            {1: ('x', '', 'ccc', 'aaa', 'descx'), 2: ('y', 'C', 'ddd', 'bbb', 'descy')},
            {'actions': {'xxx': ['ccc', 'aaa'], 'yyy': ['ddd', 'bbb']},
             'descriptions': {'xxx': 'descx', 'yyy': 'descy'}})
    assert page.dialog_data == {'ccc/aaa': 'descx'}
    # stand van page vóór de aanroep van de dialoog terugzetten t,b.v. assert statement
    page = types.SimpleNamespace(dialog_data={'descdict': {'desc': 'dict'},
                                              'actions': {'xxx': ['ccc', 'aaa'],
                                                          'yyy': ['ddd', 'bbb']}})
    assert capsys.readouterr().out == (
            f"called names2filenames with args ('settnames', {page}, True)\n"
            "called read_keydefs_and_stuff with args ('fnamekb',)\n"
            "called dml.read_data with args ('fnamedesc', {'xxx': '', 'yyy': 'descy'})\n"
            f"called gui.show_dialog with args ({page}, {testee.AccelCompleteDialog})\n"
            "called dml.write_data with args ('fnamedesc', {'xxx': 'descx', 'yyy': 'descy'})\n"
            "called _translate_keyname with arg x\n"
            "called _translate_keyname with arg y\n")


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
