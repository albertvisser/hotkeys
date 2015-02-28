# -*- coding: UTF-8 -*-

import sys, os
import wx
import wx.html as html
import wx.lib.mixins.listctrl  as  listmix
import wx.lib.filebrowsebutton as filebrowse
import wx.gizmos   as  gizmos
import images
import tcmdrkys
import string
## import datetime

from hotkeys_shared import * # constants
C_MENU = TC_MENU
INI = "tckey_config.py"

# voorziening voor starten op usb-stick onder Windows (drive letters in config aanpassen)
if WIN and __file__ != "tckey_gui.py":
    drive = os.path.splitdrive(os.getcwd())[0] + "\\"
    with open(INI) as f_in:
        lines = f_in.readlines()
    for line in lines:
        if line.startswith('TC_PAD='):
            olddrive = line[7:10]
            break
    if olddrive.upper() != drive.upper():
        bak = INI + ".bak"
        if os.path.exists(bak):
            os.remove(bak)
        os.rename(INI,bak)
        with open(INI,"w") as f_out:
            for line in lines:
                if olddrive.lower() in line:
                    f_out.write(line.replace(olddrive.lower(),drive.upper()))
                elif olddrive.upper() in line:
                    f_out.write(line.replace(olddrive.upper(),drive.upper()))
                else:
                    f_out.write(line)


