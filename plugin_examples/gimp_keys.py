"""Hotkeys plugin for The GIMP
"""
import functools
import editor.plugins.gtkaccel_keys as gk

MARKER = '(action'
F_KEYS = 'GMP_KEYS', 'GMP_DESCS'
build_data = functools.partial(gk.build_data, F_KEYS)
add_extra_attributes = gk.add_extra_attributes
