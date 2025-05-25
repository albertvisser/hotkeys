"""unittests for ./editor/plugins/dckeys.py
"""
import types
import pytest
from editor.plugins import dckeys as testee


def test__shorten_mods():
    """unittest for dckeys._shorten_mods
    """
    assert testee._shorten_mods([]) == ""
    assert testee._shorten_mods(['Ctrl', 'Alt', 'Shift', 'WinKey']) == "CASW"
    assert testee._shorten_mods(['CTRL', 'ALT', 'SHIFT']) == "CAS"
    assert testee._shorten_mods(['CLTR']) == "C"
    assert testee._shorten_mods(['xxx']) == ""


def test__translate_keynames():
    """unittest for dckeys._translate_keynames
    """
    assert testee._translate_keynames('') == ''
    assert testee._translate_keynames('   ↑  ') == 'Up'
    assert testee._translate_keynames('↓') == 'Down'
    assert testee._translate_keynames('←') == 'Left'
    assert testee._translate_keynames('→') == 'Right'
    assert testee._translate_keynames('Delete') == 'Del'
    assert testee._translate_keynames('С') == 'C'
    assert testee._translate_keynames('Pgdown') == 'PgDn'
    assert testee._translate_keynames('Pgup') == 'PgUp'
    assert testee._translate_keynames('Num *') == 'Num*'
    assert testee._translate_keynames('Num -') == 'Num-'
    assert testee._translate_keynames('  xx ') == 'xx'


def test_get_data_from_xml(monkeypatch, capsys):
    """unittest for dckeys.get_data_from_xml
    """
    def mock_parse(filename):
        print(f'called ET.parse with arg {filename}')
        return 'expected_result'
    monkeypatch.setattr(testee.ET, 'parse', mock_parse)
    assert testee.get_data_from_xml('filename') == "expected_result"
    assert capsys.readouterr().out == ("called ET.parse with arg filename\n")


def test_get_data_from_html(monkeypatch, capsys, tmp_path):
    """unittest for dckeys.get_data_from_html
    """
    def mock_beautifulsoup(*args):
        print('called BeautifulSoup with args', args)
        return 'expected_result'
    monkeypatch.setattr(testee.bs, 'BeautifulSoup', mock_beautifulsoup)
    filepath = tmp_path / 'filename'
    filepath.touch()
    assert testee.get_data_from_html(str(filepath)) == "expected_result"
    assert capsys.readouterr().out == (
            f"called BeautifulSoup with args (<_io.TextIOWrapper name='{filepath}'"
            " mode='r' encoding='UTF-8'>, 'lxml')\n")


# def test_get_data_from_csv(monkeypatch, capsys, tmp_path):
#     """unittest for dckeys.get_data_from_csv
#     """
#     def mock_reader(stream):
#         print(f'called csv.reader with arg {stream}')
#         return ['expected', 'result']
#     monkeypatch.setattr(testee.csv, 'reader', mock_reader)
#     filepath = tmp_path / 'filename'
#     filepath.touch()
#     assert testee.get_data_from_csv(str(filepath)) == ["expected", "result"]
#     assert capsys.readouterr().out == (
#             f"called csv.reader with arg <_io.TextIOWrapper name='{filepath}'"
#             " mode='r' encoding='UTF-8'>\n")


# def test_save_list_to_csv(monkeypatch, capsys, tmp_path):
#     """unittest for dckeys.save_list_to_csv
#     """
#     def mock_copy(*args):
#         print('called shutil.copyfile with args', args)
#     def mock_write(arg):
#         print(f"called csv.writer.writerow with arg '{arg}'")
#     def mock_writer(arg):
#         print(f"called csv.writer with arg {arg}")
#         return types.SimpleNamespace(writerow=mock_write)
#     monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
#     monkeypatch.setattr(testee.csv, 'writer', mock_writer)
#     filepath = tmp_path / 'filename'
#     testee.save_list_to_csv(['data', 'lines'], str(filepath))
#     assert capsys.readouterr().out == (
#             f"called csv.writer with arg <_io.TextIOWrapper name='{filepath}'"
#             " mode='w' encoding='UTF-8'>\n"
#             "called csv.writer.writerow with arg 'data'\n"
#             "called csv.writer.writerow with arg 'lines'\n")
#     filepath.touch()
#     testee.save_list_to_csv(['data', 'lines'], str(filepath))
#     assert capsys.readouterr().out == (
#             f"called shutil.copyfile with args ('{filepath}', '{str(filepath) + '~'}')\n"
#             f"called csv.writer with arg <_io.TextIOWrapper name='{filepath}'"
#             " mode='w' encoding='UTF-8'>\n"
#             "called csv.writer.writerow with arg 'data'\n"
#             "called csv.writer.writerow with arg 'lines'\n")


def test_parse_keytext():
    """unittest for dckeys.parse_keytext
    """
    assert testee.parse_keytext('Esc, Q (') == [('Esc', ''), ('Q', '')]
    assert testee.parse_keytext('A') == [('A', '')]
    assert testee.parse_keytext('Ctrl+F1, Shift+F2, Alt+F3') == [('F1', 'C'), ('F2', 'S'),
                                                                 ('F3', 'A')]
    assert testee.parse_keytext('Num +') == [('Num +', '')]
    assert testee.parse_keytext('+') == [('+', '')]
    assert testee.parse_keytext('Ctrl+') == [('+', 'C')]     # komt niet voor
    assert testee.parse_keytext('Ctrl++') == [('+', 'C')]    # komt wel voor


