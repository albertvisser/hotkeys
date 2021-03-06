"""HotKeys plugin voor VI

standard keys can be parsed in from /usr/share/vim/vim##/doc/index.txt
redefined keys are in ~/.vim/vimrc (map commands)
"""
import string
import pathlib
import collections
from .vikeys_gui import add_extra_fields, layout_extra_fields_topline
# VI_VER = (pathlib.Path(__file__).parent / 'VI_VER').read_text().strip()


def convert_key(value):
    """convert a source file keyname value to a value usable for HotKeys
    """
    w_shift = value.startswith('S-')
    w_ctrl = value.startswith('C-')
    if w_shift or w_ctrl:
        value = value[2:]
    test = {'Left': '', 'Up': '', 'Right': '', 'Down': '',
            'Home': '', 'PageDown': 'PgDn', 'PageUp': 'PgUp', 'End': '',
            'Esc': 'esc', 'Help': '', 'Tab': 'Tab', 'Undo': '',
            'BS': 'Backspace', 'CR': 'Enter', 'NL': 'Return', 'F1': '',
            'Insert': 'Ins', 'Del': '', 'Space': '',
            'MiddleMouse': 'mmb', 'LeftMouse': 'lmb', 'RightMouse': 'rmb',
            'ScrollWheelUp': 'WhlUp', 'ScrollWheelDown': 'WhlDn',
            'ScrollWheelLeft': 'WhlLeft', 'ScrollWheelRight': 'WhlRight', }[value] or value
    if w_shift:
        test += ' shift'
    if w_ctrl:
        test += ' ctrl'
    return test


class DefaultKeys:
    """build the data needed to write the csv file and more

    returns a dictionary of keydefs and a dictionary that is a collection of other data for the gui
    """
    def __init__(self, path):
        self.path = path    # needs to be a pathlib.Path instance
        self.data = []
        self.category = self.command = ''
        self.read_data()
        keys, data = self.parse_data()
        self.keydefs = {}
        self.kinds = set()
        newkey = 0
        for key, values in keys.items():
            newvalue = values
            for item, value in data[key].items():
                self.kinds.add(item)
                newkey += 1
                self.keydefs[newkey] = newvalue + (item, value)

    def read_data(self):
        """read the source file section for section and line by line
        and turn into a list of parseble commands
        """
        newcat = ''
        with self.path.open() as _in:
            header = False
            parse_already = False
            self.add_line = True
            for line in _in:
                line = line.rstrip()
                if line.startswith('=====') and not header:
                    header = True
                    parse_already = False
                    continue
                for test, item in (('1. Insert mode', ''),
                                   ('2. Normal mode', ''),
                                   ('2.1 Text objects', ''),
                                   ('2.2 Window commands', ''),
                                   ('2.3 Square bracket commands', 'Normal mode'),
                                   ("2.4 Commands starting with 'g'", 'Normal mode'),
                                   ("2.5 Commands starting with 'z'", 'Normal mode'),
                                   ('3. Visual mode', ''),
                                   ('4. Command-line editing', ''),
                                   ('5. EX commands', '')):
                    if line.strip().startswith(test) and header:
                        newcat = item or test.split(None, 1)[1]
                        if not self.category:
                            self.category = newcat
                    else:
                        continue
                if newcat == 'EX commands':
                    break
                if line.startswith('-----') and header:
                    header = False
                    parse_already = True
                    continue
                if not line:
                    continue
                if parse_already:
                    self.parse_line(line)
                    self.category = newcat
        self.data.append((self.category, self.command))

    def parse_line(self, line):
        """build a parsable commmand from one or more source lines
        """
        items = [x for x in line.split('\t') if x]
        if line.startswith('|'):
            if self.command:
                self.data.append((self.category, self.command))
            # kijk of eerste item een tweede | bevat (zou zo moeten zijn)
            # zo ja dan haal het begin er af
            try:
                pos = items[0].index('|', 1)
            except ValueError:
                pass
            else:
                items[0] = items[0][pos + 1:].lstrip()
            # en als het verder leeg is, laat het dan weg
            if not items[0]:
                items = items[1:]
            self.command = items
        elif len(items) == 2:
            pass
        elif not line:
            self.add_line = not self.add_line
        else:
            if self.add_line:
                self.command += items

    def parse_data(self):
        """parse the commands into two dictionaries with matching keys:
        one dict maps to commands with parameters and the other maps to modes and descriptions
        """
        newkeys, newdata = {}, collections.defaultdict(lambda: collections.defaultdict(list))
        seq = 0
        to_change = []
        for category, itemlist in self.data:
            command, desc = self.parse_line_elems(itemlist)
            seq += 1
            newkeys[seq] = command
            if command[0] == '1':
                cat, desc_1 = category, desc
            elif command[0] in ('2', '3', '4', '5', '6', '7', '8', '9'):
                to_change.append((seq, category))
            newdata[seq][category] = desc
        for key, category in to_change:
            newdata[key][category] = desc_1
        return newkeys, newdata

    def parse_line_elems(self, items):
        """parse list of line elements into a command and a description
        """
        if len(items) > 1:
            command, desc = items[0], ' '.join([x.strip() for x in items[1:]])
        else:
            command, desc = items[0], ''

        value = command
        self.components, self.pre_params, self.post_params = [], [], []
        while value:
            first, last = '{[<', '}]>'
            if value[0] in first:
                skip, value = self.process_parms(value, first, last)
                if skip:
                    continue
            if value.startswith('CTRL'):
                self.components.append(value[5].lower() + ' ctrl')
                value = value[6:].lstrip()
            elif value in string.ascii_uppercase:
                self.components.append(value.lower() + ' shift')
                value = value[1:].lstrip()
            elif value.startswith("'wildchar'"):
                self.components.append(value)
                value = value[10:].lstrip()
            elif value.startswith("-"):
                value = self.process_dash(value)
            else:
                extradesc, value = self.process_rest(value)
                if extradesc:
                    desc = extradesc + ' ' + desc

        pre_params = ' '.join(['[%s]' % x for x in self.pre_params])
        post_params = ' '.join(['{%s}' % x for x in self.post_params])
        command = ' + '.join(self.components), pre_params, post_params
        if desc.startswith('1 ') or desc.startswith('2 '):
            desc = desc[1:].lstrip()
        elif desc.startswith('1/2 '):
            desc = desc[3:].lstrip()
        return command, desc

    def process_parms(self, value, first, last):
        """processs a delimited value (parameter or special key
        """
        try:
            pos = value.index(last[first.index(value[0])])
        except ValueError:
            skip = False
        else:
            part = value[1:pos]
            if value[0] == '<':
                part = convert_key(part)
                self.components.append(part)
            else:
                if self.components:
                    self.post_params.append(part)
                else:
                    self.pre_params.append(part)
            value = value[pos + 1:].lstrip()
            skip = True
        return skip, value

    def process_dash(self, value):
        """process a range continuation (" - ")
        """
        try:
            pos = value.index(' ', 2)
        except ValueError:
            self.components.append(value)
            value = ''
        else:
            self.components.append(value[:pos])
            value = value[pos:].lstrip()
        return value

    def process_rest(self, value):
        """check if value starts with a value indicating that the rest is description
        if so, return empty string
        """
        desc = ''
        for part in ('use', 'replace', 'insert', 'split'):
            if value.startswith(part):
                desc = value
                value = ''
                break
        if value:
            self.components.append(value[0])
            value = value[1:].lstrip()
        return desc, value


