"""Hotkeys applicatie: intermediary module to determine for which GUI toolkit the widgets
will be imported and "relayed" to the main program
"""
from .toolkit import toolkit
if toolkit == 'qt':
    from .gui_qt import Gui, TabbedInterface, SingleDataInterface  # , DummyPage
    from .dialogs_qt import (show_message, show_cancel_message, ask_question, ask_ync_question,
                             get_textinput, get_choice, get_file_to_open, get_file_to_save,
                             show_dialog, InitialToolDialog, FilesDialog, ColumnSettingsDialog,
                             ExtraSettingsDialog, EntryDialog, CompleteDialog, NewColumnsDialog)
elif toolkit == 'wx':
    from .gui_wx import Gui, TabbedInterface, SingleDataInterface  # , DummyPage
    from .dialogs_wx import (show_message, show_cancel_message, ask_question, ask_ync_question,
                             get_textinput, get_choice, get_file_to_open, get_file_to_save,
                             show_dialog, InitialToolDialog, FilesDialog, ColumnSettingsDialog,
                             ExtraSettingsDialog, EntryDialog, CompleteDialog, NewColumnsDialog)
else:
    raise ValueError("Incorrect GUI toolkit requested (only 'qt' and 'wx' possible")
