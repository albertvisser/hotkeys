# -*- coding: UTF-8 -*-
"""HotKeys: non-gui and csv related functions
"""
import os
import sys
import pathlib
import enum
import logging

HERE = pathlib.Path(__file__).parent.resolve()  # os.path.abspath(os.path.dirname(__file__))
WIN = True if sys.platform == "win32" else False
LIN = True if os.name == 'posix' else False

LOGFILE = pathlib.Path('/tmp') / 'logs' / 'hotkeys.log'
DO_LOGGING = os.environ.get("DEBUG", '') not in ('', "0")
LOGFILE.parent.mkdir(exist_ok=True)
LOGFILE.touch(exist_ok=True)
logging.basicConfig(filename=str(LOGFILE), level=logging.DEBUG, format='%(asctime)s %(message)s')


def log(message, always=False):
    "output to log"
    if always or DO_LOGGING:
        logging.info(message)


def log_exc(message=''):
    "output exception to log"
    logging.exception(message)


def save_log():
    """intention: rename previous log file
    oddly enough, this renames the current log file immediately
    also, log messages are written to it despite the name being changed...
    """
    if not LOGFILE.exists():  # dit is dus nooit aan de hand
        return
    for last in reversed(sorted(LOGFILE.parent.glob(LOGFILE.name + '*'))):
        break
    if last.suffix == LOGFILE.suffix:
        newlast = 0
    else:
        newlast = int(last.suffix[1:]) + 1
    LOGFILE.rename(LOGFILE.with_suffix('.'.join((LOGFILE.suffix, str(newlast)))))


class SettType(enum.Enum):
    """Types of settings (second value on line with first value = setting
    """
    PLG = 'PluginName'
    PNL = 'PanelName'
    RBLD = 'RebuildCSV'
    DETS = 'ShowDetails'
    RDEF = 'RedefineKeys'


csv_settingnames = [x.value for x in SettType.__members__.values()]
mode_f, mode_r = 'Fixed', 'Remember'


def get_text(win, message_id='', text='', args=None):
    """retourneer de tekst geïdentificeerd door <message_id>
    als <text> is opgegeven wordt die gebruikt
    <args> bevat een list van waarden die in de tekst kunnen worden ingevuld
    """
    try:
        win = win.editor
    except AttributeError:
        try:
            win = win.master
        except AttributeError:
            pass
    if message_id:
        text = win.captions[message_id].replace(' / ', '\n')
    elif not text:
        text = win.captions['I_NOMSG']
        raise ValueError(text)
    if args:
        text = text.format(*args)
    return text


def get_open_title(win, message_id, oms):
    """Build title for File Open  / Save dialog
    """
    what = get_text(win, message_id)
    if oms:
        what = ' - '.join((what, oms))
    return what


def get_title(win):
    "retourneer de titel voor de te tonen pagina"
    try:
        title = win.title
    except AttributeError:
        try:
            title = win.editor.title
        except AttributeError:
            title = win.master.title
    return title
