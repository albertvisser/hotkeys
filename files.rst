Files in this directory
=======================

__init__.py
    (lege) package indicator
files.rst
    deze tekst
hotkeys.py
    starter voor de alles-in-een applicatie
tc_keys.py
    starter voor tckey_gui.py in package directory "tcmdrkeys"
tc_merge.py
    starter voor tcmerge_wx.py in package directory "tcmdrkeys"
vi_keys.py
    starter voor vikey_gui.py
de extra starters mogen wel weg eigenlijk.

niet onder version control, wel nodig:

abkey_config.py
    settings voor de abap editor plugin
dckey_config.py
    settings voor de double commander plugin
opkey_config.py
    settings voor de opera plugin
scikey_config.py
    settings voor de scite plugin
tckey_config.py
    settings voor de TC plugin
vikey_config.py
    settings voor de vi plugin
voorlopig is het gebouwd op dat deze files in deze directory zitten


files in package directory (editor)
-----------------------------------

__init__.py
    (lege) package indicator
dutch.lng
    taalbestand met Nederlandse teksten
english.lng
    taalbestand met Engelse teksten
images.py
    programma om in de wx versies gebruikte images te genereren

abap_plugin.py
    new (qt) version of the plugin
abkey_config.py
    contains file names/locations for settings
abapkeys.py
    I/O module for the settings

create_plugin.py
    probeersel voor het genereren van de basiscode voor een nieuwe plugin

doublecmd_plugin.py
    new (qt) version of the plugin
dckey_config.py
    contains file names/locations for settings
dckeys.py
    I/O module for the settings
dcmerge.py
    program for building the keydef csv

hotkeys_qt.py
    qt version of the app
hotkeys_shared.py
    shared code, currently contains constants, menu functions, base classes
hotkeys_wx.py
    original wx version of the app
hotkey_config.py
    settings for the app (language)
hotkeys_plugins.py
    plugin configuration (which ones, which imports to do)


opera_plugin.py
    new (qt) version of the plugin
opkey_config.py
    contains file names/locations for settings
opkeys.py
    I/O module for the settings
opmerge.py
    program for building the keydef csv

scikey_config.py
    contains file names/locations for settings
scikeys.py
    I/O module for the settings
scimerge.py
    program for building the keydef csv
scite_plugin.py
    new (qt) version of the plugin

tckey_config.py
    contains file names/locations for settings
tckey_wxgui.py
    older (wx) version of the plugin
tcmdrkys.py
    I/O module for the settings
    data manipulatie routines voor TC Hotkeys Editor
    gebruikt xml.etree, csv
tcmerge_mixin.py
    GUI-onafhankelijke code voor TCMerge
    moet daar nog uit afgesplitst worden
tcmerge.py
    starter voor TC Command Merger
    importeerde tcmerge_wx.py, nu tcmerge_qt.py
tcmerge_qt.py
    program for building the keydef csv qt version
tcmerge_wx.py
    program for building the keydef csv wx version
    Main GUI code voor TC Command Merger, wxPython versie
    gebruikt wx, csv
    importeert tccm_mixin, tcmdrkys
tc_plugin.py
    new (qt) version of the plugin
    main GUI code voor TC Hotkeys editor, wxPython versie
    gebruikt wx
    importeert images, tcmdrkys

vikey_config.py
    contains file names/locations for settings
vikey_gui.py
    older (wx) version of the plugin
vikeys.py
    I/O module for the settings
vi_plugin.py
    new (qt)version of the plugin
