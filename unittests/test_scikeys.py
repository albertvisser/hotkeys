"""unittests for ./plugin_examples/scikeys.py
"""
import types
from plugin_examples import scikeys as testee


def test_translate_keyname():
    """unittest for scikeys._translate_keyname
    """
    convert = {'Equal': '=', 'Escape': 'Esc', 'Delete': 'Del', 'Return': 'Enter',
               'BackSpace': 'Backspace', 'PageUp': 'PgUp', 'PageDown': 'PgDn', 'space': 'Space',
               'Keypad*': 'Num*', 'Keypad+': 'Num+', 'Keypad-': 'Num-', 'Keypad/': 'Num/', }
    for x, y in convert.items():
        assert testee._translate_keyname(x) == y


def test_nicefy_props():
    """unittest for scikeys.nicefy_props
    """
    assert testee.nicefy_props('Anything') == ('Anything', '')
    assert testee.nicefy_props('Ctrl+Alt+Shift+Anything') == ('Anything', 'CAS')
    assert testee.nicefy_props('Shift+Alt+Ctrl+KeypadPlus') == ('Keypad+', 'CAS')


def test_nicefy_source():
    """unittest for scikeys.nicefy_source
    """
    assert testee.nicefy_source('Anything') == ('Anything', '')
    assert testee.nicefy_source('<control><alt><shift>Anything') == ('Anything', 'CAS')
    assert testee.nicefy_source('<shift><alt><control>Anything') == ('Anything', 'CAS')


def test_read_commands(tmp_path):
    """unittest for scikeys.read_commands
    """
    path = tmp_path / 'cmds.html'
    path.write_text('')
    assert testee.read_commands(str(path)) == ({}, {})

    path.write_text("<html><body><table></table><table></table></body></html>")
    assert testee.read_commands(str(path)) == ({}, {})

    path.write_text("<html><body><table><thead><tr><td>hx</td><td>hy</td></tr></thead>"
                    "<tr><td>xx</td><td>yy</td></tr></table>"
                    "<table><thead><tr><td>hx</td><td>hy</td><td>hz</td></tr></thead>"
                    "<tr><td>aa</td><td>bb</td><td>cc</td></tr></table></body></html>")
    assert testee.read_commands(str(path)) == ({'0001': ('xx', 'yy')}, {'aa': ('bb', 'cc')})


def test_read_docs(monkeypatch, capsys, tmp_path):
    """unittest for scikeys.read_docs
    """
    def mock_nicefy(arg):
        "stub"
        print(f"called nicefy_props with arg '{arg}'")
        return arg[0], arg[1:]
    monkeypatch.setattr(testee, 'nicefy_props', mock_nicefy)
    path = tmp_path / 'docs.html'
    path.write_text('')
    assert testee.read_docs(str(path)) == []
    assert capsys.readouterr().out == ""

    path.write_text("<html><body><table></table></body></html>")
    assert testee.read_docs(str(path)) == []
    assert capsys.readouterr().out == ""

    path.write_text("<html><body><table><thead><tr><th>hx</th><th>hy</th><th>hz</th></tr></thead>"
                    "<tr><td>xx</td><td>yy</td><td>zz</td></tr></table>"
                    '<table summary="Keyboard commands">'
                    "<thead><tr><th>hx</th><th>hy</th><th>hz</th></tr></thead>"
                    "<tr><td>xx</td><td>yy</td><td>zz</td></tr></table></body></html>")
    assert testee.read_docs(str(path)) == [('y', 'y', 'xx')]
    assert capsys.readouterr().out == "called nicefy_props with arg 'yy'\n"


def test_read_symbols(tmp_path):
    """unittest for scikeys.read_symbols
    """
    fname = tmp_path / 'symbolsfile'
    fname.write_text('')
    assert testee.read_symbols(fname) == ({}, {})
    fname.write_text('{"IDM_xxx\n};\nstatic IFaceConstant ifaceConstants[] = {\n'
                     '    {"IDM_XXX",1},\n    {"IDM_YYY",2},\n    {"OTHER",0}\n};\n'
                     'static IFaceFunction ifaceFunctions[] = {\n'
                     '	{"Xxx", 1000, restype, {argtypes}},\n'
                     '	{"Yyy", 1001, restype, {argtypes}}\n};\n')
    assert testee.read_symbols(fname) == ({'1': 'IDM_XXX', '2': 'IDM_YYY'},
                                          {' 1000': 'Xxx', ' 1001': 'Yyy'})


def test_read_menu_gtk(monkeypatch, capsys, tmp_path):
    """unittest for scikeys.read_menu_gtk
    """
    def mock_nicefy(arg):
        print(f"called nicefy_source with arg `{arg}`")
        if '>' in arg:
            mods, key = arg.rsplit('>')
        else:
            mods, key = '', arg
        return key.strip('" '), mods.lstrip(' <"')
    monkeypatch.setattr(testee, 'nicefy_source', mock_nicefy)
    fname = tmp_path / 'gtkmenufile'
    fname.write_text(
            '\nother stuff\n# comment\n'
            'SciTEItemFactoryEntry menuItems[] = {\n'
            '    {"/View/Full Scree_n", "F11", menuSig, IDM_FULLSCREEN, "<CheckItem>"},\n'
            '    };\n'
            'SciTEItemFactoryEntry menuItemsOptions[] = {\n'
            '    {"/Options/_Wrap", "", menuSig, IDM_WRAP, "<CheckItem>"},\n'
            '    };\n'
            'SciTEItemFactoryEntry menuItemsBuffer[] = {\n'
            '    {"/Buffers/sep2", NULL, NULL, 0, "<Separator>"},\n'
            '    {"/Buffers/Buffer0", "<alt>1", menuSig, bufferCmdID + 0, "<RadioItem>"},\n'
            '    };\n'
            'SciTEItemFactoryEntry menuItemsHelp[] = {\n'
            '    {"/_Help", NULL, NULL, 0, "<Branch>"},\n'
            '    {"/Help/_Help", "F1", menuSig, IDM_HELP, 0},\n'
            '    };\n'
            'more other stuff')
    assert testee.read_menu_gtk(fname) == [('F11', '', 'IDM_FULLSCREEN'),
                                           ('1', 'alt', 'IDM_BUFFER0'),
                                           ('F1', '', 'IDM_HELP')]
    assert capsys.readouterr().out == ('called nicefy_source with arg ` "F11"`\n'
                                       'called nicefy_source with arg ` "<alt>1"`\n'
                                       'called nicefy_source with arg ` "F1"`\n')


