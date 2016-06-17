Files in this directory
=======================

__init__.py
    (lege) package indicator
files.rst
    deze tekst
hotkeys.py
    starter voor de alles-in-een applicatie
readme.rst
    program description

editor: directory containing the main program files
---------------------------------------------------

__init__.py
    (lege) package indicator
hotkey_config.py
    settings for the app (plugins, language)
hotkey_config_example.py
    version of the config file containing the example plugins
hotkeys_constants.py
    various symbols used by hotkeys_qt.py
hotkeys_qt.py
    mai program, qt version

editor/languages: directory containing the language files
---------------------------------------------------------

dutch.lng
    taalbestand met Nederlandse teksten
english.lng
    taalbestand met Engelse teksten

editor/plugins: directory meant to contain tool plugins
-------------------------------------------------------

plugin_examples: directory containing examples of these
-------------------------------------------------------

abapkeys.py
    plugin for SAP ABAP-editor (which I use at work, but I'm not allowed to use this tool there).
    support for reading the tool configuration

audacity_keys.py
    plugin for Audacity; support for reading the tool configuration and writing back to it

banshee_keys.py
    plugin for Banshee; support for reading the tool configuration

dckeys.py
    plugin for Double Commander; support for reading the tool configuration and writing back to it

operakeys.py
    plugin for Opera up until version 12; support for reading the tool configuration
    Sadly this web browser is discontinued

read_gtkaccel.py
    helper routines for plugins that manage programs using a GTK keyboard accelerator map

scikeys.py
    plugin for SciTE; support for reading the tool configuration and writing back to it

tcmdrkys.py
    plugin for Total Commander; support for reading the tool configuration and writing back to it,
    as well as a gui extension for editing keydefs
