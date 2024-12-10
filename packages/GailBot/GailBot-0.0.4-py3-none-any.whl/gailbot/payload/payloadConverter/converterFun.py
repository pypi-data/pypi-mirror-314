# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-02-28 18:13:42
# @Email:
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-21 14:15:08
# @Descriptions

import os.path
import numpy as np
from typing import List

from pydub import AudioSegment
from scipy.io.wavfile import write, read
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub.exceptions import CouldntDecodeError
from gailbot.shared.exception.serviceException import IncompatibleFileFormat

from gailbot.shared.utils.general import delete, get_name, copy, get_extension, run_cmd
from gailbot.shared.utils.logger import makelogger
from gailbot.shared.utils.media import AudioHandler

logger = makelogger("converter")


def _raise_bad_format(path: str, err: Exception):
    logger.error(err, exc_info=True)
    extension = get_extension(path)
    raise IncompatibleFileFormat(path, extension)


def _convert_audio(path, tgt_parent_directory) -> List[str]:
    tgt = os.path.join(tgt_parent_directory, get_name(path) + ".wav")
    command = ["ffmpeg", "-i", f'"{path}"', "-acodec", "pcm_s16le", f'"{tgt}"']
    if os.path.isfile(tgt):
        delete(tgt)
    result = run_cmd(command)
    if result == 0:
        return [tgt]
    else:
        raise IncompatibleFileFormat(path, get_extension(path))


def _convert_video(path, tgt_parent_directory) -> List[str]:
    try:
        video_clip = VideoFileClip(path)
        audio_clip = video_clip.audio
        name = get_name(path)
        output = os.path.join(tgt_parent_directory, f"{name}.wav")
        audio_clip.write_audiofile(output, codec="pcm_s16le", fps=44100)
        video_clip.close()
        audio_clip.close()
        return [output]
    # VideoFileClip raises `KeyError: 'video_fps'` when given an audio file
    # (wav) instead of video (mov). We catch that and raise our own exception.
    except KeyError as e:
        _raise_bad_format(path, e)


def _convert_mxf(path, tgt_parent_directory) -> List[str]:
    name = get_name(path)
    video_clip = VideoFileClip(path)
    audio_clip = video_clip.audio

    # number of bytes to encode the sound:
    # 1 for 8bit sound, 2 for 16bit, 4 for 32bit
    sound_data = audio_clip.to_soundarray(fps=44100, quantize=True, nbytes=2)

    # extract each audio channel into a separate wav file
    num_channels = audio_clip.nchannels
    outputs = []
    for i in range(num_channels):
        output_path = os.path.join(tgt_parent_directory, f"{name}{i + 1}.wav")
        channel_audio = sound_data[:, i]
        # check that the current channel isn't a duplicate of another channel
        skip_channel = any(
            np.array_equal(channel_audio, sound_data[:, j]) for j in range(i)
        )
        if not skip_channel:
            write(output_path, audio_clip.fps, channel_audio)
            outputs.append(output_path)

    audio_clip.close()
    video_clip.close()
    return outputs


def _convert_wav(path, tgt_parent_directory):
    try:
        # Ensure that the content is actually wav
        read(path)
        copy_path = os.path.join(tgt_parent_directory, os.path.basename(path))
        copy(src_path=path, tgt_path=copy_path)
        return [copy_path]
    except ValueError as e:
        _raise_bad_format(path, e)
        return _convert_audio(path=path, tgt_parent_directory=tgt_parent_directory)


class ConvertFun:
    convert_funs = {
        "mp3": _convert_audio,
        "mp4": _convert_video,
        "aac": _convert_audio,
        "m4a": _convert_audio,
        "wav": _convert_wav,
        "mov": _convert_video,
        "avi": _convert_video,
        "3gp": _convert_video,
        "mxf": _convert_mxf,
    }

    @staticmethod
    def convert_to_wav(path, tgt_parent_directory) -> List[str]:
        """
        convert the path to wav file, converted file should bed stored in tgt_parent_directory,
        and return the path of the converted file

        Parameters
        ----------
        path
        tgt_parent_directory

        Returns
        -------

        """
        file_format = get_extension(path).lower()
        return ConvertFun.convert_funs[file_format](path, tgt_parent_directory)

    @staticmethod
    def compatible_video_formats():
        return ["mp4", "mov", "3gp", "mxf", "avi"]

    @staticmethod
    def compatible_audio_formats():
        return ["mp3", "aac", "wav", "m4a"]

    @staticmethod
    def compatible_formats():
        return list(ConvertFun.convert_funs.keys())
