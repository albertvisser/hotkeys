"""Hotkeys plugin for DIA diagram editor
"""
import functools
import editor.plugins.gtkaccel_keys as gk
F_KEYS = 'DIA_KEYS', 'DIA_DESCS'
buildcsv = functools.partial(gk.buildcsv, F_KEYS)
add_extra_attributes = gk.add_extra_attributes
