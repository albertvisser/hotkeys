"""unittests for ./editor/gui_wx.py
"""
from editor import gui_wx as testee


def _test_getbitmap(monkeypatch, capsys):
    """unittest for gui_wx.getbitmap
    """
    assert testee.getbitmap(data) == "expected_result"


class TestMyListCtrl:
    """unittest for gui_wx.MyListCtrl
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.MyListCtrl object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MyListCtrl.__init__ with args', args)
        monkeypatch.setattr(testee.MyListCtrl, '__init__', mock_init)
        testobj = testee.MyListCtrl()
        assert capsys.readouterr().out == 'called MyListCtrl.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for MyListCtrl.__init__
        """
        testobj = testee.MyListCtrl(parent, ID=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        assert capsys.readouterr().out == ("")


class TestDummyPage:
    """unittest for gui_wx.DummyPage
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.DummyPage object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called DummyPage.__init__ with args', args)
        monkeypatch.setattr(testee.DummyPage, '__init__', mock_init)
        testobj = testee.DummyPage()
        assert capsys.readouterr().out == 'called DummyPage.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for DummyPage.__init__
        """
        testobj = testee.DummyPage(parent, message)
        assert capsys.readouterr().out == ("")

    def _test_exit(self, monkeypatch, capsys):
        """unittest for DummyPage.exit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.exit() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestSingleDataInterface:
    """unittest for gui_wx.SingleDataInterface
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.SingleDataInterface object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SingleDataInterface.__init__ with args', args)
        monkeypatch.setattr(testee.SingleDataInterface, '__init__', mock_init)
        testobj = testee.SingleDataInterface()
        assert capsys.readouterr().out == 'called SingleDataInterface.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.__init__
        """
        testobj = testee.SingleDataInterface(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_setup_empty_screen(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.setup_empty_screen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_empty_screen(nodata, title) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setup_list(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.setup_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_list() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_extra_fields(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_extra_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_extra_fields() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_extrascreen_editable(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_extrascreen_editable
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_extrascreen_editable(switch) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_layout_extra_fields(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.layout_extra_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.layout_extra_fields(sizer) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_resize_if_necessary(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.resize_if_necessary
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.resize_if_necessary() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_item_deselected(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_item_deselected
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_item_deselected(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_item_selected(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_item_selected
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_item_selected(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_item_activated(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_item_activated
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_item_activated(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_update(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_update
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_update(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_delete(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_delete
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_delete(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_update_columns(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.update_columns
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.update_columns(oldcount, newcount) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_refresh_headers(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.refresh_headers
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.refresh_headers(headers) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_buttons(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.enable_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_buttons(state=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_GetListCtrl(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.GetListCtrl
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.GetListCtrl() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_GetSortImages(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.GetSortImages
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.GetSortImages() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_OnSortOrderChanged(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.OnSortOrderChanged
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.OnSortOrderChanged() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_title(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_title(title) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_list(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.clear_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_list() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_build_listitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.build_listitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_listitem(key) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_listitemtext(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_listitemtext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_listitemtext(itemlist, indx, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_listitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_listitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_listitem(itemlist) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_listselection(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_listselection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_listselection(pos) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_getfirstitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.getfirstitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getfirstitem() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_widget_text(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_widget_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_widget_text(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_save(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.enable_save
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_save(state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_choice_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_choice_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_choice_value(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_combobox_text(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_combobox_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_combobox_text(cb) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_combobox(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.init_combobox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_combobox(cb, choices=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_label_text(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_label_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_label_text(lbl, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_textfield_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_textfield_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_textfield_value(txt, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_check_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_check_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_check_value(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_checkbox_state(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_checkbox_state
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_state(cb) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_delete(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.enable_delete
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_delete(state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_itemdata(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_itemdata
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_itemdata(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_checkbox_state(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_checkbox_state
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_checkbox_state(cb, state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_combobox_string(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_combobox_string
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_combobox_string(cmb, value, valuelist) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_combobox_selection(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_combobox_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_combobox_selection(cmb) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selected_keydef(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_selected_keydef
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_keydef() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_keydef_position(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_keydef_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_keydef_position(item) == "expected_result"
        assert capsys.readouterr().out == ("")


class TestTabbedInterface:
    """unittest for gui_wx.TabbedInterface
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.TabbedInterface object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TabbedInterface.__init__ with args', args)
        monkeypatch.setattr(testee.TabbedInterface, '__init__', mock_init)
        testobj = testee.TabbedInterface()
        assert capsys.readouterr().out == 'called TabbedInterface.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for TabbedInterface.__init__
        """
        testobj = testee.TabbedInterface(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_setup_selector(self, monkeypatch, capsys):
        """unittest for TabbedInterface.setup_selector
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_selector() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setup_search(self, monkeypatch, capsys):
        """unittest for TabbedInterface.setup_search
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_search() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_subscreen(self, monkeypatch, capsys):
        """unittest for TabbedInterface.add_subscreen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_subscreen(win) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_to_selector(self, monkeypatch, capsys):
        """unittest for TabbedInterface.add_to_selector
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_to_selector(txt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_format_screen(self, monkeypatch, capsys):
        """unittest for TabbedInterface.format_screen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.format_screen() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setcaptions(self, monkeypatch, capsys):
        """unittest for TabbedInterface.setcaptions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setcaptions() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_after_changing_page(self, monkeypatch, capsys):
        """unittest for TabbedInterface.after_changing_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.after_changing_page(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_panel() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selected_tool(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_tool
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_tool() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_selected_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_selected_panel(indx) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_update_search(self, monkeypatch, capsys):
        """unittest for TabbedInterface.update_search
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.update_search(items) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_after_changing_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.after_changing_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.after_changing_text(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_search_col(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_search_col
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_search_col() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_find_items(self, monkeypatch, capsys):
        """unittest for TabbedInterface.find_items
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.find_items(page, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_search_buttons(self, monkeypatch, capsys):
        """unittest for TabbedInterface.init_search_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_search_buttons() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_selected_keydef_item(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_keydef_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_selected_keydef_item(page, index) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_search_buttons(self, monkeypatch, capsys):
        """unittest for TabbedInterface.enable_search_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_search_buttons(next=None, prev=None, filter=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_filter_state_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_filter_state_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_filter_state_text() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_search_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_search_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_search_text() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_found_keydef_position(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_found_keydef_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_found_keydef_position() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_search_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.enable_search_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_search_text(value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_found_keydef_position(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_found_keydef_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_found_keydef_position() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_filter_state_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_filter_state_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_filter_state_text(state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selected_index(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_index
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_index() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_selector(self, monkeypatch, capsys):
        """unittest for TabbedInterface.clear_selector
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_selector() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_tool(self, monkeypatch, capsys):
        """unittest for TabbedInterface.remove_tool
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_tool(indx, program, program_list) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_tool(self, monkeypatch, capsys):
        """unittest for TabbedInterface.add_tool
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_tool(program, win) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_new_selection(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_new_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_new_selection(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_selected_tool(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_tool
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_selected_tool(selection) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selected_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_panel() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_replace_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.replace_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.replace_panel(indx, win, newwin) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_panel_editable(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_panel_editable
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_panel_editable(test_redef) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_refresh_locs(self, monkeypatch, capsys):
        """unittest for TabbedInterface.refresh_locs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.refresh_locs(headers) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selected_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_text() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestGui:
    """unittest for gui_wx.Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Gui.__init__ with args', args)
        monkeypatch.setattr(testee.Gui, '__init__', mock_init)
        testobj = testee.Gui()
        assert capsys.readouterr().out == 'called Gui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for Gui.__init__
        """
        testobj = testee.Gui(parent=None)
        assert capsys.readouterr().out == ("")

    def _test_go(self, monkeypatch, capsys):
        """unittest for Gui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_close(self, monkeypatch, capsys):
        """unittest for Gui.close
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.close(event=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_window_title(self, monkeypatch, capsys):
        """unittest for Gui.set_window_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_window_title(title) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_statusbar_message(self, monkeypatch, capsys):
        """unittest for Gui.statusbar_message
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.statusbar_message(message) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setup_menu(self, monkeypatch, capsys):
        """unittest for Gui.setup_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_menu() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setcaptions(self, monkeypatch, capsys):
        """unittest for Gui.setcaptions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setcaptions() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_modify_menuitem(self, monkeypatch, capsys):
        """unittest for Gui.modify_menuitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.modify_menuitem(caption, setting) == "expected_result"
        assert capsys.readouterr().out == ("")
