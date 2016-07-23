import functools
import editor.plugins.gtkaccel_keys as gk
F_KEYS = 'NEMO_KEYS'
buildcsv = functools.partial(gk.buildcsv, F_KEYS)
MyPanel = gk.MyPanel