def show_message(self, message_id, caption_id='000'):
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    na sluiten van de dialoog
    """
    dlg = wx.MessageDialog(self, self.captions[message_id],
        self.captions[caption_id],
        wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT | wx.ICON_INFORMATION
        )
    h = dlg.ShowModal()
    dlg.Destroy()
    return h

def m_read(self):
    """(menu) callback voor het lezen van de hotkeys

    vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
    zet de gelezen keys daarna ook in de gui
    """
    if not self.modified:
        h = show_message(self, '041')
        if h == wx.ID_YES:
            self.readkeys()
            self.page.PopulateList()

def m_save(self):
    """(menu) callback voor het terugschrijven van de hotkeys

    vraagt eerst of het ok is om de hotkeys weg te schrijven
    vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
    """
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
        wx.MessageBox(self.captions['037'], self.captions['000'])
        ## h = show_message(self, '037')

def m_user(self):
    """(menu) callback voor een nog niet geïmplementeerde actie"""
    return self.captions[NOT_IMPLEMENTED]

def m_exit(self):
    """(menu) callback om het programma direct af te sluiten"""
    self.Exit()

def m_loc(self):
    """(menu) callback voor aanpassen van de bestandslocaties

    vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
    toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
    (met name of de opgegeven paden kloppen)
    """
    if self.modified:
        h = show_message(self, '025')
        if h == wx.ID_YES:
            self.savekeys()
        elif h == wx.ID_CANCEL:
            return
    paths = self.ini.paden
    if self.ini.restart:
        paths.append(self.ini.restart)
    else:
        paths.append('')
    captions = [self.captions[x] for x in (
        '028','029','030','031','032','033','039','038','040'
        )]
    ## captions = ['Define file locations for:', 'TC','UC','CI','KT','HK']
    dlg = FilesDialog(self, -1, self.captions["000"], paths, captions,
        size=(350, 200),
        #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
        style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
        )
    ## dlg.CenterOnScreen()
    fout = "*"
    text = ''
    while fout:
        val = dlg.ShowModal()
        paden = [
            dlg.bTC.GetValue(),dlg.bUC.GetValue(),dlg.bCI.GetValue(),
            dlg.bKT.GetValue(),dlg.bHK.GetValue()
            ]
        restarter = dlg.bRST.GetValue()
        fout = ""
        if val == wx.ID_OK:
            text = "modified"
            for i,pad in enumerate(paden):
                if pad != "":
                    naam = captions[i]
                    if not os.path.isdir(pad):
                        fout = self.captions['034'] % naam
                    else:
                        if naam == 'Hotkeys.hky':
                            naam = 'tc default hotkeys.hky'
                        if not os.path.exists(os.path.join(pad,naam)):
                            fout = self.captions['035'] % naam
                if fout:
                    break
            if restarter and not os.path.exists(restarter):
                fout = self.captions['036'] % naam
            else:
                paden.append(restarter)
        if fout:
            mdlg = wx.MessageDialog(self,fout,self.captions["000"])
            mdlg.ShowModal()
            mdlg.Destroy()
    dlg.Destroy()
    if text:
        ## for i,pad in enumerate(paden):
            ## if pad != "":
                ## self.ini.paden[i] = pad
        self.ini.set("paden",paden)
        text = ''

def m_lang(self):
    """(menu) callback voor taalkeuze

    past de settings aan en leest het geselecteerde language file
    """
    y = [x for x in os.listdir(HERE) if os.path.splitext(x)[1] == ".lng"]
    dlg = wx.SingleChoiceDialog(
        self,self.captions["027"],self.captions["000"],
        y,
        wx.CHOICEDLG_STYLE
        )
    for i, x in enumerate(y):
        print x, self.ini.lang
        if x == self.ini.lang:
            dlg.SetSelection(i)
            break
    h = dlg.ShowModal()
    if h == wx.ID_OK:
        lang = dlg.GetStringSelection()
        self.ini.set('lang', lang)
        self.readcaptions()
        self.setcaptions()
    dlg.Destroy()

def m_about(self):
    """(menu) callback voor het tonen van de "about" dialoog
    """
    info = wx.AboutDialogInfo()
    info.Name = self.captions['000']
    info.Version = VRS
    info.Copyright = AUTH
    ## info.Description = TTL, 350, wx.ClientDC(self)
    ## info.WebSite = ("http://en.wikipedia.org/wiki/Hello_world", "Hello World home page")
    ## info.Developers = [ "Joe Programmer",
                        ## "Jane Coder",
                        ## "Vippy the Mascot" ]
    ## info.License = wordwrap(licenseText, 500, wx.ClientDC(self))
    wx.AboutBox(info)

# dispatch table for  menu callbacks
MENU_FUNC = {
    M_READ: m_read,
    M_SAVE: m_save,
    M_USER: m_user,
    M_EXIT: m_exit,
    M_LOC: m_loc,
    M_LANG: m_lang,
    M_ABOUT: m_about,
}

class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """base class voor de listcontrol

    maakt het definiëren in de gui class wat eenvoudiger
    """
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class Page(wx.Panel, listmix.ColumnSorterMixin):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    voornamelijk nodig om de specifieke verwerkingen met betrekking tot de lijst
    bij elkaar en apart van de rest te houden
    definieert feitelijk een "custom widget"
    """
    def __init__(self,parent,id,top):
        self.parent = parent
        self.top = top
        wx.Panel.__init__(self,parent,wx.ID_ANY,
        ## style=wx.BORDER_SIMPLE #wx.WANTS_CHARS
        )
        tID = wx.NewId()

        self.il = wx.ImageList(16, 16)

        self.idx1 = self.il.Add(images.getPtBitmap())
        self.sm_up = self.il.Add(images.getSmallUpArrowBitmap())
        self.sm_dn = self.il.Add(images.getSmallDnArrowBitmap())

        self.p0list = MyListCtrl(self, tID,
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
        self.itemDataMap = self.top.data
        listmix.ColumnSorterMixin.__init__(self, 5)
        #self.SortListItems(0, True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.p0list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.p0list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.p0list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.p0list)
        self.p0list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.p0list.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

    def doelayout(self):
        """zet de list control op het scherm"""
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(self.p0list,1,wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)

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
        ## print "populating list..."
        self.p0list.DeleteAllItems()
        self.p0list.DeleteAllColumns()
        self.itemDataMap = self.top.data

        # Adding columns with width and images on the column header
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT | wx.LIST_MASK_WIDTH
        info.m_format = 0
        ## info.m_width = 0
        ## info.m_text = ""
        ## self.p0list.InsertColumnInfo(0, info)

        for col, inf in enumerate((
                (C_KEY, 70),
                (C_MOD, 70),
                (C_SRT, 80),
                (C_CMD, 160),
                (C_OMS, 452)  # was 292
            )):
            inf, wid = inf
            info.m_width = wid
            info.m_text = self.parent.parent.captions[inf]
            self.p0list.InsertColumnInfo(col, info)

        self.parent.rereadlist = False

        items = self.top.data.items()
        if items is None or len(items) == 0:
            return

        kleur = False
        for key, data in items:
            ## print data
            index = self.p0list.InsertStringItem(sys.maxint, data[0])
            self.p0list.SetStringItem(index, 1, data[1])
            soort = C_DFLT if data[2] == "S" else C_RDEF
            self.p0list.SetStringItem(index, 2, self.parent.parent.captions[soort])
            self.p0list.SetStringItem(index, 3, data[3])
            self.p0list.SetStringItem(index, 4, data[4])
            self.p0list.SetItemData(index, key)
            ## if kleur:
                ## #~ self.p0list.SetItemBackgroundColour(key,wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))
            ## #~ else:
                ## self.p0list.SetItemBackgroundColour(key,wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
            ## kleur = not kleur
        self.top.defchanged = False

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
        ## print "Itemselected",seli,self.top.data[seli]
        self.top.vuldetails(seli)
        event.Skip()

    def OnItemDeselected(self, event):
        """callback op het niet meer geselecteerd zijn van een item

        er wordt gevraagd of de key definitie moet worden bijgewerkt"""
        seli = self.p0list.GetItemData(event.m_itemIndex)
        ## print "ItemDeselected",seli,self.top.data[seli]
        if self.top.defchanged:
            self.top.defchanged = False
            dlg = wx.MessageDialog(self,
                self.top.captions["020"],
                self.top.captions["000"],
                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION
                )
            h = dlg.ShowModal()
            dlg.Destroy()
            if h == wx.ID_YES:
                ## print "OK gekozen"
                self.top.aanpassen()

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


class FilesDialog(wx.Dialog):
    """dialoog met meerdere FileBrowseButtons

    voor het instellen van de bestandslocaties
    """
    def __init__(self, parent, ID, title, locations, captions,
            size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE
            ):
        self.parent = parent
        self.locations = locations
        ## print locations
        wx.Dialog.__init__(self,parent,ID,title,pos,size,style)
        sizer = wx.BoxSizer(wx.VERTICAL)

        text = captions.pop(0)
        label = wx.StaticText(self, -1, text)
        sizer.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        buttons = []
        ## callbacks = (self.bTCCallback,self.bUCCallback,
            ## self.bCICallback,self.bKTCallback,self.bHKCallback)
        rstrcap2 = captions.pop()
        rstrcap = captions.pop()
        dircap = captions.pop()

        rstrloc = locations.pop()
        for i,x in enumerate(captions):
            if i < len(locations):
                dir = locations[i]
                strt = dir
            else:
                dir = locations[0]
                strt = ""
            ## dir = os.path.split(dir)[0]
            ## print i,dir
            box = wx.BoxSizer(wx.HORIZONTAL)
            fbb = filebrowse.DirBrowseButton(
                self, -1, size=(300, -1), labelText = x,
                startDirectory = dir,
                dialogTitle = dircap % x,
                ## changeCallback = callbacks[i],
                newDirectory = False
                )
            fbb.SetValue(strt)
            box.Add(fbb, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
            sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1)
            buttons.append(fbb)
        self.bTC,self.bUC,self.bCI,self.bKT,self.bHK = buttons

        if rstrloc:
            dir,naam = os.path.split(rstrloc)
        else:
            dir,naam = locations[0],''
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.bRST = filebrowse.FileBrowseButton(
            self, -1, size=(300, -1), labelText = rstrcap,
            startDirectory = dir,
            dialogTitle = rstrcap2,
            ## changeCallback = callbacks[i],
            )
        self.bRST.SetValue(naam)
        box.Add(self.bRST, 0, wx.ALIGN_CENTRE|wx.ALL, 1)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        self.SetSizer(sizer)
        sizer.Fit(self)

    ## def bTCCallback(self, evt):
        ## print "It's the FileBrowseButton for wincmd.ini"
        ## # het zou mooi wezen als deze waarde bij wijzigen default gemaakt wordt voor de andere
        ## # maar ik denk niet dat dat kan zonder ze weg te gooien en opnieuw te maken

    ## def bUCCallback(self, evt):
        ## print "It's the FileBrowseButton for usercmd.ini", evt.GetString()

    ## def bCICallback(self, evt):
        ## print "It's the FileBrowseButton for totalcmd.inc", evt.GetString()

    ## def bKTCallback(self, evt):
        ## print "It's the FileBrowseButton for keyboard.txt", evt.GetString()

    ## def bHKCallback(self, evt):
        ## print "It's the FileBrowseButton for hotkeys.hky", evt.GetString()

class EasyPrinter(html.HtmlEasyPrinting):
    """class voor het besturen van het printen
    """
    def __init__(self):
        html.HtmlEasyPrinting.__init__(self)

    def Print(self, text, doc_name):
        """stel titel in en toon print preview scherm
        (van waaruit er geprint kan worden)"""
        self.SetHeader(doc_name)
        self.PreviewText(text)
        #~ self.PrintText(text,doc_name)

class MainWindow(wx.Frame):
    """Hoofdscherm van de applicatie"""
    def __init__(self,parent,id,args):
        self.captions = {}
        self.ini = tcmdrkys.TckSettings(INI)
        if self.ini.paden[0] == '':
            wx.MessageBox('Geen settings file ({}) in deze directory'.format(INI))
            return
        self.readcaptions()
        ## print "start",datetime.datetime.today()
        self.parent = parent
        self.modified = False
        self.orig = ["", False, False, False, False, ""]
        self.mag_weg = True
        if args:
            self.fpad = args[0]
            ext = os.path.splitext(self.fpad)[1]
            if ext == "" and not os.path.isdir(self.fpad):
                self.fpad += ".xml"
            elif ext != ".xml":
                self.fpad = ""
        else:
            self.fpad  = ""
        self.dirname,self.filename = os.path.split(self.fpad)
        #~ print self.dirname,self.filename

        self.printer = EasyPrinter()
        self.newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []
        self.readkeys()

        wid = 860 if LIN else 688
        wx.Frame.__init__(self,parent,wx.ID_ANY, "tcmdrkeys",size = (wid, 594),
                            style=wx.DEFAULT_FRAME_STYLE
                                | wx.NO_FULL_REPAINT_ON_RESIZE
                                ## | wx.BORDER_SIMPLE
                                )
        self.sb = self.CreateStatusBar() # A Statusbar in the bottom of the window

    # --- schermen opbouwen: controls plaatsen -----------------------------------------------------------------------------------------
        self.SetTitle(self.captions["000"])
        #~ self.SetIcon(wx.Icon("task.ico",wx.BITMAP_TYPE_ICO))
        ## self.SetIcon(images.gettaskIcon())
        #~ self.SetMinSize((476, 560))

        self.menuBar = wx.MenuBar()
        for title, items in C_MENU:
            menu = wx.Menu()
            for sel in items:
                if sel == -1:
                    menu.AppendSeparator()
                else:
                    menu.Append(int(sel), self.captions[sel])
                    self.Bind(wx.EVT_MENU, self.OnMenu, id=int(sel))
            self.menuBar.Append(menu, self.captions[title])
        self.SetMenuBar(self.menuBar)

        self.pnl = wx.Panel(self,-1)
        self.pnl.parent = self

        self.page = Page(self.pnl,-1,top=self)

        self.txtKey = wx.StaticText(self.pnl, -1, self.captions[C_KTXT] + " ")
        self.keylist = [x for x in string.ascii_uppercase] + \
            [x for x in string.digits] + ["F" + str(i) for i in range(1,13)] + \
            [self.captions[str(x)] for x in xrange(100,118)]

        cb = wx.ComboBox(
            self.pnl, -1, "",
            size = (65,5), choices = self.keylist,
            style=wx.CB_DROPDOWN #|wxTE_PROCESS_ENTER
            )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        self.Bind(wx.EVT_TEXT, self.EvtText, cb)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, cb)
        ## cb.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        ## cb.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.cmbKey = cb
        ## print "na opzetten keys combobox",datetime.datetime.today()

        for x in (M_CTRL, M_ALT, M_SHFT, M_WIN):
            cb = wx.CheckBox(self.pnl, -1, self.captions[x].join(("+","  "))) #, (65, 60), (150, 20), wx.NO_BORDER)
            cb.SetValue(False)
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
            if x == M_CTRL:
                self.cbCtrl = cb
            elif x == M_ALT:
                self.cbAlt = cb
            elif x == M_SHFT:
                self.cbShift = cb
            elif x == M_WIN:
                self.cbWin = cb
        ## print "na opzetten checkboxen",datetime.datetime.today()

        self.txtCmd = wx.StaticText(self.pnl, -1, self.captions[C_CTXT] + " ")
        commandlist = self.omsdict.keys()
        commandlist.sort()
        cb = wx.ComboBox(
            self.pnl, -1,
            size = (95, -1), choices = commandlist,
            style = wx.CB_DROPDOWN #|wxTE_PROCESS_ENTER
            )
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        self.Bind(wx.EVT_TEXT, self.EvtText, cb)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, cb)
        ## cb.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        ## cb.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.cmbCommando = cb
        ## print "na opzetten cmd combobox",datetime.datetime.today()
        self.bSave = wx.Button(self.pnl, -1, self.captions[C_SAVE]) ##, (120, 45))
        self.bSave.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.bSave)
        self.bDel = wx.Button(self.pnl, -1, self.captions[C_DEL]) #, size= (50,-1)) ##, (120, 45))
        self.bDel.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.bDel)

        self.txtOms = wx.TextCtrl(self.pnl, -1, size=(125, 36),
            style=wx.TE_MULTILINE | wx.TE_READONLY
            )

        self.bExit = wx.Button(self.pnl, wx.ID_EXIT, self.captions[C_EXIT])
        self.Bind(wx.EVT_BUTTON, self.Exit , self.bExit)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        ## self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        ## self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        ## print "na opzetten schermcontrols",datetime.datetime.today()

    # --- schermen opbouwen: layout -----------------------------------------------------------------------------------------
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        self.page.doelayout()
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.page,1,wx.EXPAND,0)
        sizer0.Add(sizer1,1,wx.EXPAND | wx.ALL,4)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(self.txtKey,0,wx.ALIGN_CENTER_VERTICAL,0)
        sizer3.Add(self.cmbKey,0,wx.EXPAND,0)
        sizer2.Add(sizer3,0,wx.LEFT | wx.RIGHT | wx.EXPAND,4)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(self.cbWin,0,wx.EXPAND,0)
        sizer3.Add(self.cbCtrl,0,wx.EXPAND,0)
        sizer3.Add(self.cbAlt,0,wx.EXPAND,0)
        sizer3.Add(self.cbShift,0,wx.EXPAND,0)
        sizer2.Add(sizer3,0,wx.EXPAND,0)
        sizer1.Add(sizer2,0,wx.ALL | wx.EXPAND,4)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.txtCmd,0,wx.ALIGN_CENTER_VERTICAL,0)
        sizer2.Add(self.cmbCommando,1,wx.EXPAND | wx.TOP | wx.BOTTOM ,4)
        sizer1.Add(sizer2,1,wx.LEFT | wx.RIGHT | wx.EXPAND,24)
        ## sizer0.Add(sizer1,0,wx.EXPAND)
        sizer1.Add(self.bSave,0,wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 4)
        sizer1.Add(self.bDel,0,wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 4)
        box = wx.StaticBox(self.pnl, -1, style=wx.BORDER_NONE)
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        bsizer.Add(sizer1,0,wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,8)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.txtOms,1,wx.LEFT | wx.RIGHT | wx.EXPAND, 4)
        bsizer.Add(sizer1,0,wx.EXPAND | wx.ALL ,8)
        sizer0.Add(bsizer,0,wx.EXPAND | wx.ALL,4)

        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(self.bExit,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,4)
        sizer0.Add(sizer2,0,wx.EXPAND | wx.ALL,4)
        self.pnl.SetSizer(sizer0)
        self.pnl.SetAutoLayout(True)
        sizer0.Fit(self.pnl)
        sizer0.SetSizeHints(self.pnl)
        self.pnl.Layout()
        ## print "na layouten scherm",datetime.datetime.today()
        self.Show(True)
        if len(self.data) == 0:
            dlg = wx.MessageDialog(self, self.captions['042'],
                self.captions["000"],
                wx.OK | wx.ICON_INFORMATION
                )
            h = dlg.ShowModal()
            dlg.Destroy()


    def vuldetails(self,seli):
        key, mods, soort, cmd, oms = self.data[seli]
        ## print "details vullen met",key,soort,cmd,oms
        self.bSave.Enable(False)
        if soort == 'U':
            self.bDel.Enable(True)
        self.orig =  [key, False, False, False, False, cmd]
        self.cbShift.SetValue(False)
        self.cbCtrl.SetValue(False)
        self.cbAlt.SetValue(False)
        self.cbWin.SetValue(False)
        self.cmbKey.SetValue(key)
        if 'S' in mods:
        ## for mod in mods:
            ## if mod == "S":
                self.orig[1] = True
                self.cbShift.SetValue(True)
        if 'C' in mods:
            ## elif mod == "C":
                self.orig[2] = True
                self.cbCtrl.SetValue(True)
        if 'A' in mods:
            ## elif mod == "A":
                self.orig[3] = True
                self.cbAlt.SetValue(True)
        if 'W' in mods:
            ## elif mod == "W":
                self.orig[4] = True
                self.cbWin.SetValue(True)
        self.cmbCommando.SetValue(cmd)
        self.txtOms.SetValue(oms)

    def aanpassen(self, delete=False):
        oktocontinue = True
        origkey = self.orig[0]
        key = self.cmbKey.GetValue()
        if key not in self.keylist:
            if key.upper() in self.keylist:
                key = key.upper()
                self.cmbKey.SetValue(key)
            else:
                oktocontinue = False
        origmods = ''
        if self.orig[4]:
            origmods += 'W'
        if self.orig[2]:
            origmods += 'C'
        if self.orig[3]:
            origmods += 'A'
        if self.orig[1]:
            origmods += 'S'
        mods = ""
        if self.cbWin.GetValue():
            mods += "W"
        if self.cbCtrl.GetValue():
            mods += "C"
        if self.cbAlt.GetValue():
            mods += "A"
        if self.cbShift.GetValue():
            mods += "S"
        ## if mods != "":
            ## key = " + ".join((key,mods))
        origcmd = self.orig[5]
        cmd = self.cmbCommando.GetValue()
        if cmd not in self.omsdict.keys():
            oktocontinue = False
        if not oktocontinue:
            h = self.captions['021'] if delete else self.captions['022']
            dlg = wx.MessageDialog(self, h, self.captions["000"],
                wx.OK | wx.ICON_INFORMATION
                )
            h = dlg.ShowModal()
            dlg.Destroy()
            return
        gevonden = False
        print origkey, ';', origmods, ';', key, ';', mods
        for number, value in self.data.iteritems():
            ## print number, value
            if value[0] == key and value[1] == mods:
                gevonden = True
                indx = number
                break
        if gevonden:
            if key != origkey or mods != origmods:
                dlg = wx.MessageDialog(self, self.captions["045"],
                    self.captions["000"],
                    wx.YES_NO | wx.NO_DEFAULT |  wx.ICON_INFORMATION
                    )
                h = dlg.ShowModal()
                dlg.Destroy()
                if h == wx.ID_NO:
                    oktocontinue = False
        if not delete:
            if gevonden:
                if oktocontinue:
                    self.data[indx] = (key, mods, 'U', cmd, self.omsdict[cmd])
            else:
                newdata = self.data.values()
                newvalue = (key, mods, 'U', cmd, self.omsdict[cmd])
                newdata.append(newvalue)
                newdata.sort()
                for x, y in enumerate(newdata):
                    if y == newvalue:
                        indx = x
                    self.data[x] = y
        else:
            if not gevonden:
                dlg = wx.MessageDialog(self, self.captions['023'],
                    self.captions["000"],
                    wx.OK | wx.ICON_INFORMATION
                    )
                h = dlg.ShowModal()
                dlg.Destroy()
                oktocontinue = False
            elif self.data[indx][1] == "S":
                dlg = wx.MessageDialog(self, self.captions['024'],
                    self.captions["000"],
                    wx.OK | wx.ICON_INFORMATION
                    )
                h = dlg.ShowModal()
                dlg.Destroy()
                oktocontinue = False
            else:
                # kijk of er een standaard definitie bij de toets hoort, zo ja deze terugzetten
                if self.data[indx][0] in self.defkeys:
                    cmd = self.defkeys[self.data[indx][0]]
                    if cmd in self.omsdict:
                        oms = self.omsdict[cmd]
                    else:
                        oms = cmd
                        cmd = ""
                    self.data[indx] = (key, 'S', cmd, oms)
                else:
                    del self.data[indx]
                    indx -= 1
        if oktocontinue:
            self.page.PopulateList()
            self.modified = True
            self.SetTitle(self.captions["000"] + ' ' + self.captions['017'])
            self.bSave.Enable(False)
            self.bDel.Enable(False)
            self.page.p0list.Select(indx)

    def OnMenu(self, event):
        id = str(event.GetId())
        text = MENU_FUNC[id](self)
        if text:
            dlg = wx.MessageDialog(self,text,self.captions["000"], wx.OK)
            h = dlg.ShowModal()
            dlg.Destroy()

    def EvtComboBox(self,evt):
        cb = evt.GetEventObject()
        ## print "EvtComboBox on",cb
        ## h = evt.GetString()
        ## if cb == self.cmbKey:
            ## j = self.cmbCommando.GetValue()
            ## print "h:",h
            ## print "j:",j
            ## if h != self.orig[0] and h.strip() != "" and j.strip() != "":
                ## self.defchanged = True
                ## self.bSave.Enable(True)
                ## self.bDel.Enable(True)
        ## elif cb == self.cmbCommando:
            ## j = self.cmbKey.GetValue()
            ## print "h:",h
            ## print "j:",j
            ## if h != self.orig[5] and h.strip() != "" and j.strip() != "":
                ## self.defchanged = True
                ## self.txtOms.SetValue(self.omsdict[h])
                ## self.bSave.Enable(True)
                ## self.bDel.Enable(True)

    def EvtCheckBox(self,evt):
        cb = evt.GetEventObject()
        if cb == self.cbShift:
            if cb.GetValue() != self.orig[1]:
                self.defchanged = True
                self.bSave.Enable(True)
                self.bDel.Enable(True)
        elif cb == self.cbCtrl:
            if cb.GetValue() != self.orig[2]:
                self.defchanged = True
                self.bSave.Enable(True)
                self.bDel.Enable(True)
        elif cb == self.cbAlt:
            if cb.GetValue() != self.orig[3]:
                self.defchanged = True
                self.bSave.Enable(True)
                self.bDel.Enable(True)
        elif cb == self.cbWin:
            if cb.GetValue() != self.orig[4]:
                self.defchanged = True
                self.bSave.Enable(True)
                self.bDel.Enable(True)

    def OnClick(self,evt):
        b = evt.GetEventObject()
        key = self.cmbKey.GetValue()
        cmd = self.cmbCommando.GetValue()
        if b == self.bSave:
            ## print "keydef opslaan gekozen",key,cmd
            self.aanpassen()
        elif b == self.bDel:
            ## print "keydef verwijderen gekozen",key,cmd
            self.aanpassen(delete=True)

    def OnKeyPress(self,evt):
        """
        met behulp van deze methode wordt vanaf globaal (applicatie) niveau dezelfde
        toetsenafhandelingsroutine aangeroepen als vanaf locaal (tab) niveau
        """
        keycode = evt.GetKeyCode()
        self.page.OnKeyPress(evt)
        evt.Skip()


    def EvtText(self,evt):
        self.defchanged = False
        cb = evt.GetEventObject()
        ## print "EvtText on",cb
        h = evt.GetString()
        if cb == self.cmbKey:
            ## print "h:",h
            j = self.cmbCommando.GetValue()
            ## print "j:",j
            if h.strip() == "" or j.strip() == "":
                self.bSave.Enable(False)
                self.bDel.Enable(False)
            elif h != self.orig[0]:
                self.defchanged = True
                self.bSave.Enable(True)
                self.bDel.Enable(True)
        elif cb == self.cmbCommando:
            j = self.cmbKey.GetValue()
            ## print "h:",h
            ## print "j:",j
            if h.strip() == "" or j.strip() == "":
                self.bSave.Enable(False)
                self.bDel.Enable(False)
            elif h != self.orig[5]:
                self.defchanged = True
                try:
                    self.txtOms.SetValue(self.omsdict[h])
                except KeyError:
                    print "Key bestaat niet in omsdict:",h
                    return
                self.bSave.Enable(True)
                self.bDel.Enable(True)

    def EvtTextEnter(self,evt):
        cb = evt.GetEventObject()
        ## print "EvtTextEnter on",cb

    def OnSetFocus(self,evt):
        pass

    def OnKillFocus(self,evt):
        pass

    def Exit(self,e=None):
        if self.modified:
            dlg = wx.MessageDialog(self, self.captions['025'],
                self.captions["000"],
                wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT | wx.ICON_INFORMATION
                )
            h = dlg.ShowModal()
            dlg.Destroy()
            if h == wx.ID_YES:
                self.savekeys()
            elif h == wx.ID_CANCEL:
                return
        self.Close(True)

    def readkeys(self):
        self.cmdict, self.omsdict, self.defkeys, self.data = tcmdrkys.readkeys(
            self.ini.paden)

    def savekeys(self):
        tcmdrkys.savekeys(self.ini.tcpad, self.data)
        self.modified = False
        self.SetTitle(self.captions["000"])

    def readcaptions(self):
        for x in file(os.path.join(HERE, self.ini.lang)):
            if x[0] == '#' or x.strip() == "":
                continue
            key,value = x.strip().split(None,1)
            self.captions[key] = value

    def setcaptions(self):
        title = self.captions["000"]
        if self.modified:
            title += ' ' + self.captions["017"]
        self.SetTitle(title)
        self.cbCtrl.SetLabel(self.captions[M_CTRL].join(("+", "  ")))
        self.cbAlt.SetLabel(self.captions[M_ALT].join(("+", "  ")))
        self.cbShift.SetLabel(self.captions[M_SHFT].join(("+", "  ")))
        self.bSave.SetLabel(self.captions[C_SAVE])
        self.bDel.SetLabel(self.captions[C_DEL])
        self.bExit.SetLabel(self.captions[C_EXIT])
        self.txtKey.SetLabel(self.captions[C_KTXT])
        self.txtCmd.SetLabel(self.captions[C_CTXT])
        for indx,menu in enumerate(self.menuBar.GetMenus()):
            menu, title = menu
            self.menuBar.SetLabelTop(indx, self.captions[C_MENU[indx][0]])
            for indy, item in enumerate(menu.GetMenuItems()):
                i, t = item.GetId(), item.GetItemLabel()
                if i > 0:
                    item.SetItemLabel(self.captions[C_MENU[indx][1][indy]])
        self.page.PopulateList()

    def afdrukken(self):
        self.css = ""
        if self.css != "":
            self.css = "".join(("<style>",self.css,"</style>"))
        self.text.insert(0,"".join(("<html><head><title>titel</title>",self.css,"</head><body>")))
        self.text.append("</body></html>")
        self.printer.Print("".join(self.text),self.hdr)
        return
        # de moelijke manier
        data = wx.PrintDialogData()
        data.EnableSelection(False)
        data.EnablePrintToFile(True)
        data.EnablePageNumbers(False)
        data.SetAllPages(True)
        dlg = wx.PrintDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            pdd = dlg.GetPrintDialogData()
            prt = wxPrinter(pdd)
            pda = Prtdata(self.textcanvas)
            if not prt.Print(self,prtdata,False):
                MessageBox("Unable to print the document.")
            prt.Destroy()
        dlg.Destroy()

def main(args=None):
    app = wx.App(redirect=True, filename="tckey.log")
    print '----------'
    frame = MainWindow(None, -1, args)
    app.MainLoop()

if __name__ == '__main__':
    ## h = Tcksettings()
    ## h.set('paden',['ergens',])
    ## print h.__dict__
    main(sys.argv[1:])