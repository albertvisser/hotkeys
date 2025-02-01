"""unittests for ./editor/shared.py
"""
"""HotKeys: non-gui and csv related functions
"""
import pytest
import types
import editor.shared as testee


def test_log(monkeypatch, capsys):
    """unittest for shared.log
    """
    def mock_info(arg):
        """stub
        """
        print(f'called logging.info with arg `{arg}`')
    monkeypatch.setattr(testee.logging, 'info', mock_info)
    monkeypatch.setattr(testee, 'DO_LOGGING', True)
    testee.log('information')
    assert capsys.readouterr().out == 'called logging.info with arg `information`\n'
    testee.log('information', always=True)
    assert capsys.readouterr().out == 'called logging.info with arg `information`\n'
    monkeypatch.setattr(testee, 'DO_LOGGING', False)
    testee.log('information')
    assert capsys.readouterr().out == ''
    testee.log('information', always=True)
    assert capsys.readouterr().out == 'called logging.info with arg `information`\n'


def test_log_exc(monkeypatch, capsys):
    """unittest for shared.log_exc
    """
    def mock_exception(arg):
        """stub
        """
        print(f'called logging.exception with arg `{arg}`')
    monkeypatch.setattr(testee.logging, 'exception', mock_exception)
    monkeypatch.setattr(testee, 'DO_LOGGING', True)
    testee.log_exc(message='error')
    assert capsys.readouterr().out == 'called logging.exception with arg `error`\n'
    monkeypatch.setattr(testee, 'DO_LOGGING', False)
    testee.log_exc(message='error')
    assert capsys.readouterr().out == 'called logging.exception with arg `error`\n'


def test_save_log(monkeypatch, capsys):
    """unittest for shared.save_log
    """
    def mock_glob(path, pattern):
        """stub
        """
        print('called path.glob for pattern `{pattern}` in `{path}`')
        return []
    def mock_glob_1(path, pattern):
        """stub
        """
        fn = str(path / pattern[:-1])
        return [testee.pathlib.Path(fn)]
    def mock_glob_more(path, pattern):
        """stub
        """
        fn = str(path / pattern[:-1])
        return [testee.pathlib.Path(fn + '.01'), testee.pathlib.Path(fn),
                testee.pathlib.Path(fn + '.02')]
    def mock_rename(old, new):
        """stub
        """
        print(f'called path.rename from `{old}` to `{new}`')
    monkeypatch.setattr(testee.pathlib.Path, 'rename', mock_rename)
    # monkeypatch.setattr(testee.pathlib.Path, 'glob', mock_glob)
    # testee.save_log()
    # assert capsys.readouterr().out == ''
    monkeypatch.setattr(testee.pathlib.Path, 'glob', mock_glob_1)
    testee.save_log()
    assert capsys.readouterr().out == ('called path.rename from `/tmp/logs/hotkeys.log`'
                                       ' to `/tmp/logs/hotkeys.log.00`\n')
    monkeypatch.setattr(testee.pathlib.Path, 'glob', mock_glob_more)
    # breakpoint()
    testee.save_log()
    assert capsys.readouterr().out == ('called path.rename from `/tmp/logs/hotkeys.log`'
                                       ' to `/tmp/logs/hotkeys.log.03`\n')


def test_get_text(monkeypatch, capsys):
    """unittest for shared.get_text
    """
    captionshaver = types.SimpleNamespace(captions={'m_id': 'hello / world', 'I_NOMSG': 'gargl'})
    win = types.SimpleNamespace(editor=captionshaver)
    assert testee.get_text(win, message_id='m_id') == "hello\nworld"
    assert testee.get_text(win, text='{} nice {}', args=('my', 'args')) == "my nice args"
    with pytest.raises(ValueError) as exc:
        testee.get_text(win, args=('my', 'args'))
        assert str(exc.value) == "gargl"
    win = types.SimpleNamespace(master=captionshaver)
    assert testee.get_text(win, message_id='m_id') == "hello\nworld"
    win = captionshaver
    assert testee.get_text(win, message_id='m_id') == "hello\nworld"
    win = 'not a window'
    with pytest.raises(AttributeError) as exc:
        testee.get_text(win, message_id='m_id')
        assert str(exc.value) == "AttributeError: 'str' object has no attribute 'captions'"


def test_get_open_title(monkeypatch, capsys):
    """unittest for shared.get_open_title
    """
    def mock_get(*args):
        """stub
        """
        print('called get_text with args', args)
        return 'text'
    monkeypatch.setattr(testee, 'get_text', mock_get)
    assert testee.get_open_title('win', 'message_id', '') == 'text'
    assert capsys.readouterr().out == "called get_text with args ('win', 'message_id')\n"
    assert testee.get_open_title('win', 'message_id', 'oms') == 'text - oms'
    assert capsys.readouterr().out == "called get_text with args ('win', 'message_id')\n"


def test_get_title(monkeypatch, capsys):
    """unittest for shared.get_title
    """
    titlehaver = types.SimpleNamespace(title='mytitle')
    assert testee.get_title(titlehaver) == 'mytitle'
    assert testee.get_title(types.SimpleNamespace(editor=titlehaver)) == 'mytitle'
    assert testee.get_title(types.SimpleNamespace(master=titlehaver)) == 'mytitle'
    with pytest.raises(AttributeError):
        assert testee.get_title(types.Simplenamespace()) == ''
