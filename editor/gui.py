"""Hotkeys applicatie: intermediary module to determine for which GUI toolkit the widgets
will be imported and "relayed" to the main program
"""
from .toolkit import toolkit
if toolkit == 'qt':
    from .qtgui import (Gui, TabbedInterface, SingleDataInterface, show_message, show_cancel_message,
                        ask_question, ask_ync_question, get_textinput, get_choice,
                        get_file_to_open, get_file_to_save, show_dialog, InitialToolDialogGui,
                        FilesDialogGui, SetupDialogGui, DeleteDialogGui,
                        ColumnSettingsDialogGui, NewColumnsDialogGui,
                        ExtraSettingsDialogGui, EntryDialogGui, CompleteDialogGui)
elif toolkit == 'wx':
    from .wxgui import (Gui, TabbedInterface, SingleDataInterface, show_message, show_cancel_message,
                        ask_question, ask_ync_question, get_textinput, get_choice,
                        get_file_to_open, get_file_to_save, show_dialog, InitialToolDialogGui,
                        FilesDialogGui, SetupDialogGui, DeleteDialogGui,
                        ColumnSettingsDialogGui, NewColumnsDialogGui,
                        ExtraSettingsDialogGui, EntryDialogGui, CompleteDialogGui)
else:
    raise ValueError("Incorrect GUI toolkit requested (only 'qt' and 'wx' possible")
