# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 16:53:33
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-02 19:12:31

from typing import Dict, List, Tuple

from pyannote.core import Segment
from gailbot.shared.utils.logger import makelogger

_DEFAULT_SPEAKER = 0
logger = makelogger("parsers")


def parse_into_word_dicts(transcription: Dict) -> List[Dict]:
    """
    Parse the results of the transcription into a list of dictionaries
    containing the speaker, start time, end time, and text.

    Format of the transcription is detailed here: https://github.com/linto-ai/whisper-timestamped
    """
    parsed = list()
    segments = transcription["segments"]
    try:
        for segment in segments:
            if not "words" in segment:
                continue
            word_list = segment["words"]
            for item in word_list:
                parsed.append(
                    {
                        "start": item["start"],
                        "end": item["end"],
                        "text": item["text"],
                        # NOTE: Whisper does not generate speaker, but I can
                        # potentially add that in too.
                        "speaker": str(_DEFAULT_SPEAKER),
                    }
                )
                assert parsed
    except Exception as e:
        logger.error(f"getting the error from parsing word into dict", exc_info=e)
    return parsed


def parse_into_timestamped_text(asr_res: Dict) -> List[Tuple]:
    """
    Parse results from whisper timestamped in terms of Segment
    """
    timestamp_texts = []
    for segment in asr_res["segments"]:
        if not "words" in segment:
            continue
        word_list = segment["words"]
        for item in word_list:
            start = item["start"]
            end = item["end"]
            text = item["text"]
            timestamp_texts.append((Segment(start, end), text))
    return timestamp_texts


def parse_into_full_text(asr_res: Dict) -> str:
    """
    Parse the transcription output into a string.
    """
    return asr_res["text"]


def add_speaker_info_to_text(asr_res: Dict, dir_res: Dict) -> List[Dict]:
    """
    Add speaker information to transcription results using speaker
    diarization results. Returns dictionaries
    """
    spk_text = []
    timestamp_texts = parse_into_timestamped_text(asr_res)
    for seg, text in timestamp_texts:
        spk = dir_res.crop(seg).argmax()
        spk_text.append(
            {"start": seg.start, "end": seg.end, "speaker": spk, "text": text}
        )
    return spk_text
