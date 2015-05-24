sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import editor.plugin_examples.vikeys as vikeys

def test_VIKSettings(pad):
    ini = vikeys.VIKSettings(pad)
    print ini.__dict__

def test_VIKSettings_write(pad):
    ini = vikeys.VIKSettings(pad)
    ini.pad = 'xxxx'
    ini.lang = 'yyyyy'
    ini.write(pad)

if __name__ == '__main__':
    fn = '/home/albert/tcmdrkeys/vikey_config.py'
    test_VIKSettings(fn)
    test_VIKSettings_write(fn)
    test_VIKSettings(fn)
