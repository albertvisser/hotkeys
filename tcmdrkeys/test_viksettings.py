import vikeys

def test_VIKSettings(pad):
    ini = vikeys.VIKSettings(pad)
    print ini.__dict__

def test_VIKSettings_write(pad):
    ini = vikeys.VIKSettings(pad)
    ini.pad = 'xxxx'
    ini.lang = 'yyyyy'
    ini.write(pad)

if __name__ == '__main__':
    test_VIKSettings('/home/albert/tcmdrkeys/vikey_config.py')
    test_VIKSettings_write('/home/albert/tcmdrkeys/vikey_config.py')
    test_VIKSettings('/home/albert/tcmdrkeys/vikey_config.py')
