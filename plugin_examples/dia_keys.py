"""Hotkeys plugin for DIA diagram editor
"""
import functools
import editor.plugins.gtkaccel_keys as gk
F_KEYS = 'DIA_KEYS', 'DIA_DESCS'
build_data = functools.partial(gk.build_data, F_KEYS)
add_extra_attributes = gk.add_extra_attributes