def buildcsv(page, showinfo=True):
    """build the datastructures for constructing the CSV file
    """
    if 'extra' not in page.settings:
        page.settings['extra'] = {}
    settname = 'VI_VER'
    if settname not in page.settings:
        with (pathlib.Path.home() / '.viminfo').open(encoding='latin-1') as f:
            line = f.readlines()[0]
        page.settings[settname] = line.strip().rsplit('Vim ')[1][:-1]
        page.settings['extra']['VI_VER'] = 'VI Version'
    ver = page.settings[settname]
    settname = 'VI_CMDREF'
    if settname not in page.settings:
        page.settings[settname] = '/usr/share/vim/vim{}/doc/index.txt'.format(ver)
        oms = 'Name of file containing setting names and descriptions'
        page.settings['extra'] = {settname: oms}
    path = pathlib.Path(page.settings[settname])
    keyclass = DefaultKeys(path)
    keydefs = keyclass.keydefs
    kinds = keyclass.kinds
    keylist = list(set(x[0] for x in keydefs.values()))
    return keydefs, {'types': kinds, 'keylist': keylist}


def add_extra_attributes(win):
    """define plugin-specific variables
    """
    win.init_origdata += ['', '', '']
    win.keylist = win.otherstuff['keylist']
    win.featurelist = sorted(win.otherstuff['types'])


def captions_extra_fields(win):
    "for plugin-specific fields, change the captions according to the language setting"
    win.set_label_text(win.pre_parms_label, win.master.captions['C_BPARMS'] + ':')
    win.set_label_text(win.post_parms_label, win.master.captions['C_APARMS'] + ':')
    win.set_label_text(win.feature_label, win.master.captions['C_FEAT'] + ':')


# def on_combobox(self, cb, text):
#     """handle a specific field in case it's a combobox
#     cb refers to the widget, text to the choice made
#     """
# newdata is a tuple of values from a line in the screen table
# def on_extra_selected(win, newdata):
#     "callback on selection of an item - update specific field"
#     win._origdata[win.fieldindex] = newdata[win.fieldindex]
def vul_extra_details(win, indx, item):
    """fill value for extra field (plugin-specific)
    index refers to the sequence of the field in the screen table, item is the value contained
    """
    if win.column_info[indx][0] == 'C_BPARMS':
        win.gui.set_textfield_value(win.gui.pre_parms_text, item)
        win._origdata[win.gui.ix_pre_parms] = item
    elif win.column_info[indx][0] == 'C_APARMS':
        win.gui.set_textfield_value(win.gui.post_parms_text, item)
        win._origdata[win.gui.ix_post_parms] = item
    elif win.column_info[indx][0] == 'C_FEAT':
        win.gui.set_combobox_string(win.gui.feature_select, item, win.featurelist)
        win._origdata[win.gui.ix_feature_select] = item
