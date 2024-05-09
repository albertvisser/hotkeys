"""unittests for ./editor/dialogs_qt.py
"""
from editor import dialogs_qt as testee


def _test_show_message(monkeypatch, capsys):
    """unittest for dialogs_qt.show_message
    """
    assert testee.show_message(win, message_id='', text='', args=None) == "expected_result"


def _test_show_cancel_message(monkeypatch, capsys):
    """unittest for dialogs_qt.show_cancel_message
    """
    assert testee.show_cancel_message(win, message_id='', text='', args=None) == "expected_result"


def _test_ask_question(monkeypatch, capsys):
    """unittest for dialogs_qt.ask_question
    """
    assert testee.ask_question(win, message_id='', text='', args=None) == "expected_result"


def _test_ask_ync_question(monkeypatch, capsys):
    """unittest for dialogs_qt.ask_ync_question
    """
    assert testee.ask_ync_question(win, message_id='', text='', args=None) == "expected_result"


def _test_get_textinput(monkeypatch, capsys):
    """unittest for dialogs_qt.get_textinput
    """
    assert testee.get_textinput(win, text, prompt) == "expected_result"


def _test_get_choice(monkeypatch, capsys):
    """unittest for dialogs_qt.get_choice
    """
    assert testee.get_choice(win, title, caption, choices, current) == "expected_result"


def _test_get_file_to_open(monkeypatch, capsys):
    """unittest for dialogs_qt.get_file_to_open
    """
    assert testee.get_file_to_open(win, oms='', extension='', start='') == "expected_result"


def _test_get_file_to_save(monkeypatch, capsys):
    """unittest for dialogs_qt.get_file_to_save
    """
    assert testee.get_file_to_save(win, oms='', extension='', start='') == "expected_result"


class TestInitialToolDialog:
    """unittest for dialogs_qt.InitialToolDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.InitialToolDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called InitialToolDialog.__init__ with args', args)
        monkeypatch.setattr(testee.InitialToolDialog, '__init__', mock_init)
        testobj = testee.InitialToolDialog()
        assert capsys.readouterr().out == 'called InitialToolDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for InitialToolDialog.__init__
        """
        testobj = testee.InitialToolDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for InitialToolDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestFileBrowseButton:
    """unittest for dialogs_qt.FileBrowseButton
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.FileBrowseButton object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called FileBrowseButton.__init__ with args', args)
        monkeypatch.setattr(testee.FileBrowseButton, '__init__', mock_init)
        testobj = testee.FileBrowseButton()
        assert capsys.readouterr().out == 'called FileBrowseButton.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for FileBrowseButton.__init__
        """
        testobj = testee.FileBrowseButton(parent, text="", level_down=False)
        assert capsys.readouterr().out == ("")

    def _test_browse(self, monkeypatch, capsys):
        """unittest for FileBrowseButton.browse
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.browse() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestSetupDialog:
    """unittest for dialogs_qt.SetupDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.SetupDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SetupDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SetupDialog, '__init__', mock_init)
        testobj = testee.SetupDialog()
        assert capsys.readouterr().out == 'called SetupDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SetupDialog.__init__
        """
        testobj = testee.SetupDialog(parent, name)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SetupDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestDeleteDialog:
    """unittest for dialogs_qt.DeleteDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.DeleteDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called DeleteDialog.__init__ with args', args)
        monkeypatch.setattr(testee.DeleteDialog, '__init__', mock_init)
        testobj = testee.DeleteDialog()
        assert capsys.readouterr().out == 'called DeleteDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for DeleteDialog.__init__
        """
        testobj = testee.DeleteDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for DeleteDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestFilesDialog:
    """unittest for dialogs_qt.FilesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.FilesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called FilesDialog.__init__ with args', args)
        monkeypatch.setattr(testee.FilesDialog, '__init__', mock_init)
        testobj = testee.FilesDialog()
        assert capsys.readouterr().out == 'called FilesDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for FilesDialog.__init__
        """
        testobj = testee.FilesDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_add_row(self, monkeypatch, capsys):
        """unittest for FilesDialog.add_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_row(name, path='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_delete_row(self, monkeypatch, capsys):
        """unittest for FilesDialog.delete_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.delete_row(rownum) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_program(self, monkeypatch, capsys):
        """unittest for FilesDialog.add_program
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_program() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_programs(self, monkeypatch, capsys):
        """unittest for FilesDialog.remove_programs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_programs() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for FilesDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestColumnSettingsDialog:
    """unittest for dialogs_qt.ColumnSettingsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ColumnSettingsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ColumnSettingsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ColumnSettingsDialog, '__init__', mock_init)
        testobj = testee.ColumnSettingsDialog()
        assert capsys.readouterr().out == 'called ColumnSettingsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.__init__
        """
        testobj = testee.ColumnSettingsDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_add_row(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.add_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_row(name='', width='', is_flag=False, colno='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_delete_row(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.delete_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.delete_row(rownum) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_text_changed(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.on_text_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_text_changed(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_column(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.add_column
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_column() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_columns(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.remove_columns
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_columns() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestNewColumnsDialog:
    """unittest for dialogs_qt.NewColumnsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.NewColumnsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called NewColumnsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.NewColumnsDialog, '__init__', mock_init)
        testobj = testee.NewColumnsDialog()
        assert capsys.readouterr().out == 'called NewColumnsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for NewColumnsDialog.__init__
        """
        testobj = testee.NewColumnsDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for NewColumnsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestExtraSettingsDialog:
    """unittest for dialogs_qt.ExtraSettingsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ExtraSettingsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ExtraSettingsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ExtraSettingsDialog, '__init__', mock_init)
        testobj = testee.ExtraSettingsDialog()
        assert capsys.readouterr().out == 'called ExtraSettingsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.__init__
        """
        testobj = testee.ExtraSettingsDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_add_row(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.add_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_row(name='', value='', desc='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_delete_row(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.delete_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.delete_row(rownum) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_setting(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.add_setting
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_setting() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_settings(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.remove_settings
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_settings() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestEntryDialog:
    """unittest for dialogs_qt.EntryDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.EntryDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EntryDialog.__init__ with args', args)
        monkeypatch.setattr(testee.EntryDialog, '__init__', mock_init)
        testobj = testee.EntryDialog()
        assert capsys.readouterr().out == 'called EntryDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for EntryDialog.__init__
        """
        testobj = testee.EntryDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_add_key(self, monkeypatch, capsys):
        """unittest for EntryDialog.add_key
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_key() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_delete_key(self, monkeypatch, capsys):
        """unittest for EntryDialog.delete_key
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.delete_key() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for EntryDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestCompleteDialog:
    """unittest for dialogs_qt.CompleteDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.CompleteDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CompleteDialog.__init__ with args', args)
        monkeypatch.setattr(testee.CompleteDialog, '__init__', mock_init)
        testobj = testee.CompleteDialog()
        assert capsys.readouterr().out == 'called CompleteDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for CompleteDialog.__init__
        """
        testobj = testee.CompleteDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for CompleteDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_read_data(self, monkeypatch, capsys):
        """unittest for CompleteDialog.read_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.read_data() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_build_table(self, monkeypatch, capsys):
        """unittest for CompleteDialog.build_table
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_table() == "expected_result"
        assert capsys.readouterr().out == ("")


def _test_show_dialog(monkeypatch, capsys):
    """unittest for dialogs_qt.show_dialog
    """
    assert testee.show_dialog(win, cls) == "expected_result"
