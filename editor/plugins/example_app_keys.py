# -*- coding: UTF-8 -*-

# uncomment these where appropriate
# import collections
# import PyQt4.QtGui as gui
# import PyQt4.QtCore as core

# uncomment this to define a routine to (re)build the csv file from source data
# showinfo is a switch for in case you want to show instructions
# otherstuff can be used to pass on things like a list of unassigned commands
# ** corresponds to the RebuildCSV setting **
# def buildcsv(parent, showinfo=True):
#     shortcuts = collections.defaultdict
#     otherstuff = {}
#     ...implement some logic here...
#     return shortcuts, otherstuff

# uncomment these to define routines to be used by methods of a HotKeyPanel instance
# ** corresponds to the ShowDetails setting **
# win is a reference to the HotKeyPanel instance
# def add_extra_attributes(win):
#     """add attributes specific to this plugin
#     e.g a shorter name for a collection read from buildcsv's otherstuff
#     """
#     win.some_attribute = win.otherstuff['some_value']
# box is a reference to the frame containing the screen fields
# def add_extra_fields(win, box):
#     "add fields specific to this plugin"
#     win.fieldname = gui.QFieldType(box)
# def get_frameheight():
#     "return the height for the descriptions field"
#     return x
# box is a reference to the screen layout
# def layout_extra_fields(win, box):
#     "add the specific fields to the layout"
#     sizer = gui.QBoxLayout()
#     sizer.addWidget(win.fieldname)
#     box.addLayout(sizer)
# cb refers to the widget, text to the choice made
# def on_combobox(self, cb, text):
#     "handle a specific field in case it's a combobox"
#     ...implement suitable logic here...
# def captions_extra_fields(win):
#     "change the specific field captions according to the language setting"
#     win.fieldname.setText(win.captions['some_value'])
# newdata is a tuple of values from a line in the screen table
# def on_extra_selected(win, newdata):
#     "callback on selection of an item - update specific field"
#     win._origdata[win.fieldindex] = newdata[win.fieldindex]
# index refers to the sequence of the field in the screen table, item is the value contained
# def vul_extra_details(win, indx, item):
#     "fill value for extra field"
#     if win.column_info[indx][0] == 'some_value':
#         win.fieldname.setText(item)
#         win._origdata[win.fieldindex] = item

# uncomment this to define a routine to write back the keydefs to the source data
# ** corresponds to the RedefineKeys setting **
# def savekeys(parent):
#     pass