def test_read_menu_win(monkeypatch, tmp_path):
    """unittest for scikeys.read_menu_win
    """
    monkeypatch.setattr(testee, 'nicefy_props', lambda *x: ('qq', 'rr'))
    temp_fname = tmp_path / 'winmenufile'
    temp_fname.write_text('\n xxx\nMENUITEM  "xxx"  yyy\n MENUITEM SEPARATOR  \n'
                          '   MENUITEM  "aaa\tbbb"   ccc\n')
    assert testee.read_menu_win(temp_fname) == [('qq', 'rr', 'ccc')]


class TestPropertiesFile:
    """unittest for scikeys.PropertiesFile
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for scikeys.PropertiesFile object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called PropertiesFile.__init__ with args', args)
        monkeypatch.setattr(testee.PropertiesFile, '__init__', mock_init)
        testobj = testee.PropertiesFile()
        assert capsys.readouterr().out == 'called PropertiesFile.__init__ with args ()\n'
        return testobj

    def test_init(self):
        """unittest for PropertiesFile.__init__
        """
        testobj = testee.PropertiesFile('fnaam')
        assert testobj._default_platform == "*"
        assert testobj.properties == {}
        assert testobj._var_start == '$('
        assert testobj._var_end == ')'
        assert not testobj._continue_assignment
        assert testobj._platform == testobj._default_platform
        assert testobj._fnaam == 'fnaam'
        assert testobj._acceptable_combinations == (('PLAT_WIN', 'PLAT_WIN_GTK'),
                                                    ('PLAT_GTK', 'PLAT_WIN_GTK'),
                                                    ('PLAT_GTK', 'PLAT_UNIX'),
                                                    ('PLAT_MAC', 'PLAT_UNIX'))

    def test_determine_platform(self, monkeypatch, capsys):
        """unittest for PropertiesFile._determine_platform
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._default_platform = 'x'
        testobj._platform = 'y'
        assert testobj._determine_platform('\n') == ('\n', False)
        assert testobj._platform == 'y'
        assert testobj._determine_platform('if test\n') == ('if test\n', True)
        assert testobj._platform == 'x'
        assert testobj._determine_platform('if PLAT_test\n') == ('if PLAT_test\n', True)
        assert testobj._platform == 'PLAT_test\n'

    def test_determine_continuation(self, monkeypatch, capsys):
        """unittest for PropertiesFile._determine_continuation
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj._determine_continuation('yyy\\', 'xxx') == "xxxyyy"
        assert testobj._continue_assignment
        assert testobj._determine_continuation('yyy\n', 'xxx') == "xxxyyy\n"
        assert not testobj._continue_assignment
        assert testobj._determine_continuation('yyy', 'xxx') == "xxxyyy"
        assert not testobj._continue_assignment

    def test_read_props(self, monkeypatch, capsys, tmp_path):
        """unittest for PropertiesFile.read_props
        """
        def mock_plat(line):
            print(f"called PropertiesFile._determine_platform with arg '{line}'")
            return (line, True)
        def mock_plat_2(line):
            print(f"called PropertiesFile._determine_platform with arg '{line}'")
            return (line, False)
        def mock_cont(*args):
            print("called PropertiesFile._determine_continuation with args", args)
            return args[0]
        def mock_log(*args):
            print('called log with args', args)
        # def mock_subst(*args):
        #     print(f"called PropertiesFile._do_substitutions with args", args)
        #     return [(args[0], '*', args[1])]
        # def mock_subst_2(*args):
        #     print(f"called PropertiesFile._do_substitutions with args", args)
        #     return [[]]
        monkeypatch.setattr(testee, 'log', mock_log)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._fnaam = tmp_path / 'propfile'
        testobj._fnaam.touch()
        testobj._platform = 'plat'
        testobj.properties = testee.collections.defaultdict(dict)
        testobj._var_start, testobj._var_end = '$(', ')'
        testobj._continue_assignment = True  # simulate what determine_continuation does
        testobj._determine_platform = mock_plat
        testobj._determine_continuation = mock_cont
        # testobj._do_substitutions = mock_subst
        testobj.read_props()
        assert not testobj.properties
        assert capsys.readouterr().out == ""
        testobj._fnaam.write_text('#xxx\n\n')
        testobj.read_props()
        assert not testobj.properties
        assert capsys.readouterr().out == ""
        testobj._fnaam.write_text('xxx\n')
        testobj.read_props()
        assert not testobj.properties
        assert capsys.readouterr().out == (
                "called PropertiesFile._determine_platform with arg 'xxx'\n")
        testobj._determine_platform = mock_plat_2
        testobj.read_props()
        assert not testobj.properties
        assert capsys.readouterr().out == (
                "called PropertiesFile._determine_platform with arg 'xxx'\n"
                "called PropertiesFile._determine_continuation with args ('xxx', '')\n")
        testobj._continue_assignment = False  # simulate what determine_continuation does
        testobj._fnaam.write_text('xxx=yyy\n')
        testobj.read_props()
        assert testobj.properties == {'xxx': {'plat': 'yyy'}}
        assert capsys.readouterr().out == (
                "called PropertiesFile._determine_platform with arg 'xxx=yyy'\n"
                "called PropertiesFile._determine_continuation with args ('xxx=yyy', '')\n")
        testobj.properties.clear()
        testobj._fnaam.write_text('x$(xx=yyy\n')
        testobj.read_props()
        assert testobj.properties == {'x$(xx': {'plat': 'yyy'}}
        assert capsys.readouterr().out == (
                "called PropertiesFile._determine_platform with arg 'x$(xx=yyy'\n"
                "called PropertiesFile._determine_continuation with args ('x$(xx=yyy', '')\n")
        testobj.properties.clear()
        testobj._fnaam.write_text('xxx=y$(yy\n')
        testobj.read_props()
        assert testobj.properties == {'xxx': {'plat': 'y$(yy'}}
        assert capsys.readouterr().out == (
                "called PropertiesFile._determine_platform with arg 'xxx=y$(yy'\n"
                "called PropertiesFile._determine_continuation with args ('xxx=y$(yy', '')\n")
                # "called PropertiesFile._do_substitutions with args ('xxx', 'y$(yy')\n")
        # testobj._do_substitutions = mock_subst_2
        # testobj.properties.clear()
        # testobj._fnaam.write_text('xxx=y$(yy\n')
        # testobj.read_props()
        # assert testobj.properties == {}
        # assert capsys.readouterr().out == (
        #         "called PropertiesFile._determine_platform with arg 'xxx=y$(yy'\n"
        #         "called PropertiesFile._determine_continuation with args ('xxx=y$(yy', '')\n"
        #         "called PropertiesFile._do_substitutions with args ('xxx', 'y$(yy')\n")
        testobj.properties.clear()
        testobj._fnaam.write_text('xxx yyy\n')
        testobj.read_props()
        assert testobj.properties == {}
        assert capsys.readouterr().out == (
                "called PropertiesFile._determine_platform with arg 'xxx yyy'\n"
                "called PropertiesFile._determine_continuation with args ('xxx yyy', '')\n"
                'called log with args'
                ' ("propfile                  Not an assignment: \'xxx yyy\'",)\n')

    def test_get_keydef_props(self, monkeypatch, capsys):
        """unittest for PropertiesFile.get_keydef_props
        """
        def mock_nicefy(arg):
            "stub"
            print(f"called nicefy_props with arg '{arg}'")
            return arg[0], arg[1:]
        def mock_build(self):
            self.data.append(['called', '_build_toolcommand_data'])
        def mock_process_manu(self, data):
            data.append(['called', '_process_manual_toolcommand_shortcuts'])
        def mock_process_auto(self, data):
            data.append(['called', '_process_automatic_toolcommand_shortcuts'])
        monkeypatch.setattr(testee, 'nicefy_props', mock_nicefy)
        monkeypatch.setattr(testee.PropertiesFile, '_build_toolcommand_data', mock_build)
        monkeypatch.setattr(testee.PropertiesFile, '_process_manual_toolcommand_shortcuts',
                            mock_process_manu)
        monkeypatch.setattr(testee.PropertiesFile, '_process_automatic_toolcommand_shortcuts',
                            mock_process_auto)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.data = []
        testobj.properties = {'user.shortcuts': {}, 'menu.language': {}}
        testobj.get_keydef_props()
        assert testobj.data == [['called', '_build_toolcommand_data'],
                                ('called', '_process_manual_toolcommand_shortcuts'),
                                ('called', '_process_automatic_toolcommand_shortcuts')]
        assert capsys.readouterr().out == ""
        testobj.properties = {'user.shortcuts': {'*': 'aaa|bbb|ccc|ddd'},
                              'menu.language': {'*': 'xxx|yyy|||zzz|qqq|rrr'}}
        testobj.get_keydef_props()
        assert testobj.data == [('a', 'aa', '*', '*', 'bbb', ''),
                                ('c', 'cc', '*', '*', 'ddd', ''),
                                ('q', 'qq', '*', '*', 'to_zzz', 'Show as  (*.zzz)'),
                                ['called', '_build_toolcommand_data'],
                                ('called', '_process_manual_toolcommand_shortcuts'),
                                ('called', '_process_automatic_toolcommand_shortcuts')]
        assert capsys.readouterr().out == ("called nicefy_props with arg 'aaa'\n"
                                           "called nicefy_props with arg 'ccc'\n"
                                           "called nicefy_props with arg 'qqq'\n")

    def test_build_toolcommand_data(self, monkeypatch, capsys):
        """unittest for PropertiesFile.build_toolcommand_data
        """
        def mock_nicefy(arg):
            "stub"
            print(f"called nicefy_props with arg '{arg}'")
            return reversed(arg.split('+') if '+' in arg else ('', arg))
        monkeypatch.setattr(testee, 'nicefy_props', mock_nicefy)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.data = []
        testobj.tooldata = {}
        testobj.properties = {}
        testobj._build_toolcommand_data()
        assert testobj.data == []
        assert testobj.tooldata == {}
        assert capsys.readouterr().out == ("")
        testobj.properties = {'x': 'y'}
        testobj._build_toolcommand_data()
        assert testobj.data == []
        assert testobj.tooldata == {}
        assert capsys.readouterr().out == ("")
        testobj.tooldata = {'commands': testee.collections.defaultdict(list),
                            'shortcuts': testee.collections.defaultdict(list),
                            'descriptions': testee.collections.defaultdict(list)}
        testobj.properties = {'command.compile.xxx*': {'*': 'compile-command'},
                              'command.compile.subsystem.xxx*': {'*': '2'},
                              'command.build.xxx*': {'*': 'build-command'},
                              'command.build.subsystem.xxx*': {'*': '2'},
                              'command.build.directory.xxx*': {'*': ''},
                              'command.clean.xxx*': {'*': 'clean-command'},
                              'command.clean.subsystem.xxx*': {'*': '2'},
                              'command.help.xxx*': {'*': 'help-command'},
                              'command.help.subsystem.xxx*': {'*': '2'},
                              'command.go.xxx*': {'*': 'go-command'},
                              'command.go.subsystem.xxx*': {'*': '2'},
                              'command.go.needs.xxx*': {'*': 'before-go'},
                              'command.go.needs.subsystem.xxx*': {'*': '2'},
                              'command.name.8.xxx* ': {'*': 'execute my command'},
                              'command.8.xxx*': {'*': 'my-command'},
                              'command.is.filter.8.xxx*': {'*': '1'},
                              'command.subsystem.8.xxx*': {'*': '2'},
                              'command.save.before.8.xxx*': {'*': '1'},
                              'command.input.8.xxx*': {'*': 'origin'},
                              'command.replace.selection.8.xxx*': {'*': '1'},
                              'command.quiet.8.xxx*': {'*': '1'},
                              'command.mode.8.xxx*': {'*': 'yyy'},
                              'command.name.9.xxx* ': {'*': 'execute my command'},
                              'command.9.xxx*': {'*': 'my-command'},
                              'command.is.filter.9.xxx*': {'*': '1'},
                              'command.subsystem.9.xxx*': {'*': '2'},
                              'command.save.before.9.xxx*': {'*': '1'},
                              'command.input.9.xxx*': {'*': 'origin'},
                              'command.replace.selection.9.xxx*': {'*': '1'},
                              'command.quiet.9.xxx*': {'*': '1'},
                              'command.mode.9.xxx*': {'*': 'yyy'},
                              'command.shortcut.9.xxx*': {'*': 'Ctrl+X'}}
        testobj._build_toolcommand_data()
        assert testobj.data == [('F7', 'Ctrl', 'xxx*', '*', 'compile-command', 'compile'),
                                ('F7', '', 'xxx*', '*', 'build-command', 'build'),
                                ('F7', 'Shift', 'xxx*', '*', 'clean-command', 'clean'),
                                ('F1', '', 'xxx*', '*', 'help-command', 'help'),
                                ('F5', '', 'xxx*', '*', 'go-command', 'go')]
        assert testobj.tooldata == {'commands': {'118': [('xxx*', '*', 'my-command')],
                                                 '119': [('xxx*', '*', 'my-command')]},
                                    'shortcuts': {'119': [('xxx*', '*', 'Ctrl+X')]},
                                    'descriptions': {'118': [('xxx* ', '*', 'execute my command')],
                                                     '119': [('xxx* ', '*', 'execute my command')]}}
        assert capsys.readouterr().out == ("called nicefy_props with arg 'Ctrl+F7'\n"
                                           "called nicefy_props with arg 'F7'\n"
                                           "called nicefy_props with arg 'Shift+F7'\n"
                                           "called nicefy_props with arg 'F1'\n"
                                           "called nicefy_props with arg 'F5'\n")

    def test_process_manual_toolcommand_shortcuts(self, monkeypatch, capsys):
        """unittest for PropertiesFile.process_manual_toolcommand_shortcuts
        """
        def mock_nicefy(arg):
            "stub"
            print(f"called nicefy_props with arg '{arg}'")
            return arg[0], arg[1:]
        monkeypatch.setattr(testee, 'nicefy_props', mock_nicefy)
        testobj = self.setup_testobj(monkeypatch, capsys)
        data = []
        testobj.tooldata = {'commands': {'x': 'y'},
                            'shortcuts': {},
                            'descriptions': {'a': 'b'}}
        testobj._process_manual_toolcommand_shortcuts(data)
        assert not data
        assert capsys.readouterr().out == ""
        testobj.tooldata = {'commands': {'x': 'y'},
                            'shortcuts': {'key': [('filetype', 'platform', 'keycombo')]},
                            'descriptions': {'a': 'b'}}
        testobj._process_manual_toolcommand_shortcuts(data)
        assert not data
        assert capsys.readouterr().out == ("")
        testobj.tooldata = {'commands': {'key': [('ftype', 'plat', 'other_command')]},
                            'shortcuts': {'key': [('filetype', 'platform', 'keycombo')]},
                            'descriptions': {'key': [('ftype', 'plat', 'not that description')]}}
        testobj._process_manual_toolcommand_shortcuts(data)
        assert not data
        assert capsys.readouterr().out == ("")
        testobj.tooldata = {'commands': {'key': [('ftype', 'plat', 'other_command'),
                                                 ('filetype', 'platform', 'command')]},
                            'shortcuts': {'key': [('filetype', 'platform', 'keycombo')]},
                            'descriptions': {'key': [('ftype', 'plat', 'not that description'),
                                                     ('filetype', 'platform', 'description')]}}
        testobj._process_manual_toolcommand_shortcuts(data)
        assert data == [['k', 'eycombo', 'filetype', 'platform', 'command', 'description']]
        assert capsys.readouterr().out == ("called nicefy_props with arg 'keycombo'\n"
                                           "called nicefy_props with arg 'keycombo'\n")
        data = [['k', 'eycombo', 'filetype', 'plat', 'command', 'description']]
        testobj._process_manual_toolcommand_shortcuts(data)
        assert data == [['k', 'eycombo', 'filetype', 'plat', 'command', 'description'],
                        ['k', 'eycombo', 'filetype', 'platform', 'command', 'description']]
        assert capsys.readouterr().out == ("called nicefy_props with arg 'keycombo'\n"
                                           "called nicefy_props with arg 'keycombo'\n")
        data = []
        testobj.tooldata = {'commands': {'key': [('filetype', 'plat', 'command')]},
                            'shortcuts': {'key': [('filetype', 'platform', 'keycombo')]},
                            'descriptions': {'key': [('filetype', 'platform', 'description')]}}
        testobj._process_manual_toolcommand_shortcuts(data)
        assert not data
        assert capsys.readouterr().out == "called nicefy_props with arg 'keycombo'\n"

    def test_process_automatic_toolcommand_shortcuts(self, monkeypatch, capsys):
        """unittest for PropertiesFile.process_automatic_toolcommand_shortcuts
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        data = []
        testobj.tooldata = {'commands': {},
                            'descriptions': {'a': 'b'}}
        testobj._process_automatic_toolcommand_shortcuts(data)
        assert not data
        testobj.tooldata = {'commands': {'k': [('ftype', 'plat', 'command')]},
                            'descriptions': {'a': 'b'}}
        testobj._process_automatic_toolcommand_shortcuts(data)
        assert not data
        testobj.tooldata = {'commands': {'key': [('ftype', 'plat', 'command')]},
                            'descriptions': {'a': 'b'}}
        testobj._process_automatic_toolcommand_shortcuts(data)
        assert data == [['y', 'C', 'ftype', 'plat', 'command', '']]
        data = []
        testobj.tooldata = {'commands': {'key': [('ftype', 'plat', 'command')]},
                            'descriptions': {'key': []}}
        testobj._process_automatic_toolcommand_shortcuts(data)
        assert not data
        testobj.tooldata = {'commands': {'key': [('ftype', 'plat', 'command')]},
                            'descriptions': {'key': [('ftyp', 'plat', 'description')]}}
        testobj._process_automatic_toolcommand_shortcuts(data)
        assert not data
        testobj.tooldata = {'commands': {'key': [('ftype', 'plat', 'command')]},
                            'descriptions': {'key': [('ftype', 'plat', 'description')]}}
        testobj._process_automatic_toolcommand_shortcuts(data)
        assert data == [['y', 'C', 'ftype', 'plat', 'command', 'description']]


