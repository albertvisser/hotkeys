import sys
## sys.path.append('/home/albert/projects/hotkeys')
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pprint
import tarfile
import editor.scikeys as scikeys

def test_read_commands():
    menu_commands, command_list = scikeys.read_commands(
        '/usr/share/scite/CommandValues.html')

    # dict: map command naam op omschrijving
    with open('menu_commands.txt', 'w') as _out:
        for key, item in menu_commands.items():
            print(key, ':', item, file=_out)
    # dict: map command nummer op (naam, omschrijving)
    with open('command_list.txt', 'w') as _out:
        for key, item in command_list.items():
            print(key, ':', item, file=_out)

def test_read_docs():
    keydefs = scikeys.read_docs('/usr/share/scite/SciTEDoc.html')

    # dict: map keycombo op (?, omschrijving)
    # nee, list of (key, modifiers, omschrijving)
    with open('nonmenu_keydefs.txt', 'w') as _out:
        for item in keydefs:
            print(item, file=_out)

def test_read_source():
    # first unpack source file to /tmp
    data = tarfile.open('/home/albert/Downloads/SciTE/scite353.tgz')
    data.extractall(path='/tmp')
    # list of (key, modifiers, command)
    data = scikeys.read_source_gtk('/tmp/scite/gtk/SciTEGTK.cxx')
    with open('menu_keys_gtk.txt', 'w') as _out:
        for item in data:
            print(item, file=_out)
    data = scikeys.read_source_win('/tmp/scite/win32/SciTERes.rc')
    with open('menu_keys_win.txt', 'w') as _out:
        for item in data:
            print(item, file=_out)

def test_nicefy():
    print(scikeys.nicefy('X'))
    print(scikeys.nicefy('<alt>Q'))
    print(scikeys.nicefy('<ctrl><shift>PgUp'))
    print(scikeys.nicefy('<control><shift>PgUp'))
    print(scikeys.nicefy('<control><alt><shift>Delete'))

def test_properties(from_, type_):
    props = scikeys.PropertiesFile(from_)
    props.read_props()
    props.get_keydef_props()
    # list of (key, modifiers, context, platform, omschrijving_of_commando) items
    with open('{}_keydefs.txt'.format(type_), 'w') as _out:
        for item in props.data:
            print(item, file=_out)

def test_buildcsv():
    scikeys.buildcsv(csvfile=os.path.join(os.path.dirname(__file__),
        ('test_scikeys.csv')))
    ## scikeys.buildcsv()

if __name__ == '__main__':
    ## test_read_commands()
    ## test_read_docs()
    ## test_read_source()
    ## test_properties('test/test_multiline.properties', 'global')
    ## test_properties('test/test_menu_languages.properties', 'global')
    ## test_properties('/usr/share/scite/SciTEGlobal.properties', 'global')
    ## test_properties('/home/albert/SciTEUser.properties', 'user')
    ## test_properties('/home/albert/.SciTEUser.properties', 'user')
    test_buildcsv()
