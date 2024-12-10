# -*- coding: utf-8 -*-
# @Author: Lakshita Jain
# @Date:   2023-10-03 15:01:18
# @Last Modified by:   Joanne Fan
# @Last Modified time: 2024-01-25 23:18:08
import pytest
from gailbot import GailBot
from gailbot.services.organizer.settings.objects.settingObject import SettingObject
from typing import List, Dict, Union, Tuple, Callable
from gailbot.plugins.suite import PluginSuite


def test_clear_workspace(gb: GailBot, APP_ROOT, TEST_ROOT, OUTPUT_ROOT):
    result = gb.clear_workspace()
    print(APP_ROOT, TEST_ROOT, OUTPUT_ROOT)
    assert result == True


def test_reset_workspace(gb: GailBot):
    result = gb.reset_workspace()
    assert result == True


###########################################################################
# Sources                                                                 #
###########################################################################


@pytest.mark.parametrize(
    "source, setting, overwrite, expected",
    [
        ("hello1", "SETTING_OBJECT_WHISPER", True, True),
        ("hello2", "SETTING_OBJECT_WHISPER", False, True),
        ("fake_source", "SETTING_OBJECT_WHISPER", True, False),
        ("fake_source", "SETTING_OBJECT_WHISPERX", False, False),
    ],
)
def test_apply_profile_to_source(
    gb_with_2_sources: GailBot,
    source: str,
    setting: SettingObject,
    overwrite: bool,
    expected: bool,
    request,
):
    """
    Purpose: test applying a setting profile to source
    Expected Output: True if applied, false if not
    """
    result = gb_with_2_sources.apply_profile_to_source(
        source, request.getfixturevalue(setting), overwrite
    )
    assert result == expected


@pytest.mark.parametrize(
    "source_path, output_dir, expected",
    [
        ("HELLO_1", "OUTPUT_ROOT", "hello1"),
        ("FAKE_SOURCE", "OUTPUT_ROOT", "nonexistent_source"),
        ("HELLO_2", "OUTPUT_ROOT", "hello2"),
    ],
)
def test_add_source(
    gb: GailBot, source_path: str, output_dir: str, expected: bool, request
):
    """
    Purpose: test adding a source
    Expected Output: source name if added, false if not
    """
    result = gb.add_source(
        request.getfixturevalue(source_path), request.getfixturevalue(output_dir)
    )
    assert result == expected
    assert isinstance(result, str or bool)


@pytest.mark.parametrize(
    "src_output_pairs, expected",
    [
        (["SOURCE_LIST", True]),
    ],
)
def test_add_sources(
    gb: GailBot, src_output_pairs: List[Tuple[str, str]], expected: bool, request
):
    """
    Purpose: test adding multiple sources
    Expected Output: True if all successfully added, false if not
    """
    result = gb.add_sources(request.getfixturevalue(src_output_pairs))
    assert result == expected


@pytest.mark.parametrize(
    "name, expected",
    [
        ("hello1", True),
        ("hello2", True),
        ("nonexistent_source", False),
    ],
)
def test_is_source(gb_with_2_sources: GailBot, name: str, expected: bool):
    """
    Purpose: test if a given source name is a source
    Expected Output: True if it is a soy=urce, false if not
    """
    result = gb_with_2_sources.is_source(name)
    assert result == expected


@pytest.mark.parametrize(
    "name",
    [
        ("hello1"),
    ],
)
def test_get_source_output_directory(gb_with_2_sources: GailBot, name: str):
    """
    Purpose: test getting output directory corresponding to a given source name
    Expected Output: string of output directory path
    """
    result = gb_with_2_sources.get_source_output_directory(name)
    print(result)


@pytest.mark.parametrize(
    "name, expected",
    [("hello1", True), ("hello2", True), ("nonexistent_source", False)],
)
def test_remove_source(gb_with_2_sources: GailBot, name: str, expected: str):
    """
    Purpose: test removing a source
    Expected Output: true if removed, false if not
    """
    result = gb_with_2_sources.remove_source(name)
    assert result == expected


@pytest.mark.parametrize(
    "source_names, expected",
    [
        (["hello1", "hello2"], True),
        (["source_3"], False),
        (["source_1", "source_4"], False),
    ],
)
def test_remove_sources(
    gb_with_2_sources: GailBot, source_names: List[str], expected: bool
):
    """
    Purpose: test removing multiple sources
    Expected Output: True if successfully removed, false if not
    """
    result = gb_with_2_sources.remove_sources(source_names)
    assert result == expected


