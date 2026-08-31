"""Hotkeys plugin example
"""
from ..toolkit import toolkit
# uncomment these where appropriate
# import collections

# uncomment these to implement routines for converting "otherstuff" elements that can't be stored
# in json format
# def update_otherstuff_outbound():
#     """modify dict keys from list to space-separated string to accomodate json format
#     """
#     newstuff = {}
#     for key, value in otherstuff["..."].items():
#         newkey = ' '.join(list(key))
#         if isinstance(value, set):
#             value = list(value)
#         newstuff[newkey] = value
#     otherstuff["..."] = newstuff
#     return otherstuff
# def update_otherstuff_inbound():
#     """convert dict keys from space-separated string to key-modifier-context format
#     """
#     newstuff = {}
#     for key, value in otherstuff["..."].items():
#         newkey = key.split(' ')  # split explicitely on one space
#         newstuff[newkey] = value
#     otherstuff["..."] = newstuff
#     return otherstuff

# uncomment this to define a routine to (re)build the csv file from source data
# ** corresponds to the Rebuild_data setting **
# - showinfo is a switch for in case you want to show instructions
# - otherstuff can be used to pass on things like a list of possible commands
#   to method add_extra_attributes
# def build_data(parent, showinfo=True):
#     shortcuts = collections.defaultdict()
#     otherstuff = {}
#     ...implement some logic here...
#     return shortcuts, otherstuff

# uncomment these to define a routine to extract nonstandard attributes
# ** corresponds to the ShowDetails setting **
# - win is a reference to the HotKeyPanel instance
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

# uncomment this if you need a non-standard height for the desription field and the extra fields
# next to it
# def get_frameheight():
#     "return the height for the descriptions field if different from the default"
#     return x

# uncomment and implement this to preserve descriptions not found in the tool data
# -incoming newdescs need to be stored in win.descriptions and win.otherstuff
# -they also need to be extracted into the description part of the win.data items (for display)
# def update_descriptions(win, newdescs):
#     """merge edited descriptions back into the data to save
#     """
#     win.descriptions = newdescs
#     win.otherstuff['...'] = win.descriptions
#     for key, data in win.data.items():
#         if data[..] in win.descriptions and data[-1] != win.descriptions[data['']]:
#             win.data[key] = tuple(list(data[:-1]) + [win.descriptions[data[..]]])
