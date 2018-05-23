"""Menu definition and callbacks for HotKeys
"""
import os
## import logging
import functools
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
## import PyQt5.QtCore as core

import editor.hotkeys_constants as hkc
import editor.hotkeys_dialogs_qt5 as hkd
## from editor.hotkeys_qt5 import HotkeyPanel  # <- dit gaat niet werken


# menu callbacks
def m_read(main):
    """(menu) callback voor het lezen van de hotkeys

    vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
    zet de gelezen keys daarna ook in de gui
    """
    if not main.page.settings:
        hkd.show_message(main, 'I_ADDSET')
        return
    if not main.page.modified:
        if not hkd.ask_question(main, 'Q_NOCHG'):
            return
    main.page.readkeys()
    main.page.populate_list()


def m_save(main):
    """(menu) callback voor het terugschrijven van de hotkeys

    vraagt eerst of het ok is om de hotkeys weg te schrijven
    vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
    """
    if not main.page.modified:
        if not hkd.ask_question(main, 'Q_NOCHG'):
            return
    try:
        main.page.savekeys()
    except AttributeError:
        hkd.show_message(main, 'I_DEFSAV')
        return
    hkd.show_message(main, 'I_RSTRT')


def m_loc(main):
    """(menu) callback voor aanpassen van de bestandslocaties

    vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
    toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
    (met name of de opgegeven paden kloppen)
    """
    # main.ini["plugins"] bevat de lijst met tools en csv locaties
    current_programs = [x for x, y in main.ini["plugins"]]
    current_paths = [y for x, y in main.ini["plugins"]]
    ok = hkd.FilesDialog(main).exec_()
    if ok == qtw.QDialog.Accepted:
        selection = main.book.sel.currentIndex()
        hkc.modify_settings(main.ini)

        # update the screen(s)
        # clear the selector and the stackedwidget while pairing up programs and windows
        # that need to be kept or replaced
        hlpdict = {}
        main.book.sel.clear()
        current_items = reversed([(x, y) for x, y in enumerate(current_programs)])
        new_programs = [x for x, y in main.ini["plugins"]]
        new_paths = [y for x, y in main.ini["plugins"]]
        for indx, program in current_items:  # we need to do this in reverse
            win = main.book.pnl.widget(indx)
            main.book.pnl.removeWidget(win)
            if program in new_programs:
                hlpdict[program] = win  # keep the widget
            else:
                win.close()  # lose the widget
        # add new ones, modify existing or leave them alone
        for indx, program in enumerate(new_programs):
            if program in current_programs:
                # compare the new and the existing path
                old_loc = current_paths[current_programs.index(program)]
                new_loc = new_paths[new_programs.index(program)]
                if new_loc == old_loc:  # unchanged
                    win = hlpdict[program]
                else:  # take data from different location
                    win = HotkeyPanel(main.book, new_loc)
            else:  # new entry
                loc = new_paths[indx]
                if not os.path.exists(loc):
                    loc = os.path.join(hkc.BASE, loc)
                win = HotkeyPanel(main.book, loc)
            main.book.sel.addItem(program)
            main.book.pnl.addWidget(win)
        if main.last_added:
            selection = main.book.sel.findText(main.last_added)
        if selection > len(main.ini['plugins']) - 1:
            selection -= 1
        main.book.sel.setCurrentIndex(selection)


def m_rebuild(main):
    """rebuild csv data from (updated) settings
    """
    if not main.page.settings:
        hkd.show_message(main, 'I_ADDSET')
        return
    try:
        test = main.page._keys.buildcsv
    except AttributeError:
        hkd.show_message(main, 'I_DEFRBLD')
        return
    newdata = test(main)
    if newdata[0]:
        main.page.data = newdata[0]
        main.page.otherstuff = newdata[1]
        hkc.writecsv(main.page.pad, main.page.settings, main.page.column_info,
                     main.page.data, main.ini['lang'])
        main.page.populate_list()
    else:
        try:
            mld = newdata[1]
        except IndexError:
            mld = 'No data returned, keyboard settings file unknown or nonexistant'
        hkd.show_message(main, text=mld)


