#! /usr/bin/env python3
"""A Manager for all your applications' hotkeys
"""
import argparse
from editor.main import Editor, quick_check

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-c', '--config', dest='conf',
                    help='name of module with config parameters (without .py'
                         ' extension)')
parser.add_argument('-q', '--quick-check', dest='check',
                    help='name of CSV file to check without starting up the GUI')
args = parser.parse_args()
if args.check:
    quick_check(args.check)
else:
    Editor(args)
