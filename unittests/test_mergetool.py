"""unittests for ./plugin_examples/mergetool.py
"""
import types
from editor.plugins import mergetool as testee


def test_load_matchdata(monkeypatch, capsys, tmp_path):
    """unittest for mergetool.load_matchdata
    """
    matchfile = tmp_path / 'matches'
    assert testee.load_matchdata(matchfile) == []
    matchfile.touch()
    assert testee.load_matchdata(matchfile) == []
    matchfile.write_text('x,y,z')
    assert testee.load_matchdata(matchfile) == [['x', 'y', 'z']]


def test_save_matchdata(monkeypatch, capsys, tmp_path):
    """unittest for mergetool.save_matchdata
    """
    matchfile = tmp_path / 'matches'
    testee.save_matchdata([], matchfile)
    assert matchfile.read_text() == ''
    testee.save_matchdata([('x y', 'z'), ('a b', 'c')], matchfile)
    assert matchfile.read_text() == 'x,y,z\na,b,c\n'


class MockGui:
    "testdouble for MergeDialogGui object"
    def accept(self):
        print('called MergeDialogGui.accept')
    def add_row(self, *args):
        print('called MergeDialogGui.add_row with args', args)
        return 'row'
    def add_col_to_row(self, *args):
        print('called MergeDialogGui.add_col_to_row with args', args)
        return 'col'
    def add_row_to_col(self, *args, **kwargs):
        print('called MergeDialogGui.add_row_to_col with args', args, kwargs)
        return 'row'
    def add_listitem(self, *args):
        print('called MergeDialogGui.add_listitem with args', args)
    def clear_list(self, arg):
        print('called MergeDialogGui.clear_list with arg', arg)
    def create_list(self, *args, **kwargs):
        print('called MergeDialogGui.create_list with args', args, kwargs)
        return 'list'
    def create_findbutton(self, *args, **kwargs):
        print('called MergeDialogGui.create_findbutton with args', args, kwargs)
        return 'find'
    def create_text(self):
        print('called MergeDialogGui.create_text')
        return 'text'
    def create_button(self, *args, **kwargs):
        print('called MergeDialogGui.create_button with args', args, kwargs)
        return 'button'
    def ensure_listitem_visible(self, *args):
        print('called MergeDialogGui.ensure_listitem_visible with args', args)
    def finalize_display(self, *args):
        print('called MergeDialogGui.finalize_display with args', args)
    def find_in_listbox(self, *args):
        print('called MergeDialogGui.find_in_listbox with args', args)
        return None
    def find_listitems(self, *args):
        print('called MergeDialogGui.find_listitems with args', args)
    # def findnextitem(self, *args):
    # def findprevitem(self, *args):
    def get_entry_text(self, arg):
        print('called MergeDialogGui.get_entry_text with arg', arg)
        return 'item'
    def get_first_item(self, arg):
        print('called MergeDialogGui.get_first_item with arg', arg)
        return 'first'
    def get_item_text(self, *args):
        print('called MergeDialogGui.get_item_text with args', args)
        return 'itemtext'
    def get_last_item(self, arg):
        print('called MergeDialogGui.get_last_item with arg', arg)
        return 'last'
    def get_listbox_count(self, arg):
        print('called MergeDialogGui.get_listbox_count with arg', arg)
        return 2
    # def get_listitem_count(self):
    #     print('called MergeDialogGui.get_listitem_count with arg', arg)
    #     return 'item'
    def get_search_choice(self, arg):
        print('called MergeDialogGui.get_search_choice with arg', arg)
        return 'search'
    def get_selected_item(self, arg):
        print('called MergeDialogGui.get_selected_item with arg', arg)
        return 'selected'
    def get_selected_listbox_data(self, *args):
        print('called MergeDialogGui.get_selected_listbox_data with args', args)
        return 'item', 'text1', 'text2'
    def init_display(self):
        print('called MergeDialogGui.init_display')
        return 'screen'
    def remove_listbox_item(self, *args):
        print('called MergeDialogGui.remove_listbox_item with args', args)
    def replace_listbox_item(self, *args):
        print('called MergeDialogGui.replace_listbox_item with args', args)
    def reject(self):
        print('called MergeDialogGui.reject')
    def reset_listitem_icon(self, *args):
        print('called MergeDialogGui.reset_listitem_icon with args', args)
    def set_focus_to(self, arg):
        print(f"called MergeDialogGui.set_focus_to with arg '{arg}'")
    def set_listitem_icon(self, *args):
        print('called MergeDialogGui.set_listitem_icon with args', args)
    def set_selected_item(self, *args):
        print('called MergeDialogGui.set_selected_item with args', args)