def m_tool(main):
    """define tool-specific settings
    """
    if not main.page.settings:
        main.page.settings = {x: '' for x in hkc.csv_settingnames}
    old_redef = bool(int(main.page.settings[hkc.csv_redefsett]))
    dlg = hkd.ExtraSettingsDialog(main).exec_()
    if dlg == qtw.QDialog.Accepted:
        hkc.writecsv(main.page.pad, main.page.settings, main.page.column_info,
                     main.page.data, main.ini['lang'])
        test_redef = bool(int(main.page.settings[hkc.csv_redefsett]))
        test_dets = bool(int(main.page.settings[hkc.csv_detsett]))
        test_rbld = bool(int(main.page.settings[hkc.csv_rbldsett]))
        main._menuitems['M_SAVE'].setEnabled(test_redef)
        main._menuitems['M_RBLD'].setEnabled(test_rbld)
        indx = main.book.sel.currentIndex()
        win = main.book.pnl.widget(indx)
        if test_dets != main.page.has_extrapanel:
            main.page.has_extrapanel = test_dets
            newwin = HotkeyPanel(main.book, main.book.plugins[indx][1])
            main.book.pnl.insertWidget(indx, newwin)
            main.book.pnl.setCurrentIndex(indx)
            main.book.pnl.removeWidget(win)
        elif test_redef != old_redef and test_dets:
            win = main.book.pnl.currentWidget()
            win.set_extrascreen_editable(test_redef)


def m_col(main):
    """define tool-specific settings: column properties
    """
    if not main.page.settings:
        hkd.show_message(main, 'I_ADDSET')
        return
    dlg = hkd.ColumnSettingsDialog(main).exec_()
    if dlg == qtw.QDialog.Accepted:
        new_pagedata = {}
        for key, value in main.page.data.items():
            newvalue = []
            for colinf in main.page.column_info:
                test = colinf[-1]
                if test == 'new':
                    newvalue.append('')
                else:
                    newvalue.append(value[test])
            new_pagedata[key] = newvalue
        main.page.data = new_pagedata
        main.page.column_info = [x[:-1] for x in main.page.column_info]

        hkc.writecsv(main.page.pad, main.page.settings, main.page.column_info,
                     main.page.data, main.ini['lang'])
        if not main.page.data:
            return
        hdr = qtw.QTreeWidgetItem()
        main.page.p0list.setHeaderItem(hdr)
        main.page.p0list.setHeaderLabels([main.captions[col[0]] for col in
                                          main.page.column_info])
        hdr = main.page.p0list.header()
        hdr.setSectionsClickable(True)
        for indx, col in enumerate(main.page.column_info):
            hdr.resizeSection(indx, col[1])
        hdr.setStretchLastSection(True)
        main.page.populate_list()


def m_entry(main):
    """manual entry of keyboard shortcuts
    """
    if not all((main.page.settings, main.page.column_info)):
        hkd.show_message(main, 'I_ADDCOL')
        return
    dlg = hkd.EntryDialog(main).exec_()
    if dlg == qtw.QDialog.Accepted:
        if main.page.data:
            hkc.writecsv(main.page.pad, main.page.settings, main.page.column_info,
                         main.page.data, main.ini['lang'])
            main.page.populate_list()


def m_lang(main):
    """(menu) callback voor taalkeuze

    past de settings aan en leest het geselecteerde language file
    """
    # bepaal welke language files er beschikbaar zijn
    choices = [x.name for x in hkc.HERELANG.iterdir() if x.suffix == ".lng"]
    # bepaal welke er momenteel geactiveerd is
    oldlang = main.ini['lang']
    indx = choices.index(oldlang) if oldlang in choices else 0
    lang, ok = qtw.QInputDialog.getItem(main, main.title, main.captions["P_SELLNG"],
                                        choices, current=indx, editable=False)
    if ok:
        hkc.change_setting('lang', oldlang, lang, main.ini['filename'])
        main.ini['lang'] = lang
        main.readcaptions(lang)
        main.setcaptions()