def test_merge_command_dicts():
    """unittest for scikeys.merge_command_dicts
    """
    dict_from_text = {'x': ['y0', 'y1'], 'a': ['b0', 'b1']}
    dict_from_src = {'z': ('Y0', 'Y1')}
    assert testee.merge_command_dicts(dict_from_text, dict_from_src) == {'z': (('Y0', 'Y1'), ''),
                                                                         'a': ('b0', 'b1'),
                                                                         'x': ('y0', 'y1')}


def test_build_data(monkeypatch, capsys, tmp_path):
    """unittest for scikeys.build_data
    """
    class MockTarfile:
        """stub for tarfile object
        """
        def __enter__(self):
            print('called tarfile.__enter__')
            return self
        def __exit__(self, *args):
            print('called tarfile.__exit__')
            return True
        def extractall(self, path):
            print(f'called tarfileobject.extractall with arg {path}')
    def mock_open(filename):
        print(f'called tarfile.open with arg {filename}')
        return MockTarfile()
    def mock_read_commands(arg):  # -> menu_commands, internal commands initial
        print("called scikeys.read_commands with arg", arg)
        return {1: ('command-1', 'desc-1')}, {111: ('command-2', 'desc-2')}
    def mock_read_menu_gtk(arg):    # -> menu_keys
        print("called scikeys.read_menu_gtk with arg", arg)
        return [('A', 'C', 111)]
    def mock_read_menu_win(arg):    # -> menu_keys
        print("called scikeys.read_menu_win with arg", arg)
        return [('A', 'C', 111)]
    def mock_read_symbols(arg):     # all_menu_cmds, all_int_cmds
        print("called scikeys.read_symbols with arg", arg)
        return {3: ('command-3', 'desc-3')}, {104: ('command-4', 'desc-4')}
    def mock_translate(arg):
        print("called scikeys._translate_keyname with arg", arg)
        return arg[0], arg[1:]
    def mock_merge_commands(*args):
        print("called scikeys.merge_command_dicts with args", args)
        args[0].update(args[1])
        return args[0]
    def mock_read_docs(arg):
        print("called scikeys.read_docs with arg", arg)
        return [('X', 'A', 'qqq')]
    class MockPropertiesFile:
        """stub for scikeys.PropertiesFile object
        """
        def __init__(self, fname):
            print(f'called PropertiesFile.__init__ with arg {fname}')
        def read_props(self):
            print("called PropertiesFile.read_props")
        def get_keydef_props(self):
            print("called PropertiesFile.get_keydef_props")
            self.data = [('x', 'y', 'z', 'q', 'r', 's')]
    def mock_merge_keydefs(*args):
        print("called scikeys.merge_keydefs with args", args)
        return dict(enumerate(args[0] + args[1])), ['con', 'texts']
    def mock_compare(*args):
        print("called compare_and_keep with args", args)
        return {'old': 'descs'}
    monkeypatch.setattr(testee.tarfile, 'open', mock_open)
    monkeypatch.setattr(testee, 'read_commands', mock_read_commands)
    monkeypatch.setattr(testee, 'read_menu_gtk', mock_read_menu_gtk)
    monkeypatch.setattr(testee, 'read_menu_win', mock_read_menu_win)
    monkeypatch.setattr(testee, 'read_symbols', mock_read_symbols)
    monkeypatch.setattr(testee, '_translate_keyname', mock_translate)
    monkeypatch.setattr(testee, 'merge_command_dicts', mock_merge_commands)
    monkeypatch.setattr(testee, 'read_docs', mock_read_docs)
    monkeypatch.setattr(testee, 'PropertiesFile', MockPropertiesFile)
    monkeypatch.setattr(testee, 'merge_keydefs', mock_merge_keydefs)
    monkeypatch.setattr(testee, 'compare_and_keep', mock_compare)
    page = types.SimpleNamespace(settings={'SCI_CMDS': 'commands.txt', 'SCI_SRCE': 'sourceloc',
                                           'SCI_DOCS': 'docs.txt',
                                           'SCI_GLBL': str(tmp_path / 'global/glbl.properties'),
                                           'SCI_USER': str(tmp_path / 'user/user.properties')},
                                 descriptions={})
    (tmp_path / 'global').mkdir()
    (tmp_path / 'global' / 'glbl.properties').touch()
    (tmp_path / 'global' / 'SciTE.properties').touch()
    (tmp_path / 'global' / 'Embedded.properties').touch()
    (tmp_path / 'user').mkdir()
    (tmp_path / 'user' / 'user.properties').touch()
    (tmp_path / 'user' / 'userdata').touch()  # 642->639
    assert testee.build_data(page, showinfo=True) == ({
        0: (('A', ''), 'C', '*', '*', 'S', 111, ''),
        1: (('X', ''), 'A', '*', '*', 'S', '', 'qqq'),
        2: (('x', ''), 'y', 'z', 'q', 'S', 'r', 's'),
        3: (('x', ''), 'y', 'z', 'q', 'U', 'r', 's')}, {
            'menucommands': {1: ('command-1', 'desc-1'), 3: ('command-3', 'desc-3')},
            'internal_commands': {111: ('command-2', 'desc-2'), 104: ('command-4', 'desc-4')},
            'contexts': ['con', 'texts'], 'olddescs': {'old': 'descs'}})
    assert capsys.readouterr().out == (
            "called scikeys.read_commands with arg commands.txt\n"
            "called tarfile.open with arg sourceloc\n"
            "called tarfile.__enter__\n"
            "called tarfileobject.extractall with arg /tmp\n"
            "called tarfile.__exit__\n"
            "called scikeys.read_menu_gtk with arg /tmp/scite/gtk/SciTEGTK.cxx\n"
            "called scikeys.read_symbols with arg /tmp/scite/src/IFaceTable.cxx\n"
            "called scikeys._translate_keyname with arg A\n"
            "called scikeys.merge_command_dicts with args"
            " ({1: ('command-1', 'desc-1')}, {3: ('command-3', 'desc-3')})\n"
            "called scikeys.merge_command_dicts with args"
            " ({111: ('command-2', 'desc-2')}, {104: ('command-4', 'desc-4')})\n"
            "called scikeys.read_docs with arg docs.txt\n"
            "called scikeys._translate_keyname with arg X\n"
            f"called PropertiesFile.__init__ with arg {tmp_path}/global/glbl.properties\n"
            "called PropertiesFile.read_props\n"
            "called PropertiesFile.get_keydef_props\n"
            "called scikeys._translate_keyname with arg x\n"
            f"called PropertiesFile.__init__ with arg {tmp_path}/user/user.properties\n"
            "called PropertiesFile.read_props\n"
            "called PropertiesFile.get_keydef_props\n"
            "called scikeys._translate_keyname with arg x\n"
            "called scikeys.merge_keydefs with args ([(('A', ''), 'C', '*', '*', 'S', 111, ''),"
            " (('X', ''), 'A', '*', '*', 'S', '', 'qqq'),"
            " (('x', ''), 'y', 'z', 'q', 'S', 'r', 's')],"
            " [(('x', ''), 'y', 'z', 'q', 'U', 'r', 's')],"
            " {1: ('command-1', 'desc-1'), 3: ('command-3', 'desc-3')},"
            " {111: ('command-2', 'desc-2'), 104: ('command-4', 'desc-4')})\n"
            "called compare_and_keep with args ({}, {1: ('command-1', 'desc-1'), 3: ('command-3',"
            " 'desc-3')}, {111: ('command-2', 'desc-2'), 104: ('command-4', 'desc-4')})\n")
    monkeypatch.setattr(testee.sys, 'platform', 'win32x')
    assert testee.build_data(page, showinfo=True) == ({
        0: (('A', ''), 'C', '*', '*', 'S', 111, ''),
        1: (('X', ''), 'A', '*', '*', 'S', '', 'qqq'),
        2: (('x', ''), 'y', 'z', 'q', 'S', 'r', 's'),
        3: (('x', ''), 'y', 'z', 'q', 'U', 'r', 's')}, {
            'menucommands': {1: ('command-1', 'desc-1'), 3: ('command-3', 'desc-3')},
            'internal_commands': {111: ('command-2', 'desc-2'), 104: ('command-4', 'desc-4')},
            'contexts': ['con', 'texts'], 'olddescs': {'old': 'descs'}})
    assert capsys.readouterr().out == (
            "called scikeys.read_commands with arg commands.txt\n"
            "called tarfile.open with arg sourceloc\n"
            "called tarfile.__enter__\n"
            "called tarfileobject.extractall with arg /tmp\n"
            "called tarfile.__exit__\n"
            "called scikeys.read_menu_win with arg /tmp/scite/win32/SciTERes.rc\n"
            "called scikeys.read_symbols with arg /tmp/scite/src/IFaceTable.cxx\n"
            "called scikeys._translate_keyname with arg A\n"
            "called scikeys.merge_command_dicts with args"
            " ({1: ('command-1', 'desc-1')}, {3: ('command-3', 'desc-3')})\n"
            "called scikeys.merge_command_dicts with args"
            " ({111: ('command-2', 'desc-2')}, {104: ('command-4', 'desc-4')})\n"
            "called scikeys.read_docs with arg docs.txt\n"
            "called scikeys._translate_keyname with arg X\n"
            f"called PropertiesFile.__init__ with arg {tmp_path}/global/glbl.properties\n"
            "called PropertiesFile.read_props\n"
            "called PropertiesFile.get_keydef_props\n"
            "called scikeys._translate_keyname with arg x\n"
            f"called PropertiesFile.__init__ with arg {tmp_path}/user/user.properties\n"
            "called PropertiesFile.read_props\n"
            "called PropertiesFile.get_keydef_props\n"
            "called scikeys._translate_keyname with arg x\n"
            "called scikeys.merge_keydefs with args ([(('A', ''), 'C', '*', '*', 'S', 111, ''),"
            " (('X', ''), 'A', '*', '*', 'S', '', 'qqq'),"
            " (('x', ''), 'y', 'z', 'q', 'S', 'r', 's')],"
            " [(('x', ''), 'y', 'z', 'q', 'U', 'r', 's')],"
            " {1: ('command-1', 'desc-1'), 3: ('command-3', 'desc-3')},"
            " {111: ('command-2', 'desc-2'), 104: ('command-4', 'desc-4')})\n"
            "called compare_and_keep with args ({}, {1: ('command-1', 'desc-1'), 3: ('command-3',"
            " 'desc-3')}, {111: ('command-2', 'desc-2'), 104: ('command-4', 'desc-4')})\n")
    monkeypatch.setattr(testee.sys, 'platform', 'other')
    assert testee.build_data(page, showinfo=True) == ({
        0: (('X', ''), 'A', '*', '*', 'S', '', 'qqq'),
        1: (('x', ''), 'y', 'z', 'q', 'S', 'r', 's'),
        2: (('x', ''), 'y', 'z', 'q', 'U', 'r', 's')}, {
            'menucommands': {1: ('command-1', 'desc-1'), 3: ('command-3', 'desc-3')},
            'internal_commands': {111: ('command-2', 'desc-2'), 104: ('command-4', 'desc-4')},
            'contexts': ['con', 'texts'], 'olddescs': {'old': 'descs'}})
    assert capsys.readouterr().out == (
            "called scikeys.read_commands with arg commands.txt\n"
            "called tarfile.open with arg sourceloc\n"
            "called tarfile.__enter__\n"
            "called tarfileobject.extractall with arg /tmp\n"
            "called tarfile.__exit__\n"
            "called scikeys.read_symbols with arg /tmp/scite/src/IFaceTable.cxx\n"
            "called scikeys.merge_command_dicts with args"
            " ({1: ('command-1', 'desc-1')}, {3: ('command-3', 'desc-3')})\n"
            "called scikeys.merge_command_dicts with args"
            " ({111: ('command-2', 'desc-2')}, {104: ('command-4', 'desc-4')})\n"
            "called scikeys.read_docs with arg docs.txt\n"
            "called scikeys._translate_keyname with arg X\n"
            f"called PropertiesFile.__init__ with arg {tmp_path}/global/glbl.properties\n"
            "called PropertiesFile.read_props\n"
            "called PropertiesFile.get_keydef_props\n"
            "called scikeys._translate_keyname with arg x\n"
            f"called PropertiesFile.__init__ with arg {tmp_path}/user/user.properties\n"
            "called PropertiesFile.read_props\n"
            "called PropertiesFile.get_keydef_props\n"
            "called scikeys._translate_keyname with arg x\n"
            "called scikeys.merge_keydefs with args ([(('X', ''), 'A', '*', '*', 'S', '', 'qqq'),"
            " (('x', ''), 'y', 'z', 'q', 'S', 'r', 's')],"
            " [(('x', ''), 'y', 'z', 'q', 'U', 'r', 's')],"
            " {1: ('command-1', 'desc-1'), 3: ('command-3', 'desc-3')},"
            " {111: ('command-2', 'desc-2'), 104: ('command-4', 'desc-4')})\n"
            "called compare_and_keep with args ({}, {1: ('command-1', 'desc-1'), 3: ('command-3',"
            " 'desc-3')}, {111: ('command-2', 'desc-2'), 104: ('command-4', 'desc-4')})\n")


