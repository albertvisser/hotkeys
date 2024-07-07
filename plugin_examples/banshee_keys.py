"""Hotkeys plugin for Banshee Music Player
"""
import functools
import editor.plugins.gtkaccel_keys as gk
F_KEYS = 'BNSH_KEYS'
build_data = functools.partial(gk.build_data, F_KEYS)
add_extra_attributes = gk.add_extra_attributes
