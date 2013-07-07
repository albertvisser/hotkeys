# -*- coding: UTF-8 -*-

import os
import sys
HERE = os.path.abspath(os.path.dirname(__file__))
TTL = "A hotkey viewer/editor"
VRS = "1.1.x"
AUTH = "(C) 2008 Albert Visser"
## INI = "vikey_config.py"
WIN = True if sys.platform == "win32" else False
LIN = True if os.name == 'posix' else False
# voorziening voor starten op usb-stick onder Windows (drive letters in config aanpassen)
## if WIN and __file__ != "tckey_gui.py":
    ## drive = os.path.splitdrive(os.getcwd())[0] + "\\"
    ## with open(INI) as f_in:
        ## lines = f_in.readlines()
    ## for line in lines:
        ## if line.startswith('TC_PAD='):
            ## olddrive = line[7:10]
            ## break
    ## if olddrive.upper() != drive.upper():
        ## bak = INI + ".bak"
        ## if os.path.exists(bak):
            ## os.remove(bak)
        ## os.rename(INI,bak)
        ## with open(INI,"w") as f_out:
            ## for line in lines:
                ## if olddrive.lower() in line:
                    ## f_out.write(line.replace(olddrive.lower(),drive.upper()))
                ## elif olddrive.upper() in line:
                    ## f_out.write(line.replace(olddrive.upper(),drive.upper()))
                ## else:
                    ## f_out.write(line)

# constanten voor  captions en dergelijke (correspondeert met nummers in language files)
C_KEY, C_MOD, C_SRT, C_CMD, C_OMS = '001', '043', '002', '003', '004'
C_DFLT, C_RDEF = '005', '006'
M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'
C_SAVE, C_DEL, C_EXIT, C_KTXT, C_CTXT ='010', '011', '012', '018', '019'
M_APP, M_READ, M_SAVE, M_USER, M_EXIT = '200', '201', '202', '203', '209'
M_SETT, M_LOC, M_LANG, M_HELP, M_ABOUT = '210', '211', '212', '290', '299'
C_MENU = (
    (M_APP,(M_READ, M_SAVE, -1 , M_EXIT)),
    (M_SETT,(M_LOC,M_LANG)),
    (M_HELP,(M_ABOUT,))
    )
NOT_IMPLEMENTED = '404'
