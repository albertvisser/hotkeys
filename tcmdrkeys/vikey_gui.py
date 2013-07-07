# -*- coding: UTF-8 -*-

import sys, os
import wx
import wx.html as html
import wx.lib.mixins.listctrl  as  listmix
import wx.lib.filebrowsebutton as filebrowse
import wx.gizmos   as  gizmos
import images
import vikeys
## import datetime

HERE = os.path.abspath(os.path.dirname(__file__))
TTL = "A hotkey editor"
VRS = "1.1.x"
AUTH = "(C) 2008 Albert Visser"
INI = "vikey_config.py"
WIN = True if sys.platform == "win32" else False
LIN = True if sys.platform == 'linux2' else False
C_KEY, C_MOD, C_SRT, C_CMD, C_OMS = '001', '043', '002', '003', '004'

class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """base class voor de listcontrol

    maakt het definiëren in de gui class wat eenvoudiger
    """
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class VIPanel(wx.Panel, listmix.ColumnSorterMixin):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    voornamelijk nodig om de specifieke verwerkingen met betrekking tot de lijst
    bij elkaar en apart van de rest te houden
    definieert feitelijk een "custom widget"
    """
    def __init__(self, parent, id):
        self.parent = parent
        self.ini = vikeys.VIKSettings(INI) # 1 pad + language instelling
        self.readkeys()
        self.readcaptions()
        wx.Panel.__init__(self, parent, wx.ID_ANY,
            ## style=wx.BORDER_SIMPLE
            ## | wx.WANTS_CHARS
        )

        self.il = wx.ImageList(16, 16)

        self.idx1 = self.il.Add(images.getPtBitmap())
        self.sm_up = self.il.Add(images.getSmallUpArrowBitmap())
        self.sm_dn = self.il.Add(images.getSmallDnArrowBitmap())

        self.p0list = MyListCtrl(self, -1,
                                 ## size=(500,500),
                                 style=wx.LC_REPORT
                                 | wx.BORDER_SUNKEN
                                 #~ | wx.LC_VRULES
                                 | wx.LC_HRULES
                                 | wx.LC_SINGLE_SEL
                                 )
        ## self.p0list.SetMinSize((440,444))

        self.p0list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.PopulateList()

        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        self.itemDataMap = self.data
        listmix.ColumnSorterMixin.__init__(self, 3) # 5)
        #self.SortListItems(0, True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.p0list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.p0list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.p0list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.p0list)
        self.p0list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.p0list.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

    def doelayout(self):
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(self.p0list, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)
        ## self.Layout()

    def readkeys(self):
        self.data = vikeys.readkeys(self.ini.pad)

    def savekeys(self):
        vikeys.savekeys(self.ini.pad, self.data)
        self.modified = False
        self.SetTitle(self.captions["000"])

    def readcaptions(self):
        self.captions = {}
        with open(os.path.join(HERE, self.ini.lang)) as f_in:
            for x in f_in:
                if x[0] == '#' or x.strip() == "":
                    continue
                key, value = x.strip().split(None,1)
                self.captions[key] = value
        self.captions['000'] = 'VI hotkeys'
        return self.captions

    def setcaptions(self):
        title = self.captions["000"]
        if self.modified:
            title += ' ' + self.captions["017"]
        self.SetTitle(title)
        self.page.PopulateList()

    def OnKeyPress(self, evt):
        """callback bij gebruik van een toets(encombinatie)
        """
        keycode = evt.GetKeyCode()
        togo = keycode - 48
        if evt.GetModifiers() == wx.MOD_ALT: # evt.AltDown()
            if keycode == wx.WXK_LEFT or keycode == wx.WXK_NUMPAD_LEFT: #  keycode == 314
                pass
            elif keycode == wx.WXK_RIGHT or keycode == wx.WXK_NUMPAD_RIGHT: #  keycode == 316
                pass
            ## elif togo >= 0 and togo <= self.parent.pages: # Alt-0 t/m Alt-6
                ## pass
            elif keycode == 83: # Alt-S
                pass
            elif keycode == 70: # Alt-F
                pass
            elif keycode == 71: # Alt-G
                pass
        elif evt.GetModifiers() == wx.MOD_CONTROL: # evt.ControlDown()
            if keycode == 81: # Ctrl-Q
                pass
            elif keycode == 80: # Ctrl-P
                self.keyprint(evt)
            elif keycode == 79: # Ctrl-O
                pass
            elif keycode == 78: # Ctrl-N
                pass
            elif keycode == 70: # Ctrl-H
                pass
            elif keycode == 90: # Ctrl-Z
                pass
        elif keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:# 13 or 372: # Enter
            pass
        #~ else:
            #~ evt.Skip()
        evt.Skip()

    def OnEvtText(self,evt):
        """callback op het wijzigen van de tekst

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        #~ print "self.init is", self.init
        if not self.init:
            #~ print "ok, enabling buttons"
            self.enableButtons()

    def OnEvtComboBox(self,evt):
        """callback op het gebruik van een combobox

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        self.enableButtons()

    def PopulateList(self):
        """vullen van de list control
        """
        self.p0list.DeleteAllItems()
        self.p0list.DeleteAllColumns()
        self.itemDataMap = self.data

        # Adding columns with width and images on the column header
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT | wx.LIST_MASK_WIDTH
        info.m_format = 0
        ## info.m_width = 0
        ## info.m_text = ""
        ## self.p0list.InsertColumnInfo(0, info)

        for col,inf in enumerate((
                (C_KEY,120),
                ## (C_MOD,70),
                (C_SRT,120),
                ## (C_CMD,160),
                (C_OMS,292)
            )):
            inf,wid = inf
            info.m_width = wid
            info.m_text = self.captions[inf]
            self.p0list.InsertColumnInfo(col, info)

        ## self.parent.rereadlist = False

        items = self.data.items()
        if items is None or len(items) == 0:
            return

        kleur = False
        for key, data in items:
            ## print data
            index = self.p0list.InsertStringItem(sys.maxint, data[0])
            self.p0list.SetStringItem(index, 1, data[1])
            self.p0list.SetStringItem(index, 2, data[2])
            ## soort = C_DFLT if data[2] == "S" else C_RDEF
            ## self.p0list.SetStringItem(index, 2, self.captions[soort])
            ## self.p0list.SetStringItem(index, 3, data[3])
            ## self.p0list.SetStringItem(index, 4, data[4])
            self.p0list.SetItemData(index, key)
            ## if kleur:
                ## #~ self.p0list.SetItemBackgroundColour(key,wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))
            ## #~ else:
                ## self.p0list.SetItemBackgroundColour(key,wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
            ## kleur = not kleur
        self.defchanged = False

    def GetListCtrl(self):
        """ten behoeve van de columnsorter mixin"""
        return self.p0list

    def GetSortImages(self):
        """ten behoeve van de columnsorter mixin"""
        return (self.sm_dn, self.sm_up)

    def AfterSort(self):
        """ na het sorteren moeten de regels weer om en om gekleurd worden"""
        kleur = False
        for key in range(len(self.data.items)):
            if kleur:
                #~ self.p0list.SetItemBackgroundColour(key,wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))
            #~ else:
                self.p0list.SetItemBackgroundColour(key,wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
            kleur = not kleur

    def OnItemSelected(self, event):
        """callback op het selecteren van een item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
        seli = self.p0list.GetItemData(event.m_itemIndex)
        ## print "Itemselected",seli,self.data[seli]
        self.vuldetails(seli)
        event.Skip()

    def OnItemDeselected(self, event):
        """callback op het niet meer geselecteerd zijn van een item

        er wordt gevraagd of de key definitie moet worden bijgewerkt"""
        seli = self.p0list.GetItemData(event.m_itemIndex)
        ## print "ItemDeselected",seli,self.data[seli]
        if self.defchanged:
            self.defchanged = False
            dlg = wx.MessageDialog(self,
                self.parent.captions["020"],
                self.parent.captions["000"],
                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION
                )
            h = dlg.ShowModal()
            dlg.Destroy()
            if h == wx.ID_YES:
                ## print "OK gekozen"
                self.aanpassen()

    def OnItemActivated(self, event):
        """callback op het activeren van een item (onderdeel van het selecteren)
        """
        self.currentItem = event.m_itemIndex

    def OnColClick(self, event):
        """callback op het klikken op een kolomtitel
        """
        ## print "OnColClick: %d\n" % event.GetColumn()
        ## self.parent.sorter = self.GetColumnSorter()
        event.Skip()

    def OnDoubleClick(self, event):
        """callback op dubbelklikken op een kolomtitel
        """
        pass
        # self.log.WriteText("OnDoubleClick item %s\n" % self.p0list.GetItemText(self.currentItem))
        event.Skip()


    def enableButtons(self, state=True):
        """anders wordt de gelijknamige methode van de Panel base class geactiveerd"""
        pass

    def keyprint(self,evt):
        pass