def m_about(main):
    """(menu) callback voor het tonen van de "about" dialoog
    """
    hkd.show_message(main, text='\n'.join(main.captions['T_ABOUT'].format(
        main.captions['T_SHORT'], hkc.VRS, hkc.AUTH,
        main.captions['T_LONG']).split(' / ')))


def m_pref(main):
    """mogelijkheid bieden om een tool op te geven dat default getoond wordt
    """
    oldpref = main.ini.get("initial", None)
    oldmode = main.ini.get("startup", None)
    main.prefs = oldmode, oldpref
    ok = hkd.InitialToolDialog(main).exec_()
    if ok == qtw.QDialog.Accepted:
        mode, pref = main.prefs
        print('in m_pref: {}, {}'.format(mode, pref))
        if mode:
            main.ini['startup'] = mode
            hkc.change_setting('startup', oldmode, mode, main.ini['filename'])
        if mode == 'Fixed':
            main.ini['initial'] = pref
            hkc.change_setting('initial', oldpref, pref, main.ini['filename'])


def m_exit(main):
    """(menu) callback om het programma direct af te sluiten
    """
    main.exit()


# menu definition using the previously defined functions
MENUS = (('M_APP', (
         ('M_SETT', ((
             ('M_LOC', (m_loc, 'Ctrl+F')),
             ('M_LANG', (m_lang, 'Ctrl+L')),
             ('M_PREF', (m_pref, ''))), '')),
         ('M_EXIT', (m_exit, 'Ctrl+Q')), )),
         ('M_TOOL', (
             ('M_SETT', ((
                 ('M_COL', (m_col, '')),
                 ('M_MISC', (m_tool, '')),
                 ('M_ENTR', (m_entry, '')), ), '')),
             ('M_READ', (m_read, 'Ctrl+R')),
             ('M_RBLD', (m_rebuild, 'Ctrl+B')),
             ('M_SAVE', (m_save, 'Ctrl+S')), )),
         ('M_HELP', (
             ('M_ABOUT', (m_about, 'Ctrl+H')), )))


# menu creation (called each time the HotkeyPanel changes)
def setup_menu(main):
    main._menuitems = {}  # []
    for title, items in MENUS:
        menu = main.menu_bar.addMenu(main.captions[title])
        main._menuitems[title] = menu
        for sel in items:
            if sel == -1:
                menu.addSeparator()
                continue
            else:
                sel, values = sel
                callback, shortcut = values
                if callable(callback):
                    act = create_menuaction(main, sel, callback, shortcut)
                    menu.addAction(act)
                    main._menuitems[sel] = act
                else:
                    submenu = menu.addMenu(main.captions[sel])
                    main._menuitems[sel] = submenu
                    for sel, values in callback:
                        callback, shortcut = values
                        act = create_menuaction(main, sel, callback, shortcut)
                        submenu.addAction(act)
                        main._menuitems[sel] = act


def create_menuaction(main, sel, callback, shortcut):
    """return created action w. some special cases
    """
    act = qtw.QAction(main.captions[sel], main)
    act.triggered.connect(functools.partial(callback, main))
    act.setShortcut(shortcut)
    if sel == 'M_READ':
        if not main.page.data:
            act.setEnabled(False)
    if sel == 'M_RBLD':
        try:
            act.setEnabled(bool(int(main.page.settings[hkc.csv_rbldsett])))
        except KeyError:
            act.setEnabled(False)
    elif sel == 'M_SAVE':
        try:
            act.setEnabled(bool(int(main.page.settings[hkc.csv_redefsett])))
        except KeyError:
            act.setEnabled(False)
    return act
