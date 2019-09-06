"""Hotkeys plugins voor Total Commander - GUI toolkit specifieke code
"""

from ..toolkit import toolkit
if toolkit == 'qt':
    from .tcmdrkeys_qt import send_mergedialog
elif toolkit == 'wx':
    from .tcmdrkeys_wx import send_mergedialog
