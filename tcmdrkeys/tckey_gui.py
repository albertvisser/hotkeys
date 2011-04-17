#! C:/python25/python
# -*- coding: UTF-8 -*-
TTL = "A hotkey editor"
VRS = "1.1.x"
AUTH = "(C) 2008 Albert Visser"
#globals om direct aan het begin van dit file te kunnen zien en aanpassen wanneer nodig
INI = "tckey.ini"

import sys, os
WIN = True if sys.platform == "win32" else False
LIN = True if sys.platform == 'linux2' else False
if WIN and file_!= "tckey_gui.py":
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

import wx
import wx.html as html
import wx.lib.mixins.listctrl  as  listmix
import wx.lib.filebrowsebutton as filebrowse
import wx.gizmos   as  gizmos
import images
import tcmdrkys
import string
## import datetime

C_KEY, C_MOD, C_SRT, C_CMD, C_OMS = '001', '043', '002', '003', '004'
C_DFLT, C_RDEF = '005', '006'
M_CTRL, M_ALT, M_SHFT = '007', '008', '009'
C_SAVE, C_DEL, C_EXIT, C_KTXT, C_CTXT ='010', '011', '012', '018', '019'
M_APP, M_READ, M_SAVE, M_USER, M_EXIT = '200', '201', '202', '203', '209'
M_SETT, M_LOC, M_LANG, M_HELP, M_ABOUT = '210', '211', '212', '290', '299'
C_MENU = (
    (M_APP,(M_READ, M_SAVE, M_USER, -1 , M_EXIT)),
    (M_SETT,(M_LOC,M_LANG)),
    (M_HELP,(M_ABOUT,))
    )
NOT_IMPLEMENTED = '404'

def show_message(self, message_id, caption_id='000'):
    dlg = wx.MessageDialog(self, self.captions[message_id],
        self.captions[caption_id],
        wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT | wx.ICON_INFORMATION
        )
    h = dlg.ShowModal()
    dlg.Destroy()
    return h

def m_read(self):
    if not self.modified:
        h = show_message(self, '041')
        if h == wx.ID_YES:
            self.readkeys()
            self.page.PopulateList()

def m_save(self):
    if not self.modified:
        h = show_message(self, '041')
        if h == wx.ID_YES:
            self.savekeys()
            if self.ini.restart:
                h = show_message(self, '026')
                if h == wx.ID_YES:
                    os.system(self.ini.restart) # "C:\Program Files\totalcmd\addons\ReloadTC.exe"
            else:
                h = show_message(self, '037')

def m_user(self):
    return self.captions[NOT_IMPLEMENTED]

def m_exit(self):
    self.Exit()

def m_loc(self):
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
    y = [x for x in os.listdir(os.getcwd()) if os.path.splitext(x)[1] == ".lng"]
    dlg = wx.SingleChoiceDialog(
        self,self.captions["027"],self.captions["000"],
        y,
        wx.CHOICEDLG_STYLE
        )
    for i,x in enumerate(y):
        if x == self.ini.lang:
            dlg.SetSelection(i)
            break
    h = dlg.ShowModal()
    if h == wx.ID_OK:
        lang = dlg.GetStringSelection()
        self.ini.set('lang',lang)
        for x in file(lang):
            if x[0] == '#' or x.strip() == "":
                continue
            key,value = x.strip().split(None,1)
            self.captions[key] = value
        self.setcaptions()
    dlg.Destroy()

def m_about(self):
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

MENU_FUNC = {
    M_READ: m_read,
    M_SAVE: m_save,
    M_USER: m_user,
    M_EXIT: m_exit,
    M_LOC: m_loc,
    M_LANG: m_lang,
    M_ABOUT: m_about,
}

