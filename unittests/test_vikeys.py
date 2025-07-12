"""unittests for ./editor/plugins/vikeys.py
"""
import types
from editor.plugins import vikeys as testee


def test_convert_key():
    """unittest for vikeys.convert_key
    """
    for text in ('Left', 'Up', 'Right', 'Down', 'Home', 'End', 'Help', 'Undo', 'F1', 'Del', 'Space'):
        assert testee.convert_key(text) == text
    assert testee.convert_key('S-PageDown') =='PgDn shift'
    assert testee.convert_key('C-PageUp') =='PgUp ctrl'
    assert testee.convert_key('Esc') =='esc'
    assert testee.convert_key('Tab') =='Tab'
    assert testee.convert_key('BS') =='Backspace'
    assert testee.convert_key('CR') =='Enter'
    assert testee.convert_key('NL') =='Return'
    assert testee.convert_key('Insert') =='Ins'
    assert testee.convert_key('MiddleMouse') =='mmb'
    assert testee.convert_key('LeftMouse') =='lmb'
    assert testee.convert_key('RightMouse') =='rmb'
    assert testee.convert_key('ScrollWheelUp') =='WhlUp'
    assert testee.convert_key('ScrollWheelDown') =='WhlDn'
    assert testee.convert_key('ScrollWheelLeft') =='WhlLeft'
    assert testee.convert_key('ScrollWheelRight') =='WhlRight'


