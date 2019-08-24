"""Hotkeys plugin example

this module contains the general, non gui-toolkit specific part of the code
"""
# uncomment these where appropriate
# import collections
# from example_app_keys_gui import add_extra_fields, layout_extra_fields_*, captions_extra_fields

# uncomment this to define a routine to (re)build the csv file from source data
# showinfo is a switch for in case you want to show instructions
# otherstuff can be used to pass on things like a list of possible commands
# to method add_extra_attributes
# ** corresponds to the RebuildCSV setting **
# def buildcsv(parent, showinfo=True):
#     shortcuts = collections.defaultdict()
#     otherstuff = {}
#     ...implement some logic here...
#     return shortcuts, otherstuff

# uncomment these to define routines to be used by methods of a HotKeyPanel instance
# ** corresponds to the ShowDetails setting **
# win is a reference to the HotKeyPanel instance
# def add_extra_attributes(win):
#     """add attributes specific to this plugin
#     e.g a shorter name for a collection read from buildcsv's otherstuff
#     some of these are needed when filling fields in the details part of the screen
#     """
#     win.contextslist = win.otherstuff['...']
#     win.commandslist = win.otherstuff['...']

# def vul_extra_details(win, indx, item):
#     """fill value for extra field (plugin-specific)
#     indx refers to the sequence of the field in the screen table, item is the value contained
#     """
#     if win.column_info[indx][0] == 'some_value':
#         win.fieldname.setText(item)
#         win._origdata[win.fieldindex] = item

# def lees_extra_details(win):
#     ...

# uncomment this to define a routine to write back the keydefs to the source data
# ** corresponds to the RedefineKeys setting **
# def savekeys(parent):
#     pass