class MainWindow(wx.Frame):
    """Hoofdscherm van de applicatie"""
    def __init__(self, parent, id): # , args):

        wid = 800 if LIN else 688
        hig = 594
        wx.Frame.__init__(self,parent, wx.ID_ANY, "VI keys", size=(wid, hig),
                            style=wx.DEFAULT_FRAME_STYLE
                                | wx.NO_FULL_REPAINT_ON_RESIZE
                                ## | wx.BORDER_SIMPLE
                                )
        ## self.sb = self.CreateStatusBar() # A Statusbar in the bottom of the window
        self.pnl = wx.Panel(self, -1)
        self.page = VIPanel(self.pnl, -1)
        self.captions = self.page.captions

    # --- schermen opbouwen: controls plaatsen -----------------------------------------------------------------------------------------
        self.SetTitle(self.captions["000"])
        #~ self.SetIcon(wx.Icon("task.ico",wx.BITMAP_TYPE_ICO))
        ## self.SetIcon(images.gettaskIcon())
        #~ self.SetMinSize((476, 560))

    # --- schermen opbouwen: layout -----------------------------------------------------------------------------------------
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        self.page.doelayout()
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.page, 1, wx.EXPAND) # , 0)
        sizer0.Add(sizer1, 1, wx.EXPAND | wx.ALL,4)

        self.pnl.SetSizer(sizer0)
        self.pnl.SetAutoLayout(True)
        sizer0.Fit(self.pnl)
        sizer0.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.Show(True)
        if len(self.page.data) == 0:
            dlg = wx.MessageDialog(self, self.captions['042'],
                self.captions["000"],
                wx.OK | wx.ICON_INFORMATION
                )
            h = dlg.ShowModal()
            dlg.Destroy()

def main():
    app = wx.App(redirect=True,filename="vikey_gui.log")
    print '----------'
    frame = MainWindow(None, -1)
    app.MainLoop()

if __name__ == '__main__':
    ## h = Tcksettings()
    ## h.set('paden',['ergens',])
    ## print h.__dict__
    main()
