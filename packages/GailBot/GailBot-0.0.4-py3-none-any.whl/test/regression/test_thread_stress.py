# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-02-06 10:19:08
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-02-06 15:35:20
import os.path
from gailbot.api import GailBot
from gailbot.sourceManager.sourceObject import Watcher

OUTPUT = "/Users/yike/Desktop/gbtest/output"
TEST_ROOT = "/Users/yike/Desktop/gbtest/input"


class TestWatcher(Watcher):
    def watch(self, progress: str):
        print(progress)


def test_parallel_transcription():
    gb = GailBot()
    source_ids = [
        gb.add_source(
            source_path=os.path.join(TEST_ROOT, "hello2.wav"), output_dir=OUTPUT
        )
        for _ in range(4)
    ]
    source_ids.extend(
        [
            gb.add_source(
                source_path=os.path.join(TEST_ROOT, "short_test/shorttest.wav"),
                output_dir=OUTPUT,
            )
            for _ in range(4)
        ]
    )
    for id in source_ids:
        gb.add_progress_watcher(id, TestWatcher())
    result = gb.transcribe(source_ids)
    assert not result.failure
