"""Hotkeys applicatie: intermediary module to determine for which GUI toolkit the widgets
will be imported and "relayed" to the main program
"""
# from .gui_qt import Gui, TabbedInterface, SingleDataInterface
# from .dialogs_qt import show_message, ask_question, get_textinput, get_choice
# from .dialogs_qt import manage_startupsettings, manage_filesettings
# from .dialogs_qt import manage_columnsettings, manage_extrasettings, manual_entry
from .gui_wx import Gui, TabbedInterface, SingleDataInterface
from .dialogs_wx import show_message, ask_question, get_textinput, get_choice
from .dialogs_wx import manage_startupsettings, manage_filesettings
from .dialogs_wx import manage_columnsettings, manage_extrasettings, manual_entry
