import functools
import editor.plugins.gtkaccel_keys as gk
F_KEYS = 'BNSH_KEYS'
buildcsv = functools.partial(gk.buildcsv, F_KEYS)
MyPanel = gk.MyPanel
