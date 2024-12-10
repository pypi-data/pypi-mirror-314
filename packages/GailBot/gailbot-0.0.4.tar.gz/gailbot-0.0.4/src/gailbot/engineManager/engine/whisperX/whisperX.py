# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-08-06 13:32:05
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-09 18:04:17
import os
import torch
from typing import List, Dict

from threading import Lock
import whisperx

from gailbot.shared.utils.logger import makelogger


from gailbot.shared.utils.media import MediaHandler

from gailbot.shared.utils.general import get_extension
from gailbot.engineManager.engine.engine import Engine
from gailbot.engineManager.engine.whisperX.whisperXSetting import WhisperXSetting

logger = makelogger("whisperX")


class WhisperX(Engine):
    model_pool = dict()
    model_pool_lock = Lock()
    batch_size = 4
    device = "cpu"

    def __init__(self, setting: WhisperXSetting):
        super().__init__()
        self.setting = setting
        self._successful = False
        self.device = self.get_device()
        self.compute_type = self.get_compute_type()

    def __str__(self):
        return "whisperX"

    def __repr__(self):
        """
        Returns all the configurations and additional metadata
        """
        return "whisperX"

    def get_device(self):
        return 'cuda' if torch.cuda.is_available() else 'cpu'

    def get_compute_type(self):
        if self.device == 'cuda':
            device_properties = torch.cuda.get_device_properties(torch.cuda.current_device())
            if device_properties.major >= 7:  
                return 'float16'
        return 'float32'

    def load_model(
        self,
        language: str
    ):
        with self.model_pool_lock:
            if language in self.model_pool:
                return self.model_pool[language]
            else:
                asr_options = { 
                    "max_new_tokens": 500, 
                    "clip_timestamps": True, 
                    "hallucination_silence_threshold": 0.5,
                    "temperatures": self.setting.temperature, 
                    "initial_prompt": self.setting.initial_prompt,
                    "condition_on_previous_text": self.setting.condition_on_previous_text,
                    "no_speech_threshold": self.setting.no_speech_threshold
                }
                model = whisperx.load_model(
                    "base", device= self.device, language=language, compute_type = "int8", asr_options= asr_options, vad_options={"vad_onset": self.setting.vad_onset, "vad_offset": self.setting.vad_offset}
                )
                self.model_pool[language] = model
                return model

    def transcribe(self, audio_path, payload_workspace) -> List[Dict[str, str]]:
        """
        Use the engine to transcribe an item
        """
        audio = whisperx.load_audio(audio_path)
        model = self.load_model(self.setting.language)
        result = model.transcribe(
            audio, batch_size=self.batch_size, language=self.setting.language, chunk_size= self.setting.chunk_size
        )
        try:
            model_a, metadata = whisperx.load_align_model(
                language_code=result["language"], device=self.device
            )
        except Exception as e:
            logger.error(e, exc_info=e)

        print("aligned  model")
        result = whisperx.align(
            result["segments"],
            model_a,
            metadata,
            audio,
            self.device,
            return_char_alignments=False,
            interpolate_method= self.setting.interpolate_method
        )
        res = []
        segments = result["segments"]
        nxt_timestamp = 0
        for segment in segments:
            for word in segment["words"]:
                res.append(
                    {
                        "start": word.get("start", nxt_timestamp),
                        "end": word.get("end", nxt_timestamp),
                        "text": word.get("word", "null"),
                        "speaker": "0",
                    }
                )
                nxt_timestamp = word.get("end", nxt_timestamp) + 0.00001
        self._successful = True
        return res

    def was_transcription_successful(self) -> bool:
        """
        Return true if the transcription is successful
        """
        return self._successful

    def get_engine_name(self) -> str:
        """
        Obtain the name of the current engine.
        """
        return "whisperX"

    def get_supported_formats(self) -> List[str]:
        """
        Obtain a list of audio file formats that are supported.
        """
        return ["wav"]

    def is_file_supported(self, filepath: str) -> bool:
        """
        Determine if the given file is supported by the engine.
        """
        return get_extension(filepath) in self.get_supported_formats()