@pytest.mark.parametrize(
    "source_name, expected",
    [
        ("hello1", "WHISPER_PROFILE"),
        ("hello2", "WHISPERX_PROFILE"),
        ("fake_source", False),
    ],
)
def test_get_source_profile_dict(
    gb_with_sources_and_settings: GailBot, source_name: str, expected, request
):
    """
    Purpose: test getting profile dict corresponding to a source
    Expected Output: profile dict
    """
    result = gb_with_sources_and_settings.get_source_profile_data(source_name)
    if result == False:
        assert result == expected
    else:
        assert result == request.getfixturevalue(expected)


def test_clear_source_memory(gb_with_2_sources: GailBot):
    """
    Purpose: test clearing all sources
    Expected Output: True
    """
    result = gb_with_2_sources.clear_source_memory()
    assert result == True


# TODO: function not in API

# def test_get_all_source_names(gb_with_2_sources: GailBot):
#     """
#     Purpose: test getting names of all sources
#     Expected Output: list of source names
#     """
#     result = gb_with_2_sources.get_all_source_names()
#     assert result == ["hello1", "hello2", "hello_video"]


@pytest.mark.parametrize(
    "source_name, expected",
    [
        ("hello1", "test"),
        ("hello2", "test2"),
        ("source_3", False),
        ("source_4", False),
    ],
)
def test_source_profile_name(
    gb_with_sources_and_settings: GailBot, source_name: str, expected
):
    """
    Purpose: test getting names of source profiles
    Expected Output: profile name
    """
    result = gb_with_sources_and_settings.source_profile_name(source_name)
    assert result == expected


###########################################################################
# Transcribe                                                              #
###########################################################################


@pytest.mark.parametrize(
    "source_name",
    [(["hello_video"]), (["hello1"]), (["hello2"])],
)
def test_transcribe(gb_with_sources_and_settings: GailBot, source_name: List[str]):
    """
    Purpose: Test trascribing a gailbot object
    """
    result = gb_with_sources_and_settings.transcribe(source_name)
    print(result)


###########################################################################
# Profile (Setting)                                                      #
###########################################################################


@pytest.mark.parametrize(
    "name, profile, overwrite, expected",
    [
        ("Whisper", "WHISPER_PROFILE", True, True),
        ("WhisperX", "WHISPERX_PROFILE", False, True),
    ],
)
def test_create_new_profile(
    gb_with_all_engines: GailBot,
    name: str,
    profile,
    overwrite: bool,
    expected: bool,
    request,
):
    """
    Purpose: Test creating a new profile
    """
    result = gb_with_all_engines.create_new_profile(
        name, request.getfixturevalue(profile), overwrite
    )
    assert result == expected


# TODO: function not in API

# @pytest.mark.parametrize(
#     "profile_name",
#     [
#         ("whisper"),
#     ],
# )
# def test_save_profile(gb_with_profile: GailBot, profile_name: str):
#     """
#     Purpose: Test saving a profile
#     """
#     result = gb_with_profile.save_profile(profile_name)
#     assert result != False


@pytest.mark.parametrize(
    "profile_name, expected",
    [
        ("whisper", "WHISPER_PROFILE"),
    ],
)
def test_get_profile_dict(
    gb_with_profile: GailBot, profile_name: str, request, expected
):
    """
    Purpose: Test getting profile dict
    """
    result = gb_with_profile.get_profile_data(profile_name)
    assert result == request.getfixturevalue(expected)


# TODO: function not in API

# def test_get_all_profiles_data(gb_with_profile: GailBot):
#     result = gb_with_profile.get_all_profiles_data()
#     print(result)


def test_all_profile_names(gb_with_profile: GailBot):
    result = gb_with_profile.all_profile_names()
    print(result)


@pytest.mark.parametrize(
    "old_name, new_name, expected",
    [
        ("whisper", "whisper_2", True),
        ("nonexistant_profile", "nothing", False),
    ],
)
def test_rename_profile(gb_with_profile, old_name, new_name, expected):
    print(gb_with_profile.all_profile_names())
    result = gb_with_profile.rename_profile(old_name, new_name)
    if expected == True:
        gb_with_profile.rename_profile(new_name, old_name)
    assert result == expected


@pytest.mark.parametrize(
    "profile_name, new_profile, expected",
    [
        ("whisper", "WHISPERX_PROFILE", True),
        ("nonexistant_profile", "WHISPER_PROFILE", False),
    ],
)
def test_update_profile(gb: GailBot, profile_name: str, new_profile, expected, request):
    result = gb.update_profile(profile_name, request.getfixturevalue(new_profile))
    assert result == expected


# TODO: function not in API

