"""VI plugin for HotKeys - intermediary file to direct which gui-toolkit specific module
functions are imported from
"""
from ..toolkit import toolkit
if toolkit == 'qt':
    from .vikeys_qt import add_extra_fields, layout_extra_fields_topline
elif toolkit == 'wx':
    from .vikeys_wx import add_extra_fields, layout_extra_fields_topline
else:
    raise ValueError('Unknown GUI toolkit')
