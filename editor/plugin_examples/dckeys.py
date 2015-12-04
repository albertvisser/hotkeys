# -*- coding: utf-8 -*-
"""
Het gaat alleen om het keydefs opnieuw opbouwen. De overige regels (settings en
kolomdefinities) blijven gehandhaafd. De settings bevat de locatie(s) van het/de
bronbestand.
De naam van het gebruikte settings bestand is vastgelegd in .config/doublecmd.xml
als text bij het subelement NameShortcutFile van root element doublecmd

Ik heb helaas qua doublecommander files alleen shortcuts.sfc, dat bevat wel een
mapping van definities of commando's maar ik heb geen file met mappings van comman-
do's op omschrijvingen.
Eventueel kan ik daar de html files in /usr/share/doublcmd/doc/en voor gebruiken
maar dat is wel een paar sub-versies terug (0.5 ipv 0.10)
"""

from __future__ import print_function
import os
import collections
import xml.etree.ElementTree as et
import bs4 as bs # import BeautifulSoup

def _short_mods(modifier_list):
    result = ''
    if 'Ctrl' in modifier_list:
        result += 'C'
    if 'Alt' in modifier_list:
        result += 'A'
    if 'Shift' in modifier_list:
        result += 'S'
    return result

def _translate_keynames(inp):
    "translate cursor keys as shown in html to notation in xml"
    convert = {' ↑': 'Up', ' ↓': 'Down', ' ←': 'Left', ' →': 'Right'}
    return convert[inp] if inp in convert else inp

def parse_keytext(text):
    """leid keynamen en modifiers op uit tekst

    geeft een list terug van keynaam - modifier-list paren
    voorziet nog niet in , key al dan niet met modifiers
    """
    retval = []

    # split keycombos
    shortcuts = text.split(', ')
    for sc in shortcuts:

        # split for modifiers
        test = sc.split('+')
        keyname = test[-1]
        modifiers = test[:-1]

        # correct for + key
        if keyname == '':
            keyname = '+'
            if modifiers[-1] == '': # + key not on numpad
                modifiers.pop()
            elif modifiers[-1] == 'Num ': # + key on numpad
                keyname = modifiers.pop() + keyname

        retval.append((keyname, _short_mods(modifiers)))

    return retval

def get_keydefs(path):
    """
    huidige keydefs afleiden
    NB splitsen op + geeft mogelijk soms onjuist resultaat (bv bij Num +)
    """

    # read the key definitions file
    data = et.parse(path)

    # (re)build the definitions for the csv file
    keydata = collections.OrderedDict()
    key = 0
    root = data.getroot()
    for form in list(root.find('Hotkeys')):
        context = form.get('Name')
        for hotkey in form:
            shortcut = hotkey.find('Shortcut').text
            parts = shortcut.split('+')
            keyname = parts[-1]
            modifiers = _short_mods(parts[:-1])
            command = hotkey.find('Command').text
            key += 1
            keydata[key] = (keyname, modifiers, context, command)

    return keydata


def get_stdkeys(path):
    """determine standard keys

    keyname moet nog verder opgesplitst worden, in elk geval de modifiers nog apart
    en sommige kunnen meer combo's (gescheiden door komma's) bevatten
    NB splitsen op + geeft soms onjuist resultaat (bv bij Num +)
    """

    with open(path) as doc:
        soup = bs.BeautifulSoup(doc)

    stdkeys = []
    sections = soup.find_all('div', class_='SECT1')
    for div in sections:

        context = div.select("h2 a")
        if not context:
            continue

        context = context[0]['name']

        tbody = div.select('table tbody tr')

        for row in tbody:
            for col in row.select('td'):
                test = col.select('tt')
                if test:
                    keynames = parse_keytext(test[0].text) # kan meer dan 1 key / keycombo bevatten
                else:
                    oms = col.text # zelfde omschrijving als uit cmd's ? Heb ik deze nodig?
            for name in keynames:
                stdkeys.append((_translate_keynames(name), context, oms))

    return stdkeys

def get_cmddict(path):

    with open(path) as doc:
        soup = bs.BeautifulSoup(doc)

    cmddict = {}
    div = soup.find_all('div', class_='CHAPTER')[0]
    tbody = div.select('div > table > tbody > tr')

    for row in tbody:
        command, oms = '', ''
        for col in row.find_all('td', recursive=False):
            test = col.select('tt > div > a')
            if test:
                command = test[0].text
            else:
                oms = ''
                for item in col.contents:
                    if isinstance(item, bs.Tag):
                        if item.name == 'br':
                            break
                        else:
                            oms += item.text
                    else:
                        oms += str(item)
        cmddict[command] = oms

    return cmddict


def buildcsv(settings, parent=None):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand
    """
    shortcuts = collections.OrderedDict()

    keydata = get_keydefs(settings['DC_PATH'][0])
    # to determine if keys have been redefined
    stdkeys = get_stdkeys(settings['DC_KEYS'][0])
    # to find descriptions for commands
    cmddict = get_cmddict(settings['DC_CMDS'][0])
    for key, value in keydata.items():
        templist = list(value)
        templist.insert(-1, '') # standard / customized
        try:
            templist.append(cmddict[value[3]])
        except KeyError:
            templist.append('')
        shortcuts[key] = tuple(templist)

    return shortcuts

def savekeys(pad):
    """schrijf de gegevens terug

    voorlopig nog niet mogelijk
    aangepaste keys samenstellen tot een user.shortcuts statement en dat
    invoegen in shortcuts.scf
    """
    pass
