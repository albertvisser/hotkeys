"""unittests for ./editor/plugins/gtkaccel_keys_wx.py
"""
import types
from editor.plugins import gtkaccel_keys_wx as wxtestee
from mockgui import mockwxwidgets as mockwx


class _TestAccelCompleteDialog:
    """unittests for gtkaccel_keys_wx.AccelCompleteDialog object
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gtkaccel_keys_wx.AccelCompleteDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """

    def test_read_data(self, monkeypatch, capsys):
        """unittest for AccelCompleteDialog.read_data
        """

    def test_build_table(self, monkeypatch, capsys):
        """unittest for AccelCompleteDialog.read_data
        """
