import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import editor.dckeys

def test_buildcsv():
    editor.dckeys.buildcsv(csvfile='test_dckeys.csv')

def test_parse_keytext():
    test = editor.dckeys.parse_keytext('A')
    assert test == [('A', '')]
    test = editor.dckeys.parse_keytext('Ctrl+A')
    assert test == [('A', 'C')]
    test = editor.dckeys.parse_keytext('Shift+Ctrl+A')
    assert test == [('A', 'CS')]
    test = editor.dckeys.parse_keytext('+')
    assert test == [('+', '')]
    test = editor.dckeys.parse_keytext('Num +')
    assert test == [('Num +', '')]
    test = editor.dckeys.parse_keytext('Ctrl++')
    assert test == [('+', 'C')]
    test = editor.dckeys.parse_keytext('Shift+Ctrl++')
    assert test == [('+', 'CS')]
    test = editor.dckeys.parse_keytext('Shift+Ctrl+Num +')
    assert test == [('Num +', 'CS')]
    test = editor.dckeys.parse_keytext('Ctrl+A, F1')
    assert test == [('A', 'C'), ('F1', '')]
    test = editor.dckeys.parse_keytext('Ctrl+A, Num +')
    assert test == [('A', 'C'), ('Num +', '')]
    test = editor.dckeys.parse_keytext('Ctrl+A, Ctrl++')
    assert test == [('A', 'C'), ('+', 'C')]
    test = editor.dckeys.parse_keytext(',')
    assert test == [(',', '')]
    test = editor.dckeys.parse_keytext('","')
    assert test == [('","', '')]
    test = editor.dckeys.parse_keytext('Ctrl+,')
    assert test == [(',', 'C')]
    test = editor.dckeys.parse_keytext('Ctrl+","')
    assert test == [('","', 'C')]
    test = editor.dckeys.parse_keytext(',, A')
    assert test == [(',', ''), ('A', '')]
    ## test == editor.dckeys.parse_keytext(', , A') # improbable
    ## assert test ==
    test = editor.dckeys.parse_keytext('",", A')
    assert test == [('","', ''), ('A', '')]
    test = editor.dckeys.parse_keytext('+, A')
    assert test == [('+', ''), ('A', '')]
    test = editor.dckeys.parse_keytext('+, ,')
    assert test == [('+', ''), (',', '')]

if __name__ == '__main__':
    test_buildcsv()
    ## test_parse_keytext()