# @pytest.mark.parametrize(
#     "profile_name, expected",
#     [
#         ("whisper", {"HiLabSuite": {"OutputFileManager": [] ,
#                             "SyllableRatePlugin": [ "OutputFileManager",]}}),
#         ("nonexistant_profile", False),
#     ],
# )
# def test_get_plugin_profile(gb_with_profile: GailBot, profile_name: str, expected):
#     result = gb_with_profile.get_plugin_profile(profile_name)
#     assert result == expected


@pytest.mark.parametrize(
    "profile_name, expected",
    [
        ("whisper", True),
        ("nonexistant_profile", False),
    ],
)
def test_remove_profile(gb_with_profile: GailBot, profile_name: str, expected: bool):
    result = gb_with_profile.remove_profile(profile_name)
    assert result == expected


# TODO: function not in API

# @pytest.mark.parametrize(
#     "profile_names, expected",
#     [
#         (["whisper"], True),
#         (["whisper", "nonexistant_profile"], False),
#     ],
# )
# def test_remove_multiple_profiles(
#     gb_with_profile: GailBot, profile_names: List[str], expected: bool
# ):
#     result = gb_with_profile.remove_multiple_profiles(profile_names)
#     assert result == expected


@pytest.mark.parametrize(
    "profile_name, expected",
    [
        ("whisper", True),
        ("nonexistent_profile", False),
    ],
)
def test_is_profile(gb_with_profile: GailBot, profile_name: str, expected: bool):
    result = gb_with_profile.is_profile(profile_name)
    assert result == expected


@pytest.mark.parametrize(
    "source, profile_name, expected",
    [
        ("HELLO_1", "whisper", True),
        ("HELLO_1", "nonexistent_profile", True),
    ],
)
def test_apply_profile_to_source2(
    gb_with_source: GailBot, source: str, profile_name: str, expected: bool, request
):
    result = gb_with_source.apply_profile_to_source(
        request.getfixturevalue(source), profile_name
    )
    assert result == expected


@pytest.mark.parametrize(
    "sources, profile_name, expected",
    [
        (["hello1"], "whisper", True),
        (["hello1", "hello2"], "nonexistent_profile", True),
    ],
)
def test_apply_profile_to_sources(
    gb_with_2_sources: GailBot, sources: List[str], profile_name: str, expected: bool
):
    result = gb_with_2_sources.apply_profile_to_sources(sources, profile_name)
    assert result == expected


@pytest.mark.parametrize(
    "profile_name, expected",
    [
        ("Default", True),
        ("Profile2", False),
    ],
)
def test_is_profile_in_use(gb_with_sources_and_profile, profile_name, expected):
    result = gb_with_sources_and_profile.is_profile_in_use(profile_name)
    assert result == expected


def test_default_profile_name(gb_with_2_sources: GailBot):
    result = gb_with_2_sources.default_profile_name()
    assert result == "Default"


# TODO: function not in API

# @pytest.mark.parametrize(
#     "profile_name, expected",
#     [
#         ("whisper", True),
#         ("Profile2", False),
#     ],
# )
# def test_set_default_profile(
#     gb_with_profile: GailBot, profile_name: str, expected: bool
# ):
#     result = gb_with_profile.set_default_profile(profile_name)
#     assert result == expected


##########################################################################
# Plugin Suite                                                            #
##########################################################################


@pytest.mark.parametrize(
    "plugin_sources, expected",
    [
        ("PLUGIN_SUITE", None),
    ],
)
def test_register_plugin_suite(
    gb: GailBot, plugin_sources: str, expected: List[str], request
):
    result = gb.register_plugin_suite(request.getfixturevalue(plugin_sources))
    assert result == expected


# TODO: function not in API

# @pytest.mark.parametrize(
#     "suite_name",
#     [
#         ("HiLabSuite"),
#     ],
# )
# def test_get_plugin_suite(gb_with_suite: GailBot, suite_name: str):
#     result = gb_with_suite.get_plugin_suite(suite_name)
#     assert isinstance(result, PluginSuite)


@pytest.mark.parametrize(
    "suite_name, expected",
    [
        ("HiLabSuite", True),
        ("fakeSuite", False),
    ],
)
def test_is_plugin_suite(gb_with_suite: GailBot, suite_name: str, expected: bool):
    result = gb_with_suite.is_plugin_suite(suite_name)
    assert result == expected


@pytest.mark.parametrize(
    "suite_name, expected",
    [
        ("HiLabSuite", True),
    ],
)
def test_remove_plugin_suite(gb_with_suite: GailBot, suite_name: str, expected: bool):
    result = gb_with_suite.remove_plugin_suite(suite_name)
    assert result == expected


