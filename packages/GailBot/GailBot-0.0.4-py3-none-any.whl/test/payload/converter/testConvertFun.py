# -*- coding: utf-8 -*-
# @Author: Joanne Fan
# @Date:   2024-02-28 23:11:18
# @Email:
# @Last Modified by:   Joanne Fan
# @Last Modified time: 2024-03-13 15:18:26
# @Descriptions

import pytest
import os.path
from gailbot.shared.exception.serviceException import IncompatibleFileFormat
from gailbot.payload import ConvertFun
from test.test_data import TestData


@pytest.fixture
def converter():
    return ConvertFun()


def run_convert(converter, filepath, tgt_par_dir):
    filename = os.path.basename(filepath)
    no_ext_filename = os.path.splitext(filename)[0]

    tgt_wavpath_list = converter.convert_to_wav(filepath, str(tgt_par_dir))

    if len(tgt_wavpath_list) == 1:
        outfile_name = f"{no_ext_filename}.wav"
        outfile_path = tgt_par_dir.join(outfile_name)
        assert outfile_path.exists()
        assert tgt_wavpath_list[0] == outfile_path
    else:
        for i, tgt_wavpath in enumerate(tgt_wavpath_list):
            outfile_name = f"{no_ext_filename}{i + 1}.wav"
            outfile_path = tgt_par_dir.join(outfile_name)
            assert outfile_path.exists()
            assert tgt_wavpath == outfile_path

    converter.convert_to_wav(filepath, TestData.OUTPUT)


@pytest.mark.parametrize("filename", ['hello.mp3',
                                      'hello.aac',
                                      'hello.mp4',
                                      'hello.mov',
                                      'hello.avi',
                                      'hello.3gp',
                                      'short.mxf'
                                      ])
def test_convert_formats(converter, filename, tmpdir):
    tgt_parent_dir = tmpdir.mkdir("output")
    filepath = os.path.join(TestData.INPUT, filename)
    run_convert(converter, filepath, tgt_parent_dir)


# The file's content is a different audio format than the audio format
# named by the extension. Should raise exception.
@pytest.mark.parametrize("filename", ['hello1aac.mp3'])
def test_convert_mismatched_audios(converter, filename, tmpdir):
    tgt_parent_dir = tmpdir.mkdir("output")
    filepath = os.path.join(TestData.BAD_INPUT, filename)

    with pytest.raises(IncompatibleFileFormat) as e:
        converter.convert_to_wav(filepath, str(tgt_parent_dir))


# The file's content is a different video format than the video format
# named by the extension. Should not raise exception. 
# TODO mxf NOT included in this case.
@pytest.mark.parametrize("filename", ['failvidmov.mp4',
                                      'hello3gp.avi',
                                      'hello1avi.3gp',
                                      'hello1avi.mov'
                                      ])
def test_convert_mismatched_videos(converter, filename, tmpdir):
    tgt_parent_dir = tmpdir.mkdir("output")
    filepath = os.path.join(TestData.BAD_INPUT, filename)
    run_convert(converter, filepath, tgt_parent_dir)


# The file's content is not wav, even though the extension is .wav. Should
# raise exception.
@pytest.mark.parametrize("filename", ['hello1mp3.wav'])
def test_convert_wav_fail(converter, filename, tmpdir):
    tgt_parent_dir = tmpdir.mkdir("output")
    filepath = os.path.join(TestData.BAD_INPUT, filename)

    with pytest.raises(IncompatibleFileFormat) as e:
        converter.convert_to_wav(filepath, str(tgt_parent_dir))


# audio vs video mismatched should raise exception.
@pytest.mark.parametrize("filename", ['hellowav.mov'])
def test_convert_mismatched_vid_audio(converter, filename, tmpdir):
    tgt_parent_dir = tmpdir.mkdir("output")
    filepath = os.path.join(TestData.BAD_INPUT, filename)

    with pytest.raises(IncompatibleFileFormat) as e:
        converter.convert_to_wav(filepath, str(tgt_parent_dir))
