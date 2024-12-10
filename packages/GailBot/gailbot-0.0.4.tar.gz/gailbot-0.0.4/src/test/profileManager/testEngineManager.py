# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-26 16:16:54
# @Last Modified by:   Joanne Fan
# @Last Modified time: 2024-02-10 21:01:46
import pytest
import os

from gailbot.engineManager.engineManager import EngineManager
from gailbot.shared.exception.serviceException import EngineNotFound, DuplicateProfile, RemoveDefaultEngine
from gailbot.shared.utils.general import is_file


@pytest.fixture()
def engineWorkspace(tmp_path):
    temp_ws = tmp_path / "temp_workspace"
    temp_ws.mkdir()
    return temp_ws


@pytest.fixture()
def eManager(engineWorkspace):
    return EngineManager(engineWorkspace)


@pytest.fixture()
def eManagerWhisperx(eManager, WHISPERX_SETTING):
    eManager.add_engine("test_whisperX_engine", WHISPERX_SETTING)
    return eManager


def test_remove_default_engine(eManager):
    with pytest.raises(RemoveDefaultEngine):
        eManager.remove_engine(eManager.default_name)


def test_add_engine(eManager, WATSON_SETTING, WHISPERX_SETTING):
    assert eManager.add_engine("test_watson_engine", WATSON_SETTING)
    assert eManager.is_engine("test_watson_engine")

    assert eManager.add_engine("test_whisperX_engine", WHISPERX_SETTING)
    assert eManager.is_engine("test_whisperX_engine")

    eManagerB = EngineManager(eManager.workspace)
    assert eManagerB.is_engine("test_watson_engine")
    assert eManagerB.is_engine("test_whisperX_engine")


def test_add_engine_fail(eManagerWhisperx, WHISPERX_SETTING):
    with pytest.raises(DuplicateProfile):
        eManagerWhisperx.add_engine("test_whisperX_engine", WHISPERX_SETTING)


def test_remove_engine(eManagerWhisperx):
    engine_name = "test_whisperX_engine"
    eManagerWhisperx.remove_engine(engine_name)

    assert not eManagerWhisperx.is_engine(engine_name)
    assert engine_name not in eManagerWhisperx.available_engines

    path = os.path.join(eManagerWhisperx.workspace, f"{engine_name}.toml")
    assert not is_file(path)


def test_remove_engine_fail(eManager):
    with pytest.raises(EngineNotFound):
        eManager.remove_engine("test_whisperX_engine")


def test_get_engine_provider(eManager):
    provider = eManager.get_engine_provider(eManager.default_name)
    assert provider.engine_data() == eManager.default_data


def test_get_engine_provider_fail(eManager):
    with pytest.raises(EngineNotFound):
        engine_provider = eManager.get_engine_provider("test_whisperX_engine")


def test_get_engine_data(eManagerWhisperx, WHISPERX_SETTING):
    # Default engine data
    engine_data = eManagerWhisperx.get_engine_setting(eManagerWhisperx.default_name)
    assert engine_data == eManagerWhisperx.default_data

    # WhisperX engine data
    engine_data = eManagerWhisperx.get_engine_setting("test_whisperX_engine")
    assert engine_data == WHISPERX_SETTING


def test_get_engine_data_fail(eManager):
    with pytest.raises(EngineNotFound):
        engine_data = eManager.get_engine_setting("test_whisperX_engine")


def test_update_engine(eManagerWhisperx, WHISPERX_SETTING):
    new_setting = WHISPERX_SETTING.copy()
    new_setting["language"] = "french"
    assert eManagerWhisperx.update_engine("test_whisperX_engine", new_setting)
    assert eManagerWhisperx.get_engine_setting("test_whisperX_engine") == new_setting


def test_update_engine_fail(eManager):
    with pytest.raises(EngineNotFound):
        eManager.update_engine("test_whisperX_engine", {})