class Tcksettings(object):
    def __init__(self,fn):
        self.fn = fn
        self.namen = ['TC_PAD','UC_PAD','CI_PAD','KT_PAD','HK_PAD','LANG','RESTART']
        self.paden = ['','','','','']
        self.lang = ''
        self.restart = ''
        if not os.path.exists(self.fn):
            return
        for x in file(self.fn):
            if x.strip() == "" or x.startswith('#'):
                continue
            naam,waarde = x.strip().split('=')
            try:
                ix = self.namen.index(naam)
            except ValueError:
                ix = -1
            if 0 <= ix <= 4:
                self.paden[ix] = waarde
            elif ix == 5:
                self.lang = os.path.join(os.path.split(__file__)[0],waarde)
            elif ix == 6:
                self.restart = waarde
        self.tcpad, self.ucpad, self.cipad, self.ktpad, self.hkpad = self.paden
        for x in reversed(self.paden):
            if x == '':
                self.paden.pop()
            else:
                break

    def set(self,item,value):
        items = []
        argnamen = ("tcpad","ucpad","cipad","ktpad","hkpad")
        if item in argnamen:
            for i,x in enumerate(argnamen):
                print i,x
                if item == x:
                    item = self.namen[i]
                    while len(self.paden) <= i:
                        self.paden.append('')
                    print item,i
                    self.paden[i] = value
                    break
        elif item == "paden":
            if type(value) is list and len(value) == 6:
                self.paden = value
            else:
                raise ValueError("Tcksettings needs list with 6 'paden'")
        elif item == "lang":
            item = self.namen[5]
            self.lang = value
        elif item == "restart":
            item = self.namen[6]
            self.restart = value
        elif item in self.namen:
            for i,x in enumerate(argnamen):
                if item == x:
                    if 0 <= i <= 4:
                        self.paden[i] = value
                    elif x == 5:
                        self.lang = value
                    elif ix == 6:
                        self.restart = value
                    break
        else:
            raise ValueError("Tcksettings object doesn't know '%s'" % item)
        f = open(self.fn)
        ini = f.readlines()
        f.close()
        f = open(INI,"w")
        for x in ini:
            if "=" in x:
                try:
                    naam,waarde = x.split("=",1)
                except ValueError:
                    pass
                if naam == item:
                    x = "=".join((naam,value)) + '\n'
                elif naam in self.namen and naam != "LANG":
                    i = self.namen.index(naam)
                    if i == 6:
                        i = 5
                    x = "=".join((naam,self.paden[i])) + "\n"
                ## # in plaats van:
                ## elif item == "paden":
                    ## for i,y in enumerate(self.namen):
                        ## if i < 5 and h == y:
                            ## x = "=".join((h,self.paden[i])) + '\n'
                            ## break
                        ## elif i == 6:
                            ## self.restart = self.paden.pop()
                            ## x = "=".join((h,self.restart)) + '\n'
            f.write(x)
        f.close()

class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class Page(wx.Panel, listmix.ColumnSorterMixin):
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
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(self.p0list,1,wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)

    def OnKeyPress(self, evt):
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
        #~ print "self.init is", self.init
        if not self.init:
            #~ print "ok, enabling buttons"
            self.enableButtons()

    def OnEvtComboBox(self,evt):
        self.enableButtons()

    def PopulateList(self):
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

        for col,inf in enumerate((
                (C_KEY,70),
                (C_MOD,70),
                (C_SRT,80),
                (C_CMD,160),
                (C_OMS,292)
            )):
            inf,wid = inf
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
        return self.p0list

    def GetSortImages(self):
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
        seli = self.p0list.GetItemData(event.m_itemIndex)
        ## print "Itemselected",seli,self.top.data[seli]
        self.top.vuldetails(seli)
        event.Skip()

    def OnItemDeselected(self, event):
        seli = self.p0list.GetItemData(event.m_itemIndex)
        ## print "ItemDeselected",seli,self.top.data[seli]
        if self.top.defchanged:
            self.top.defchanged = False
            dlg = wx.MessageDialog(self,
                self.parent.captions["020"],
                self.parent.captions["000"],
                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION
                )
            h = dlg.ShowModal()
            dlg.Destroy()
            if h == wx.ID_YES:
                ## print "OK gekozen"
                self.top.aanpassen()

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex

    def OnColClick(self, event):
        ## print "OnColClick: %d\n" % event.GetColumn()
        ## self.parent.sorter = self.GetColumnSorter()
        event.Skip()

    def OnDoubleClick(self, event):
        pass
        # self.log.WriteText("OnDoubleClick item %s\n" % self.p0list.GetItemText(self.currentItem))
        event.Skip()


    def enableButtons(self,state=True):
        pass # anders wordt de methode van de Page class geactiveerd

    def keyprint(self,evt):
        pass


