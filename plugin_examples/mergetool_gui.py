"""choose the gui toolkit-specific code
"""
from ..toolkit import toolkit
if toolkit == 'qt':
    from ..plugins.mergetool_qt import MergeDialogGui
elif toolkit == 'wx':
    from ..plugins.mergetool_wx import MergeDialogGui

