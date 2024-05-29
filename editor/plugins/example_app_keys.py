"""Hotkeys plugin example

this module contains the general, non gui-toolkit specific part of the code
"""
# uncomment these where appropriate
# import collections
# from example_app_keys_gui import layout_extra_fields_*  # om dit beschikbaar te maken voor import

# uncomment this to define a routine to (re)build the csv file from source data
# showinfo is a switch for in case you want to show instructions
# otherstuff can be used to pass on things like a list of possible commands
# to method add_extra_attributes
# ** corresponds to the Rebuild_data setting **
# def build_data(parent, showinfo=True):
#     shortcuts = collections.defaultdict()
#     otherstuff = {}
#     ...implement some logic here...
#     return shortcuts, otherstuff

# uncomment these to define routines to be used by methods of a HotKeyPanel instance
# ** corresponds to the ShowDetails setting **
# win is a reference to the HotKeyPanel instance
# def add_extra_attributes(win):
#     """add attributes specific to this plugin
#     e.g a shorter name for a collection read from build_data's otherstuff
#     some of these are needed when filling fields in the details part of the screen
#     """
#     win.contextslist = win.otherstuff['...']
#     win.commandslist = win.otherstuff['...']

# uncomment this to define a routine to write back the keydefs to the source data
# ** corresponds to the RedefineKeys setting **
# def savekeys(parent):
#     pass
