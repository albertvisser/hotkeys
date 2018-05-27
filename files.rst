Files in this directory
=======================

__init__.py
    (lege) package indicator
files.rst
    deze tekst
readme.rst
    program description
start.py
    starter voor de alles-in-een applicatie

editor: directory containing the main program files
---------------------------------------------------

__init__.py
    (lege) package indicator
hotkey_config.py
    settings for the app (plugins, language)
hotkey_config_all.py (not included)
    version of the config file containing all plugin examples
hotkey_config_example.py
    version of the config file containing the demo/sample plugin
hotkeys_constants.py
    various symbols used by hotkeys_qt.py as well as non-gui routines
hotkeys_dialogs_qt5.py
    various dialogs called by the main program
hotkeys_qt4.py
    main program, pyqt4 version (no longer maintained)
hotkeys_qt5.py
    main program, pyqt5 version
hotkeys_wx.py
    main program, wxpython version (no longer maintained)

editor/languages: directory containing the language files
---------------------------------------------------------

dutch.lng
    taalbestand met Nederlandse teksten
english.lng
    taalbestand met Engelse teksten

editor/plugins: directory meant to contain tool plugins
-------------------------------------------------------

example_app_hotkeys.csv
    sample CSV file
example_app_keys.py
    sample plugin (all code commented out)
readme.txt
    placeholder

plugin_examples: directory containing examples of these
-------------------------------------------------------
support for showing keydef details is now built into the main program

abapkeys.py
    plugin for SAP ABAP-editor (which I use at work, but I'm not allowed to use
    this tool there).
    support for reading the tool configuration

audacity_keys.py
    plugin for Audacity; support for reading the tool configuration and writing
    back to it

banshee_keys.py
    plugin for Banshee; uses gtkaccel_keys.py

bash_keys.py
    plugin for Bash; currently empty

completedialog.py
    classes for dialogs to add descriptions not provided by program settings

dckeys.py
    plugin for Double Commander; support for reading the tool configuration and
    writing back to it

dia_keys.py
    plugin for Dia; uses gtkaccel_keys.py

gimp_keys.py
    plugin for GIMP; uses gtkaccel_keys.py

gtkaccel_keys.py
    shared routines for plugins using a gtkaccel_map; support for reading tool
    configuration

nemo_keys.py
    plugin for Nemo; uses gtkaccel_keys.py

operakeys.py
    plugin for Opera up until version 12; support for reading the tool configuration
    Sadly this web browser is discontinued

opkeys.py
    plugin for Opera from version 15 onwards; support for reading the tool
    configuration

pgadmin3_keys
    plugin for PGAdmin3; currently generates a csv file from text

read_gtkaccel.py
    helper routines for plugins that manage programs using a GTK keyboard accelerator map

scikeys.py
    plugin for SciTE; support for reading the tool configuration and writing back
    to it

system_keys.py
    plugin for system-wide keyboard shortcuts; currently generates a csv file from
    text

tcmdrkys.py
    plugin for Total Commander; support for reading the tool configuration and
    writing back to it,
    as well as a gui extension for editing keydefs

vikeys.py
    plugin for VI(M); currently generates a csv file from text

vivaldi_keys.py
    plugin for Vivaldi; currently generates a csv file from text
