"""choose the gui toolkit-specific code
"""
from ...toolkit import toolkit
if toolkit == 'qt':
    from ...plugins.mergetool.qtgui import MergeDialogGui
elif toolkit == 'wx':
    from ...plugins.mergetool.wxgui import MergeDialogGui
