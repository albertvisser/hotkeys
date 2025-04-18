"""HotKeys plugin voor VI

standard keys can be parsed in from /usr/share/vim/vim##/doc/index.txt
redefined keys are in ~/.vim/vimrc (map commands)
"""
import string
import pathlib
import contextlib
import collections
from .vikeys_gui import layout_extra_fields_topline
CONTEXTS = ['Normal mode', 'Insert mode', 'Visual mode', 'Command-line editing']
KINDS = ['Window commands', 'Text objects']
EXCMD = "EX commands"
CATEGORYLIST = ((f'1. {CONTEXTS[1]}', ''),
                (f'2. {CONTEXTS[0]}', ''),
                (f'2.1 {KINDS[1]}', ''),
                (f'2.2 {KINDS[0]}', ''),
                ('2.3 Square bracket commands', f'{CONTEXTS[0]}'),
                ("2.4 Commands starting with 'g'", f'{CONTEXTS[0]}'),
                ("2.5 Commands starting with 'z'", f'{CONTEXTS[0]}'),
                ("2.6. Operator-pending mode", f'{CONTEXTS[0]}'),
                (f'3. {CONTEXTS[2]}', ''),
                (f'4. {CONTEXTS[3]}line editing', ''),
                (f'5. Terminal-Job mode', ''),
                (f'6. {EXCMD}', ''))
STARTDELIMS, ENDDELIMS = '{[<', '}]>'


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
    """build the data needed to write the keydef file and more

    returns a dictionary of keydefs and a dictionary that is a collection of other data for the gui
    """
    def __init__(self, path):
        self.path = path    # needs to be a pathlib.Path instance
        self.data = []
        self.category = self.command = ''
        self.read_data()
        keys, data = self.parse_data()
        self.keydefs = {}
        self.contexts = CONTEXTS
        self.kinds = KINDS
        newkey = 0
        for key, values in keys.items():
            keydef, bparms, aparms = values
            for item, value in data[key].items():
                newkey += 1
                context = ''
                if item in self.contexts:
                    context, item = item, ''
                self.keydefs[newkey] = (keydef, context, bparms, aparms, item, value)

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
                for test, item in CATEGORYLIST:
                    if line.strip().startswith(test) and header:
                        newcat = item or test.split(None, 1)[1]
                        if not self.category:
                            self.category = newcat
                    else:
                        continue
                if newcat == EXCMD:
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
            # bewaar het eerder opgebouwde commando:
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
        elif self.add_line:
            self.command += items

    def parse_data(self):
        """parse the commands into two dictionaries with matching keys:
        one dict maps to commands with parameters and the other maps to modes and descriptions
        """
        newkeys, newdata = {}, collections.defaultdict(dict)
        seq = 0
        to_change = []
        for category, itemlist in self.data:
            command, desc = self.parse_line_elems(itemlist)
            seq += 1
            newkeys[seq] = command
            if command[0] == '1':
                desc_1 = desc
            elif command[0] in ('2', '3', '4', '5', '6', '7', '8', '9'):
                to_change.append((seq, category))
                desc_1 = '?'
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
            value = self.check_for_and_process_delimited(value)
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

        pre_params = ' '.join([f'[{x}]' for x in self.pre_params])
        post_params = ' '.join([f'{{{x}}}' for x in self.post_params])
        command = ' + '.join(self.components), pre_params, post_params
        if desc.startswith(('1 ', '2 ')):
            desc = desc[1:].lstrip()
        elif desc.startswith('1/2 '):
            desc = desc[3:].lstrip()
        return command, desc

    def check_for_and_process_delimited(self, value):
        """processs a delimited value (parameter or special key)
        """
        firstchar = value[0]
        if firstchar not in STARTDELIMS:
            return value
        try:
            pos = value.index(ENDDELIMS[STARTDELIMS.index(value[0])])
        except ValueError:
            return value
        part = value[1:pos]
        if value[0] == '<':
            self.components.append(convert_key(part))
        elif self.components:
            self.post_params.append(part)
        else:
            self.pre_params.append(part)
        return value[pos + 1:].lstrip()

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


def build_data(page):
    """build the datastructures for constructing the keydef file
    """
    path = get_vimdoc_path()
    if not path:
        return {}, {}
    keyclass = DefaultKeys(path)
    keydefs = keyclass.keydefs
    contexts = keyclass.contexts + ['']
    kinds = keyclass.kinds + ['']
    keylist = list(set(x[0] for x in keydefs.values()))
    return keydefs, {'contexts': contexts, 'types': kinds, 'keylist': keylist}


def get_vimdoc_path():
    "determine location of VIm docs for current version"
    # command = 'vi_get_runtime'
    # result = subprocess.run(command, capture_output=True)
    # path = pathlib.Path(result.stdout.decode().strip()) / 'doc' / 'index.txt'
    basedir = pathlib.Path('/usr/share/vim')
    for item in basedir.iterdir():
        if item.is_dir():
            ver = ''
            with contextlib.suppress(ValueError):
                ver = int(str(item.name)[3:])
            if ver:
                return item / 'doc' / 'index.txt'
    else:
        return ''


def add_extra_attributes(win):
    """define plugin-specific variables
    """
    win.keylist = win.otherstuff['keylist']
    win.contextslist = sorted(win.otherstuff['contexts'])
    win.featurelist = sorted(win.otherstuff['types'])
