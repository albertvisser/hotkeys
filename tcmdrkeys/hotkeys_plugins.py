# plugin imports
from .tc_plugin import TC_MENU, TC_MENU_FUNC
from .tc_plugin import MyPanel as TCPanel
from .vi_plugin import MyPanel as VIPanel
from .scite_plugin import MyPanel as SciTEPanel
from .opera_plugin import MyPanel as OperaPanel
from .doublecmd_plugin import MyPanel as DCPanel
from .abap_plugin import MyPanel as ABPanel
from .generic_plugin import MyPanel as EmptyPanel

# list containing the plugins themselves
PLUGINS = [
    ("VI", VIPanel),
    ("Total Commander", TCPanel),
    ("SciTE", SciTEPanel),
    ("Double Commander", DCPanel),
    ("Opera", OperaPanel),
    ("ABAP Editor", ABPanel),
    ]

# dict containing additional menus, if any
MENUS = {}
for key, _ in PLUGINS:
    MENUS[key] = ((), {})
MENUS["Total Commander"] = (TC_MENU, TC_MENU_FUNC)