class TestDefaultKeys:
    """unittest for vikeys.DefaultKeys
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for vikeys.DefaultKeys object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called DefaultKeys.__init__ with args', args)
        monkeypatch.setattr(testee.DefaultKeys, '__init__', mock_init)
        testobj = testee.DefaultKeys()
        assert capsys.readouterr().out == 'called DefaultKeys.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for DefaultKeys.__init__
        """
        def mock_read(self):
            print('called DefaultKeys.read_data')
        def mock_parse(self):
            print('called DefaultKeys.parse_data')
            return {}, {}
        def mock_parse_2(self):
            print('called DefaultKeys.parse_data')
            return ({'x': ['k', 'b', 'a'], 'y': ['k', 'b', 'a']},
                    {'x': {'q': ['i', 'v']}, 'y': {'Normal mode': 'v'}})
        monkeypatch.setattr(testee.DefaultKeys, 'read_data', mock_read)
        monkeypatch.setattr(testee.DefaultKeys, 'parse_data', mock_parse)
        testobj = testee.DefaultKeys('path')
        assert testobj.path == 'path'
        assert testobj.data == []
        assert testobj.category == ''
        assert testobj.command == ''
        assert testobj.keydefs == {}
        assert testobj.contexts == testee.CONTEXTS
        assert testobj.kinds == testee.KINDS
        assert capsys.readouterr().out == ('called DefaultKeys.read_data\n'
                                           'called DefaultKeys.parse_data\n')
        monkeypatch.setattr(testee.DefaultKeys, 'parse_data', mock_parse_2)
        testobj = testee.DefaultKeys('path')
        assert testobj.path == 'path'
        assert testobj.data == []
        assert testobj.category == ''
        assert testobj.command == ''
        assert testobj.keydefs == {1: ('k', '', 'b', 'a', 'q', ['i', 'v']),
                                   2: ('k', 'Normal mode', 'b', 'a', '', 'v')}
        assert testobj.contexts == testee.CONTEXTS
        assert testobj.kinds == testee.KINDS
        assert capsys.readouterr().out == ('called DefaultKeys.read_data\n'
                                           'called DefaultKeys.parse_data\n')

    def test_read_data(self, monkeypatch, capsys, tmp_path):
        """unittest for DefaultKeys.read_data
        """
        def mock_parse(line):
            print(f"called DefaultKeys.parse_line with arg '{line}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.path = tmp_path / 'read_data_tst'
        testobj.parse_line = mock_parse
        testobj.category = testobj.command = ''
        testobj.data = []
        testobj.path.touch()
        testobj.read_data()
        assert testobj.data == [('', '')]
        assert capsys.readouterr().out == ""
        monkeypatch.setattr(testee, 'EXCMD', 'qrst')
        monkeypatch.setattr(testee, 'CATEGORYLIST', [('1 xxx', ''), ('2 yyy', 'zzz'),
                                                     (f'3 {testee.EXCMD}', '')])
        testobj.path.write_text(('bladibla\n'
                                 '=====i=====\n\n1 xxx     ...\n-----------\n'
                                 '\nline-to-parse\n'
                                 '===========\n\n2 yyyyyyyyyyy\n-----------\n'
                                 '\nnext-line-to-parse\nanother-line-to-parse\n\nbladibla\n\n'
                                 f'===========\n\n3 {testee.EXCMD}\n-----------\n'
                                 '\nno-more-line-parsing\n'))
        testobj.category = testobj.command = ''
        testobj.data = []
        testobj.read_data()
        assert testobj.data == [('zzz', '')]
        assert capsys.readouterr().out == (
                "called DefaultKeys.parse_line with arg 'line-to-parse'\n"
                "called DefaultKeys.parse_line with arg 'next-line-to-parse'\n"
                "called DefaultKeys.parse_line with arg 'another-line-to-parse'\n"
                "called DefaultKeys.parse_line with arg 'bladibla'\n")
        # eerst testmethode maken, dan self.category vervangen
        # eigenlijk command ook maar die wordt in parse_line niet alleen gelezen maar ook aangepast

    def test_parse_line(self, monkeypatch, capsys):
        """unittest for DefaultKeys.parse_line
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.data = []
        testobj.command = ''
        testobj.add_line = True
        testobj.parse_line('')
        assert not testobj.add_line
        assert not testobj.command
        assert not testobj.data
        testobj.parse_line('hello\t\thello')
        assert not testobj.add_line
        assert not testobj.command
        assert not testobj.data
        testobj.add_line = True
        testobj.parse_line('hello\t\thello')
        assert testobj.add_line
        assert not testobj.command
        assert not testobj.data
        testobj.add_line = False
        testobj.parse_line('hello\thello\thello')
        assert not testobj.add_line
        assert not testobj.command
        assert not testobj.data
        testobj.add_line = True
        testobj.command = []
        testobj.parse_line('hello\thello\thello')
        assert testobj.add_line
        assert testobj.command == ['hello', 'hello', 'hello']  # is dit wat ik wil
        assert not testobj.data                                # of gebeurt dit nooit

        testobj.command = ''
        testobj.parse_line('|abc')
        assert testobj.command == ['|abc']  # komt niet voor
        assert not testobj.data
        testobj.command = ''
        testobj.parse_line('|abc|')
        assert not testobj.command
        assert not testobj.data
        testobj.parse_line('|abc\tdef\tghi')
        assert testobj.command == ['|abc', 'def', 'ghi']  # komt niet voor
        assert not testobj.data
        testobj.command = ''
        testobj.parse_line('|abc|\tdef\tghi')
        assert testobj.command == ['def', 'ghi']
        assert not testobj.data
        testobj.category = 'x'
        testobj.command = ['y', 'z']
        testobj.parse_line('|abc|\tdef\tghi')
        assert testobj.command == ['def', 'ghi']
        assert testobj.data == [('x', ['y', 'z'])]

    def test_parse_data(self, monkeypatch, capsys):
        """unittest for DefaultKeys.parse_data
        """
        def mock_parse_line_elems(arg):
            print(f'called DefaultKeys.parse_line_elems with arg {arg}')
            return arg
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parse_line_elems = mock_parse_line_elems
        testobj.data = []
        assert testobj.parse_data() == ({}, {})
        assert capsys.readouterr().out == ""
        testobj.data = [
                ('aa', ['a1', 'aaa']),
                ('bb', ['1b', 'bbb']),
                ('cc', ['cc', 'ccc']),
                ('dd', ['2d', 'ddd']),
                ('ee', ['ee', 'eee']),
                ('ff', ['3f', 'fff']),
                ('gg', ['gg', 'ggg']),
                ('hh', ['4h', 'hhh']),
                ('ii', ['ii', 'iii']),
                ('jj', ['5j', 'jjj']),
                ('kk', ['kk', 'kkk']),
                ('ll', ['6l', 'lll']),
                ('mm', ['mm', 'mmm']),
                ('nn', ['7n', 'nnn']),
                ('oo', ['oo', 'ooo']),
                ('pp', ['8p', 'ppp']),
                ('qq', ['qq', 'qqq']),
                ('rr', ['9r', 'rrr']),
                ('ss', ['ss', 'sss']),
                # ('tt', ['10t', 'ttt']), # deze gaat desc1 ('?') overschrijven
                ('uu', ['bb', 'cc'])]
        assert testobj.parse_data() == (
                {1: 'a1', 2: '1b', 3: 'cc', 4: '2d', 5: 'ee', 6: '3f', 7: 'gg', 8: '4h', 9: 'ii',
                 10: '5j', 11: 'kk', 12: '6l', 13: 'mm', 14: '7n', 15: 'oo', 16: '8p', 17: 'qq',
                 18: '9r', 19: 'ss', 20: '10t', 20: 'bb'},
                {1: {'aa': 'aaa'}, 2: {'bb': 'bbb'}, 3: {'cc': 'ccc'}, 4: {'dd': '?'},
                 5: {'ee': 'eee'}, 6: {'ff': '?'}, 7: {'gg': 'ggg'}, 8: {'hh': '?'},
                 9: {'ii': 'iii'}, 10: {'jj': '?'}, 11: {'kk': 'kkk'}, 12: {'ll': '?'},
                 13: {'mm': 'mmm'}, 14: {'nn': '?'}, 15: {'oo': 'ooo'}, 16: {'pp': '?'},
                 17: {'qq': 'qqq'}, 18: {'rr': '?'}, 19: {'ss': 'sss'}, 20: {'tt': '?'},
                 20: {'uu': 'cc'}})
        assert capsys.readouterr().out == (
                "called DefaultKeys.parse_line_elems with arg ['a1', 'aaa']\n"
                "called DefaultKeys.parse_line_elems with arg ['1b', 'bbb']\n"
                "called DefaultKeys.parse_line_elems with arg ['cc', 'ccc']\n"
                "called DefaultKeys.parse_line_elems with arg ['2d', 'ddd']\n"
                "called DefaultKeys.parse_line_elems with arg ['ee', 'eee']\n"
                "called DefaultKeys.parse_line_elems with arg ['3f', 'fff']\n"
                "called DefaultKeys.parse_line_elems with arg ['gg', 'ggg']\n"
                "called DefaultKeys.parse_line_elems with arg ['4h', 'hhh']\n"
                "called DefaultKeys.parse_line_elems with arg ['ii', 'iii']\n"
                "called DefaultKeys.parse_line_elems with arg ['5j', 'jjj']\n"
                "called DefaultKeys.parse_line_elems with arg ['kk', 'kkk']\n"
                "called DefaultKeys.parse_line_elems with arg ['6l', 'lll']\n"
                "called DefaultKeys.parse_line_elems with arg ['mm', 'mmm']\n"
                "called DefaultKeys.parse_line_elems with arg ['7n', 'nnn']\n"
                "called DefaultKeys.parse_line_elems with arg ['oo', 'ooo']\n"
                "called DefaultKeys.parse_line_elems with arg ['8p', 'ppp']\n"
                "called DefaultKeys.parse_line_elems with arg ['qq', 'qqq']\n"
                "called DefaultKeys.parse_line_elems with arg ['9r', 'rrr']\n"
                "called DefaultKeys.parse_line_elems with arg ['ss', 'sss']\n"
                # "called DefaultKeys.parse_line_elems with arg ['10t', 'ttt']\n"
                "called DefaultKeys.parse_line_elems with arg ['bb', 'cc']\n")
        testobj.data = [
                ('aa', ['a1', 'aaa']),
                ('bb', ['bb', 'bbb']),
                ('cc', ['cc', 'ccc']),
                ('dd', ['dd', 'ddd']),
                ('ee', ['ee', 'eee']),
                ('ff', ['ff', 'fff']),
                ('gg', ['gg', 'ggg']),
                ('hh', ['hh', 'hhh']),
                ('ii', ['ii', 'iii']),
                ('jj', ['jj', 'jjj']),
                ('kk', ['kk', 'kkk']),
                ('ll', ['ll', 'lll']),
                ('mm', ['mm', 'mmm']),
                ('nn', ['nn', 'nnn']),
                ('oo', ['oo', 'ooo']),
                ('pp', ['pp', 'ppp']),
                ('qq', ['qq', 'qqq']),
                ('rr', ['rr', 'rrr']),
                ('ss', ['ss', 'sss']),
                ('tt', ['tt', 'ttt']),
                ('uu', ['bb', 'cc'])]
        assert testobj.parse_data() == (
                {1: 'a1', 2: 'bb', 3: 'cc', 4: 'dd', 5: 'ee', 6: 'ff', 7: 'gg', 8: 'hh', 9: 'ii',
                 10: 'jj', 11: 'kk', 12: 'll', 13: 'mm', 14: 'nn', 15: 'oo', 16: 'pp', 17: 'qq',
                 18: 'rr', 19: 'ss', 20: 'tt', 21: 'bb'},
                {1: {'aa': 'aaa'}, 2: {'bb': 'bbb'}, 3: {'cc': 'ccc'}, 4: {'dd': 'ddd'},
                 5: {'ee': 'eee'}, 6: {'ff': 'fff'}, 7: {'gg': 'ggg'}, 8: {'hh': 'hhh'},
                 9: {'ii': 'iii'}, 10: {'jj': 'jjj'}, 11: {'kk': 'kkk'}, 12: {'ll': 'lll'},
                 13: {'mm': 'mmm'}, 14: {'nn': 'nnn'}, 15: {'oo': 'ooo'}, 16: {'pp': 'ppp'},
                 17: {'qq': 'qqq'}, 18: {'rr': 'rrr'}, 19: {'ss': 'sss'}, 20: {'tt': 'ttt'},
                 21: {'uu': 'cc'}})
        assert capsys.readouterr().out == (
                "called DefaultKeys.parse_line_elems with arg ['a1', 'aaa']\n"
                "called DefaultKeys.parse_line_elems with arg ['bb', 'bbb']\n"
                "called DefaultKeys.parse_line_elems with arg ['cc', 'ccc']\n"
                "called DefaultKeys.parse_line_elems with arg ['dd', 'ddd']\n"
                "called DefaultKeys.parse_line_elems with arg ['ee', 'eee']\n"
                "called DefaultKeys.parse_line_elems with arg ['ff', 'fff']\n"
                "called DefaultKeys.parse_line_elems with arg ['gg', 'ggg']\n"
                "called DefaultKeys.parse_line_elems with arg ['hh', 'hhh']\n"
                "called DefaultKeys.parse_line_elems with arg ['ii', 'iii']\n"
                "called DefaultKeys.parse_line_elems with arg ['jj', 'jjj']\n"
                "called DefaultKeys.parse_line_elems with arg ['kk', 'kkk']\n"
                "called DefaultKeys.parse_line_elems with arg ['ll', 'lll']\n"
                "called DefaultKeys.parse_line_elems with arg ['mm', 'mmm']\n"
                "called DefaultKeys.parse_line_elems with arg ['nn', 'nnn']\n"
                "called DefaultKeys.parse_line_elems with arg ['oo', 'ooo']\n"
                "called DefaultKeys.parse_line_elems with arg ['pp', 'ppp']\n"
                "called DefaultKeys.parse_line_elems with arg ['qq', 'qqq']\n"
                "called DefaultKeys.parse_line_elems with arg ['rr', 'rrr']\n"
                "called DefaultKeys.parse_line_elems with arg ['ss', 'sss']\n"
                "called DefaultKeys.parse_line_elems with arg ['tt', 'ttt']\n"
                "called DefaultKeys.parse_line_elems with arg ['bb', 'cc']\n")

    def test_parse_line_elems(self, monkeypatch, capsys):
        """unittest for DefaultKeys.parse_line_elems
        """
        def mock_delimited(self, value):
            print(f"called Processor.check_for_and_process_delimiters with arg '{value}'")
            self.components = []
            self.pre_params = []
            self.post_params = []
            return value
        def mock_delimited_2(self, value):
            print(f"called Processor.check_for_and_process_delimiters with arg '{value}'")
            self.components = ['qqq', 'rrr']
            self.pre_params = ['aaa', 'bbb']
            self.post_params = ['yyy', 'zzz']
            return value
        def mock_dash(value):
            print(f"called Processor.process_dash with arg '{value}'")
            return '' # value
        def mock_rest(value):
            print(f"called Processor.process_rest with arg '{value}'")
            return '', ''
        def mock_rest_2(value):
            print(f"called Processor.process_rest with arg '{value}'")
            return value, ''
        monkeypatch.setattr(testee.DefaultKeys, 'check_for_and_process_delimited', mock_delimited)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.process_dash = mock_dash
        testobj.process_rest = mock_rest
        assert testobj.parse_line_elems(['xxx']) == (('', '', ''), '')  # ('xxx', '')
        assert capsys.readouterr().out == (
                "called Processor.check_for_and_process_delimiters with arg 'xxx'\n"
                "called Processor.process_rest with arg 'xxx'\n")
        assert testobj.parse_line_elems(['xxx', ' yyy ']) == (('', '', ''), 'yyy')
        assert capsys.readouterr().out == (
                "called Processor.check_for_and_process_delimiters with arg 'xxx'\n"
                "called Processor.process_rest with arg 'xxx'\n")
        testobj.process_rest = mock_rest_2
        assert testobj.parse_line_elems(['CTRL x', ' 1 yyy ']) == (('x ctrl', '', ''), 'yyy')
        assert capsys.readouterr().out == (
                "called Processor.check_for_and_process_delimiters with arg 'CTRL x'\n")
        assert testobj.parse_line_elems(['X', ' 2 yyy ']) == (('x shift', '', ''), 'yyy')
        assert capsys.readouterr().out == (
                "called Processor.check_for_and_process_delimiters with arg 'X'\n")
        assert testobj.parse_line_elems(["'wildchar' x", ' yyy ']) == (('', '', ''), 'x yyy')
        assert capsys.readouterr().out == (
                "called Processor.check_for_and_process_delimiters with arg ''wildchar' x'\n"
                "called Processor.check_for_and_process_delimiters with arg 'x'\n"
                "called Processor.process_rest with arg 'x'\n")
        monkeypatch.setattr(testee.DefaultKeys, 'check_for_and_process_delimited', mock_delimited_2)
        assert testobj.parse_line_elems(['-xxx', ' 1/2 yyy ']) == (('qqq + rrr', '[aaa] [bbb]',
                                                               '{yyy} {zzz}'), 'yyy')
        assert capsys.readouterr().out == (
                "called Processor.check_for_and_process_delimiters with arg '-xxx'\n"
                "called Processor.process_dash with arg '-xxx'\n")

    def test_check_for_and_process_delimited(self, monkeypatch, capsys):
        """unittest for DefaultKeys.process_parms
        """
        def mock_convert(arg):
            print(f"called convert_key with arg '{arg}'")
            return arg
        monkeypatch.setattr(testee, 'convert_key', mock_convert)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.components = []
        testobj.pre_params = []
        testobj.post_params = []
        assert testobj.check_for_and_process_delimited('value') == 'value'
        assert not testobj.components
        assert not testobj.pre_params
        assert not testobj.post_params
        assert capsys.readouterr().out == ("")
        assert testobj.check_for_and_process_delimited('{value') == '{value'
        assert not testobj.components
        assert not testobj.pre_params
        assert not testobj.post_params
        assert capsys.readouterr().out == ("")
        assert testobj.check_for_and_process_delimited('<value') == '<value'
        assert not testobj.components
        assert not testobj.pre_params
        assert not testobj.post_params
        assert capsys.readouterr().out == ("")
        assert testobj.check_for_and_process_delimited('[value') == '[value'
        assert not testobj.components
        assert not testobj.pre_params
        assert not testobj.post_params
        assert capsys.readouterr().out == ("")
        assert testobj.check_for_and_process_delimited('{val}ue') == 'ue'
        assert not testobj.components
        assert testobj.pre_params == ['val']
        assert not testobj.post_params
        assert capsys.readouterr().out == ("")
        testobj.pre_params = []
        assert testobj.check_for_and_process_delimited('<valu>e') == 'e'
        assert testobj.components == ['valu']
        assert not testobj.pre_params
        assert not testobj.post_params
        assert capsys.readouterr().out == ("called convert_key with arg 'valu'\n")
        testobj.components = []
        assert testobj.check_for_and_process_delimited('[value]') == ''
        assert not testobj.components
        assert testobj.pre_params == ['value']
        assert not testobj.post_params
        assert capsys.readouterr().out == ("")
        testobj.components = ['xxx']
        testobj.pre_params = []
        assert testobj.check_for_and_process_delimited('{val}ue') == 'ue'
        assert testobj.components == ['xxx']
        assert not testobj.pre_params
        assert testobj.post_params == ['val']
        assert capsys.readouterr().out == ("")
        testobj.post_params = []
        assert testobj.check_for_and_process_delimited('{val}ue') == 'ue'
        assert testobj.components == ['xxx']
        assert not testobj.pre_params
        assert testobj.post_params == ['val']
        assert capsys.readouterr().out == ("")

    def test_process_dash(self, monkeypatch, capsys):
        """unittest for DefaultKeys.process_dash
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.components = []
        assert testobj.process_dash('xxxx') == ''
        assert testobj.components == ['xxxx']

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.components = []
        assert testobj.process_dash('xx x') == 'x'
        assert testobj.components == ['xx']

    def test_process_rest(self, monkeypatch, capsys):
        """unittest for DefaultKeys.process_rest
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.components = []
        assert testobj.process_rest('abcd efgh ijkl') == ('', 'bcd efgh ijkl')
        assert testobj.components == ['a']
        testobj.components = []
        assert testobj.process_rest('use efgh ijkl') == ('use efgh ijkl', '')
        assert testobj.components == []
        testobj.components = []
        assert testobj.process_rest('replace efgh ijkl') == ('replace efgh ijkl', '')
        assert testobj.components == []
        testobj.components = []
        assert testobj.process_rest('insert efgh ijkl') == ('insert efgh ijkl', '')
        assert testobj.components == []
        testobj.components = []
        assert testobj.process_rest('split efgh ijkl') == ('split efgh ijkl', '')
        assert testobj.components == []


def test_build_data(monkeypatch, capsys):
    """unittest for vikeys.build_data
    """
    def mock_get():
        "stub"
        print('called get_vimdoc_path')
        return ''
    def mock_get_2():
        "stub"
        print('called get_vimdoc_path')
        return 'vimpath'
    class MockDefKeys:
        "stub"
        def __init__(self, path):
            print(f"called DefaultKeys.__init__ with arg '{path}'")
            self.keydefs = {'k': ['e', 'y'], 'd': ['e', 'fs']}
            self.contexts = ['c', 't']
            self.kinds = ['kn', 'ds']
    monkeypatch.setattr(testee, 'get_vimdoc_path', mock_get)
    monkeypatch.setattr(testee, 'DefaultKeys', MockDefKeys)
    assert testee.build_data('page') == ({}, {})
    assert capsys.readouterr().out == "called get_vimdoc_path\n"
    monkeypatch.setattr(testee, 'get_vimdoc_path', mock_get_2)
    assert testee.build_data('page') == ({'k': ['e', 'y'], 'd': ['e', 'fs']},
                                         {'contexts': ['c', 't', ''], 'types': ['kn', 'ds', ''],
                                          'keylist': ['e']})
    assert capsys.readouterr().out == ("called get_vimdoc_path\n"
                                       "called DefaultKeys.__init__ with arg 'vimpath'\n")


def test_get_vimdoc_path(monkeypatch, capsys):
    """unittest for vikeys.get_vimdoc_path
    """
    def mock_iter(arg):
        "stub"
        print(f'called path.iterdir with arg {arg}')
        return ([])
    def mock_iter2(arg):
        "stub"
        print(f'called path.iterdir with arg {arg}')
        return ([testee.pathlib.Path('xxx'), testee.pathlib.Path('yyy')])
    def mock_iter3(arg):
        "stub"
        print(f'called path.iterdir with arg {arg}')
        return ([testee.pathlib.Path('xxx'), testee.pathlib.Path('yyy22')])
    def mock_isdir(arg):
        "stub"
        print(f'called path.isdir with arg {arg}')
        return False
    def mock_isdir2(arg):
        "stub"
        print(f'called path.isdir with arg {arg}')
        return True
    monkeypatch.setattr(testee.pathlib.Path, 'iterdir', mock_iter)
    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_isdir)
    assert testee.get_vimdoc_path() == ''
    assert capsys.readouterr().out == 'called path.iterdir with arg /usr/share/vim\n'
    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_isdir2)
    assert testee.get_vimdoc_path() == ''
    assert capsys.readouterr().out == 'called path.iterdir with arg /usr/share/vim\n'
    monkeypatch.setattr(testee.pathlib.Path, 'iterdir', mock_iter2)
    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_isdir)
    assert testee.get_vimdoc_path() == ''
    assert capsys.readouterr().out == ('called path.iterdir with arg /usr/share/vim\n'
                                       'called path.isdir with arg xxx\n'
                                       'called path.isdir with arg yyy\n')
    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_isdir2)
    assert testee.get_vimdoc_path() == ''
    assert capsys.readouterr().out == ('called path.iterdir with arg /usr/share/vim\n'
                                       'called path.isdir with arg xxx\n'
                                       'called path.isdir with arg yyy\n')
    monkeypatch.setattr(testee.pathlib.Path, 'iterdir', mock_iter3)
    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_isdir)
    assert testee.get_vimdoc_path() == ''
    assert capsys.readouterr().out == ('called path.iterdir with arg /usr/share/vim\n'
                                       'called path.isdir with arg xxx\n'
                                       'called path.isdir with arg yyy22\n')
    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_isdir2)
    assert testee.get_vimdoc_path() == testee.pathlib.Path('yyy22/doc/index.txt')
    assert capsys.readouterr().out == ('called path.iterdir with arg /usr/share/vim\n'
                                       'called path.isdir with arg xxx\n'
                                       'called path.isdir with arg yyy22\n')


def test_add_extra_attributes():
    """unittest for vikeys.add_extra_attributes
    """
    win = types.SimpleNamespace(otherstuff = {'keylist': ['y', 'x'], 'contexts': ['b', 'a'],
                                              'types': ['t', 's']})
    testee.add_extra_attributes(win)
    assert win.keylist == ['y', 'x']
    assert win.contextslist == ['a', 'b']
    assert win.featurelist == ['s', 't']
