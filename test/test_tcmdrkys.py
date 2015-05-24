import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import editor.plugin_examples.tcmdrkys as tc
from logbook import Logger, FileHandler
logger = Logger(__file__)

def test_keymods(key, win):
    logger.info('keymods("{}") = "{}"'.format(key, tc.keymods(key, win)))

def test_keymods2(key):
    logger.info('keymods2("{}") = "{}"'.format(key, tc.keymods2(key)))

def test_userkeys(root):
    logger.info('test userkeys')
    data = tc.userkeys(root)
    for line in data:
        logger.info(line)

def test_keyboardtext():
    kt = tc.keyboardtext(os.getcwd())
    for item in kt:
        logger.info('%s %s' % item)

def test_tckeys():
    cl = tc.TCKeys([os.getcwd(),])
    cl.read()
    for item in cl.defkeys:
        logger.info('%s %s' % item)
    ## cl.turn_into_xml()
    ## cl.write()
    ## h = raw_input()

def test_readkeys():
    cmdict, omsdict, defkeys, data = tc.readkeys([os.getcwd(),])
    ## print defkeys
    for key, value in defkeys.items():
        logger.info('%s %s' % (key, value))

if __name__ == '__main__':
    log_handler = FileHandler('test_tcmdrkys.log')
    with log_handler.applicationbound():
        logger.info('')
        ## for key in ('F11', 'C+D', 'AS+C', 'CS+H', 'NUM + 1', 'WCA+F6', 'W + V'):
            ## test_keymods(key, win=False)
        ## logger.info('')
        ## for key in ("F1", "ALT+SHIFT+F5", "NUM +", "SHIFT+NUM +", "SHIFT+NUM -"):
            ## test_keymods2(key)
        ## logger.info('')
        ## test_userkeys(os.getcwd())
        ## test_tckeys()
        test_keyboardtext()
        ## test_readkeys()