def _test_merge_keydefs(monkeypatch, capsys):
    """unittest for scikeys.merge_keydefs
    """
    default_keys = {}
    userdef_keys = {}
    menu_commands = {}
    internal_commands = {}
    assert testee.merge_keydefs(default_keys, userdef_keys,
                                menu_commands, internal_commands) == ({}, [])
    assert capsys.readouterr().out == ("")


def test_compare_and_keep():
    """unittest for scikeys.compare_and_keep
    """
    newstuff = {1: ('a', 'b'), 2: ('c', 'd'), 3: ('e', ''), 4: ('g', 'h')}
    otherstuff = {}
    oldstuff = {'c': 'd', 'e': 'f', 'g': 'i'}
    # breakpoint()
    assert testee.compare_and_keep(oldstuff, newstuff, otherstuff) == {'g': 'i'}
    assert newstuff == {1: ('a', 'b'), 2: ('c', 'd'), 3: ('e', 'f'), 4: ('g', 'h')}
    assert not otherstuff
    newstuff = {1: ('a', 'b'), 2: ('c', 'd'), 3: ('e', ''), 4: ('g', 'h')}
    otherstuff = {}
    oldstuff = {'c': 'd', 'e': 'f', 'g': 'i'}
    assert testee.compare_and_keep(oldstuff, otherstuff, newstuff) == {'g': 'i'}
    assert newstuff == {1: ('a', 'b'), 2: ('c', 'd'), 3: ('e', 'f'), 4: ('g', 'h')}
    assert not otherstuff


