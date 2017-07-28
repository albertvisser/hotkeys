"""Hotkeys plugin for The GIMP
"""
import functools
import editor.plugins.gtkaccel_keys as gk
F_KEYS = 'GMP_KEYS'
buildcsv = functools.partial(gk.buildcsv, F_KEYS)
add_extra_attributes = gk.add_extra_attributes
