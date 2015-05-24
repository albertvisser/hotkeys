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
    qt version of the app
hotkeys_wx.py
    original wx version of the app
images.py
    programma om in de wx versies gebruikte images te genereren

editor/languages: directory containing the language files
---------------------------------------------------------

dutch.lng
    taalbestand met Nederlandse teksten
english.lng
    taalbestand met Engelse teksten

editor/plugins: directory meant to contain tool plugins
-------------------------------------------------------

editor/plugin_examples: directory containing examples of these
--------------------------------------------------------------

abapkeys.py
    specific code for the ABAP plugin
audacity_keys.py
bash_keys.py
dckeys.py
    specific code for the double commander plugin
filezilla_keys.py
firefox_keys.py
gimp_keys.py
kdiff3_keys.py
operakeys.py
opkeys.py
    specific code for the Opera plugin
scikeys.py
    specific code for the SciTE plugin
tcmdrkys.py
    specific code for the TC plugin
    gebruikt xml.etree, csv
tckey_wxgui.py
    older (wx) version of TC the plugin
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
vivaldi_keys.py

editor/test: diirectory containg test programs and data
-------------------------------------------------------

test_dckeys.py
test_scikeys.py
test_tcmdrkeys.py
test_viksettings.py
