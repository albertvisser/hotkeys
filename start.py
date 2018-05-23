#! /usr/bin/env python3
"""A Manager for all your applications' hotkeys
"""
import argparse
## from editor.hotkeys_wx import main
## from editor.hotkeys_qt import main
from editor.hotkeys_qt5 import main

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-c', '--config', dest='conf',
                    help='name of module with config parameters (without .py'
                         ' extension)')
args = parser.parse_args()
main(args)
