"""Hotkeys plugins voor gtk-accel based apps - GUI toolkit specifieke code
"""

from ..toolkit import toolkit
if toolkit == 'qt':
    from .gtkaccel_keys_qt import send_completedialog
elif toolkit == 'wx':
    from .gtkaccel_keys_wx import send_completedialog
