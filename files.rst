Files in this directory
=======================

__init__.py
    (lege) package indicator
files.rst
    deze tekst
hotkeys.py
    starter voor de alles-in-een applicatie



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

abapkeys.py
    specific code for the ABAP plugin
dckeys.py
    specific code for the double commander plugin

hotkeys_qt.py
    qt version of the app
hotkeys_wx.py
    original wx version of the app
hotkey_config.py
    settings for the app (language)

opkeys.py
    specific code for the Opera plugin
scikeys.py
    specific code for the SciTE plugin

tckey_config.py
    contains file names/locations for settings
tckey_wxgui.py
    older (wx) version of the plugin
tcmdrkys.py
    I/O module for the settings
    data manipulatie routines voor TC Hotkeys Editor
    gebruikt xml.etree, csv
tcmerge.py
    starter voor TC Command Merger
    importeerde tcmerge_wx.py, nu tcmerge_qt.py
tcmerge_qt.py
    program for building the keydef csv qt version
    NB: the non-ui parts may be transferred to tcmdrkys.py
tcmerge_wx.py
    program for building the keydef csv wx version
    Main GUI code voor TC Command Merger, wxPython versie
    gebruikt wx, csv
    importeert tccm_mixin, tcmdrkys

vikeys.py
    specific code for the VI plugin
