# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-03-13 18:20:30
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-06 14:31:16
import os

import pytest

from gailbot import GailBot
from test.test_data import TestData


@pytest.fixture(scope="module", autouse=True)
def gb():
    gailbot = GailBot()
    return gailbot


@pytest.mark.parametrize("audio_file", ["all/60sec.mp3"])
def test_transcribe_audio(gb, audio_file):
    gb.add_source(
        source_path=os.path.join(TestData.INPUT, audio_file), output_dir=TestData.OUTPUT
    )

    result = gb.transcribe()
    assert result.success_output
    assert not (result.invalid or result.failure)


@pytest.mark.parametrize("video_file", ["short.mxf"])
def test_transcribe_mxf_video(gb, video_file):
    # add single video file
    gb.add_source(
        source_path=os.path.join(TestData.INPUT, video_file), output_dir=TestData.OUTPUT
    )

    result = gb.transcribe()
    assert result.success_output
    assert not (result.invalid or result.failure)


def test_transcribed_2ab():
    gb = GailBot()
    gb.add_source(
        source_path=TestData.test2ab_transcribed,
        output_dir=TestData.OUTPUT,
    )
    result = gb.transcribe()
    assert not result.failure