class FilesDialog(wx.Dialog):
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
    def __init__(self):
        html.HtmlEasyPrinting.__init__(self)

    def Print(self, text, doc_name):
        self.SetHeader(doc_name)
        self.PreviewText(text)
        #~ self.PrintText(text,doc_name)

class MainWindow(wx.Frame):
    def __init__(self,parent,id,args):
        self.captions = {}
        self.ini = Tcksettings(INI)
        for x in file(self.ini.lang):
            if x[0] == '#' or x.strip() == "":
                continue
            key,value = x.strip().split(None,1)
            self.captions[key] = value
        ## print "start",datetime.datetime.today()
        self.parent = parent
        self.modified = False
        self.orig = ["",False,False,False,""]
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
        (self.dirname,self.filename) = os.path.split(self.fpad)
        #~ print self.dirname,self.filename

        self.printer = EasyPrinter()
        self.newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []
        self.readkeys()

        wid = 768 if LIN else 688
        wx.Frame.__init__(self,parent,wx.ID_ANY, "tcmdrkeys",size = (wid, 594),
                            style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE|wx.BORDER_SIMPLE)
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

        for x in (M_CTRL,M_ALT,M_SHFT):
            cb = wx.CheckBox(self.pnl, -1, self.captions[x].join(("+","  "))) #, (65, 60), (150, 20), wx.NO_BORDER)
            cb.SetValue(False)
            self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
            if x == M_CTRL:
                self.cbCtrl = cb
            elif x == M_ALT:
                self.cbAlt = cb
            elif x == M_SHFT:
                self.cbShift = cb
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
        self.orig =  [key,False,False,False,cmd]
        self.cbShift.SetValue(False)
        self.cbCtrl.SetValue(False)
        self.cbAlt.SetValue(False)
        self.cmbKey.SetValue(key)
        for mod in mods:
            if mod == "S":
                self.orig[1] = True
                self.cbShift.SetValue(True)
            elif mod == "C":
                self.orig[2] = True
                self.cbCtrl.SetValue(True)
            elif mod == "A":
                self.orig[3] = True
                self.cbAlt.SetValue(True)
        self.cmbCommando.SetValue(cmd)
        self.txtOms.SetValue(oms)

    def aanpassen(self,delete=False):
        go = True
        key = self.cmbKey.GetValue()
        if key not in self.keylist:
            if key.upper() in self.keylist:
                key = key.upper()
                self.cmbKey.SetValue(key)
            else:
                go = False
        mods = ""
        if self.cbCtrl.GetValue():
            mods += "C"
        if self.cbAlt.GetValue():
            mods += "A"
        if self.cbShift.GetValue():
            mods += "S"
        ## if mods != "":
            ## key = " + ".join((key,mods))
        cmd = self.cmbCommando.GetValue()
        if cmd not in self.omsdict.keys():
            go = False
        if not go:
            h = self.captions['021'] if delete else self.captions['022']
            dlg = wx.MessageDialog(self, h, self.captions["000"],
                wx.OK | wx.ICON_INFORMATION
                )
            h = dlg.ShowModal()
            dlg.Destroy()
            return
        gevonden = False
        for x in enumerate(self.data.values()):
            if x[1][0] == key:
                gevonden = True
                indx = x[0]
                break
        if not delete:
            if gevonden:
                self.data[indx] = (key,mods,'U',cmd,self.omsdict[cmd])
            else:
                newdata = self.data.values()
                newdata.append((key,mods,'U',cmd,self.omsdict[cmd]))
                newdata.sort()
                for x,y in enumerate(newdata):
                    self.data[x] = y
            self.page.PopulateList()
            self.modified = True
            self.bSave.Enable(False)
            self.bDel.Enable(False)
        else:
            if not gevonden:
                dlg = wx.MessageDialog(self, self.captions['023'],
                    self.captions["000"],
                    wx.OK | wx.ICON_INFORMATION
                    )
                h = dlg.ShowModal()
                dlg.Destroy()
            elif self.data[indx][1] == "S":
                dlg = wx.MessageDialog(self, self.captions['024'],
                    self.captions["000"],
                    wx.OK | wx.ICON_INFORMATION
                    )
                h = dlg.ShowModal()
                dlg.Destroy()
            else:
                # kijk of er een standaard definitie bij de toets hoort, zo ja deze terugzetten
                if self.data[indx][0] in self.defkeys:
                    cmd = self.defkeys[self.data[indx][0]]
                    if cmd in self.omsdict:
                        oms = self.omsdict[cmd]
                    else:
                        oms = cmd
                        cmd = ""
                    self.data[indx] = (key,'S',cmd,oms)
                else:
                    del self.data[indx]
                self.page.PopulateList()
                self.modified = True
                self.bSave.Enable(False)
                self.bDel.Enable(False)

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
            ## if h != self.orig[4] and h.strip() != "" and j.strip() != "":
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
            elif h != self.orig[4]:
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
        cl = tcmdrkys.tckeys(*self.ini.paden)
        cmdict,self.omsdict = cl.read()
        self.defkeys = cl.defkeys
        ## kys = cl.keydict.keys()
        ## kys.sort()
        self.data = {}
        for ix, hotkey in enumerate(sorted(cl.keydict.keys())):
            try:
                ky, mod = hotkey.split(" + ")
            except ValueError:
                ky,mod = hotkey,""
            srt, desc, cmd = cl.keydict[hotkey]
            self.data[ix] = (ky, mod, srt, cmd, desc)

    def savekeys(self):
        cl = tcmdrkys.tckeys(".")
        for ky, mod, srt, cmd, desc in self.data.values():
            hotkey = " + ".join((ky, mod)) if mod != '' else ky
            cl.keydict[hotkey] = (srt, desc, cmd)
        ## for x,y in cl.keydict.items():
            ## print x,y
        cl.write()

    def setcaptions(self):
        self.SetTitle(self.captions["000"])
        self.cbCtrl.SetLabel(self.captions[M_CTRL].join(("+","  ")))
        self.cbAlt.SetLabel(self.captions[M_ALT].join(("+","  ")))
        self.cbShift.SetLabel(self.captions[M_SHFT].join(("+","  ")))
        self.bSave.SetLabel(self.captions[C_SAVE])
        self.bDel.SetLabel(self.captions[C_DEL])
        self.bExit.SetLabel(self.captions[C_EXIT])
        self.txtKey.SetLabel(self.captions[C_KTXT])
        self.txtCmd.SetLabel(self.captions[C_CTXT])
        for indx,menu in enumerate(self.menuBar.GetMenus()):
            menu,title = menu
            self.menuBar.SetLabelTop(indx,self.captions[C_MENU[indx][0]])
            for indy,item in enumerate(menu.GetMenuItems()):
                i,t = item.GetId(),item.GetItemLabel()
                if i > 0:
                    item.SetItemLabel(self.captions[C_MENU[indx][1][indy]])
        self.page.PopulateList()

        pass

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
    app = wx.PySimpleApp(redirect=True,filename="tckey.log")
    frame = MainWindow(None, -1, args)
    app.MainLoop()

if __name__ == '__main__':
    ## h = Tcksettings()
    ## h.set('paden',['ergens',])
    ## print h.__dict__
    main(sys.argv[1:])
