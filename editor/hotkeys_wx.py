# -*- coding: UTF-8 -*-
"""hotkeys.py wxPython version - currently unmaintained

    main gui (choicebook)
    importeert de verschillende applicatiemodules
    hierin wordt het menu gedefinieerd en de functies die daarbij horen
    het idee is dat de menuopties wanneer nodig uitgegrijsd zijn en dat
        in de routines wordt uitgevraagd wat te doen bij welke applicatie
    voor wat betreft de instellingen:
        taalkeuze: op dit niveau
        paden: op applicatie niveau
"""
import os
import sys
import wx
import wx.adv
import editor.hotkeys_constants as hkc
## sys.path.append('plugins')
## import editor.plugins.vikey_wxgui

#------------ start of code copied from vikey_wxgui.py -------------------------------
import wx.lib.mixins.listctrl  as  listmix
import editor.images as images
import editor.plugins.vikeys
INI = "vikey_config.py"
#------------ end of code copied from vikey_wxgui.py -------------------------------

def show_message(self, message_id, caption_id='T_MAIN'):
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    na sluiten van de dialoog
    """
    with wx.MessageDialog(self, self.captions[message_id], self.captions[caption_id],
                          wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT | wx.ICON_INFORMATION) as dlg:
        h = dlg.ShowModal()
    ## dlg.Destroy()
    return h

# TODO: aanpassen aan nieuwe architectuur
#------------ start of code copied from vikey_wxgui.py -------------------------------
class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """base class voor de listcontrol

    maakt het definiëren in de gui class wat eenvoudiger
    """
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
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
        self.ini = INI # 1 pad + language instelling
        #self.readkeys()
        self.data = {0: ('i', 'action', 'enter insert mode'),
                     1: ('Esc', 'action', 'cancel insert mode'),
                     2: ('d + d', 'action', 'delete current line'),
                     3: ('$', 'motion', 'to end of line')}
        self.readcaptions()
        wx.Panel.__init__(self, parent)  # , wx.ID_ANY,
            ## style=wx.BORDER_SIMPLE
            ## | wx.WANTS_CHARS
        ## )

        # self.il = wx.ImageList(16, 16)

        # self.idx1 = self.il.Add(images.getPtBitmap())
        # self.sm_up = self.il.Add(images.getSmallUpArrowBitmap())
        # self.sm_dn = self.il.Add(images.getSmallDnArrowBitmap())

        self.p0list = MyListCtrl(self, -1,
                                 ## size=(500,500),
                                 style=wx.LC_REPORT
                                 | wx.BORDER_SUNKEN
                                 #~ | wx.LC_VRULES
                                 | wx.LC_HRULES
                                 | wx.LC_SINGLE_SEL
                                 )
        ## self.p0list.SetMinSize((440,444))

        # self.p0list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.populate_list()

        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        self.itemdatamap = self.data
        listmix.ColumnSorterMixin.__init__(self, 3) # 5)
        #self.SortListItems(0, True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected, self.p0list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_item_deselected, self.p0list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated, self.p0list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.on_column_click, self.p0list)
        self.p0list.Bind(wx.EVT_LEFT_DCLICK, self.on_doubleclick)
        self.p0list.Bind(wx.EVT_KEY_DOWN, self.on_keypress)

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
        self.SetTitle(self.captions['T_MAIN'])

    def readcaptions(self):
        self.captions = {}
        # with open(os.path.join(HERE, self.ini.lang)) as f_in:
        with open(os.path.join(hkc.HERE, 'languages', 'english.lng')) as f_in:
            for x in f_in:
                if x[0] == '#' or x.strip() == "":
                    continue
                key, value = x.strip().split(None,1)
                self.captions[key] = value
        self.captions['T_MAIN'] = 'VI hotkeys'
        return self.captions

    def setcaptions(self):
        title = self.captions['T_MAIN']
        if self.modified:
            title += ' ' + self.captions["017"]
        self.SetTitle(title)
        self.page.populate_list()

    def on_keypress(self, evt):
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
            self.enable_buttons()

    def OnEvtComboBox(self,evt):
        """callback op het gebruik van een combobox

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        self.enable_buttons()

    def populate_list(self):
        """vullen van de list control
        """
        self.p0list.DeleteAllItems()
        self.p0list.DeleteAllColumns()
        self.itemdatamap = self.data

        # Adding columns with width and images on the column header
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT | wx.LIST_MASK_WIDTH
        info.m_format = 0
        ## info.m_width = 0
        ## info.m_text = ""
        ## self.p0list.InsertColumnInfo(0, info)

        for col, inf in enumerate((('C_KEY',120),
                                   ## ('C_MOD',70),
                                   ('C_TYPE',120),
                                   ## ('C_CMD',160),
                                   ('C_DESC',292))):
            title, width = inf
            self.p0list.InsertColumn(col,  self.captions[title])
            self.p0list.SetColumnWidth(col, width)

        ## self.parent.rereadlist = False

        items = self.data.items()
        if items is None or len(items) == 0:
            return

        kleur = False
        for key, data in items:
            ## print data
            index = self.p0list.InsertItem(sys.maxsize, data[0])
            self.p0list.SetItem(index, 1, data[1])
            self.p0list.SetItem(index, 2, data[2])
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

    def on_item_selected(self, event):
        """callback op het selecteren van een item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
        seli = self.p0list.GetItemData(event.m_itemIndex)
        ## print "Itemselected",seli,self.data[seli]
        self.vuldetails(seli)
        event.Skip()

    def on_item_deselected(self, event):
        """callback op het niet meer geselecteerd zijn van een item

        er wordt gevraagd of de key definitie moet worden bijgewerkt"""
        seli = self.p0list.GetItemData(event.m_itemIndex)
        ## print "ItemDeselected",seli,self.data[seli]
        if self.defchanged:
            self.defchanged = False
            with wx.MessageDialog(self, self.parent.captions["020"], self.parent.captions['T_MAIN'],
                                  wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION) as dlg:
                h = dlg.ShowModal()
            ## dlg.Destroy()
            if h == wx.ID_YES:
                ## print "OK gekozen"
                self.aanpassen()

    def on_item_activated(self, event):
        """callback op het activeren van een item (onderdeel van het selecteren)
        """
        self.current_item = event.m_itemIndex

    def on_column_click(self, event):
        """callback op het klikken op een kolomtitel
        """
        ## print "on_column_click: %d\n" % event.GetColumn()
        ## self.parent.sorter = self.GetColumnSorter()
        event.Skip()

    def on_doubleclick(self, event):
        """callback op dubbelklikken op een kolomtitel
        """
        pass
        # self.log.WriteText("on_doubleclick item %s\n" % self.p0list.GetItemText(self.current_item))
        event.Skip()


    def enable_buttons(self, state=True):
        """anders wordt de gelijknamige methode van de Panel base class geactiveerd"""
        pass

    def keyprint(self,evt):
        pass
#------------ end of code copied from vikey_wxgui.py -------------------------------
#----------------------------------------------------------------------------

pagetexts = [ "VI", "Total Commander", "Double Commander", "And", "Many", "More"]

class MainWindow(wx.Frame):
    """Hoofdscherm van de applicatie"""
    def __init__(self,parent,id,args):
        wid = 860 if hkc.LIN else 688
        hig = 594
        wx.Frame.__init__(self,parent,wx.ID_ANY, "tcmdrkeys",size = (wid, hig),
                            style=wx.DEFAULT_FRAME_STYLE
                                | wx.NO_FULL_REPAINT_ON_RESIZE
                                ## | wx.BORDER_SIMPLE
                                )
        self.sb = self.CreateStatusBar() # A Statusbar in the bottom of the window
        self.readcaptions('english.lng')
        ## print('in mainwindow', self.captions)
        # TODO: aanpassen aan nieuwe architectuur
        self.menuBar = wx.MenuBar()
        for title, items in (('M_APP', (
                                ('M_SETT', (
                                    ('M_LOC', self.m_loc),
                                    ('M_LANG', self.m_lang))),
                                ('M_EXIT', self.m_exit))),
                             ('M_TOOL', (
                                ('M_READ', self.m_read),
                                ('M_SAVE', self.m_save))),
                             ('M_HELP', (
                                ('M_ABOUT', self.m_about),))):
            menu = wx.Menu()
            for sel in items:
                if sel == -1:
                    menu.AppendSeparator()
                else:
                    sel, value = sel
                    if callable(value):
                        item = wx.MenuItem(None, -1, self.captions[sel])
                        menu.Append(item)
                        self.Bind(wx.EVT_MENU, value, id=item.GetId())
                    else:
                        submenu = wx.Menu()
                        for selitem, callback in value:
                            item = wx.MenuItem(None, -1, self.captions[selitem])
                            submenu.Append(item)
                            self.Bind(wx.EVT_MENU, callback, id=item.GetId())
                        menu.AppendSubMenu(submenu, self.captions[sel])
            self.menuBar.Append(menu, self.captions[title])
        self.SetMenuBar(self.menuBar)

        # self.pnl = wx.Panel(self, -1) #, style=wx.BORDER_SIMPLE)
        self.book = wx.Choicebook(self, -1) # , size= (600, 700))
        for txt in pagetexts:
            if txt == "VI":  # and False: # tijdelijk om dit niet te laten gebeuren
                win = VIPanel(self.book, -1)
                ## win.doelayout()
#------------ start of code copied from vikey_wxgui.py -------------------------------
                self.captions = win.captions
                win.doelayout()
                if len(win.data) == 0:
                    with wx.MessageDialog(self, self.captions['042'], self.captions['T_MAIN'],
                                          wx.OK | wx.ICON_INFORMATION) as dlg:
                        dlg.ShowModal()
                    # dlg.Destroy()
#------------ end of code copied from vikey_wxgui.py -------------------------------
            else:
                win = wx.Panel(self.book, -1 ) #, style=wx.BORDER_SIMPLE)
                st = wx.StaticText(win, -1, txt, (10,10))
            self.book.AddPage(win, txt)
        self.book.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.book.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGING, self.OnPageChanging)

        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.book, 1, wx.EXPAND | wx.ALL, 0)
        sizer0.Add(sizer1, 1, wx.EXPAND | wx.ALL, 0)
        btn = wx.Button(self, label=self.captions['C_EXIT'])
        btn.Bind(wx.EVT_BUTTON, self.exit)
        sizer0.Add(btn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(sizer0)
        self.SetAutoLayout(True)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)
        # self.pnl.Layout()
        self.Show(True)

    def m_read(self, event):
        """(menu) callback voor het lezen van de hotkeys

        vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
        zet de gelezen keys daarna ook in de gui
        """
        wx.MessageBox('Lezen gekozen', self.captions['T_MAIN'])
        return
        if not self.modified:
            h = show_message(self, '041')
            if h == wx.ID_YES:
                self.readkeys()
                self.page.populate_list()

    def m_save(self, event):
        """(menu) callback voor het terugschrijven van de hotkeys

        vraagt eerst of het ok is om de hotkeys weg te schrijven
        vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
        """
        wx.MessageBox('Opslaan gekozen', self.captions['T_MAIN']) #hkc.NOT_IMPLEMENTED)
        return
        if not self.modified:
            h = show_message(self, '041')
            if h != wx.ID_YES:
                return
        self.savekeys()
        if self.ini.restart:
            h = show_message(self, '026')
            if h == wx.ID_YES:
                os.system(self.ini.restart)
        else:
            wx.MessageBox(self.captions['037'], self.captions['T_MAIN'])
            ## h = show_message(self, '037')

    def m_user(self, event):
        """(menu) callback voor een nog niet geïmplementeerde actie"""
        return self.captions[hkc.NOT_IMPLEMENTED]

    def m_loc(self, event):
        """(menu) callback voor aanpassen van de bestandslocaties

        vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
        toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
        (met name of de opgegeven paden kloppen)
        """
        wx.MessageBox('paden gekozen', self.captions['T_MAIN']) #hkc.NOT_IMPLEMENTED)
        return
        if self.modified:
            h = show_message(self, '025')
            if h == wx.ID_YES:
                self.savekeys()
            elif h == wx.ID_CANCEL:
                return
        paths = [self.ini.pad,]
        captions = [self.captions[x] for x in ('028','044','039')]
        ## captions = ['Define file locations for:', 'TC','UC','CI','KT','HK']
        dlg = FilesDialog(self, -1, self.captions['T_MAIN'], paths, captions,
            size=(400, 200),
            #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
            style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
            )
        ## dlg.CenterOnScreen()
        fout = "*"
        text = ''
        while fout:
            val = dlg.ShowModal()
            pad = dlg.bVI.GetValue()
            fout = ""
            if val == wx.ID_OK:
                text = "modified"
                if pad != "":
                    naam = self.captions['044']
                    if not os.path.isdir(pad):
                        fout = self.captions['034'] % naam
                    elif not os.path.exists(os.path.join(pad,naam)):
                        fout = self.captions['035'] % naam
            if fout:
                mdlg = wx.MessageDialog(self,fout,self.captions['T_MAIN'])
                mdlg.ShowModal()
                mdlg.Destroy()
        dlg.Destroy()
        if text:
            ## for i,pad in enumerate(paden):
                ## if pad != "":
                    ## self.ini.paden[i] = pad
            self.ini.pad = pad
            self.ini.write()
            text = ''

    def m_lang(self, event):
        """(menu) callback voor taalkeuze

        past de settings aan en leest het geselecteerde language file
        """
        choices = [x for x in os.listdir(os.path.join(hkc.HERE, 'languages'))
                   if os.path.splitext(x)[1] == ".lng"]
        with wx.SingleChoiceDialog(self, self.captions['P_SELLNG'], self.captions['T_MAIN'], choices,
                                   wx.CHOICEDLG_STYLE) as dlg:
            for i, x in enumerate(choices):
                print(x, self.ini.lang)
                if x == self.ini.lang:
                    dlg.SetSelection(i)
                    break
            h = dlg.ShowModal()
            if h == wx.ID_OK:
                lang = dlg.GetStringSelection()
                self.ini.lang = lang
                self.ini.write()
                self.readcaptions()
                self.setcaptions()
        ## dlg.Destroy()

    def m_about(self, event):
        """(menu) callback voor het tonen van de "about" dialoog
        """
        info = wx.adv.AboutDialogInfo()
        info.Name = self.captions['T_MAIN']
        info.Version = hkc.VRS
        info.Copyright = hkc.AUTH
        ## info.Description = hkc.TTL, 350, wx.ClientDC(self)
        ## info.WebSite = ("http://en.wikipedia.org/wiki/Hello_world", "Hello World home page")
        ## info.Developers = [ "Joe Programmer",
                            ## "Jane Coder",
                            ## "Vippy the Mascot" ]
        ## info.License = wordwrap(licenseText, 500, wx.ClientDC(self))
        wx.adv.AboutBox(info, self)

    def m_exit(self, event):
        """(menu) callback om het programma direct af te sluiten"""
        self.exit()

    def exit(self, event=None):
        self.Close(True)

    def readcaptions(self, lang):
        self.captions = {}
        with open(os.path.join(hkc.HERE, 'languages', lang)) as f_in:
            for x in f_in:
                if x[0] == '#' or x.strip() == "":
                    continue
                key, value = x.strip().split(None,1)
                self.captions[key] = value
        return self.captions

    ## def on_menu(self, event):
        ## id = str(event.GetId())
        ## text = MENU_FUNC[id](self)
        ## if text:
            ## dlg = wx.MessageDialog(self,text,self.captions['T_MAIN'], wx.OK)
            ## h = dlg.ShowModal()
            ## dlg.Destroy()

    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        ## sel = self.GetSelection()
        ## self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        ## sel = self.GetSelection()
        ## self.log.write('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()


def main(args=None):
    app = wx.App()  # redirect=True, filename="hotkeys.log")
    print('----------')
    frame = MainWindow(None, -1, args)
    app.MainLoop()
