keydef_id = 'gtk_accel_path'
conversion_map = (
    ('bracketright', ']'),
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
    ('Subtract', '-')
    )

def convert_key(inp):
    return out

def build_mods(inp):
    return out

def read_keydefs(filename):
    keydefs = []
    actions, others = {}, []
    new_id = 0
    with open(filename) as _in:
        for line in _in:
            coloned = False
            if keydef_id in line:
                if line.startswith(';'):
                    coloned = True  # don't know what this means
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
                        if '<Primary' in test: mods += 'C'
                        if '<Alt' in test: mods += 'A'
                        if '<Shift' in test: mods += 'S'
                    ## print(test)
                    keydefs.append((key, mods, new_id))
    return keydefs, actions, others

def build_extended_keydefs(keydefs, actions):
    keydefs_full, used = [], {}
    for key, mods, command in keydefs:
        keydefs_full.append('Keydef,{},{},{}'.format(key, mods, actions[command]))
        used[command] = '' # can't pop these from actions because the may have been reused
    for key in actions:
        if key in used: continue
        keydefs_full.append('Keydef,,,{}'.format(actions[key]))
    return keydefs_full

def main():
    for item in (
            '/home/albert/.gimp-2.8/menurc',
            ## '/home/albert/.config/banshee-1/gtk_accel_map'
            ## '/home/albert/.dia/menurc',
            ):
        keydefs, actions, other = read_keydefs(item)
        print(keydefs)
        print(actions)
        print(other)
        keydefs_full = build_extended_keydefs(keydefs, actions)
        for item in keydefs_full:
            print(item)

if __name__ == "__main__":
    main()