def test_add_extra_attributes():
    """unittest for scikeys.add_extra_attributes
    """
    win = types.SimpleNamespace(keylist=['key', 'list'],
                                otherstuff={'contexts': ['x', 'y'],
                                            'menucommands': {'x': ('y0', 'y1'), 'z': ('q0', 'q1')},
                                            'internal_commands': {'a': ('b1', 'b2')}})
    testee.add_extra_attributes(win)
    assert win.contextslist == win.otherstuff['contexts']
    assert win.commandskeys == ['x', 'z', 'a', '']
    assert win.commandslist == ['y0', 'q0', 'b1', '']
    assert win.contextactionsdict == {}
    assert win.descriptions == {'y0': 'y1', 'q0': 'q1', 'b1': 'b2'}
    assert win.keylist == ['key', 'list', 'Movement']


def test_update_descriptions():
    """unittest for scikeys.update_descriptions
    """
    win = types.SimpleNamespace(data={'x': ('a', 'b', 'd', 'e', 'f', 'g', 'h')},
                                otherstuff={'menucommands': {1: ('IDM_X', 'xxxx'),
                                                             2: ('IDM_Y', 'yyyy')},
                                            'internal_commands': {100: ('aaa', 'aaaa'),
                                                                  200: ('bbb', 'bbbb')}})
    testee.update_descriptions(win, {})
    assert win.otherstuff['menucommands'] == {1: ('IDM_X', 'xxxx'), 2: ('IDM_Y', 'yyyy')}
    assert win.otherstuff['internal_commands'] == {100: ('aaa', 'aaaa'), 200: ('bbb', 'bbbb')}
    assert win.descriptions == {}
    assert win.data['x'] == ('a', 'b', 'd', 'e', 'f', 'g', 'h')
    win = types.SimpleNamespace(data={'x': ('a', 'b', 'd', 'e', 'f', 'IDM_X', 'h'),
                                      'y': ('p', 'q', 'r', 's', 't', 'bbb', 'v')},
                                otherstuff={'menucommands': {1: ('IDM_X', 'xxxx'),
                                                             2: ('IDM_Y', 'yyyy')},
                                            'internal_commands': {100: ('aaa', 'aaaa'),
                                                                  200: ('bbb', 'bbbb')}})
    testee.update_descriptions(win, {'': 'z', 'IDM_X': 'XXX', 'bbb': 'BBB'})
    assert win.otherstuff['menucommands'] == {1: ('IDM_X', 'XXX'), 2: ('IDM_Y', 'yyyy')}
    assert win.otherstuff['internal_commands'] == {100: ('aaa', 'aaaa'), 200: ('bbb', 'BBB')}
    assert win.descriptions == {'': 'z', 'IDM_X': 'XXX', 'bbb': 'BBB'}
    assert win.data == {'x': ('a', 'b', 'd', 'e', 'f', 'IDM_X', 'XXX'),
                        'y': ('p', 'q', 'r', 's', 't', 'bbb', 'BBB')}
    win = types.SimpleNamespace(data={'x': ('a', 'b', 'd', 'e', 'f', 'IDM_X', 'xxxx'),
                                      'y': ('p', 'q', 'r', 's', 't', 'bbb', 'bbbb')},
                                otherstuff={'menucommands': {1: ('IDM_X', 'xxxx'),
                                                             2: ('IDM_Y', 'yyyy')},
                                            'internal_commands': {100: ('aaa', 'aaaa'),
                                                                  200: ('bbb', 'bbbb')}})
    testee.update_descriptions(win, {'': 'z', 'IDM_X': 'xxxx', 'bbb': 'bbbb'})
    assert win.otherstuff['menucommands'] == {1: ('IDM_X', 'xxxx'), 2: ('IDM_Y', 'yyyy')}
    assert win.otherstuff['internal_commands'] == {100: ('aaa', 'aaaa'), 200: ('bbb', 'bbbb')}
    assert win.descriptions == {'': 'z', 'IDM_X': 'xxxx', 'bbb': 'bbbb'}
    assert win.data == {'x': ('a', 'b', 'd', 'e', 'f', 'IDM_X', 'xxxx'),
                        'y': ('p', 'q', 'r', 's', 't', 'bbb', 'bbbb')}


def _test_savekeys(monkeypatch, capsys):
    """unittest for scikeys.savekeys - not implemented (yet?)
    """
    parent = types.SimpleNamespace()
    assert testee.savekeys(parent) == "expected_result"
    assert capsys.readouterr().out == ("")
