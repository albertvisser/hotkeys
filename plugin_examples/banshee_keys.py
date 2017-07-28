"""Hotkeys plugin for Banshee Music Player
"""
import functools
import editor.plugins.gtkaccel_keys as gk
F_KEYS = 'BNSH_KEYS'
buildcsv = functools.partial(gk.buildcsv, F_KEYS)
add_extra_attributes = gk.add_extra_attributes
