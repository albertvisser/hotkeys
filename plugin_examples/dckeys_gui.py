"""Hotkeys plugin for Double Commander
intermediary file to direct which gui-toolkit specific module functions are imported from
"""
from ..toolkit import toolkit
if toolkit == 'qt':
    from .dckeys_qt import layout_extra_fields  # , DcCompleteDialog
elif toolkit == 'wx':
    from .dckeys_wx import layout_extra_fields  # , DcCompleteDialog
else:
    raise ValueError('Unknown GUI toolkit')
