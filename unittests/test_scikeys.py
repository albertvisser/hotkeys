"""unittests for ./plugin_examples/scikeys.py
"""
from plugin_examples import scikeys as testee


def test_translate_keyname(monkeypatch, capsys):
    """unittest for scikeys._translate_keyname
    """
    convert = {'Equal': '=', 'Escape': 'Esc', 'Delete': 'Del', 'Return': 'Enter',
               'BackSpace': 'Backspace', 'PageUp': 'PgUp', 'PageDown': 'PgDn', 'space': 'Space',
               'Keypad*': 'Num*', 'Keypad+': 'Num+', 'Keypad-': 'Num-', 'Keypad/': 'Num/', }
    for x, y in convert.items():
        assert testee._translate_keyname(x) == y


def test_nicefy_props(monkeypatch):
    """unittest for scikeys.nicefy_props
    """
    assert testee.nicefy_props('Anything') == ('Anything', '')
    assert testee.nicefy_props('Ctrl+Alt+Shift+Anything') == ('Anything', 'CAS')
    assert testee.nicefy_props('Shift+Alt+Ctrl+KeypadPlus') == ('Keypad+', 'CAS')


def test_nicefy_source(monkeypatch):
    """unittest for scikeys.nicefy_source
    """
    assert testee.nicefy_source('Anything') == ('Anything', '')
    assert testee.nicefy_source('<control><alt><shift>Anything') == ('Anything', 'CAS')
    assert testee.nicefy_source('<shift><alt><control>Anything') == ('Anything', 'CAS')


def test_read_commands(monkeypatch, tmp_path):
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


def test_read_symbols(monkeypatch, tmp_path):
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
    assert capsys.readouterr().out == ('called nicefy_source with arg ` "F11"`i\n'
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

    def _test_init(self, monkeypatch, capsys):
        """unittest for PropertiesFile.__init__
        """
        testobj = testee.PropertiesFile(fnaam)
        assert capsys.readouterr().out == ("")

    def _test__determine_platform(self, monkeypatch, capsys):
        """unittest for PropertiesFile._determine_platform
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj._determine_platform(line) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test__determine_continuation(self, monkeypatch, capsys):
        """unittest for PropertiesFile._determine_continuation
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj._determine_continuation(line, result) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_read_props(self, monkeypatch, capsys):
        """unittest for PropertiesFile.read_props
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.read_props() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_keydef_props(self, monkeypatch, capsys):
        """unittest for PropertiesFile.get_keydef_props
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_keydef_props() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test__do_substitutions(self, monkeypatch, capsys):
        """unittest for PropertiesFile._do_substitutions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj._do_substitutions(prop, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test__create_variants(self, monkeypatch, capsys):
        """unittest for PropertiesFile._create_variants
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj._create_variants(varnaam, regel, eind) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test__expand_from_other(self, monkeypatch, capsys):
        """unittest for PropertiesFile._expand_from_other
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj._expand_from_other(varnaam, regel, eind) == "expected_result"
        assert capsys.readouterr().out == ("")


def _test_merge_command_dicts(monkeypatch, capsys):
    """unittest for scikeys.merge_command_dicts
    """
    assert testee.merge_command_dicts(dict_from_text, dict_from_src) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_build_data(monkeypatch, capsys):
    """unittest for scikeys.build_data
    """
    assert testee.build_data(page, showinfo=True) == "expected_result"
    assert capsys.readouterr().out == ("")

    def _test_get_next_defitem(self, monkeypatch, capsys):
        """unittest for PropertiesFile.get_next_defitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_next_defitem() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_next_useritem(self, monkeypatch, capsys):
        """unittest for PropertiesFile.get_next_useritem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_next_useritem() == "expected_result"
        assert capsys.readouterr().out == ("")


def _test_add_extra_attributes(monkeypatch, capsys):
    """unittest for scikeys.add_extra_attributes
    """
    assert testee.add_extra_attributes(win) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_savekeys(monkeypatch, capsys):
    """unittest for scikeys.savekeys
    """
    assert testee.savekeys(parent) == "expected_result"
    assert capsys.readouterr().out == ("")
