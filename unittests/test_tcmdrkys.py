"""unittests for ./editor/plugins/tcmdrkys.py
"""
import pytest
from editor.plugins import tcmdrkys as testee


def test_read_lines(monkeypatch, capsys, tmp_path):
    """unittest for tcmdrkys.read_lines
    """
    fn = tmp_path / 'testfile'
    with pytest.raises(FileNotFoundError) as exc:
        testee.read_lines(str(fn))
    loc = testee.os.path.dirname(testee.__file__)
    assert str(exc.value) == f"[Errno 2] No such file or directory: '{loc}/tc_fallback/testfile'"
    assert capsys.readouterr().out == ""
    fn.write_text('xxx\nyyy\n')
    assert testee.read_lines(str(fn)) == ['xxx\n', 'yyy\n']
    assert capsys.readouterr().out == ("")


def _test_keymods_old(monkeypatch, capsys):
    """unittest for tcmdrkys.keymods_old
    """
    assert testee.keymods_old(x) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_keymods(monkeypatch, capsys):
    """unittest for tcmdrkys.keymods
    """
    assert testee.keymods(x) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_defaultcommands(monkeypatch, capsys):
    """unittest for tcmdrkys.defaultcommands
    """
    assert testee.defaultcommands(root) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_defaultkeys(monkeypatch, capsys):
    """unittest for tcmdrkys.defaultkeys
    """
    assert testee.defaultkeys(root) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_usercommands(monkeypatch, capsys):
    """unittest for tcmdrkys.usercommands
    """
    assert testee.usercommands(root) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_userkeys(monkeypatch, capsys):
    """unittest for tcmdrkys.userkeys
    """
    assert testee.userkeys(root) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_translate_keyname(monkeypatch, capsys):
    """unittest for tcmdrkys.translate_keyname
    """
    assert testee.translate_keyname(inp) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_build_data(monkeypatch, capsys):
    """unittest for tcmdrkys.build_data
    """
    assert testee.build_data(page, showinfo=True) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_add_extra_attributes(monkeypatch, capsys):
    """unittest for tcmdrkys.add_extra_attributes
    """
    assert testee.add_extra_attributes(win) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_get_frameheight(monkeypatch, capsys):
    """unittest for tcmdrkys.get_frameheight
    """
    assert testee.get_frameheight() == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_savekeys(monkeypatch, capsys):
    """unittest for tcmdrkys.savekeys
    """
    assert testee.savekeys(parent) == "expected_result"
    assert capsys.readouterr().out == ("")
