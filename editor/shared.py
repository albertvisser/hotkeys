"""HotKeys: non-gui and keydef related functions
"""
import os
import sys
import pathlib
import contextlib
import enum
import logging

HERE = pathlib.Path(__file__).parent.resolve()  # os.path.abspath(os.path.dirname(__file__))
HERELANG = HERE / 'languages'    # os.path.join(HERE, 'languages')
WIN = sys.platform == "win32"
LIN = os.name == 'posix'

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
    """alter the log file name, adding a next-highest version number
    currently caters for max. 100 versions
    """
    # for last in reversed(sorted(LOGFILE.parent.glob(LOGFILE.name + '*'))):
    #    break
    last = list(reversed(sorted(LOGFILE.parent.glob(LOGFILE.name + '*'))))[0]
    newlast = 0 if last.suffix == LOGFILE.suffix else int(last.suffix[1:]) + 1
    LOGFILE.rename(LOGFILE.with_suffix('.'.join((LOGFILE.suffix, f'{newlast:02}'))))


class SettType(enum.Enum):
    """Types of settings (second value on line with first value = setting
    """
    PLG = 'PluginName'
    PNL = 'PanelName'
    RBLD = 'RebuildData'
    DETS = 'ShowDetails'
    RDEF = 'RedefineKeys'


settingnames = [x.value for x in SettType.__members__.values()]
mode_f, mode_r = 'Fixed', 'Remember'


def get_text(win, message_id='', text='', args=None):
    """retourneer de tekst geïdentificeerd door <message_id>
    als <text> is opgegeven wordt die gebruikt
    <args> bevat een list van waarden die in de tekst kunnen worden ingevuld
    """
    # try:
    #     win = win.editor
    # except AttributeError:
    #     with contextlib.suppress(AttributeError):
    #         win = win.master
    win = get_appropriate_window(win)
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
        what = f'{what} - {oms}'
    return what


def get_title(win):
    "retourneer de titel voor de te tonen pagina"
    # try:
    #     title = win.title
    # except AttributeError:
    #     try:
    #         title = win.editor.title
    #     except AttributeError:
    #         title = win.master.title
    return get_appropriate_window(win).title


def get_appropriate_window(win):
    "find the widget associated with a window"
    if hasattr(win, 'editor'):
        win = win.editor
    elif hasattr(win, 'master'):
        win = win.master
    return win