def test_analyze_keydefs():
    """unittest for dckeys.analyze_keydefs
    """
    # 157-224
    soup = testee.bs.BeautifulSoup('<html><div>nothing to parse</div></html>', 'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({}, {}, {}, [])
    # 159-222
    soup = testee.bs.BeautifulSoup('<html><div><p>nothing to parse</p></div></html>', 'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({}, {}, {}, [])
    # 159-222
    soup = testee.bs.BeautifulSoup('<html><div><table>empty table</table></div></html>', 'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({}, {}, {}, [])
    # 162-222
    soup = testee.bs.BeautifulSoup('<html><div><table><thead><th>just a header</th></thead></table>'
                                   '</div></html>', 'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({}, {}, {}, [])
    # 162-222
    soup = testee.bs.BeautifulSoup('<html><div><table><tr class="rowcategorytitle"><td></td></tr>'
                                   '</table></div></html>', 'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({}, {}, {}, [])
    # 165-222
    soup = testee.bs.BeautifulSoup('<html><div><table><tr class="rowsubtitle"><td></td></tr>'
                                   '</table></div></html>', 'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({}, {}, {}, [])
    # 165-222
    soup = testee.bs.BeautifulSoup('<html><div><table><tr>empty row</tr></table></div></html>',
                                   'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({}, {}, {}, [])
    # 170-208, 214-217, 220-223
    soup = testee.bs.BeautifulSoup('<html><div><table><tr><th>just a header</th></tr></table>'
                                   '</div></html>', 'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({}, {}, {}, [])
    # 170-208, 214-217, 220-223
    soup = testee.bs.BeautifulSoup('<html><div><table><tr><td></td></tr>'
                                   '</table></div></html>', 'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({}, {}, {}, [])
    # 173-208, 214-217, 220-223
    soup = testee.bs.BeautifulSoup('<html><div><table><tr><td class="x"></td></tr>'
                                   '</table></div></html>', 'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({}, {}, {}, [])
    # 174-180, 182-208, 214-217, 220-223
    soup = testee.bs.BeautifulSoup('<html><div><table><tr><td class="cmdcell">'
                                   'do-not-parse<p>do-not-parse</p>'
                                   '<div class="x">do-not-parse</div></td>'
                                   '<td class="cmdhintcell">'
                                   '<table class="x"><tr><td>do-not-parse</td></tr></table>'
                                   '<table class="innercmddesc">empty-table</table>'
                                   '<table class="innercmddesc"><p>empty-table</p></table>'
                                   '<table class="innercmddesc"><tr>empty-row</tr></table>'
                                   '<table class="innercmddesc"><tr><td class="x">xxx</td></tr>'
                                   '</table>'
                                   '</td></tr></table></div></html>', 'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({}, {}, {}, [])
    # 178, 180, 187, 189, 200-201, 203, 205, 207, 214-217, 220-223
    soup = testee.bs.BeautifulSoup('<html><div><table><tr><td class="cmdcell">'
                                   '<div class="longcmdname"><a>yyyyyy.</a></div>'
                                   '<div class="shrtctkey">kkk</div></td>'
                                   '<td class="cmdhintcell">descitem'
                                   '<p>a longer\ndescription</p>'
                                   '<table class="innercmddesc"><tr><td>inner desc</td></tr></table>'
                                   '<table class="innercmddesc"><tr>'
                                   '<td class="innerdescparamcell">param</td>'
                                   '<td class="innerdescvaluecell">value</td>'
                                   '<td class="innerdescdesccell">pdesc</td></tr></table>'
                                   '</td></tr><tr><td class="cmdcell">'
                                   '<div class="cmdname"><a>xxx.</a></div>'
                                   '<div class="shrtctkey">lll</div></td>'
                                   '</td></tr></table></div></html>', 'lxml')
    root = soup.select('div')[0]
    assert testee.analyze_keydefs(root) == ({'xxx': '',
                                             'yyyyyy': 'descitem a longer description inner desc'},
                                            {('Kkk', ''): {('Main', 'yyyyyy')},
                                             ('Lll', ''): {('Main', 'xxx')}},
                                            {'yyyyyy': [('', '', ''), ('param', 'value', 'pdesc')]},
                                            ['yyyyyy', 'xxx'])


def test_build_data(monkeypatch, capsys):
    """unittest for dckeys.build_data
    """
    class MockBuilder:
        """stub for dckeys.CsvBuilder object
        """
        def __init__(self, *args):
            print('called MockBuilder.__init__ with args', args)
            self.page = args[0]
            self.counter = 0
            self.olddescs = {'old': 'descs'}
        def get_settings_pathnames(self, *args):
            print('called MockBuilder.get_settings_pathnames with args', args)
            if self.page.name in ('nokbfile', 'newkbfile'):
                return '', 'keys', 'cmds', 'sett', 'desc'
            return 'kbf', 'keys', 'cmds', 'sett', 'desc'
        def check_path_setting(self, *args):
            print('called MockBuilder.check_path_setting with args', args)
            if self.page.name == 'nokbfile':
                self.counter += 1
                return '' if self.counter == 1 else 'newkbf'
            return 'newkbf' if self.page.name == 'newkbfile' else ''
        def get_keydefs(self, *args):
            print('called MockBuilder.get_keydefs with args', args)
            self.defaults = {'def': 'aults'}
        def get_stdkeys(self, *args):
            print('called MockBuilder.get_stdkeys with args', args)
            self.stdkeys = {'std': 'keys'}
        def get_toolbarcmds(self, *args):
            print('called MockBuilder.get_toolbarcmds with args', args)
        def get_cmddict(self, *args):
            print('called MockBuilder.get_cmddict with args', args)
            self.cmddict = {'cmd': 'dict'}
        def assemble_shortcuts(self):
            print('called MockBuilder.assemble_shortcuts')
            self.contexts = {'con', 'texts'}
            self.controls = {'con', 'trols'}
            self.params = {'params': ''}
            self.catdict = {'cat': 'dict'}
        def compare_descriptions(self, *args):
            print('called MockBuilder.compare_descriptions with args', args)
        def format_shortcuts(self, *args):
            print('called MockBuilder.format_shortcuts with args', args)
            self.shortcuts = {'short': 'cuts'}
            self.contexts_list = ['xx_yyy'] if self.page.name == 'newkbfile' else []
    def mock_get_data_from_xml(arg):
        print('called get_data_from_xml with arg', arg)
        return 'xml data'
    def mock_get_data_from_html(arg):
        print('called get_data_from_html with arg', arg)
        return 'html_data'
    def mock_show(*args, **kwargs):
        print('called gui.show_message with args', args, kwargs)
    monkeypatch.setattr(testee, 'CsvBuilder', MockBuilder)
    monkeypatch.setattr(testee, 'get_data_from_xml', mock_get_data_from_xml)
    monkeypatch.setattr(testee, 'get_data_from_html', mock_get_data_from_html)
    monkeypatch.setattr(testee, 'show_message', mock_show)
    page = types.SimpleNamespace(name='', settings={}, descriptions={'x': 'y'})
    page.gui = types.SimpleNamespace()
    assert testee.build_data(page, showinfo=False) == (
            {'short': 'cuts'},
            {'olddescs': {'old': 'descs'},'stdkeys': {'std': 'keys'},
             'defaults': {'def': 'aults'}, 'cmddict': {'cmd': 'dict'},
             'contexts': ['con', 'texts'], 'restrictions': ['con', 'trols'],
             'cmdparms': {'params': ''}, 'catdict': {'cat': 'dict'}})
    assert capsys.readouterr().out == (
            f"called MockBuilder.__init__ with args ({page}, False)\n"
            "called MockBuilder.get_settings_pathnames with args ()\n"
            "called get_data_from_xml with arg kbf\n"
            "called MockBuilder.get_keydefs with args ('xml data',)\n"
            "called get_data_from_html with arg keys\n"
            "called MockBuilder.get_stdkeys with args ('html_data',)\n"
            "called get_data_from_xml with arg sett\n"
            "called MockBuilder.get_toolbarcmds with args ('xml data',)\n"
            "called get_data_from_html with arg cmds\n"
            "called MockBuilder.get_cmddict with args ('html_data',)\n"
            "called MockBuilder.assemble_shortcuts\n"
            "called MockBuilder.compare_descriptions with args ({'x': 'y'},)\n"
            "called MockBuilder.format_shortcuts with args ()\n")
    assert testee.build_data(page) == (
            {'short': 'cuts'},
            {'olddescs': {'old': 'descs'},'stdkeys': {'std': 'keys'},
             'defaults': {'def': 'aults'}, 'cmddict': {'cmd': 'dict'},
             'contexts': ['con', 'texts'], 'restrictions': ['con', 'trols'],
             'cmdparms': {'params': ''}, 'catdict': {'cat': 'dict'}})
    assert capsys.readouterr().out == (
            f"called MockBuilder.__init__ with args ({page}, True)\n"
            "called MockBuilder.get_settings_pathnames with args ()\n"
            "called MockBuilder.check_path_setting with args ('kbf',)\n"
            "called get_data_from_xml with arg kbf\n"
            "called MockBuilder.get_keydefs with args ('xml data',)\n"
            "called get_data_from_html with arg keys\n"
            "called MockBuilder.get_stdkeys with args ('html_data',)\n"
            "called get_data_from_xml with arg sett\n"
            "called MockBuilder.get_toolbarcmds with args ('xml data',)\n"
            "called get_data_from_html with arg cmds\n"
            "called MockBuilder.get_cmddict with args ('html_data',)\n"
            "called MockBuilder.assemble_shortcuts\n"
            "called MockBuilder.compare_descriptions with args ({'x': 'y'},)\n"
            "called MockBuilder.format_shortcuts with args ()\n")
    page.name = 'nokbfile'
    page.title = 'xx'
    page.gui.master = page
    assert testee.build_data(page) == (
            {'short': 'cuts'},
            {'olddescs': {'old': 'descs'},'stdkeys': {'std': 'keys'},
             'defaults': {'def': 'aults'}, 'cmddict': {'cmd': 'dict'},
             'contexts': ['con', 'texts'], 'restrictions': ['con', 'trols'],
             'cmdparms': {'params': ''}, 'catdict': {'cat': 'dict'}})
    # mimic the original settings path before entering it in check_path_setting
    page.settings = {}
    assert capsys.readouterr().out == (
            f"called MockBuilder.__init__ with args ({page}, True)\n"
            "called MockBuilder.get_settings_pathnames with args ()\n"
            "called MockBuilder.check_path_setting with args ('',)\n"
            f"called gui.show_message with args ({page.gui},)"
            " {'text': 'You MUST provide a name for the settings file'}\n"
            "called MockBuilder.check_path_setting with args ('',)\n"
            "called get_data_from_xml with arg newkbf\n"
            "called MockBuilder.get_keydefs with args ('xml data',)\n"
            "called get_data_from_html with arg keys\n"
            "called MockBuilder.get_stdkeys with args ('html_data',)\n"
            "called get_data_from_xml with arg sett\n"
            "called MockBuilder.get_toolbarcmds with args ('xml data',)\n"
            "called get_data_from_html with arg cmds\n"
            "called MockBuilder.get_cmddict with args ('html_data',)\n"
            "called MockBuilder.assemble_shortcuts\n"
            "called MockBuilder.compare_descriptions with args ({'x': 'y'},)\n"
            "called MockBuilder.format_shortcuts with args ()\n")
    page.name = 'newkbfile'
    assert testee.build_data(page) == (
            {'short': 'cuts'},
            {'olddescs': {'old': 'descs'},'stdkeys': {'std': 'keys'},
             'defaults': {'def': 'aults'}, 'cmddict': {'cmd': 'dict'},
             'contexts': ['con', 'texts'], 'restrictions': ['con', 'trols'],
             'cmdparms': {'params': ''}, 'catdict': {'cat': 'dict'}})
    # mimic the original settings path before entering it in check_path_setting
    page.settings = {}
    assert capsys.readouterr().out == (
            f"called MockBuilder.__init__ with args ({page}, True)\n"
            "called MockBuilder.get_settings_pathnames with args ()\n"
            "called MockBuilder.check_path_setting with args ('',)\n"
            "called get_data_from_xml with arg newkbf\n"
            "called MockBuilder.get_keydefs with args ('xml data',)\n"
            "called get_data_from_html with arg keys\n"
            "called MockBuilder.get_stdkeys with args ('html_data',)\n"
            "called get_data_from_xml with arg sett\n"
            "called MockBuilder.get_toolbarcmds with args ('xml data',)\n"
            "called get_data_from_html with arg cmds\n"
            "called MockBuilder.get_cmddict with args ('html_data',)\n"
            "called MockBuilder.assemble_shortcuts\n"
            "called MockBuilder.compare_descriptions with args ({'x': 'y'},)\n"
            "called MockBuilder.format_shortcuts with args ()\n")


class TestCsvBuilder:
    """unittest for dckeys.CsvBuilder
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dckeys.CsvBuilder object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CsvBuilder.__init__ with args', args)
        monkeypatch.setattr(testee.CsvBuilder, '__init__', mock_init)
        testobj = testee.CsvBuilder()
        assert capsys.readouterr().out == 'called CsvBuilder.__init__ with args ()\n'
        return testobj

    def test_init(self):
        """unittest for CsvBuilder.__init__
        """
        page = types.SimpleNamespace(descriptions='olddescs')
        testobj = testee.CsvBuilder(page, True)
        assert testobj.page == page
        assert testobj.showinfo
        assert testobj.olddescs == 'olddescs'
        assert testobj.definedkeys == {}
        assert testobj.stdkeys == {}
        assert testobj.cmddict == {}
        assert testobj.tbcmddict == {}
        assert testobj.defaults == {}
        assert testobj.params == {}
        assert testobj.catdict == {}
        assert testobj.shortcuts == {}
        assert testobj.contexts == set()
        assert testobj.contexts_list == []
        assert testobj.controls == {'', 'Command Line', 'Files Panel', 'Quick Search'}
        assert testobj.tobematched == {}
        assert testobj.unlisted_cmds == []

    def test_get_settings_pathnames(self, monkeypatch, capsys):
        """unittest for CsvBuilder.get_settings_pathnames
        """
        def mock_run(*args, **kwargs):
            print('called subprocess run with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.os.path, 'exists', lambda *x: False)
        monkeypatch.setattr(testee.subprocess, 'run', mock_run)
        testobj.page = types.SimpleNamespace(settings={
            'DC_PATH': 'xxx', 'DC_KEYS': 'yyy', 'DC_CMDS': 'zzz', 'DC_SETT': 'ppp', 'DC_DESC': 'qqq'})
        assert testobj.get_settings_pathnames() == ('xxx', f'{testee.TEMPLOC}/yyy',
                                                    f'{testee.TEMPLOC}/zzz', 'ppp', 'qqq')
        assert testobj.page.settings == {'DC_PATH': 'xxx', 'DC_KEYS': 'yyy', 'DC_CMDS': 'zzz',
                                         'DC_SETT': 'ppp', 'DC_DESC': 'qqq'}
        assert capsys.readouterr().out == ""
        testobj.page = types.SimpleNamespace(settings={})
        assert testobj.get_settings_pathnames() == (f'{testee.CONFPATH}/shortcuts.scf',
                                                    f'{testee.TEMPLOC}/shortcuts.html',
                                                    f'{testee.TEMPLOC}/cmds.html',
                                                    f'{testee.CONFPATH}/doublecmd.xml',
                                                    f'{testee.HERE}/dc_descs.csv')
        assert testobj.page.settings == {'DC_PATH': f'{testee.CONFPATH}/shortcuts.scf',
                                         'DC_KEYS': f'{testee.DOCSPATH}/shortcuts.html',
                                         'DC_CMDS': f'{testee.DOCSPATH}/cmds.html',
                                         'DC_SETT': f'{testee.CONFPATH}/doublecmd.xml',
                                         'DC_DESC': f'{testee.HERE}/dc_descs.csv'}
        assert capsys.readouterr().out == (
                f"called subprocess run with args (['wget', '{testee.DOCSPATH}/shortcuts.html',"
                f" '-P', '{testee.TEMPLOC}', '-nc'],) {{'check': False}}\n"
                f"called subprocess run with args (['wget', '{testee.DOCSPATH}/cmds.html', '-P',"
                f" '{testee.TEMPLOC}', '-nc'],) {{'check': False}}\n")
        monkeypatch.setattr(testee.os.path, 'exists', lambda *x: True)
        testobj.page = types.SimpleNamespace(settings={
            'DC_PATH': 'xxx', 'DC_KEYS': 'yyy', 'DC_CMDS': 'zzz', 'DC_SETT': 'ppp', 'DC_DESC': 'qqq'})
        assert testobj.get_settings_pathnames() == ('xxx', f'{testee.TEMPLOC}/yyy',
                                                    f'{testee.TEMPLOC}/zzz', 'ppp', 'qqq')
        assert testobj.page.settings == {'DC_PATH': 'xxx', 'DC_KEYS': 'yyy', 'DC_CMDS': 'zzz',
                                         'DC_SETT': 'ppp', 'DC_DESC': 'qqq'}
        assert capsys.readouterr().out == ""
        testobj.page = types.SimpleNamespace(settings={})
        assert testobj.get_settings_pathnames() == (f'{testee.CONFPATH}/shortcuts.scf',
                                                    f'{testee.TEMPLOC}/shortcuts.html',
                                                    f'{testee.TEMPLOC}/cmds.html',
                                                    f'{testee.CONFPATH}/doublecmd.xml',
                                                    f'{testee.HERE}/dc_descs.csv')
        assert testobj.page.settings == {'DC_PATH': f'{testee.CONFPATH}/shortcuts.scf',
                                         'DC_KEYS': f'{testee.DOCSPATH}/shortcuts.html',
                                         'DC_CMDS': f'{testee.DOCSPATH}/cmds.html',
                                         'DC_SETT': f'{testee.CONFPATH}/doublecmd.xml',
                                         'DC_DESC': f'{testee.HERE}/dc_descs.csv'}
        assert capsys.readouterr().out == ""

    def test_check_path_setting(self, monkeypatch, capsys):
        """unittest for CsvBuilder.check_path_setting
        """
        def mock_ask(*args, **kwargs):
            print('called gui.ask_ync_question with args', args, kwargs)
            return False, True
        def mock_ask_2(*args, **kwargs):
            print('called gui.ask_ync_question with args', args, kwargs)
            return True, True
        def mock_get(*args, **kwargs):
            print('called gui.get_file_to_open with args', args, kwargs)
            return ''
        def mock_get_2(*args, **kwargs):
            print('called gui.get_file_to_open with args', args, kwargs)
            return 'xxx'
        monkeypatch.setattr(testee, 'ask_ync_question', mock_ask)
        monkeypatch.setattr(testee, 'get_file_to_open', mock_get)
        monkeypatch.setattr(testee, 'instructions', 'qqq')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.page = types.SimpleNamespace(gui=types.SimpleNamespace())
        assert testobj.check_path_setting('initial') == ""
        assert capsys.readouterr().out == (
                "called gui.ask_ync_question with args (namespace(),) {'text': 'qqq'}\n")
        monkeypatch.setattr(testee, 'ask_ync_question', mock_ask_2)
        assert testobj.check_path_setting('initial') == ""
        assert capsys.readouterr().out == (
                "called gui.ask_ync_question with args (namespace(),) {'text': 'qqq'}\n"
                "called gui.get_file_to_open with args"
                " (namespace(),) {'extension': 'SCF files (*.scf)', 'start': 'initial'}\n")
        monkeypatch.setattr(testee, 'get_file_to_open', mock_get_2)
        assert testobj.check_path_setting('initial') == "xxx"
        assert capsys.readouterr().out == (
                "called gui.ask_ync_question with args (namespace(),) {'text': 'qqq'}\n"
                "called gui.get_file_to_open with args"
                " (namespace(),) {'extension': 'SCF files (*.scf)', 'start': 'initial'}\n")

    def test_get_keydefs(self, monkeypatch, capsys):
        """unittest for CsvBuilder.get_keydefs
        """
        def mock_shorten(*args):
            print('called _shorten_mods with args', args)
            return ''.join(args[0])
        monkeypatch.setattr(testee, '_shorten_mods', mock_shorten)
        root = testee.ET.fromstring('<doublecmd><Hotkeys></Hotkeys></doublecmd>')
        data = testee.ET.ElementTree(root)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.contexts = set()
        testobj.controls = set()
        testobj.definedkeys = {}
        testobj.get_keydefs(data)
        assert not testobj.contexts
        assert not testobj.controls
        assert not testobj.definedkeys
        assert capsys.readouterr().out == ""
        root = testee.ET.fromstring('<doublecmd><Hotkeys><Form Name="form1">'
                                    '<Hotkey><Shortcut>XXX</Shortcut><Command>YYY</Command></Hotkey>'
                                    '<Hotkey><Shortcut>A+A</Shortcut><Command>BBB</Command>'
                                    '<Param>ccc=ddd</Param></Hotkey>'
                                    '<Hotkey><Shortcut>PP+</Shortcut><Command>QQQ</Command>'
                                    '<Control>RRR</Control></Hotkey></Form>'
                                    '<Form Name="form2">'
                                    '<Hotkey><Shortcut>X+X</Shortcut><Command>YYY</Command>'
                                    '<Param>aaa=bbb</Param><Param>ccc=ddd</Param>'
                                    '<Control>eee</Control><Control>RRR</Control></Hotkey>'
                                    '</Form></Hotkeys></doublecmd>')
        data = testee.ET.ElementTree(root)
        testobj.contexts = set()
        testobj.controls = set()
        testobj.definedkeys = {}
        testobj.get_keydefs(data)
        assert testobj.contexts == {'form1', 'form2'}
        assert testobj.controls == {'', 'RRR', 'eee'}
        assert testobj.definedkeys == {
                ('XXX', '', 'form1'): {'cmd': 'YYY', 'param': '', 'ctrl': ''},
                ('A', 'A', 'form1'): {'cmd': 'BBB', 'param': 'ccc=ddd', 'ctrl': ''},
                ('PP+', '', 'form1'): {'cmd': 'QQQ', 'param': '', 'ctrl': 'RRR'},
                ('X', 'X', 'form2'): {'cmd': 'YYY', 'param': 'aaa=bbb;ccc=ddd', 'ctrl': 'eee;RRR'}}
        assert capsys.readouterr().out == ("called _shorten_mods with args ([],)\n"
                                           "called _shorten_mods with args (['A'],)\n"
                                           "called _shorten_mods with args ([],)\n"
                                           "called _shorten_mods with args (['X'],)\n")

    def test_get_stdkeys(self, monkeypatch, capsys):
        """unittest for CsvBuilder.get_stdkeys
        """
        def mock_parse(arg):
            print(f"called parse_keytext with arg '{arg}'")
            return [('x', 'y')]
        def mock_translate(arg):
            print(f"called _translate_keynames with arg '{arg}'")
            return arg
        monkeypatch.setattr(testee, 'parse_keytext', mock_parse)
        monkeypatch.setattr(testee, '_translate_keynames', mock_translate)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.contexts_list = []
        testobj.stdkeys = {}
        soup = testee.bs.BeautifulSoup('<html><p>nothing to see here</p></html>', 'lxml')
        testobj.get_stdkeys(soup)
        assert not testobj.contexts_list
        assert not testobj.stdkeys
        assert capsys.readouterr().out == ""
        soup = testee.bs.BeautifulSoup('<html><div><p>still nothing to see</p></div></html>', 'lxml')
        testobj.get_stdkeys(soup)
        assert not testobj.contexts_list
        assert not testobj.stdkeys
        assert capsys.readouterr().out == ""
        soup = testee.bs.BeautifulSoup('<html><div><h2><a name="intro">still nothing</a>'
                                       '</h2></div></html>', 'lxml')
        testobj.get_stdkeys(soup)
        assert not testobj.contexts_list
        assert not testobj.stdkeys
        assert capsys.readouterr().out == ""
        soup = testee.bs.BeautifulSoup('<html><div><h2><a name="options">still nothing</a>'
                                       '</h2></div></html>', 'lxml')
        testobj.get_stdkeys(soup)
        assert not testobj.contexts_list
        assert not testobj.stdkeys
        assert capsys.readouterr().out == ""
        soup = testee.bs.BeautifulSoup('<html><div><h2><a name="main_window"><table><tr></tr>'
                                       '</table></a></h2></div></html>', 'lxml')
        testobj.get_stdkeys(soup)
        assert testobj.contexts_list == ['Main']
        assert not testobj.stdkeys
        assert capsys.readouterr().out == ""
        testobj.contexts_list = []
        soup = testee.bs.BeautifulSoup('<html><div><h2><a name="main_window"><table><tr class="x">'
                                       '</tr></table></a></h2></div></html>', 'lxml')
        testobj.get_stdkeys(soup)
        assert testobj.contexts_list == ['Main']
        assert not testobj.stdkeys
        assert capsys.readouterr().out == ""
        testobj.contexts_list = []
        soup = testee.bs.BeautifulSoup('<html><div><h2><a name="main_window"><table><tr>'
                                       '<td>still nothing?</td>'
                                       '</tr></table></a></h2></div></html>', 'lxml')
        testobj.get_stdkeys(soup)
        assert testobj.contexts_list == ['Main']
        assert testobj.stdkeys == {}
        assert capsys.readouterr().out == ""
        testobj.contexts_list = []
        soup = testee.bs.BeautifulSoup('<html><div><h2><a name="main_window"><table><tr>'
                                       '<td class="xxx">still nothing?</td>'
                                       '</tr></table></a></h2></div></html>', 'lxml')
        testobj.get_stdkeys(soup)
        assert testobj.contexts_list == ['Main']
        assert testobj.stdkeys == {}
        assert capsys.readouterr().out == ""
        testobj.contexts_list = []
        soup = testee.bs.BeautifulSoup('<html><div><h2><a name="main_window"><table><tr>'
                                       '<td class="varcell"><div>keycombo</div></td>'
                                       '<td>description</td>'
                                       '</tr></table></a></h2></div></html>', 'lxml')
        testobj.get_stdkeys(soup)
        assert testobj.contexts_list == ['Main']
        assert testobj.stdkeys == {('x', 'y', 'Main'): 'description'}
        assert capsys.readouterr().out == ("called parse_keytext with arg 'keycombo'\n"
                                           "called _translate_keynames with arg 'x'\n")

    def test_get_cmddict(self, monkeypatch, capsys):
        """unittest for CsvBuilder.get_cmddict
        """
        def mock_analyze(data):
            print(f"called analyze_keydefs with arg '{data}'")
            return {'cd': 'cmd'}, {'da': 'dflt'}, {'cp': 'parm'}, 'cl'
        monkeypatch.setattr(testee, 'analyze_keydefs', mock_analyze)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cmddict = {}
        testobj.defaults = {}
        testobj.params = {}
        testobj.catdict = {}
        soup = testee.bs.BeautifulSoup('<html><p>nothing to see here</p></html>', 'lxml')
        with pytest.raises(IndexError):
            testobj.get_cmddict(soup)  # geen div(s) met class dchelpage
        soup = testee.bs.BeautifulSoup('<html><div>nothing here either</div></html>', 'lxml')
        with pytest.raises(IndexError):
            testobj.get_cmddict(soup)  # geen div(s) met class dchelpage
        soup = testee.bs.BeautifulSoup('<html><div class="dchelpage">still nothing</dov></html>',
                                       'lxml')
        testobj.get_cmddict(soup)
        assert not testobj.cmddict
        assert not testobj.defaults
        assert not testobj.params
        assert not testobj.catdict
        assert capsys.readouterr().out == ""
        soup = testee.bs.BeautifulSoup('<html><div class="dchelpage"><p>nope</p></div></html>',
                                       'lxml')
        testobj.get_cmddict(soup)
        assert not testobj.cmddict
        assert not testobj.defaults
        assert not testobj.params
        assert not testobj.catdict
        assert capsys.readouterr().out == ""
        soup = testee.bs.BeautifulSoup('<html><div class="dchelpage"><div>nope</dov></div></html>',
                                       'lxml')
        testobj.get_cmddict(soup)
        assert not testobj.cmddict
        assert not testobj.defaults
        assert not testobj.params
        assert not testobj.catdict
        assert capsys.readouterr().out == ""
        soup = testee.bs.BeautifulSoup('<html><div class="dchelpage"><div><p>nope</p></div></div>'
                                       '</html>', 'lxml')
        testobj.get_cmddict(soup)
        assert not testobj.cmddict
        assert not testobj.defaults
        assert not testobj.params
        assert not testobj.catdict
        assert capsys.readouterr().out == ""
        soup = testee.bs.BeautifulSoup('<html><div class="dchelpage"><div><h2>nope</h2></div></div>'
                                       '</html>', 'lxml')
        testobj.get_cmddict(soup)
        assert not testobj.cmddict
        assert not testobj.defaults
        assert not testobj.params
        assert not testobj.catdict
        assert capsys.readouterr().out == ""
        soup = testee.bs.BeautifulSoup('<html><div class="dchelpage"><div><h2><a>nope</a></h2>'
                                       '</div></div></html>', 'lxml')
        with pytest.raises(KeyError):
            testobj.get_cmddict(soup)  # geen a met "name" attribute
        soup = testee.bs.BeautifulSoup('<html><div class="dchelpage"><div><h2><a name="xxx">'
                                       'nope</a></h2></div></div></html>', 'lxml')
        testobj.get_cmddict(soup)
        assert not testobj.cmddict
        assert not testobj.defaults
        assert not testobj.params
        assert not testobj.catdict
        assert capsys.readouterr().out == ""
        soup = testee.bs.BeautifulSoup('<html><div class="dchelpage"><div><h2><a name="catxxx">'
                                       'finally!</a></h2></div></div></html>', 'lxml')
        testobj.get_cmddict(soup)
        assert testobj.cmddict == {'cd': 'cmd'}
        assert testobj.defaults == {'da': 'dflt'}
        assert testobj.params == {'cp': 'parm'}
        assert testobj.catdict == {'xxx': 'cl'}
        arg = '<div><h2><a name="catxxx">finally!</a></h2></div>'
        assert capsys.readouterr().out == f"called analyze_keydefs with arg '{arg}'\n"

    def test_get_toolbarcmds(self, monkeypatch, capsys):
        """unittest for CsvBuilder.get_toolbarcmds
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tbcmddict = {}
        root = testee.ET.fromstring("<doublecmd><Toolbars></Toolbars></doublecmd>")
        data = testee.ET.ElementTree(root)
        testobj.get_toolbarcmds(data)
        assert not testobj.tbcmddict
        root = testee.ET.fromstring("<doublecmd><Toolbars><MainToolbar></MainToolbar></Toolbars>"
                                    "</doublecmd>")
        data = testee.ET.ElementTree(root)
        testobj.get_toolbarcmds(data)
        assert not testobj.tbcmddict
        root = testee.ET.fromstring("<doublecmd><Toolbars><MainToolbar><Row></Row></MainToolbar>"
                                    "</Toolbars></doublecmd>")
        data = testee.ET.ElementTree(root)
        testobj.get_toolbarcmds(data)
        assert not testobj.tbcmddict
        root = testee.ET.fromstring("<doublecmd><Toolbars><MainToolbar><Row><Stuff>xxx</Stuff>"
                                    "</Row></MainToolbar></Toolbars></doublecmd>")
        data = testee.ET.ElementTree(root)
        testobj.get_toolbarcmds(data)
        assert not testobj.tbcmddict
        root = testee.ET.fromstring("<doublecmd><Toolbars><MainToolbar><Row><Program><ID>xxx</ID>"
                                    "<Command>yyy</Command><Hint>zzz</Hint><Params>qqq</Params>"
                                    "</Program></Row></MainToolbar></Toolbars></doublecmd>")
        data = testee.ET.ElementTree(root)
        testobj.get_toolbarcmds(data)
        assert testobj.tbcmddict == {('MainToolbar', 'xxx'): ('zzz', 'yyy', 'qqq')}
        testobj.tbcmddict = {}
        root = testee.ET.fromstring("<doublecmd><Toolbars><MainToolbar><Row><Program><ID>xxx</ID>"
                                    "<Command>yyy</Command></Program></Row></MainToolbar>"
                                    "</Toolbars></doublecmd>")
        data = testee.ET.ElementTree(root)
        testobj.get_toolbarcmds(data)
        assert testobj.tbcmddict == {('MainToolbar', 'xxx'): ('', 'yyy', '')}

    # def test_add_missing_descriptions(self, monkeypatch, capsys):
    #     """unittest for CsvBuilder.add_missing_descriptions
    #     """
    #     def mock_show(*args):
    #         print('called show_dialog with args', args)
    #         return False
    #     def mock_show_2(*args):
    #         print('called show_dialog with args', args)
    #         return True
    #     monkeypatch.setattr(testee, 'show_dialog', mock_show)
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.showinfo = False
    #     testobj.cmddict = {}
    #     assert testobj.add_missing_descriptions([]) == []
    #     assert not testobj.cmddict
    #     assert capsys.readouterr().out == ""
    #     assert testobj.add_missing_descriptions([('desc', 'list')]) == [('desc', 'list')]
    #     assert testobj.cmddict == {'desc': 'list'}
    #     assert capsys.readouterr().out == ""
    #     testobj.cmddict = {'x': 'y'}
    #     assert testobj.add_missing_descriptions([('desc', 'list')]) == [('desc', 'list')]
    #     assert testobj.cmddict == {'x': 'y', 'desc': 'list'}
    #     assert capsys.readouterr().out == ""
    #     testobj.cmddict = {'desc': ''}
    #     assert testobj.add_missing_descriptions([('desc', 'list')]) == [('desc', 'list')]
    #     assert testobj.cmddict == {'desc': 'list'}
    #     assert capsys.readouterr().out == ""
    #     testobj.cmddict = {'desc': 'xxx'}
    #     assert testobj.add_missing_descriptions([('desc', 'list')]) == [('desc', 'list')]
    #     assert testobj.cmddict == {'desc': 'xxx'}
    #     assert capsys.readouterr().out == ""
    #     testobj.showinfo = True
    #     testobj.page = types.SimpleNamespace()
    #     testobj.cmddict = {}
    #     assert testobj.add_missing_descriptions([('desc', 'list')]) == [('desc', 'list')]
    #     assert testobj.cmddict == {'desc': 'list'}
    #     testobj.page.dialog_data['cmddict'] = {}  # restore page to original state
    #     assert capsys.readouterr().out == (f"called show_dialog with args ({testobj.page},"
    #                                        " <class 'editor.plugins.dckeys_qt.DcCompleteDialog'>)\n")
    #     monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
    #     assert testobj.add_missing_descriptions([('desc', 'list')]) == [('desc', 'list')]
    #     assert testobj.cmddict == {'desc': 'list'}
    #     assert capsys.readouterr().out == (f"called show_dialog with args ({testobj.page},"
    #                                        " <class 'editor.plugins.dckeys_qt.DcCompleteDialog'>)\n")

    def test_compare_descriptions(self, monkeypatch, capsys):
        """unittest for CsvBuilder.add_missing_descriptions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cmddict = {}
        olddescs = {}
        testobj.compare_descriptions(olddescs)
        assert not testobj.cmddict
        assert not testobj.olddescs
        testobj.cmddict = {'x': 'y', 'p': 'q', 'g': 'h', 'k': ''}
        olddescs = {'a': 'b', 'p': 'r', 'g': 'h', 'k': 'l'}
        testobj.compare_descriptions(olddescs)
        assert testobj.cmddict == {'x': 'y', 'p': 'q', 'g': 'h', 'k': 'l'}
        assert testobj.olddescs == {'a': 'b', 'p': 'r'}

    def test_assemble_shortcuts(self, monkeypatch, capsys):
        """unittest for CsvBuilder.assemble_shortcuts
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.definedkeys = {}
        testobj.stdkeys = {}
        testobj.shortcuts = {}
        testobj.defaults = {}
        testobj.cmddict = {}
        testobj.tbcmddict = {}
        testobj.unlisted_cmds = []
        testobj.tobematched = {}
        testobj.assemble_shortcuts()
        assert testobj.tobematched == {}
        assert testobj.cmddict == {}
        assert testobj.shortcuts == {}
        testobj.definedkeys = {('x', 'y', 'z'): {'cmd': 'cmnd', 'param': 'parm', 'ctrl': 'control'}}
        testobj.stdkeys = {'stdkey': 'stdkeydesc'}
        testobj.assemble_shortcuts()
        assert testobj.tobematched == {}
        assert testobj.unlisted_cmds == ['cmnd']
        assert testobj.cmddict == {'cmnd': ''}
        assert testobj.shortcuts == {('x', 'y', 'z'): {'cmd': 'cmnd', 'param': 'parm',
                                                       'ctrl': 'control', 'standard': ''},
                                     'stdkey': {'cmd': '', 'param': '', 'ctrl': '',
                                                'standard': 'S', 'desc': 'stdkeydesc'}}
        testobj.definedkeys = {('x', 'y', 'z'): {'cmd': 'cmnd', 'param': 'parm', 'ctrl': 'control'}}
        testobj.stdkeys = {'stdkey': 'stdkeydesc'}
        testobj.defaults = {('x', 'y'): {('z', 'cmnd')}}
        testobj.assemble_shortcuts()
        assert testobj.tobematched == {}
        assert testobj.unlisted_cmds == ['cmnd']
        assert testobj.cmddict == {'cmnd': ''}
        assert testobj.shortcuts == {('x', 'y', 'z'): {'cmd': 'cmnd', 'param': 'parm',
                                                       'ctrl': 'control', 'standard': 'S'},
                                     'stdkey': {'cmd': '', 'param': '', 'ctrl': '',
                                                'standard': 'S', 'desc': 'stdkeydesc'}}
        testobj.stdkeys = {}
        testobj.cmddict = {}
        testobj.defaults = {('x', 'y'): {('u', 'cmnd')}}
        testobj.stdkeys = {'stdkey': 'stdkeydesc'}
        testobj.shortcuts = {'stdkey': 'xxx'}
        testobj.definedkeys = {('x', 'y', 'z'): {'cmd': 'cm_ExecuteToolbarItem',
                                                 'param': 'context=TfrmOptionsToobar;'
                                                 'ToolBarID=TBI;ToolItemID=TII',
                                                 'ctrl': 'control', 'standard': 'S'}}
        testobj.tbcmddict = {('TBI', 'TII'): ['TBoms', 'TBcmd', 'TBparm']}
        testobj.unlisted_cmds = []
        testobj.assemble_shortcuts()
        assert testobj.tobematched == {}
        assert testobj.unlisted_cmds == []
        assert testobj.cmddict == {}
        assert testobj.shortcuts == {'stdkey': 'xxx', ('x', 'y', 'z'): {
            'cmd': 'cm_ExecuteToolbarItem',
            'param': 'context=TfrmOptionsToobar;ToolBarID=TBI;ToolItemID=TII',
            'ctrl': 'control', 'standard': 'U', 'desc': 'TBoms (TBcmd TBparm)'}}
        testobj.definedkeys = {('x', 'y', 'z'): {'cmd': 'cmnd', 'param': 'parm', 'ctrl': 'control'},
                               ('a', 'b', 'c'): {'cmd': 'c'},
                               ('d', 'e', 'f'): {'cmd': 'd'},
                               ('p', 'q', 'r'): {'cmd': 'xxx', 'desc': 'this'}}
        testobj.cmddict = {'c': 'something', 'xxx': 'this', 'd': 'it'}
        testobj.stdkeys = {('x', 'y', 'z'): 'stdkey', ('p', 'q', 'r'): 'yyy', ('d', 'e', 'f'): 'it'}
        testobj.defaults = {('x', 'y'): {('u', 'cmnd')}}
        testobj.shortcuts = {}
        testobj.assemble_shortcuts()
        assert testobj.tobematched == {('p', 'q', 'r'): {'stdkeys_oms': 'yyy',
                                                         'cmddict_oms': 'this'}}
        assert testobj.unlisted_cmds == ['cmnd']
        assert testobj.cmddict == {'c': 'something', 'cmnd': 'stdkey', 'xxx': 'this', 'd': 'it'}
        assert testobj.shortcuts == {('x', 'y', 'z'): {'cmd': 'cmnd', 'param': 'parm',
                                                       'ctrl': 'control', 'standard': 'S',
                                                       'desc': 'stdkey'},
                                     ('a', 'b', 'c'): {'cmd': 'c', 'standard': '',
                                                       'desc': 'something'},
                                     ('d', 'e', 'f'): {'cmd': 'd', 'standard': 'S', 'desc': 'it'},
                                     ('p', 'q', 'r'): {'cmd': 'xxx', 'standard': 'S',
                                                       'desc': 'this'}}

    def test_format_shortcuts(self, monkeypatch, capsys):
        """unittest for CsvBuilder.format_shortcuts
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.shortcuts = {}
        testobj.format_shortcuts()
        assert not testobj.shortcuts
        testobj.shortcuts = {('x', 'y', 'z'): {'standard': 's', 'cmd': 'c', 'param': 'p',
                                               'ctrl': 'ct'},
                             ('a', 'b', 'c'): {'standard': 'st', 'cmd': 'cm', 'param': 'pm',
                                               'ctrl': 'ct', 'desc': 'de'}}
        testobj.unlisted_cmds = []
        testobj.cmddict = {'c': '', 'cm': 'de'}
        testobj.format_shortcuts()
        assert testobj.shortcuts == {1: ('x', 'y', 's', 'z', 'c', 'p', 'ct', ''),
                                     2: ('a', 'b', 'st', 'c', 'cm', 'pm', 'ct', 'de')}
        assert testobj.unlisted_cmds == ['c']
        testobj.shortcuts = {('x', 'y', 'z'): {'standard': 's', 'cmd': 'c', 'param': 'p',
                                               'ctrl': 'ct'},
                             ('a', 'b', 'c'): {'standard': 'st', 'cmd': 'cm', 'param': 'pm',
                                               'ctrl': 'ct', 'desc': 'de'}}
        testobj.unlisted_cmds = []
        testobj.cmddict = {'c': 'xx', 'cm': 'yy'}
        testobj.format_shortcuts()
        assert testobj.shortcuts == {1: ('x', 'y', 's', 'z', 'c', 'p', 'ct', 'xx'),
                                     2: ('a', 'b', 'st', 'c', 'cm', 'pm', 'ct', 'yy')}
        assert not testobj.unlisted_cmds


def test_update_otherstuff_inbound():
    """unittest for dckeys.update_otherstuff_inbound
    """
    otherstuff = {'stdkeys': {}, 'defaults': {}}
    assert testee.update_otherstuff_inbound(otherstuff) == {'stdkeys': {}, 'defaults': {}}
    otherstuff = {'stdkeys': {'x y': 'z', 'a b c': 'dd', 'q  r': 's', 'D (1) A XX': '...'},
                  'defaults': {'a': 'b', 'x y  z   q r': 's'}}
    assert testee.update_otherstuff_inbound(otherstuff) == {
            'stdkeys': {('x', 'y'): 'z', ('a', 'b', 'c'): 'dd', ('q', '', 'r'): 's',
                        ('D (1)', 'A', 'XX'): '...'},
            'defaults': {('a',): 'b', ('x', 'y', '', 'z', '', '', 'q', 'r'): 's'}}


def test_update_otherstuff_outbound():
    """unittest for dckeys.update_otherstuff_outbound
    """
    otherstuff = {'stdkeys': {}, 'defaults': {}}
    assert testee.update_otherstuff_outbound(otherstuff) == {'stdkeys': {}, 'defaults': {}}
    otherstuff = {'stdkeys': {('x', 'y'): 'z', ('a', 'b', 'c'): {'d', 'e'}, ('q', '', 'r'): 's'},
                  'defaults': {('a',): 'b', ('x', 'y', '', 'z', '', '', 'q', 'r'): {'s', 't'}}}
    assert testee.update_otherstuff_outbound(otherstuff) == {
            'stdkeys': {'x y': 'z', 'a b c': ['d', 'e'], 'q  r': 's'},
            'defaults': {'a': 'b', 'x y  z   q r': ['s', 't']}}


def test_build_shortcut():
    """unittest for dckeys.build_shortcut
    """
    assert testee.build_shortcut('a', '') == "A"
    assert testee.build_shortcut('B', 'WASC') == "Ctrl+Shift+Alt+WinKey+B"
    assert testee.build_shortcut('anything', 'caws') == "Anything"
    assert testee.build_shortcut('anything', 'else') == "Anything"


def test_savekeys(monkeypatch, capsys):
    """unittest for dckeys.savekeys
    """
    def mock_show(*args, **kwargs):
        print('called show_cancel_message with args', args, kwargs)
        return False
    def mock_show_2(*args, **kwargs):
        print('called show_cancel_message with args', args, kwargs)
        return True
    def mock_get(*args, **kwargs):
        print('called get_file_to_save with args', args, kwargs)
        return ''
    def mock_get_2(*args, **kwargs):
        print('called get_file_to_save with args', args, kwargs)
        return 'filename'
    def mock_build(*args):
        print('called build_shortcut with args', args)
        return '+'.join(args)
    def mock_copy(*args):
        print('shutil.copyfile with args', args)
    class MockSDI:
        "stub for SimgleDataInterface object"
    class MockElement:
        "stub for ElementTree.Element object"
        def __init__(self, name, **attrs):
            print(f"called ET.Element.__init__ with args ('{name}',)", attrs)
            self.name = name
            self.children = []
            self.attrib = {x: attrs[x] for x in attrs}
        def find(self, name):
            print(f"called ET.Element.find with arg {name}")
            for child in self.children:
                if child.name == name:
                    return child
            else:
                return None
    def MockSubElement(obj, name, **attrs):
        "stub for ElementTree.SubElement object factory"
        print(f"called ET.SubElement with args(<Element '{obj.name}'>, '{name}')", attrs)
        result = MockElement(name, **attrs)
        obj.children.append(result)
        return result
    class MockElementTree:
        "stub for ElementTree.ElementTree object"
        def __init__(self, root):
            print(f"called ET.ElementTree.__init__ with arg <Element '{root.name}'>")
            self.root = root
        def write(self, *args, **kwargs):
            print('called ET.ElementTree.write with args', args, kwargs)
        def getroot(self):
            print('called ET.ElementTree.getroot')
            return self.root
    def mock_parse(self, *args):
        print('called ET.ElementTree.parse with args', args)
        root = MockElement('doublecmd', DCVersion='dcv')
        head = MockSubElement(root, 'Hotkeys', Version='ver')
        return MockElementTree(root)
    monkeypatch.setattr(testee, 'show_cancel_message', mock_show)
    monkeypatch.setattr(testee, 'get_file_to_save', mock_get)
    monkeypatch.setattr(testee, 'build_shortcut', mock_build)
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
    monkeypatch.setattr(testee.ET, 'Element', MockElement)
    monkeypatch.setattr(testee.ET, 'SubElement', MockSubElement)
    monkeypatch.setattr(testee.ET, 'ElementTree', MockElementTree)
    monkeypatch.setattr(testee.ET, 'parse', mock_parse)
    monkeypatch.setattr(testee, 'how_to_save', 'how to save')
    page = types.SimpleNamespace(data={}, settings={'DC_PATH': 'xxx'}, gui=MockSDI())
    testee.savekeys(page)
    assert capsys.readouterr().out == (
            f"called show_cancel_message with args ({page.gui},) {{'text': 'how to save'}}\n")
    monkeypatch.setattr(testee, 'show_cancel_message', mock_show_2)
    testee.savekeys(page)
    assert capsys.readouterr().out == (
            f"called show_cancel_message with args ({page.gui},) {{'text': 'how to save'}}\n"
            "called get_file_to_save with args"
            f" ({page.gui},) {{'extension': 'SCF files (*.scf)', 'start': 'xxx'}}\n")
    monkeypatch.setattr(testee, 'get_file_to_save', mock_get_2)
    testee.savekeys(page)
    assert capsys.readouterr().out == (
            f"called show_cancel_message with args ({page.gui},) {{'text': 'how to save'}}\n"
            "called get_file_to_save with args"
            f" ({page.gui},) {{'extension': 'SCF files (*.scf)', 'start': 'xxx'}}\n"
            "called ET.ElementTree.parse with args ()\n"
            "called ET.Element.__init__ with args ('doublecmd',) {'DCVersion': 'dcv'}\n"
            "called ET.SubElement with args(<Element 'doublecmd'>, 'Hotkeys')"
            " {'Version': 'ver'}\n"
            "called ET.Element.__init__ with args ('Hotkeys',) {'Version': 'ver'}\n"
            "called ET.ElementTree.__init__ with arg <Element 'doublecmd'>\n"
            "called ET.ElementTree.getroot\n"
            "called ET.Element.find with arg Hotkeys\n"
            "called ET.Element.__init__ with args ('doublecmd',) {'DCVersion': 'dcv'}\n"
            "called ET.SubElement with args(<Element 'doublecmd'>, 'Hotkeys')"
            " {'Version': 'ver'}\n"
            "called ET.Element.__init__ with args ('Hotkeys',) {'Version': 'ver'}\n"
            "shutil.copyfile with args ('filename', 'filename.bak')\n"
            "called ET.ElementTree.__init__ with arg <Element 'doublecmd'>\n"
            "called ET.ElementTree.write with args"
            " ('filename',) {'encoding': 'UTF-8', 'xml_declaration': True}\n")
    page.data = {1: ['key1', 'mods', 'kind', 'context', 'command', '', '', 'desc1'],
               2: ['key2', 'mods', 'kind', 'context', 'command2', 'parm', 'ctrl', 'desc2'],
               3: ['key3', 'mods', 'kind', 'cntxt', 'command3', 'parm', 'ctrl', 'desc3']}
    testee.savekeys(page)
    assert capsys.readouterr().out == (
            f"called show_cancel_message with args ({page.gui},) {{'text': 'how to save'}}\n"
            "called get_file_to_save with args"
            f" ({page.gui},) {{'extension': 'SCF files (*.scf)', 'start': 'xxx'}}\n"
            "called ET.ElementTree.parse with args ()\n"
            "called ET.Element.__init__ with args ('doublecmd',) {'DCVersion': 'dcv'}\n"
            "called ET.SubElement with args(<Element 'doublecmd'>, 'Hotkeys')"
            " {'Version': 'ver'}\n"
            "called ET.Element.__init__ with args ('Hotkeys',) {'Version': 'ver'}\n"
            "called ET.ElementTree.__init__ with arg <Element 'doublecmd'>\n"
            "called ET.ElementTree.getroot\n"
            "called ET.Element.find with arg Hotkeys\n"
            "called ET.Element.__init__ with args ('doublecmd',) {'DCVersion': 'dcv'}\n"
            "called ET.SubElement with args(<Element 'doublecmd'>, 'Hotkeys')"
            " {'Version': 'ver'}\n"
            "called ET.Element.__init__ with args ('Hotkeys',) {'Version': 'ver'}\n"
            "called ET.SubElement with args(<Element 'Hotkeys'>, 'Form') {'Name': 'cntxt'}\n"
            "called ET.Element.__init__ with args ('Form',) {'Name': 'cntxt'}\n"
            "called ET.SubElement with args(<Element 'Form'>, 'Hotkey') {}\n"
            "called ET.Element.__init__ with args ('Hotkey',) {}\n"
            "called ET.SubElement with args(<Element 'Hotkey'>, 'Shortcut') {}\n"
            "called ET.Element.__init__ with args ('Shortcut',) {}\n"
            "called build_shortcut with args ('key3', 'mods')\n"
            "called ET.SubElement with args(<Element 'Hotkey'>, 'Command') {}\n"
            "called ET.Element.__init__ with args ('Command',) {}\n"
            "called ET.SubElement with args(<Element 'Hotkey'>, 'Param') {}\n"
            "called ET.Element.__init__ with args ('Param',) {}\n"
            "called ET.SubElement with args(<Element 'Hotkey'>, 'Control') {}\n"
            "called ET.Element.__init__ with args ('Control',) {}\n"
            "called ET.SubElement with args(<Element 'Hotkeys'>, 'Form') {'Name': 'context'}\n"
            "called ET.Element.__init__ with args ('Form',) {'Name': 'context'}\n"
            "called ET.SubElement with args(<Element 'Form'>, 'Hotkey') {}\n"
            "called ET.Element.__init__ with args ('Hotkey',) {}\n"
            "called ET.SubElement with args(<Element 'Hotkey'>, 'Shortcut') {}\n"
            "called ET.Element.__init__ with args ('Shortcut',) {}\n"
            "called build_shortcut with args ('key1', 'mods')\n"
            "called ET.SubElement with args(<Element 'Hotkey'>, 'Command') {}\n"
            "called ET.Element.__init__ with args ('Command',) {}\n"
            "called ET.SubElement with args(<Element 'Form'>, 'Hotkey') {}\n"
            "called ET.Element.__init__ with args ('Hotkey',) {}\n"
            "called ET.SubElement with args(<Element 'Hotkey'>, 'Shortcut') {}\n"
            "called ET.Element.__init__ with args ('Shortcut',) {}\n"
            "called build_shortcut with args ('key2', 'mods')\n"
            "called ET.SubElement with args(<Element 'Hotkey'>, 'Command') {}\n"
            "called ET.Element.__init__ with args ('Command',) {}\n"
            "called ET.SubElement with args(<Element 'Hotkey'>, 'Param') {}\n"
            "called ET.Element.__init__ with args ('Param',) {}\n"
            "called ET.SubElement with args(<Element 'Hotkey'>, 'Control') {}\n"
            "called ET.Element.__init__ with args ('Control',) {}\n"
            "shutil.copyfile with args ('filename', 'filename.bak')\n"
            "called ET.ElementTree.__init__ with arg <Element 'doublecmd'>\n"
            "called ET.ElementTree.write with args"
            " ('filename',) {'encoding': 'UTF-8', 'xml_declaration': True}\n")


def test_savekeys_2(monkeypatch, capsys, tmp_path):
    """unittest for dckeys.savekeys  - ElementTree niet gesimuleerd
    """
    def mock_show(*args, **kwargs):
        print('called show_cancel_message with args', args, kwargs)
        return True
    def mock_get(*args, **kwargs):
        print('called get_file_to_save with args', args, kwargs)
        return str(filename)
    def mock_build(*args):
        print('called build_shortcut with args', args)
        return '+'.join(args)
    def mock_copy(*args):
        print('shutil.copyfile with args', args)
    class MockSDI:
        "stub for SimgleDataInterface object"
    filename = tmp_path / 'testfile'
    filename.write_text('<doublecmd DCVersion="0.6.6 beta"><Hotkeys Version="20"/></doublecmd>')
    monkeypatch.setattr(testee, 'show_cancel_message', mock_show)
    monkeypatch.setattr(testee, 'get_file_to_save', mock_get)
    monkeypatch.setattr(testee, 'build_shortcut', mock_build)
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
    monkeypatch.setattr(testee, 'how_to_save', 'how to save')
    page = types.SimpleNamespace(settings={'DC_PATH': 'xxx'}, gui=MockSDI(), data={
        1: ['key1', 'mods', 'kind', 'context', 'command', '', '', 'desc1'],
        2: ['key2', 'mods', 'kind', 'context', 'command2', 'parm', 'ctrl', 'desc2'],
        3: ['key3', 'mods', 'kind', 'cntxt', 'command3', 'parm', 'ctrl', 'desc3']})
    testee.savekeys(page)
    assert filename.exists()
    assert filename.read_text() == (
            "<?xml version='1.0' encoding='UTF-8'?>\n"
            '<doublecmd DCVersion="0.6.6 beta"><Hotkeys Version="20">'
            '<Form Name="cntxt">'
            '<Hotkey><Shortcut>key3+mods</Shortcut><Command>command3</Command>'
            '<Param>parm</Param><Control>ctrl</Control></Hotkey></Form>'
            '<Form Name="context">'
            '<Hotkey><Shortcut>key1+mods</Shortcut><Command>command</Command></Hotkey>'
            '<Hotkey><Shortcut>key2+mods</Shortcut><Command>command2</Command>'
            '<Param>parm</Param><Control>ctrl</Control></Hotkey></Form></Hotkeys></doublecmd>')
    assert capsys.readouterr().out == (
            f"called show_cancel_message with args ({page.gui},) {{'text': 'how to save'}}\n"
            "called get_file_to_save with args"
            f" ({page.gui},) {{'extension': 'SCF files (*.scf)', 'start': 'xxx'}}\n"
            "called build_shortcut with args ('key3', 'mods')\n"
            "called build_shortcut with args ('key1', 'mods')\n"
            "called build_shortcut with args ('key2', 'mods')\n"
            f"shutil.copyfile with args ('{filename}', '{filename}.bak')\n")


def test_add_extra_attributes():
    """unittest for dckeys.add_extra_attributes
    """
    win = types.SimpleNamespace(otherstuff={'cmddict': {'z': 'zzz', 'x': 'xxx', 'y': 'yyy'},
                                            'contexts': ['aa', 'bb'], 'restrictions': ['q', 'r']})
    testee.add_extra_attributes(win)
    assert win.commandslist == ['x', 'y', 'z']
    assert win.descriptions == {'z': 'zzz', 'x': 'xxx', 'y': 'yyy'}
    assert win.contextslist == ['aa', 'bb']
    assert win.contextactionsdict == {'aa': ['x', 'y', 'z'], 'bb': ['x', 'y', 'z']}
    assert win.controlslist == ['q', 'r']


def test_get_frameheight():
    """unittest for dckeys.get_frameheight
    """
    assert testee.get_frameheight() == 120

def test_update_descriptions(monkeypatch):
    """unittest for dckeys.update_descriptions
    """
    win = types.SimpleNamespace(data={'x': ('a', 'b', 'd', 'e', 'f', 'g')}, otherstuff={})
    testee.update_descriptions(win, {'y': 'z'})
    assert win.otherstuff['cmddict'] == {'y': 'z'}
    assert win.descriptions == {'y': 'z'}
    assert win.data['x'] == ('a', 'b', 'd', 'e', 'f', 'g')
    win = types.SimpleNamespace(data={'x': ('a', 'b', 'd', 'e', 'f', 'g')}, otherstuff={})
    testee.update_descriptions(win, {'f': 'z'})
    assert win.otherstuff['cmddict'] == {'f': 'z'}
    assert win.descriptions == {'f': 'z'}
    assert win.data['x'] == ('a', 'b', 'd', 'e', 'f', 'z')
    win = types.SimpleNamespace(data={'x': ('a', 'b', 'd', 'e', 'f', 'g')}, otherstuff={})
    testee.update_descriptions(win, {'f': 'g'})
    assert win.otherstuff['cmddict'] == {'f': 'g'}
    assert win.descriptions == {'f': 'g'}
    assert win.data['x'] == ('a', 'b', 'd', 'e', 'f', 'g')
