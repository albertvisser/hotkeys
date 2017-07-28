"""basic plugin for tool using a gtkaccel_map - gui independent stuff
"""
import collections

keydef_id = 'gtk_accel_path'
conversion_map = (('bracketright', ']'),
                  ('bracketleft', '['),
                  ('less', '<'),
                  ('plus', '+'),
                  ('minus', '-'),
                  ('comma', ','),
                  ('grave', '`'),
                  ('period', '.'),
                  ('greater', '>'),
                  ('semicolon', ';'),
                  ('backslash', '\\'),
                  ('KP_', 'Num'),
                  ('Add', '+'),
                  ('Subtract', '-'))


def convert_key(inp):
    """map gtk key name to HotKeys key name
    """
    return out


def build_mods(inp):
    """Um...
    """
    return out


def read_keydefs_and_stuff(filename):
    """Get data from file
    """
    keydefs, actions, others = readfile(filename)
    result = {'keydefs': keydefs}

    actiondict = collections.defaultdict(list)
    new_actions = {}
    descriptions = {}
    for key, value in actions.items():
        context, action = value.lstrip('/').split('/', 1)
        actiondict[context].append(action)
        new_actions[key] = (context, action)
        descriptions[key] = ''
    actions = new_actions
    contextlist = [x for x in actiondict.keys()]
    result.update({'actions': actions, 'actionscontext': actiondict,
                   'contexts': contextlist, 'descriptions': descriptions})

    if others:
        othersdict = collections.defaultdict(list)
        otheractions = {}
        otherkeys = []
        keyval = 0
        for key, value in others:
            context, action = key.lstrip('/').split('/', 1)
            othersdict[context].append(action)
            keyval += 1
            otheractions[keyval] = (context, action)
            if value:
                otherkeys.append((value, keyval))
        result.update({'others': others, 'othercontext': othersdict,
                       'otherkeys': otherkeys})

    return result


def readfile(filename):
    """ read and parse the accel file
    """
    keydefs = []
    actions, others = {}, []
    new_id = 0
    with open(filename) as _in:
        for line in _in:
            ## colon_ed = False
            if keydef_id in line:
                if line.startswith(';'):
                    ## colon_ed = True  # don't know what this means: line ended in colon
                    line = line[1:].strip()
                line = line.rsplit(')', 1)[0]
                data = line.split(keydef_id, 1)[1].strip().split('" "')
                if len(data) != 2:
                    print(line)
                    print('contains more/less that 2 items, what to do?')
                    continue
                name = data[0].lstrip('"')
                key = data[-1].rstrip('"')
                ## commented = coloned
                ## name, key = [x.replace('"', '') for x in data[-2:]]
                if '<Actions>' not in name:
                    others.append((name, key))
                    continue
                name = name.replace('<Actions>', '')
                new_id += 1
                actions[new_id] = name
                ## key = key.replace(')', '')
                if key:
                    test = key.split('>')
                    key = test[-1]
                    for x, y in conversion_map:
                        key = key.replace(x, y)
                    key = key.capitalize()
                    mods = ''
                    if len(test) > 1:
                        if '<Primary' in test:
                            mods += 'C'
                        if '<Alt' in test:
                            mods += 'A'
                        if '<Shift' in test:
                            mods += 'S'
                    ## print(test)
                    keydefs.append((key, mods, new_id))

    return keydefs, actions, others


def build_extended_keydefs(keydefs, actions):  # the old version
    """create lines for csv file
    """
    keydefs_full, used = [], {}
    for key, mods, command in keydefs:
        keydefs_full.append('Keydef,{},{},{}'.format(key, mods, actions[command]))
        used[command] = ''  # can't pop these from actions because the may have been reused
    for key in actions:
        if key in used:
            continue
        keydefs_full.append('Keydef,,,{}'.format(actions[key]))
    return keydefs_full


def main():
    """test function
    """
    import pprint
    for item in ('/home/albert/.gimp-2.8/menurc',
                 '/home/albert/.config/banshee-1/gtk_accel_map',
                 '/home/albert/.dia/menurc'):
        stuff = read_keydefs_and_stuff(item)
        pprint.pprint(stuff)

if __name__ == "__main__":
    main()
