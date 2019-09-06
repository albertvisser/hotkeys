"""Hotkeys plugin for Double Commander
intermediary file to direct which gui-toolkit specific module functions are imported from
"""
from ..toolkit import toolkit
if toolkit == 'qt':
    from .dckeys_qt import add_extra_fields, layout_extra_fields, send_completedialog
elif toolkit == 'wx':
    from .dckeys_wx import add_extra_fields, layout_extra_fields, send_completedialog
else:
    raise ValueError('Unknown GUI toolkit')
