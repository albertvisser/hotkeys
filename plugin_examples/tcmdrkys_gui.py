"""Hotkeys plugins voor Total Commander - GUI toolkit specifieke code
"""

from ..toolkit import toolkit
if toolkit == 'qt':
    from .tcmdrkys_qt import send_mergedialog
elif toolkit == 'wx':
    from .tcmdrkys_wx import send_mergedialog