def test_get_all_plugin_suites(gb_with_suite: GailBot):
    result = gb_with_suite.get_all_plugin_suites()
    assert list(result) == [
        "HiLabSuite",
    ]


def test_get_plugin_suite_metadata(gb_with_suite: GailBot):
    result = gb_with_suite.get_plugin_suite_metadata("HiLabSuite")
    assert result == {
        "Author": "hilab",
        "Email": "hilab.tufts.edu",
        "Version": "v.0.1a",
    }


def test_get_plugin_suite_dependency_grapha(gb_with_suite: GailBot):
    result = gb_with_suite.get_plugin_suite_dependency_graph("HiLabSuite")
    print(result)


def test_get_plugin_suite_documentation_path(gb_with_suite: GailBot):
    result = gb_with_suite.get_plugin_suite_documentation_path("HiLabSuite")
    print(result)


@pytest.mark.parametrize(
    "suite_name, expected",
    [
        ("HiLabSuite", False),
    ],
)
def test_is_suite_in_use(gb_with_suite: GailBot, suite_name: str, expected: bool):
    result = gb_with_suite.is_suite_in_use(suite_name)
    assert result == expected


@pytest.mark.parametrize(
    "suite_name, expected",
    [
        ("HiLabSuite", True),
    ],
)
def test_is_official_suite(gb_with_suite: GailBot, suite_name: str, expected: bool):
    result = gb_with_suite.is_official_suite(suite_name)
    assert result == expected


@pytest.mark.parametrize(
    "suite_name",
    [("MySuite",)],
)
def test_get_suite_path(gb_with_suite: GailBot, suite_name: str):
    result = gb_with_suite.get_suite_path(suite_name)
    print(result)


# ###########################################################################
# # Engines                                                                 #
# ###########################################################################


def test_available_engines(gb_with_all_engines: GailBot):
    result = gb_with_all_engines.available_engines()
    print(result)


@pytest.mark.parametrize(
    "name, setting, overwrite, expected",
    [
        ("WHISPER_NAME", "WHISPER_SETTING", True, True),
        ("WHISPERX_NAME", "WHISPERX_SETTING", True, True),
        ("GOOGLE_NAME", "GOOGLE_SETTING", True, True),
        ("WATSON_NAME", "WATSON_SETTING", True, True),
    ],
)
def test_add_new_engine(
    name: str, setting: Dict, overwrite: bool, expected: bool, request, gb: GailBot
):
    result = gb.add_new_engine(
        request.getfixturevalue(name), request.getfixturevalue(setting), overwrite
    )
    assert result == expected


@pytest.mark.parametrize(
    "name, expected",
    [
        ("whisper", True),
        ("engine2", False),
    ],
)
def test_remove_engine_setting(name: str, expected: bool, gb_with_all_engines: GailBot):
    result = gb_with_all_engines.remove_engine(name)
    assert result == expected


@pytest.mark.parametrize(
    "name, setting, expected",
    [
        ("WHISPER_NAME", "WHISPER_SETTING", True),
        ("WHISPERX_NAME", "WHISPERX_SETTING", True),
        ("GOOGLE_NAME", "GOOGLE_SETTING", True),
        ("WATSON_NAME", "WATSON_SETTING", True),
    ],
)
def test_update_engine_setting(
    name: str, setting: Dict, expected: bool, gb_with_all_engines: GailBot, request
):
    result = gb_with_all_engines.update_engine(
        request.getfixturevalue(name), request.getfixturevalue(setting)
    )
    assert result == expected


@pytest.mark.parametrize(
    "name, expected",
    [
        ("whisper", "WHISPER_SETTING"),
        ("engine2", False),
    ],
)
def test_get_engine_data(name: str, expected, gb_with_all_engines: GailBot, request):
    result = gb_with_all_engines.get_engine_data(name)
    if expected != False:
        assert result == request.getfixturevalue(expected)
    else:
        assert result == expected


# TODO: Function not in API
#
# @pytest.mark.parametrize(
#     "name, expected",
#     [
#         ("whisper", True),
#         ("whisperX", True),
#     ],
# )
# def test_is_engine_setting_in_use(
#     name: str, expected: bool, gb_with_sources_and_settings: GailBot
# ):
#     result = gb_with_sources_and_settings.is_engine_setting_in_use(name)
#     assert result == expected


@pytest.mark.parametrize(
    "name, expected",
    [
        ("whisper", True),
        ("engine2", False),
    ],
)
def test_is_engine(gb_with_all_engines: GailBot, name: str, expected: bool):
    result = gb_with_all_engines.is_engine(name)
    assert result == expected


def test_default_engine_name(gb_with_all_engines: GailBot):
    result = gb_with_all_engines.default_engine_name()
    print(result)
