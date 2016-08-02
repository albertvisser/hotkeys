"""
This file contains some program wide settings
"""
# supported tools
# Each entry is a tuple containing the name of the tool and the full path to a
# csv file, where the key definitions are stored and also some settings specific
# This particular setting uses a predefined path relative to this file
plugins = [
    ("Example App", "editor/plugins/example_app_hotkeys.csv"),
    ]
# interface language
# name (not full path) of the current language file
LANG='english.lng'
# application to show: selected or remember on closing
STARTUP = 'Remember'
# application to show on startup
INITIAL = 'Example App'
