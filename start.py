#! /usr/bin/env python3
"""A Manager for all your applications' hotkeys
"""
import argparse
from editor.main import Editor, quick_check

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-c', '--config', dest='conf',
                    help='full name of file with config parameters (with .json' ' extension)')
parser.add_argument('-q', '--quick-check', dest='check',
                    help='full name of config file to check without starting up the GUI')
parser.add_argument('-s', '--startapp', dest='start', help='name of tool to display on startup')
args = parser.parse_args()
if args.check:
    quick_check(args.check)
else:
    Editor(args)
