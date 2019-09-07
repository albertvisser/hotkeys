"""Hotkeys plugins voor gtk-accel based apps - GUI toolkit specifieke code
"""

from ..toolkit import toolkit
if toolkit == 'qt':
    from .gtkaccel_keys_qt import AccelCompleteDialog
elif toolkit == 'wx':
    from .gtkaccel_keys_wx import AccelCompleteDialog
