# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-02-25 08:58:26
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-03-26 15:21:13
import os.path
from dataclasses import dataclass


@dataclass
class TestData:
    OUTPUT = "/Users/yike/Desktop/gbtest/output"
    INPUT = "/Users/yike/Desktop/gbtest/input"
    BAD_INPUT = os.path.join(INPUT, "media_formats")
    MIX_DIR = os.path.join(INPUT, "mixed_dir")
    hello = os.path.join(INPUT, "hello2.wav")
    test2ab = os.path.join(INPUT, "test2ab")
    test2ab_transcribed = os.path.join(INPUT, "test2ab_transcribed")
    test0638_transcribed = os.path.join(INPUT, "0638-transcribed")
    small_dir2 = os.path.join(INPUT, "small_test2")
    small_dir4 = os.path.join(INPUT, "small_test4")
    small_dir6 = os.path.join(INPUT, "small_test6")
    test_mp3 = os.path.join(INPUT, "test.mp3")
    callhome_small = os.path.join(INPUT, "callhome_small")
    callhome_full = os.path.join(INPUT, "callhome_full")
