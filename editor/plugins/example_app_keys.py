# -*- coding: UTF-8 -*-

# uncomment these where appropriate
# import collections
# import PyQt5.QtWidgets as qtw
# import PyQt5.QtGui as gui
# import PyQt5.QtCore as core

# uncomment this to define a routine to (re)build the csv file from source data
# showinfo is a switch for in case you want to show instructions
# otherstuff can be used to pass on things like a list of possible commands
# ** corresponds to the RebuildCSV setting **
# def buildcsv(parent, showinfo=True):
#     shortcuts = collections.defaultdict()
#     otherstuff = {}
#     ...implement some logic here...
#     return shortcuts, otherstuff

# uncomment these to define routines to be used by methods of a HotKeyPanel instance
# ** corresponds to the ShowDetails setting **
# win is a reference to the HotKeyPanel instance
# box is a reference to the frame containing the screen fields
# def add_extra_attributes(win):
#     """add attributes specific to this plugin
#     e.g a shorter name for a collection read from buildcsv's otherstuff
#     some of these are needed when filling fields in the details part of the screen
#     """
#     win.contextslist = win.otherstuff['...']
#     win.commandslist = win.otherstuff['...']
# def add_extra_fields(win, box):
#     """add fields specific to this plugin
#     """
#     win.fieldname = qtw.QFieldType(box)
# def get_frameheight():
#     "return the height for the descriptions field"
#     return x
# def layout_extra_fields_topline(win, box):
#     """add the specific fields to the layout
#     use this if you want to use the screen line the `keys` field is on
#     """
#     sizer = qtw.QHBoxLayout()
#     sizer.addWidget(win.fieldname)
#     box.addLayout(sizer)
# def layout_extra_fields_nextline(win, box):
#     """add the specific fields to the layout
#     use this if you want to make a new line above the description field
#     """
#     sizer = qtw.QHBoxLayout()
#     sizer.addWidget(win.fieldname)
#     box.addLayout(sizer)
# def layout_extra_fields(win, box):
#     """add the specific fields to the layout
#     use this if you want to put them next to the description field
#     adjust the desc field's height accordingly using `get_frameheight`
#     """
#     sizer = qtw.QVBoxLayout()
#     sizer.addWidget(win.fieldname)
#     box.addLayout(sizer)
# def on_combobox(self, cb, text):
#     """handle a specific field in case it's a combobox
#     cb refers to the widget, text to the choice made
#     """
#     ...implement suitable logic here...
# def captions_extra_fields(win):
#     "for plugin-specific fields, change the captions according to the language setting"
#     win.fieldname.setText(win.captions['some_value'])
# newdata is a tuple of values from a line in the screen table
# def on_extra_selected(win, newdata):
#     "callback on selection of an item - update specific field"
#     win._origdata[win.fieldindex] = newdata[win.fieldindex]
# def vul_extra_details(win, indx, item):
#     """fill value for extra field (plugin-specific)
#     index refers to the sequence of the field in the screen table, item is the value contained
#     """
#     if win.column_info[indx][0] == 'some_value':
#         win.fieldname.setText(item)
#         win._origdata[win.fieldindex] = item

# uncomment this to define a routine to write back the keydefs to the source data
# ** corresponds to the RedefineKeys setting **
# def savekeys(parent):
#     pass
