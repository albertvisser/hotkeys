# -*- coding: UTF-8 -*-

import os
import sys

HERE = os.path.abspath(os.path.dirname(__file__))
## try:
    ## HOME = os.environ('HOME')
## except KeyError:
    ## HOME = os.environ('USERPROFILE') # Windows
CONF = os.path.join(HERE, 'hotkey_config.py') # don't import, can be modified at runtime
VRS = "2.1.x"
AUTH = "(C) 2008-today Albert Visser"
WIN = True if sys.platform == "win32" else False
## LIN = True if sys.platform == 'linux2' else False
LIN = True if os.name == 'posix' else False

# constanten voor  captions en dergelijke (correspondeert met nummers in language files)
# *** toegesneden op TC verplaatsen naar TC plugin? ***
C_KEY, C_MOD, C_SRT, C_CMD, C_OMS = '001', '043', '002', '003', '004'
C_DFLT, C_RDEF = '005', '006'
M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'
C_SAVE, C_DEL, C_EXIT, C_KTXT, C_CTXT ='010', '011', '012', '018', '019'
M_APP, M_READ, M_SAVE, M_RBLD, M_EXIT = '200', '201', '202', '203', '209'
M_SETT, M_LOC, M_LANG, M_TOOL, M_COL = '210', '211', '212', '213', '214'
M_HELP, M_ABOUT = '290', '299'
NOT_IMPLEMENTED = '404'

csv_linetypes = ['Setting', 'Title', 'Width', 'Seq', 'is_type', 'Keydef']
csv_settingtype, csv_keydeftype = csv_linetypes[0], csv_linetypes[-1]
csv_titletype, csv_widthtype, csv_seqnumtype, csv_istypetype = csv_linetypes[1:-1]
csv_settingnames = ['PluginName', 'PanelName', 'RebuildCSV', 'RedefineKeys']
csv_oms = dict(zip(csv_settingnames + csv_linetypes[1: -1], (
 'Naam van de module met toolspecifieke code (zonder .py)',
 'Naam van het toolpanel in de selector',
 "1 = possible to rebuild this file from the tools' settings; else 0",
 '1 = possible to change keydefs and save them back; else 0',
 'Titles of the columns in the display; refer to keys in the language file',
 'Column widths',
 'Column sequence numbers in the display',
 '1 = Column indicates if keydef is original or (re)defined; else 0')))
csv_sample_data = []
for indx, data in enumerate((
        [C_KEY, C_MOD, C_OMS],
        [120, 90, 292],
        [0, 1, 2],
        [0, 0, 0],)):
    name = csv_linetypes[indx + 1]
    oms = csv_oms[name]
    data.insert(0, name)
    data.append(oms)
    csv_sample_data.append(data)
plugin_skeleton = """# -*- coding: UTF-8 -*-\n
# uncomment these where appropriate
# import collections
# import PyQt4.QtGui as gui
# import PyQt4.QtCore as core

# uncomment this to define a routine to (re)build the csv file from source data
# def buildcsv(settings):
#     shortcuts = collections.defaultdict
#     ...implement some logic here...
#     return shortcuts

# uncomment this to define a subpanel used for (re)defining hotkeys
# copy the contents of this class from DummyPanel in hotkeys_qt.py
# class MyPanel(gui.QFrame):
#     pass

# uncomment this to define a routine to write back the keydefs to the source data
# def savekeys(filename):
#     pass
"""
