# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-03-30 11:57:13
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-05-10 13:37:15
import pytest
from gailbot import GailBot, ProfileSetting
from gailbot.sourceManager.watcher import Watcher
from test.test_data import TestData
from copy import deepcopy


class TestWatcher(Watcher):
    def watch(self, progress: str):
        print(progress)


GOOGLE_API = "/Users/yike/Desktop/gbtest/input/google-api.json"
WHISPERX_ENGINE = "whisperx engine pipeline test"
WHISPERX_PROFILE = "whisperx profile pipeline test"

GOOGLE_ENGINE = "google engine pipeline test"
GOOGLE_PROFILE = "google profile pipeline test"

WHISPER_ENGINE = "whisper engine pipeline test"
WHISPER_PROFILE = "whisper profile pipeline test"

WATSON_ENGINE = "watson engine pipeline test"
WATSON_PROFILE = "watson profile pipeline test"

PLUGIN_SETTING = {"HiLabSuite": ["ChatPlugin", "TextPlugin", "CSVPlugin", "XmlPlugin"]}


@pytest.fixture(scope="module", autouse=True)
def gb():
    gailbot = GailBot()
    # add whisperX profile
    if not gailbot.is_engine(WHISPERX_ENGINE):
        gailbot.add_engine(WHISPERX_ENGINE, {"engine": "whisperX", "language": "en"})
    if not gailbot.is_profile(WHISPERX_PROFILE):
        gailbot.create_profile(
            WHISPERX_PROFILE,
            ProfileSetting(
                engine_setting_name=WHISPERX_ENGINE,
                plugin_suite_setting=deepcopy(PLUGIN_SETTING),
            ),
        )

    # add whisper profile
    whisper_engine_setting = {
        "engine": "whisper",
        "language": "English",
        "speaker_detect": False,
    }
    if not gailbot.is_engine(WHISPER_ENGINE):
        gailbot.add_engine(name=WHISPER_ENGINE, setting=whisper_engine_setting)
    if not gailbot.is_profile(WHISPER_PROFILE):
        gailbot.create_profile(
            name=WHISPER_PROFILE,
            setting=ProfileSetting(
                engine_setting_name=WHISPER_ENGINE,
                plugin_suite_setting=deepcopy(PLUGIN_SETTING),
            ),
        )

    # add google profile
    google_engine_setting = {"engine": "google", "google_api_key": GOOGLE_API}
    if not gailbot.is_engine(GOOGLE_ENGINE):
        assert gailbot.add_engine(name=GOOGLE_ENGINE, setting=google_engine_setting)
    if not gailbot.is_profile(GOOGLE_PROFILE):
        gailbot.create_profile(
            name=GOOGLE_PROFILE,
            setting=ProfileSetting(
                engine_setting_name=GOOGLE_ENGINE,
                plugin_suite_setting=deepcopy(PLUGIN_SETTING),
            ),
        )

    # add watson profile
    WATSON_API_KEY = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
    WATSON_REGION = "dallas"
    WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"
    watson_engine_setting = {
        "engine": "watson",
        "apikey": WATSON_API_KEY,
        "region": WATSON_REGION,
        "base_model": WATSON_BASE_LANG_MODEL,
    }

    if not gailbot.is_engine(WATSON_ENGINE):
        gailbot.add_engine(name=WATSON_ENGINE, setting=watson_engine_setting)
    if not gailbot.is_profile(WATSON_PROFILE):
        gailbot.create_profile(
            name=WATSON_PROFILE,
            setting=ProfileSetting(
                engine_setting_name=WATSON_ENGINE,
                plugin_suite_setting=deepcopy(PLUGIN_SETTING),
            ),
        )

    return gailbot


@pytest.mark.parametrize(
    "profile", [WATSON_PROFILE, WHISPER_PROFILE, WHISPERX_PROFILE, GOOGLE_PROFILE]
)
def test_hello(gb: GailBot, profile: str):
    ids = [gb.add_source(TestData.hello, TestData.OUTPUT) for _ in range(4)]
    for source_id in ids:
        gb.apply_profile_to_source(source_id, profile)
        gb.add_progress_watcher(source_id, TestWatcher())
    result = gb.transcribe()
    assert result.success_output and not (result.failure or result.invalid)


@pytest.mark.parametrize(
    "profile", [WATSON_PROFILE, WHISPER_PROFILE, WHISPERX_PROFILE, GOOGLE_PROFILE]
)
def test_test2ab(gb: GailBot, profile: str):
    ids = [gb.add_source(TestData.test2ab, TestData.OUTPUT) for _ in range(2)]
    for source_id in ids:
        gb.apply_profile_to_source(source_id, profile)
        gb.add_progress_watcher(source_id, TestWatcher())
    result = gb.transcribe()
    assert result.success_output and not (result.failure or result.invalid)


@pytest.mark.parametrize(
    "profile", [WATSON_PROFILE, WHISPER_PROFILE, WHISPERX_PROFILE, GOOGLE_PROFILE]
)
def test_callhome_small(gb: GailBot, profile: str):
    ids = [gb.add_source(TestData.callhome_small, TestData.OUTPUT) for _ in range(2)]
    for source_id in ids:
        gb.apply_profile_to_source(source_id, profile)
        gb.add_progress_watcher(source_id, TestWatcher())
    result = gb.transcribe()
    assert result.success_output and not (result.failure or result.invalid)


def test_previously_transcribed(gb: GailBot):
    ids = [
        gb.add_source(TestData.test2ab_transcribed, TestData.OUTPUT),
        gb.add_source(TestData.test0638_transcribed, TestData.OUTPUT),
    ]
    for source_id in ids:
        gb.add_progress_watcher(source_id, TestWatcher())
    result = gb.transcribe()
    assert result.success_output and not (result.failure or result.invalid)


@pytest.mark.parametrize("path", [TestData.test_mp3])
def test_mp3(gb: GailBot, path):
    ids = [
        gb.add_source(path, TestData.OUTPUT),
        gb.add_source(path, TestData.OUTPUT),
    ]
    for source_id in ids:
        gb.add_progress_watcher(source_id, TestWatcher())
    result = gb.transcribe()
    assert result.success_output and not (result.failure or result.invalid)


def test_whisper_whisperX(gb: GailBot):
    ids = [
        gb.add_source(TestData.hello, TestData.OUTPUT),
        gb.add_source(TestData.hello, TestData.OUTPUT),
    ]

    for source_id in ids:
        gb.add_progress_watcher(source_id, TestWatcher())

    gb.apply_profile_to_source(ids[0], WHISPER_PROFILE)
    gb.apply_profile_to_source(ids[1], WHISPERX_PROFILE)
    result = gb.transcribe()
    assert result.success_output
    assert not (result.failure or result.invalid)
    print(result)
