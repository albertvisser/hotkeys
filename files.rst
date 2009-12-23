Files in this directory
=======================

tc_keys.py
    starter voor tckey_gui.py in package directory "tcmdrkeys"
tc_merge.py
    starter voor tcmerge_wx.py in package directory "tcmdrkeys"

files in package directory
--------------------------

__init__.py
    (lege) package indicator
dutch.lng
    taalbestand met Nederlandse teksten
english.lng
    taalbestand met Engelse teksten
images.py
    programma om gebruikte images te genereren
tccm.py
    starter voor TC Command Merger
    importeert tcmerge_wx
tccm_mixin.py
    GUI-onafhankelijke code voor TCMerge
    moet daar nog uit afgesplitst worden
tckey_gui.py
    main GUI code voor TC Hotkeys editor, wxPython versie
    gebruikt wx
    importeert images, tcmdrkys
tcmdrkys.py
    data manipulatie routines voor TC Hotkeys Editor
    gebruikt xml.etree, csv
tcmerge_wx.py
    Main GUI code voor TC Command Merger, wxPython versie
    gebruikt wx, csv
    importeert tccm_mixin, tcmdrkys


maakt geen deel uit van project files:
--------------------------------------

tccm_command_merger_for_total_commander
    korte beschrijving/requirement voor tccm