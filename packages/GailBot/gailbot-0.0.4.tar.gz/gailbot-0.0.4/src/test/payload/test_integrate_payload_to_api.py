# -*- coding: utf-8 -*-
# @Author: Vivian Li 
# @Date:   2024-02-24 14:33:17
# @Last Modified by:   Joanne Fan
# @Last Modified time: 2024-03-13 15:18:26
# @Description: Integration testing to transcribe sources through api interface
import os.path
import pytest

from gailbot import GailBot
from gailbot import ConverterType
from test.test_data import TestData


@pytest.fixture(scope="module", autouse=True)
def gb():
    gailbot = GailBot()
    return gailbot


def test_transcribe_audio(gb):
    # add single audio file
    gb.add_source(
        source_path=TestData.hello,
        output_dir=TestData.OUTPUT
    )

    result = gb.transcribe()
    assert result.success_output
    assert not (result.invalid or result.failure)


@pytest.mark.parametrize("video_file", ["hello.mp4",
                                        "hello.mov",
                                        "hello.3gp",
                                        "hello.avi",
                                        "short.mxf"])
def test_transcribe_video(gb, video_file):
    # add single video file
    gb.add_source(
        source_path=os.path.join(TestData.INPUT, video_file),
        output_dir=TestData.OUTPUT
    )

    result = gb.transcribe()
    assert result.success_output
    assert not (result.invalid or result.failure)


@pytest.mark.parametrize("audio_file", ["hello.mp3",
                                        "hello.wav",
                                        "hello.aac"])
def test_transcribe_audio(gb, audio_file):
    gb.add_source(
        source_path=os.path.join(TestData.INPUT, audio_file),
        output_dir=TestData.OUTPUT
    )

    result = gb.transcribe()
    assert result.success_output
    assert not (result.invalid or result.failure)


@pytest.mark.parametrize("video_file", ["short.mxf"])
def test_transcribe_mxf_video(gb, video_file):
    # add single video file
    gb.add_source(
        source_path=os.path.join(TestData.INPUT, video_file),
        output_dir=TestData.OUTPUT
    )

    result = gb.transcribe()
    assert result.success_output
    assert not (result.invalid or result.failure)


@pytest.mark.parametrize("con_dir", ["mix_format"])
def test_mixed_dir(gb, con_dir):
    # add single video file
    id = gb.add_source(
        source_path=os.path.join(TestData.MIX_DIR, con_dir),
        output_dir=TestData.OUTPUT
    )
    gb.change_source_converter(id, ConverterType.MixedDirectory)
    result = gb.transcribe()
    assert result.success_output
    assert not (result.invalid or result.failure)


def test_transcribe_conv_dir(gb):
    gb.add_source(
        source_path=TestData.test2ab,
        output_dir=TestData.OUTPUT
    )

    result = gb.transcribe()
    assert result.success_output
    assert not (result.invalid or result.failure)


def test_transcribed_dir(gb):
    gb.add_source(
        source_path=TestData.test2ab_transcribed,
        output_dir=TestData.OUTPUT
    )

    result = gb.transcribe()
    assert result.success_output
    assert not (result.invalid or result.failure)


def test_change_converter(gb):
    sourceId = gb.add_source(
        source_path=TestData.small_dir2,
        output_dir=TestData.OUTPUT
    )
    gb.change_source_converter(sourceId, ConverterType.MixedDirectory)
    result = gb.transcribe([sourceId])
    assert result.success_output
    assert not (result.invalid or result.failure)
