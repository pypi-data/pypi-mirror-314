# -*- coding: utf-8 -*-
# @Author: Vivian Li 
# @Date:   2024-02-23 18:03:11
# @Last Modified by:   Vivian Li 
# @Last Modified time: 2024-02-25 16:19:10
from gailbot import ProfileSetting
from gailbot.shared.exception.serviceException import DuplicateProfile
from gailbot import GailBot


def test_crete_duplicate_profile():
    GailBot().reset_workspace()
    gb = GailBot()
    gb.create_profile(name="test",
                      setting=ProfileSetting(engine_setting_name=gb.default_engine_name(), plugin_suite_setting={}))
    assert gb.is_profile("test")
    assert gb.get_profile_setting("test").engine_setting_name == gb.default_engine_name()

    try:
        gb.create_profile(name="test",
                          setting=ProfileSetting(engine_setting_name=gb.default_engine_name(), plugin_suite_setting={}))
        assert False
    except Exception as e:
        assert isinstance(e, DuplicateProfile)


def test_update_profile():
    GailBot().reset_workspace()
    gb = GailBot()
    gb.create_profile(name="test",
                      setting=ProfileSetting(engine_setting_name=gb.default_engine_name(), plugin_suite_setting={}))
    assert gb.is_profile("test")
    assert gb.get_profile_setting("test").engine_setting_name == gb.default_engine_name()
    assert not gb.get_profile_setting("test").plugin_suite_setting.keys()

    gb.update_profile(profile_name="test",
                      new_setting=gb.get_profile_setting(gb.profile_manager.default_profile_name))
    assert gb.get_profile_setting("test").plugin_suite_setting.keys()