class TestMerger:
    """unittests for mergetool.Merger
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for mergetool.Merger object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called Merger.__init__ with args', args)
        monkeypatch.setattr(testee.Merger, '__init__', mock_init)
        testobj = testee.Merger()
        assert capsys.readouterr().out == 'called Merger.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Merger.__init__
        """
        class MockGui:
            "testdouble for MergeDialogGui object"
            def __init__(self, *args):
                print('called MergeDialogGui.__init__ with args', args)
        def mock_build(self):
            print('called Merger.build_screen')
        def mock_create(self):
            print('called Merger.create_shortcuts')
        def mock_load(self):
            print('called Merger.load_files')
        monkeypatch.setattr(testee, 'MergeDialogGui', MockGui)
        monkeypatch.setattr(testee.Merger, 'build_screen', mock_build)
        monkeypatch.setattr(testee.Merger, 'create_shortcuts', mock_create)
        monkeypatch.setattr(testee.Merger, 'load_files', mock_load)
        testobj = testee.Merger('parent', 'master')
        assert testobj.parent == 'parent'
        assert testobj.master == 'master'
        assert isinstance(testobj.gui, testee.MergeDialogGui)
        assert testobj.keysearch == ['', 1, []]
        assert testobj.cmdsearch == ['', 1, []]
        assert testobj.keyresults == []
        assert testobj.cmdresults == []
        # assert not testobj.set_match_from_key
        # assert not testobj.set_key_from_match
        # assert not testobj.set_match_from_command
        # assert not testobj.set_command_from_match
        assert capsys.readouterr().out == (
                f"called MergeDialogGui.__init__ with args ({testobj}, 'master')\n"
                "called Merger.build_screen\n"
                "called Merger.create_shortcuts\n"
                "called Merger.load_files\n")

    def test_build_screen(self, monkeypatch, capsys):
        """unittest for Merger.build_screen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.build_screen()
        assert testobj.listkeys == 'list'
        assert testobj.findkeybutton == 'find'
        assert testobj.findkeytext == 'text'
        assert testobj.nextkey == 'button'
        assert testobj.prevkey == 'button'
        assert testobj.listcmds == 'list'
        assert testobj.findcmdbutton == 'find'
        assert testobj.findcmdtext == 'text'
        assert testobj.nextcmd == 'button'
        assert testobj.prevcmd == 'button'
        assert testobj.listmatches == 'list'
        assert testobj.btn_match == 'button'
        assert testobj.btn_delete == 'button'
        assert testobj.btn_load == 'button'
        assert testobj.btn_clear == 'button'
        assert testobj.btn_save == 'button'
        assert testobj.btn_quit == 'button'
        assert testobj.btn_build == 'button'
        assert capsys.readouterr().out == (
            "called MergeDialogGui.init_display\n"
            "called MergeDialogGui.add_row with args ('screen',)\n"
            "called MergeDialogGui.add_col_to_row with args ('row',)\n"
            "called MergeDialogGui.create_list with args"
            " () {'columns': ['Key', 'Description'],"
            f" 'callback': {testobj.select_match_fromkeys}}}\n"
            "called MergeDialogGui.add_row_to_col with args ('col', 'list') {'left_align': True}\n"
            "called MergeDialogGui.create_findbutton with args () {'columns': ('key', 'text')}\n"
            "called MergeDialogGui.create_text\n"
            "called MergeDialogGui.create_button with args"
            f" ('&Next', {testobj.findnextkey}) {{'size': 50}}\n"
            "called MergeDialogGui.create_button with args"
            f" ('&Prev', {testobj.findprevkey}) {{'size': 50}}\n"
            "called MergeDialogGui.add_row_to_col with args"
            " ('col', 'find', 'text', 'button', 'button') {'left_align': True}\n"
            "called MergeDialogGui.add_col_to_row with args ('row',)\n"
            "called MergeDialogGui.create_list with args"
            " () {'columns': ['Command', 'Description'],"
            f" 'callback': {testobj.select_match_from_cmds}}}\n"
            "called MergeDialogGui.add_row_to_col with args ('col', 'list') {'center': True}\n"
            "called MergeDialogGui.create_findbutton with args () {'columns': ('cmd', 'text')}\n"
            "called MergeDialogGui.create_text\n"
            "called MergeDialogGui.create_button with args"
            f" ('Ne&Xt', {testobj.findnextcmd}) {{'size': 50}}\n"
            "called MergeDialogGui.create_button with args"
            f" ('Pre&V', {testobj.findprevcmd}) {{'size': 50}}\n"
            "called MergeDialogGui.add_row_to_col with args"
            " ('col', 'find', 'text', 'button', 'button') {'left_align': True}\n"
            "called MergeDialogGui.add_col_to_row with args ('row',)\n"
            "called MergeDialogGui.create_list with args"
            " () {'columns': ['Key', 'Command'],"
            f" 'callback': {testobj.select_listitems_from_matches}}}\n"
            "called MergeDialogGui.add_row_to_col with args"
            " ('col', 'list') {'right_align': True}\n"
            "called MergeDialogGui.create_button with args"
            f" ('&+ Add/Replace match', {testobj.make_match}) {{}}\n"
            "called MergeDialogGui.create_button with args"
            f" ('&- Discard match', {testobj.delete_match}) {{}}\n"
            "called MergeDialogGui.add_row_to_col with args"
            " ('col', 'button', 'button') {'center': True}\n"
            "called MergeDialogGui.create_button with args"
            f" ('&Load matches', {testobj.load_matches}) {{}}\n"
            "called MergeDialogGui.create_button with args"
            f" ('&Clear All', {testobj.reset_all}) {{}}\n"
            "called MergeDialogGui.create_button with args"
            f" ('&Save matches', {testobj.save_matches}) {{}}\n"
            "called MergeDialogGui.create_button with args"
            f" ('&Afsluiten', {testobj.close}) {{}}\n"
            "called MergeDialogGui.create_button with args"
            f" ('&Build CSV', {testobj.confirm}) {{}}\n"
            "called MergeDialogGui.add_row_to_col with args"
            " ('screen', 'button', 'button', 'button', 'button', 'button') {'center': True}\n"
            "called MergeDialogGui.finalize_display with args ('screen',)\n")

    def test_create_shortcuts(self, monkeypatch, capsys):
        """unittest for Merger.create_shortcuts
        """
        def mock_create(*args):
            print('called MergeDialogGui.create_hotkey with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(create_hotkey=mock_create)
        assert testobj.create_shortcuts() == (
            ('keylist', testobj.focus_keylist, 'Ctrl+1', 'Focus list of keyboard shortcuts'),
            ('cmdlist', testobj.focus_cmdlist, 'Ctrl+2', 'Focus list of commands'),
            ('matchlist', testobj.focus_matchlist, 'Ctrl+3', 'Focus list of connections'),
            ('findkey', testobj.focus_findkey, 'Ctrl+F', 'Enter search phrase for shortcut'),
            ('nextkey', testobj.findnextkey, 'Ctrl+N', 'Forward in shortcut search results'),
            ('prevkey', testobj.findprevkey, 'Ctrl+P', 'Back in shortcut search results'),
            ('findcmd', testobj.focus_findcmd, 'Ctrl+Shift+F', 'Enter search phrase for command'),
            ('nextcmd', testobj.findnextcmd, 'Ctrl+Shift+N', 'Forward in command search results'),
            ('prevcmd', testobj.findprevcmd, 'Ctrl+Shift+P', 'Back in command search results'),
            ('match', testobj.make_match, 'Ctrl+M', 'Connect command to shortcut'),
            ('delmatch', testobj.delete_match, 'Ctrl+Shift+M', 'Disconnect command from shortcut'),
            ('load', testobj.load_matches, 'Ctrl+L', 'Load previously made connections'),
            ('update', testobj.save_matches, 'Ctrl+U', 'Save all command-shortcut connections'),
            ('clear', testobj.reset_all, 'Ctrl+Del', 'Discard all command-shortcut connections'),
            ('save', testobj.confirm, 'Ctrl+S', 'Save connections to settings and leave dialog'),
            ('quit', testobj.close, 'Ctrl+Q', 'Leave dialog without saving'),
            ('help', testobj.help, 'F1', 'This help'))
        assert capsys.readouterr().out == (
            "called MergeDialogGui.create_hotkey with args ('keylist',"
            f" {testobj.focus_keylist}, 'Ctrl+1', 'Focus list of keyboard shortcuts')\n"
            "called MergeDialogGui.create_hotkey with args ('cmdlist',"
            f" {testobj.focus_cmdlist}, 'Ctrl+2', 'Focus list of commands')\n"
            "called MergeDialogGui.create_hotkey with args ('matchlist',"
            f" {testobj.focus_matchlist}, 'Ctrl+3', 'Focus list of connections')\n"
            "called MergeDialogGui.create_hotkey with args ('findkey',"
            f" {testobj.focus_findkey}, 'Ctrl+F', 'Enter search phrase for shortcut')\n"
            "called MergeDialogGui.create_hotkey with args ('nextkey',"
            f" {testobj.findnextkey}, 'Ctrl+N', 'Forward in shortcut search results')\n"
            "called MergeDialogGui.create_hotkey with args ('prevkey',"
            f" {testobj.findprevkey}, 'Ctrl+P', 'Back in shortcut search results')\n"
            "called MergeDialogGui.create_hotkey with args ('findcmd',"
            f" {testobj.focus_findcmd}, 'Ctrl+Shift+F', 'Enter search phrase for command')\n"
            "called MergeDialogGui.create_hotkey with args ('nextcmd',"
            f" {testobj.findnextcmd}, 'Ctrl+Shift+N', 'Forward in command search results')\n"
            "called MergeDialogGui.create_hotkey with args ('prevcmd',"
            f" {testobj.findprevcmd}, 'Ctrl+Shift+P', 'Back in command search results')\n"
            "called MergeDialogGui.create_hotkey with args ('match',"
            f" {testobj.make_match}, 'Ctrl+M', 'Connect command to shortcut')\n"
            "called MergeDialogGui.create_hotkey with args ('delmatch',"
            f" {testobj.delete_match}, 'Ctrl+Shift+M', 'Disconnect command from shortcut')\n"
            "called MergeDialogGui.create_hotkey with args ('load',"
            f" {testobj.load_matches}, 'Ctrl+L', 'Load previously made connections')\n"
            "called MergeDialogGui.create_hotkey with args ('update',"
            f" {testobj.save_matches}, 'Ctrl+U', 'Save all command-shortcut connections')\n"
            "called MergeDialogGui.create_hotkey with args ('clear',"
            f" {testobj.reset_all}, 'Ctrl+Del', 'Discard all command-shortcut connections')\n"
            "called MergeDialogGui.create_hotkey with args ('save',"
            f" {testobj.confirm}, 'Ctrl+S', 'Save connections to settings and leave dialog')\n"
            "called MergeDialogGui.create_hotkey with args ('quit', "
            f"{testobj.close}, 'Ctrl+Q', 'Leave dialog without saving')\n"
            "called MergeDialogGui.create_hotkey with args ('help', "
            f"{testobj.help}, 'F1', 'This help')\n")

    def test_load_files(self, monkeypatch, capsys):
        """unittest for Merger.load_files
        """
        def mock_loadkeys():
            print('called Merger.load_keys')
        def mock_loadcmds():
            print('called Merger.load_commands')
        def mock_reset():
            print('called Merger.reset_all')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.load_keys = mock_loadkeys
        testobj.load_commands = mock_loadcmds
        testobj.reset_all = mock_reset
        testobj.load_files()
        assert capsys.readouterr().out == ("called Merger.load_keys\n"
                                           "called Merger.load_commands\n"
                                           "called Merger.reset_all\n")

    def test_load_keys(self, monkeypatch, capsys):
        """unittest for Merger.load_keys
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(keylist_data={})
        testobj.gui = MockGui()
        testobj.listkeys = 'listbox'
        testobj.load_keys()
        assert testobj.keydict == {}
        assert testobj.keydata == []
        assert testobj.keytexts == []
        assert capsys.readouterr().out == "called MergeDialogGui.clear_list with arg listbox\n"
        testobj.parent.keylist_data = {('x', 'y'): {'oms': 'z'}, ('a', 'b'): {'oms': 'c'}}
        testobj.load_keys()
        assert testobj.keydict == {('x', 'y'): {'oms': 'z'}, ('a', 'b'): {'oms': 'c'}}
        assert testobj.keydata == ['a b', 'x y']
        assert testobj.keytexts == ['c', 'z']
        assert capsys.readouterr().out == (
                "called MergeDialogGui.clear_list with arg listbox\n"
                "called MergeDialogGui.add_listitem with args ('listbox', 'a b', 'c')\n"
                "called MergeDialogGui.add_listitem with args ('listbox', 'x y', 'z')\n")

    def test_load_commands(self, monkeypatch, capsys):
        """unittest for Merger.load_commands
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(cmdlist_data={})
        testobj.gui = MockGui()
        testobj.listcmds = 'listbox'
        testobj.load_commands()
        assert testobj.cmddict == {}
        assert testobj.cmddata == []
        assert testobj.cmdtexts == []
        assert capsys.readouterr().out == "called MergeDialogGui.clear_list with arg listbox\n"
        testobj.parent.cmdlist_data = {('x', 'y'): {'oms': 'z'}, ('a', 'b'): {'oms': 'c'}}
        testobj.load_commands()
        assert testobj.cmddict == {('x', 'y'): {'oms': 'z'}, ('a', 'b'): {'oms': 'c'}}
        assert testobj.cmddata == [('a', 'b'), ('x', 'y')]
        assert testobj.cmdtexts == ['c', 'z']
        assert capsys.readouterr().out == (
                "called MergeDialogGui.clear_list with arg listbox\n"
                "called MergeDialogGui.add_listitem with args ('listbox', ('a', 'b'), 'c')\n"
                "called MergeDialogGui.add_listitem with args ('listbox', ('x', 'y'), 'z')\n")

    def test_load_matches(self, monkeypatch, capsys):
        """unittest for Merger.load_matches
        """
        def mock_reset():
            print('called Merger.reset_all')
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        def mock_find(*args):
            print('called MergeDialogGui.find_in_listbox with args', args)
            return 'itemindex'
        testee.gui.show_message = mock_show
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.listmatches = 'listmatches'
        testobj.listkeys = 'listkeys'
        testobj.parent = types.SimpleNamespace(matchlist_data={})
        testobj.reset_all = mock_reset
        testobj.load_matches()
        assert capsys.readouterr().out == ("called Merger.reset_all\n"
                                           "called gui.show_message with args"
                                           f" ({testobj.gui},) {{'text': 'No saved data found'}}\n")
        testobj.parent.matchlist_data = [('x', 'y', 'z'), ('a', 'b', 'c')]
        testobj.load_matches()
        assert capsys.readouterr().out == (
                "called Merger.reset_all\n"
                "called MergeDialogGui.add_listitem with args ('listmatches', 'a b', 'c')\n"
                "called MergeDialogGui.find_in_listbox with args ('listkeys', 'a b')\n"
                # "called MergeDialogGui.set_listitem_icon with args ('listkeys', 'itemindex')\n"
                "called MergeDialogGui.add_listitem with args ('listmatches', 'x y', 'z')\n"
                "called MergeDialogGui.find_in_listbox with args ('listkeys', 'x y')\n")
                # "called MergeDialogGui.set_listitem_icon with args ('listkeys', 'itemindex')\n")
        testobj.gui.find_in_listbox = mock_find
        testobj.load_matches()
        assert capsys.readouterr().out == (
                "called Merger.reset_all\n"
                "called MergeDialogGui.add_listitem with args ('listmatches', 'a b', 'c')\n"
                "called MergeDialogGui.find_in_listbox with args ('listkeys', 'a b')\n"
                "called MergeDialogGui.set_listitem_icon with args ('listkeys', 'itemindex')\n"
                "called MergeDialogGui.add_listitem with args ('listmatches', 'x y', 'z')\n"
                "called MergeDialogGui.find_in_listbox with args ('listkeys', 'x y')\n"
                "called MergeDialogGui.set_listitem_icon with args ('listkeys', 'itemindex')\n")

    def test_reset_all(self, monkeypatch, capsys):
        """unittest for Merger.reset_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.listmatches = 'listmatches'
        testobj.listkeys = 'listkeys'
        testobj.reset_all()
        assert capsys.readouterr().out == (
                "called MergeDialogGui.clear_list with arg listmatches\n"
                "called MergeDialogGui.get_listbox_count with arg listkeys\n"
                "called MergeDialogGui.reset_listitem_icon with args ('listkeys', 0)\n"
                "called MergeDialogGui.reset_listitem_icon with args ('listkeys', 1)\n")

    def test_make_match(self, monkeypatch, capsys):
        """unittest for Merger.make_match
        """
        def mock_find(*args):
            print('called MergeDialogGui.find_in_listbox with args', args)
            return 'itemindex'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.listmatches = 'listmatches'
        testobj.listkeys = 'listkeys'
        testobj.listcmds = 'listcmds'
        testobj.make_match()
        assert capsys.readouterr().out == (
            "called MergeDialogGui.get_selected_listbox_data with args ('listkeys',)\n"
            "called MergeDialogGui.get_selected_listbox_data with args ('listcmds',)\n"
            "called MergeDialogGui.find_in_listbox with args ('listmatches', 'text1')\n"
            "called MergeDialogGui.add_listitem with args ('listmatches', 'text1', 'text1')\n"
            "called MergeDialogGui.ensure_listitem_visible with args ('listmatches', None)\n"
            "called MergeDialogGui.set_listitem_icon with args ('listkeys', 'item')\n")
        testobj.gui.find_in_listbox = mock_find
        testobj.make_match()
        assert capsys.readouterr().out == (
            "called MergeDialogGui.get_selected_listbox_data with args ('listkeys',)\n"
            "called MergeDialogGui.get_selected_listbox_data with args ('listcmds',)\n"
            "called MergeDialogGui.find_in_listbox with args ('listmatches', 'text1')\n"
            "called MergeDialogGui.replace_listbox_item with args"
            " ('listmatches', 'itemindex', 'text1')\n"
            "called MergeDialogGui.ensure_listitem_visible with args ('listmatches', 'itemindex')\n"
            "called MergeDialogGui.set_listitem_icon with args ('listkeys', 'item')\n")

    def test_delete_match(self, monkeypatch, capsys):
        """unittest for Merger.delete_match
        """
        def mock_get(*args):
            print('called MergeDialogGui.get_selected_listbox_data with args', args)
            return None, None, None
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        def mock_question(*args, **kwargs):
            print('called gui.ask_question with args', args, kwargs)
            return False
        def mock_question_2(*args, **kwargs):
            print('called gui.ask_question with args', args, kwargs)
            return True
        def mock_find(*args):
            print('called MergeDialogGui.find_in_listbox with args', args)
            return 'itemindex'
        testee.gui.show_message = mock_show
        testee.gui.ask_question = mock_question
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.listmatches = 'listmatches'
        testobj.listkeys = 'listkeys'
        testobj.listcmds = 'listcmds'
        testobj.delete_match()
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_selected_listbox_data with args ('listmatches',)\n"
                "called gui.ask_question with args"
                f" ({testobj.gui},) {{'text': 'Really delete?'}}\n")
        testee.gui.ask_question = mock_question_2
        testobj.delete_match()
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_selected_listbox_data with args ('listmatches',)\n"
                "called gui.ask_question with args"
                f" ({testobj.gui},) {{'text': 'Really delete?'}}\n"
                "called MergeDialogGui.get_item_text with args ('listmatches', 'item', 0)\n"
                "called MergeDialogGui.remove_listbox_item with args ('listmatches', 'item')\n"
                "called MergeDialogGui.find_in_listbox with args ('listkeys', 'itemtext')\n")
        testobj.gui.find_in_listbox = mock_find
        testobj.delete_match()
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_selected_listbox_data with args ('listmatches',)\n"
                "called gui.ask_question with args"
                f" ({testobj.gui},) {{'text': 'Really delete?'}}\n"
                "called MergeDialogGui.get_item_text with args ('listmatches', 'item', 0)\n"
                "called MergeDialogGui.remove_listbox_item with args ('listmatches', 'item')\n"
                "called MergeDialogGui.find_in_listbox with args ('listkeys', 'itemtext')\n"
                "called MergeDialogGui.reset_listitem_icon with args ('listkeys', 'itemindex')\n")
        testobj.gui.get_selected_listbox_data = mock_get
        testobj.delete_match()
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_selected_listbox_data with args ('listmatches',)\n"
                "called gui.show_message with args"
                f" ({testobj.gui},) {{'text': 'choose an item to delete'}}\n")

    def test_save_matches(self, monkeypatch, capsys):
        """unittest for Merger.save_matches
        """
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        def mock_save(*args):
            print('called save_matches with args', args)
        def mock_count(arg):
            print('called MergeDialogGui.get_listbox_count with arg', arg)
            return 0
        monkeypatch.setattr(testee, 'save_matchdata', mock_save)
        testee.gui.show_message = mock_show
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(matchfile='matchfile', tempdata=[])
        testobj.gui = MockGui()
        testobj.listmatches = 'listmatches'
        testobj.listkeys = 'listkeys'
        testobj.listcmds = 'listcmds'
        testobj.save_matches()
        assert not testobj.parent.tempdata
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n"
                "called MergeDialogGui.get_item_text with args ('listmatches', 0, 0)\n"
                "called MergeDialogGui.get_item_text with args ('listmatches', 0, 1)\n"
                "called MergeDialogGui.get_item_text with args ('listmatches', 1, 0)\n"
                "called MergeDialogGui.get_item_text with args ('listmatches', 1, 1)\n"
                "called save_matches with args"
                " ([('itemtext', 'itemtext'), ('itemtext', 'itemtext')], 'matchfile')\n"
                f"called gui.show_message with args ({testobj.gui},) {{'text': 'Data saved'}}\n")
        testobj.save_matches(tofile=False)
        assert testobj.parent.tempdata == [('itemtext', 'itemtext'), ('itemtext', 'itemtext')]
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n"
                "called MergeDialogGui.get_item_text with args ('listmatches', 0, 0)\n"
                "called MergeDialogGui.get_item_text with args ('listmatches', 0, 1)\n"
                "called MergeDialogGui.get_item_text with args ('listmatches', 1, 0)\n"
                "called MergeDialogGui.get_item_text with args ('listmatches', 1, 1)\n")
        testobj.gui.get_listbox_count = mock_count
        testobj.parent.tempdata = []
        testobj.save_matches()
        assert not testobj.parent.tempdata
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n"
                "called gui.show_message with args"
                f" ({testobj.gui},) {{'text': 'No data to save'}}\n")

    def test_focus_keylist(self, monkeypatch, capsys):
        """unittest for Merger.focus_keylist
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.listkeys = 'listkeys'
        testobj.focus_keylist()
        assert capsys.readouterr().out == (
                "called MergeDialogGui.set_focus_to with arg 'listkeys'\n")

    def test_focus_cmdlist(self, monkeypatch, capsys):
        """unittest for Merger.focus_cmdlist
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.listcmds = 'listcmds'
        testobj.focus_cmdlist()
        assert capsys.readouterr().out == (
                "called MergeDialogGui.set_focus_to with arg 'listcmds'\n")

    def test_focus_matchlist(self, monkeypatch, capsys):
        """unittest for Merger.focus_matchlist
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.listmatches = 'listmatches'
        testobj.focus_matchlist()
        assert capsys.readouterr().out == (
                "called MergeDialogGui.set_focus_to with arg 'listmatches'\n")

    def test_focus_findkey(self, monkeypatch, capsys):
        """unittest for Merger.focus_findkey
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.findkeytext = 'findkeytext'
        testobj.focus_findkey()
        assert capsys.readouterr().out == (
                "called MergeDialogGui.set_focus_to with arg 'findkeytext'\n")

    def test_focus_findcmd(self, monkeypatch, capsys):
        """unittest for Merger.focus_findcmd
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.findcmdtext = 'findcmdtext'
        testobj.focus_findcmd()
        assert capsys.readouterr().out == (
                "called MergeDialogGui.set_focus_to with arg 'findcmdtext'\n")

    def test_findnextkey(self, monkeypatch, capsys):
        """unittest for Merger.findnextkey
        """
        def mock_find(*args):
            print('called Merger.findnextitem with args', args)
            return None
        def mock_find_2(*args):
            print('called Merger.findnextitem with args', args)
            return 'xxx', 'yyy'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.findnextitem = mock_find
        testobj.findkeybutton = 'findkeybutton'
        testobj.findkeytext = 'findkeytext'
        testobj.keysearch = 'keysearch'
        testobj.listkeys = 'listkeys'
        testobj.keyresults = 'keyresults'
        testobj.findnextkey()
        assert testobj.keysearch == 'keysearch'
        assert testobj.keyresults == 'keyresults'
        assert capsys.readouterr().out == (
                "called Merger.findnextitem with args"
                " ('findkeybutton', 'findkeytext', 'keysearch', 'listkeys', 'keyresults')\n")
        testobj.findnextitem = mock_find_2
        testobj.findnextkey()
        assert testobj.keysearch == 'xxx'
        assert testobj.keyresults == 'yyy'
        assert capsys.readouterr().out == (
                "called Merger.findnextitem with args"
                " ('findkeybutton', 'findkeytext', 'keysearch', 'listkeys', 'keyresults')\n")

    def test_findprevkey(self, monkeypatch, capsys):
        """unittest for Merger.findprevkey
        """
        def mock_find(*args):
            print('called Merger.findprevitem with args', args)
            return None
        def mock_find_2(*args):
            print('called Merger.findprevitem with args', args)
            return 'xxx', 'yyy'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.findprevitem = mock_find
        testobj.findkeybutton = 'findkeybutton'
        testobj.findkeytext = 'findkeytext'
        testobj.keysearch = 'keysearch'
        testobj.listkeys = 'listkeys'
        testobj.keyresults = 'keyresults'
        testobj.findprevkey()
        assert testobj.keysearch == 'keysearch'
        assert testobj.keyresults == 'keyresults'
        assert capsys.readouterr().out == (
                "called Merger.findprevitem with args"
                " ('findkeybutton', 'findkeytext', 'keysearch', 'listkeys', 'keyresults')\n")
        testobj.findprevitem = mock_find_2
        testobj.findprevkey()
        assert testobj.keysearch == 'xxx'
        assert testobj.keyresults == 'yyy'
        assert capsys.readouterr().out == (
                "called Merger.findprevitem with args"
                " ('findkeybutton', 'findkeytext', 'keysearch', 'listkeys', 'keyresults')\n")

    def test_findnextcmd(self, monkeypatch, capsys):
        """unittest for Merger.findnextcmd
        """
        def mock_find(*args):
            print('called Merger.findnextitem with args', args)
            return None
        def mock_find_2(*args):
            print('called Merger.findnextitem with args', args)
            return 'xxx', 'yyy'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.findnextitem = mock_find
        testobj.findcmdbutton = 'findcmdbutton'
        testobj.findcmdtext = 'findcmdtext'
        testobj.cmdsearch = 'cmdsearch'
        testobj.listcmds = 'listcmds'
        testobj.cmdresults = 'cmdresults'
        testobj.findnextcmd()
        assert testobj.cmdsearch == 'cmdsearch'
        assert testobj.cmdresults == 'cmdresults'
        assert capsys.readouterr().out == (
                "called Merger.findnextitem with args"
                " ('findcmdbutton', 'findcmdtext', 'cmdsearch', 'listcmds', 'cmdresults')\n")
        testobj.findnextitem = mock_find_2
        testobj.findnextcmd()
        assert testobj.cmdsearch == 'xxx'
        assert testobj.cmdresults == 'yyy'
        assert capsys.readouterr().out == (
                "called Merger.findnextitem with args"
                " ('findcmdbutton', 'findcmdtext', 'cmdsearch', 'listcmds', 'cmdresults')\n")

    def test_findprevcmd(self, monkeypatch, capsys):
        """unittest for Merger.findprevcmd
        """
        def mock_find(*args):
            print('called Merger.findprevitem with args', args)
            return None
        def mock_find_2(*args):
            print('called Merger.findprevitem with args', args)
            return 'xxx', 'yyy'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.findprevitem = mock_find
        testobj.findcmdbutton = 'findcmdbutton'
        testobj.findcmdtext = 'findcmdtext'
        testobj.cmdsearch = 'cmdsearch'
        testobj.listcmds = 'listcmds'
        testobj.cmdresults = 'cmdresults'
        testobj.findprevcmd()
        assert testobj.cmdsearch == 'cmdsearch'
        assert testobj.cmdresults == 'cmdresults'
        assert capsys.readouterr().out == (
                "called Merger.findprevitem with args"
                " ('findcmdbutton', 'findcmdtext', 'cmdsearch', 'listcmds', 'cmdresults')\n")
        testobj.findprevitem = mock_find_2
        testobj.findprevcmd()
        assert testobj.cmdsearch == 'xxx'
        assert testobj.cmdresults == 'yyy'
        assert capsys.readouterr().out == (
                "called Merger.findprevitem with args"
                " ('findcmdbutton', 'findcmdtext', 'cmdsearch', 'listcmds', 'cmdresults')\n")

    def test_findnextitem(self, monkeypatch, capsys):
        """unittest for Merger.findnextitem
        """
        def mock_find(*args):
            print('called Merger.finditem with args', args)
        def mock_find_2(*args):
            print('called Merger.finditem with args', args)
            return '', 'yyy', ['aaa', 'bbb', 'selected']
        def mock_find_3(*args):
            print('called Merger.finditem with args', args)
            return '', 'yyy', ['aaa', 'bbb', 'selected', 'ccc']
        def mock_find_4(*args):
            print('called Merger.finditem with args', args)
            return 'xxx', 'yyy', ['aaa', 'bbb']
        def mock_find_5(*args):
            print('called Merger.finditem with args', args)
            return 'xxx', 'yyy', ['first', 'selected', 'selected+1']
        def mock_selected(arg):
            print('called MergeDialogGui.get_selected_item with arg', arg)
        def mock_selected_2(arg):
            print('called MergeDialogGui.get_selected_item with arg', arg)
            return -1
        def mock_text(*args):
            print('called MergeDialogGui.get_item_text with args', args)
            return args[1]
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        testee.gui.show_message = mock_show
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.gui.get_item_text = mock_text
        testobj.finditem = mock_find
        result = testobj.findnextitem('button', 'field', 'search', 'itemlist', [])
        assert result is None
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n")
        testobj.finditem = mock_find_2
        result = testobj.findnextitem('button', 'field', 'search', 'itemlist', [])
        assert result is None
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.set_selected_item with args ('itemlist', 'aaa')\n")
        testobj.finditem = mock_find_3
        result = testobj.findnextitem('button', 'field', 'search', 'itemlist', [])
        assert result is None
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.set_selected_item with args ('itemlist', 'ccc')\n")
        testobj.finditem = mock_find_4
        result = testobj.findnextitem('button', 'field', 'search', 'itemlist', [])
        assert result is None
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'aaa', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'bbb', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            f"called gui.show_message with args ({testobj.gui},)"
            " {'text': 'No (next) item found'}\n")
        testobj.finditem = mock_find_5
        result = testobj.findnextitem('button', 'field', 'search', 'itemlist', [])
        assert result == ('yyy', ['first', 'selected', 'selected+1'])
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'first', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected+1', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            "called MergeDialogGui.set_selected_item with args ('itemlist', 'selected+1')\n")
        testobj.gui.get_selected_item = mock_selected
        result = testobj.findnextitem('button', 'field', 'search', 'itemlist', [])
        assert result == ('yyy', ['first', 'selected', 'selected+1'])
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.get_first_item with arg itemlist\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'first', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'first', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'first', 0)\n"
            "called MergeDialogGui.set_selected_item with args ('itemlist', 'selected')\n")
        testobj.gui.get_selected_item = mock_selected_2
        result = testobj.findnextitem('button', 'field', 'search', 'itemlist', [])
        assert result == ('yyy', ['first', 'selected', 'selected+1'])
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.get_first_item with arg itemlist\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'first', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'first', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'first', 0)\n"
            "called MergeDialogGui.set_selected_item with args ('itemlist', 'selected')\n")

# 283-305   Merger.findprevitem (23)
    def test_findprevitem(self, monkeypatch, capsys):
        """unittest for Merger.findprevitem
        """
        def mock_find(*args):
            print('called Merger.finditem with args', args)
        def mock_find_2(*args):
            print('called Merger.finditem with args', args)
            return 'xxx', 'yyy', ['aaa', 'bbb', 'selected']
        def mock_find_3(*args):
            print('called Merger.finditem with args', args)
            return 'xxx', 'yyy', ['selectee']
        def mock_find_4(*args):
            print('called Merger.finditem with args', args)
            return '', 'yyy', ['selected']
        def mock_find_5(*args):
            print('called Merger.finditem with args', args)
            return '', 'yyy', ['aaa', 'bbb', 'selected', 'last']
        def mock_selected(arg):
            print('called MergeDialogGui.get_selected_item with arg', arg)
            return -1
        def mock_selected_2(arg):
            print('called MergeDialogGui.get_selected_item with arg', arg)
            return None
        def mock_text(*args):
            print('called MergeDialogGui.get_item_text with args', args)
            return args[1]
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        testee.gui.show_message = mock_show
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.gui.get_item_text = mock_text
        testobj.finditem = mock_find
        result = testobj.findprevitem('button', 'field', 'search', 'itemlist', [])
        assert result is None
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n")
        testobj.finditem = mock_find_2
        result = testobj.findprevitem('button', 'field', 'search', 'itemlist', [])
        assert result == ('yyy', ['aaa', 'bbb', 'selected'])
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'bbb', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            "called MergeDialogGui.set_selected_item with args ('itemlist', 'bbb')\n")
        testobj.finditem = mock_find_3
        result = testobj.findprevitem('button', 'field', 'search', 'itemlist', [])
        assert result is None
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selectee', 0)\n"
            "called MergeDialogGui.get_item_text with args ('itemlist', 'selected', 0)\n"
            f"called gui.show_message with args ({testobj.gui},)"
            " {'text': 'No previous item found'}\n")
        testobj.finditem = mock_find_4
        result = testobj.findprevitem('button', 'field', 'search', 'itemlist', [])
        assert result is None
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.set_selected_item with args ('itemlist', 'selected')\n")
        testobj.finditem = mock_find_5
        result = testobj.findprevitem('button', 'field', 'search', 'itemlist', [])
        assert result is None
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.set_selected_item with args ('itemlist', 'bbb')\n")
        testobj.gui.get_selected_item = mock_selected
        result = testobj.findprevitem('button', 'field', 'search', 'itemlist', [])
        assert result is None
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.get_last_item with arg itemlist\n"
            "called MergeDialogGui.set_selected_item with args ('itemlist', 'selected')\n")
        testobj.gui.get_selected_item = mock_selected_2
        result = testobj.findprevitem('button', 'field', 'search', 'itemlist', [])
        assert result is None
        assert capsys.readouterr().out == (
            "called Merger.finditem with args ('button', 'field', 'search', 'itemlist', [])\n"
            "called MergeDialogGui.get_selected_item with arg itemlist\n"
            "called MergeDialogGui.get_last_item with arg itemlist\n"
            "called MergeDialogGui.set_selected_item with args ('itemlist', 'selected')\n")

    def test_finditem(self, monkeypatch, capsys):
        """unittest for Merger.finditem
        """
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        def mock_get(arg):
            print('called MergeDialogGui.get_entry_text with arg', arg)
            return 'old_for'
        def mock_get_2(arg):
            print('called MergeDialogGui.get_entry_text with arg', arg)
            return ''
        def mock_choice(arg):
            print('called MergeDialogGui.get_search_choice with arg', arg)
            return 'old_in'
        testee.gui.show_message = mock_show
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()

        result = testobj.finditem('srch_for', 'srch_in', ('old_for', 'old_in'), ['itemlist'], [])
        assert result == (True, ('item', 'search'), None)
        assert capsys.readouterr().out == (
            "called MergeDialogGui.get_entry_text with arg srch_in\n"
            "called MergeDialogGui.get_search_choice with arg srch_for\n"
            "called MergeDialogGui.find_listitems with args (['itemlist'], 'item', 'search')\n")
        testobj.gui.get_entry_text = mock_get
        result = testobj.finditem('srch_for', 'srch_in', ('old_for', 'old_in'), ['itemlist'], [])
        assert result == (True, ('old_for', 'search'), None)
        assert capsys.readouterr().out == (
            "called MergeDialogGui.get_entry_text with arg srch_in\n"
            "called MergeDialogGui.get_search_choice with arg srch_for\n"
            "called MergeDialogGui.find_listitems with args (['itemlist'], 'old_for', 'search')\n")
        testobj.gui.get_search_choice = mock_choice
        result = testobj.finditem('srch_for', 'srch_in', ('old_for', 'old_in'), ['itemlist'], [])
        assert result == (False, ('old_for', 'old_in'), [])
        assert capsys.readouterr().out == (
            "called MergeDialogGui.get_entry_text with arg srch_in\n"
            "called MergeDialogGui.get_search_choice with arg srch_for\n")
        testobj.gui.get_entry_text = mock_get_2
        assert testobj.finditem('_for', '_in', ('old_for', 'old_in'), ['itemlist'], []) is None
        assert capsys.readouterr().out == (
            "called MergeDialogGui.get_entry_text with arg _in\n"
            f"called gui.show_message with args ({testobj.gui},)"
            " {'text': 'Please enter text to search for'}\n")

    def test_select_match_fromkeys(self, monkeypatch, capsys):
        """unittest for Merger.select_match_fromkeys
        """
        def mock_find(*args):
            print('called Merger.find_related with args', args)
        def mock_find_2(*args):
            print('called Merger.find_related with args', args)
            return 'found'
        def mock_count(arg):
            print('called MergeDialogGui.get_listbox_count with arg', arg)
            return 0
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.listmatches = 'listmatches'
        testobj.listkeys = 'listkeys'
        # testobj.set_key_from_match = testobj.set_match_from_key = False
        testobj.find_related = mock_find
        testobj.select_match_fromkeys()
        # assert not testobj.set_match_from_key
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n"
                "called Merger.find_related with args (('listkeys', 0), ('listmatches', 0))\n")
        testobj.find_related = mock_find_2
        testobj.select_match_fromkeys()
        # assert not testobj.set_match_from_key
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n"
                "called Merger.find_related with args (('listkeys', 0), ('listmatches', 0))\n"
                "called MergeDialogGui.set_selected_item with args ('listmatches', 'found')\n")
        # zonder die switches is dit dubbel
        # # testobj.set_key_from_match = True
        # testobj.select_match_fromkeys()
        # # assert not testobj.set_match_from_key
        # assert capsys.readouterr().out == (
        #         "called MergeDialogGui.get_listbox_count with arg listmatches\n"
        #         "called Merger.find_related with args (('listkeys', 0), ('listmatches', 0))\n"
        #         "called MergeDialogGui.set_selected_item with args ('listmatches', 'found')\n")
        testobj.gui.get_listbox_count = mock_count
        testobj.select_match_fromkeys()
        # assert not testobj.set_match_from_key
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n")

    def test_select_match_from_cmds(self, monkeypatch, capsys):
        """unittest for Merger.select_match_from_cmds
        """
        def mock_find(*args):
            print('called Merger.find_related with args', args)
        def mock_find_2(*args):
            print('called Merger.find_related with args', args)
            return 'found'
        def mock_count(arg):
            print('called MergeDialogGui.get_listbox_count with arg', arg)
            return 0
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.listmatches = 'listmatches'
        testobj.listcmds = 'listcmds'
        # testobj.set_command_from_match = testobj.set_match_from_command = False
        testobj.find_related = mock_find
        testobj.select_match_from_cmds()
        # assert not testobj.set_match_from_command
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n"
                "called Merger.find_related with args (('listcmds', 0), ('listmatches', 1))\n")
        testobj.find_related = mock_find_2
        testobj.select_match_from_cmds()
        # assert not testobj.set_match_from_command
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n"
                "called Merger.find_related with args (('listcmds', 0), ('listmatches', 1))\n"
                "called MergeDialogGui.set_selected_item with args ('listmatches', 'found')\n")
        # zonder die switches is dit dubbel
        # # testobj.set_command_from_match = True
        # testobj.select_match_from_cmds()
        # # assert not testobj.set_match_from_command
        # assert capsys.readouterr().out == (
        #         "called MergeDialogGui.get_listbox_count with arg listmatches\n"
        #         "called Merger.find_related with args (('listcmds', 0), ('listmatches', 1))\n"
        #         "called MergeDialogGui.set_selected_item with args ('listmatches', 'found')\n")
        testobj.gui.get_listbox_count = mock_count
        testobj.select_match_from_cmds()
        # assert not testobj.set_match_from_command
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n")

    def test_select_listitems_from_matches(self, monkeypatch, capsys):
        """unittest for Merger.select_listitems_from_matches
        """
        def mock_find(*args):
            print('called Merger.find_related with args', args)
        def mock_find_2(*args):
            print('called Merger.find_related with args', args)
            return 'found'
        def mock_count(arg):
            print('called MergeDialogGui.get_listbox_count with arg', arg)
            return 0
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.find_related = mock_find
        testobj.listmatches = 'listmatches'
        testobj.listkeys = 'listkeys'
        testobj.listcmds = 'listcmds'
        # testobj.set_match_from_key = testobj.set_match_from_command = False
        # testobj.set_key_from_match = testobj.set_command_from_match = False
        testobj.select_listitems_from_matches()
        # assert not testobj.set_key_from_match
        # assert not testobj.set_command_from_match
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n"
                "called Merger.find_related with args (('listmatches', 0), ('listkeys', 0))\n"
                "called Merger.find_related with args (('listmatches', 1), ('listcmds', 0))\n")
        testobj.find_related = mock_find_2
        # testobj.set_match_from_key = True
        testobj.select_listitems_from_matches()
        # assert not testobj.set_key_from_match
        # assert not testobj.set_command_from_match
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n"
                "called Merger.find_related with args (('listmatches', 0), ('listkeys', 0))\n"
                "called MergeDialogGui.set_selected_item with args ('listkeys', 'found')\n"
                "called Merger.find_related with args (('listmatches', 1), ('listcmds', 0))\n"
                "called MergeDialogGui.set_selected_item with args ('listcmds', 'found')\n")
        # zonder die switches is dit overbodig
        # # testobj.set_match_from_key = False
        # # testobj.set_match_from_command = True
        # testobj.select_listitems_from_matches()
        # # assert not testobj.set_key_from_match
        # # assert not testobj.set_command_from_match
        # assert capsys.readouterr().out == (
        #         "called MergeDialogGui.get_listbox_count with arg listmatches\n"
        #         "called Merger.find_related with args (('listmatches', 0), ('listkeys', 0))\n"
        #         "called MergeDialogGui.set_selected_item with args ('listkeys', 'found')\n"
        #         "called Merger.find_related with args (('listmatches', 1), ('listcmds', 0))\n"
        #         "called MergeDialogGui.set_selected_item with args ('listcmds', 'found')\n")
        # # testobj.set_match_from_key = testobj.set_match_from_command = True
        # testobj.select_listitems_from_matches()
        # # assert not testobj.set_key_from_match
        # # assert not testobj.set_command_from_match
        # assert capsys.readouterr().out == (
        #         "called MergeDialogGui.get_listbox_count with arg listmatches\n"
        #         "called Merger.find_related with args (('listmatches', 0), ('listkeys', 0))\n"
        #         "called MergeDialogGui.set_selected_item with args ('listkeys', 'found')\n"
        #         "called Merger.find_related with args (('listmatches', 1), ('listcmds', 0))\n"
        #         "called MergeDialogGui.set_selected_item with args ('listcmds', 'found')\n")
        testobj.gui.get_listbox_count = mock_count
        testobj.select_listitems_from_matches()
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_listbox_count with arg listmatches\n")

    def test_find_related(self, monkeypatch, capsys):
        """unittest for Merger.find_related
        """
        def mock_find(*args):
            print('called MergeDialogGui.find_listitems with args', args)
            return ['item']
        def mock_selected(arg):
            print('called MergeDialogGui.get_selected_item with arg', arg)
            return -1
        def mock_selected_2(arg):
            print('called MergeDialogGui.get_selected_item with arg', arg)
            return None
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.find_related(('xxx', 'a'), ('yyy', 'b'))
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_selected_item with arg xxx\n"
                "called MergeDialogGui.get_item_text with args ('xxx', 'selected', 'a')\n"
                "called MergeDialogGui.find_listitems with args ('yyy', 'itemtext', 'b')\n")
        testobj.gui.find_listitems = mock_find
        testobj.find_related(('xxx', 'a'), ('yyy', 'b'))
        assert capsys.readouterr().out == (
                "called MergeDialogGui.get_selected_item with arg xxx\n"
                "called MergeDialogGui.get_item_text with args ('xxx', 'selected', 'a')\n"
                "called MergeDialogGui.find_listitems with args ('yyy', 'itemtext', 'b')\n")
        testobj.gui.get_selected_item = mock_selected
        testobj.find_related(('xxx', 'a'), ('yyy', 'b'))
        assert capsys.readouterr().out == "called MergeDialogGui.get_selected_item with arg xxx\n"
        testobj.gui.get_selected_item = mock_selected_2
        testobj.find_related(('xxx', 'a'), ('yyy', 'b'))
        assert capsys.readouterr().out == "called MergeDialogGui.get_selected_item with arg xxx\n"

    def test_confirm(self, monkeypatch, capsys):
        """unittest for Merger.confirm
        """
        def mock_save(**kwargs):
            print('called save_matches with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.save_matches = mock_save
        testobj.gui = MockGui()
        testobj.confirm()
        assert capsys.readouterr().out == ("called save_matches with args {'tofile': False}\n"
                                           "called MergeDialogGui.accept\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for Merger.close
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockGui()
        testobj.close()
        assert capsys.readouterr().out == "called MergeDialogGui.reject\n"

    def test_help(self, monkeypatch, capsys):
        """unittest for Merger.help
        """
        def mock_create():
            print('called Merger.create_shortcuts')
            return [('', '', 'xxx', 'yyy'), ('', '', '123456789012345678901234567890123', 'qqq')]
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = 'MergeDialogGui'
        testobj.create_shortcuts = mock_create
        testobj.help()
        assert capsys.readouterr().out == ("called Merger.create_shortcuts\n"
                                           "called gui.show_message with args ('MergeDialogGui',)"
                                           " {'text': 'xxx                           yyy\\n"
                                           "123456789012345678901234567890123qqq'}\n")
