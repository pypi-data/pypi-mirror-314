# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:43:29
# @Last Modified by:   Lakshita Jain
# @Last Modified time: 2023-11-30 16:53:18

from typing import Dict, List

from gailbot.engineManager.engine.engine import Engine
from gailbot.engineManager.engine.whisper.core import WhisperCore
from gailbot.shared.utils.general import get_extension
from gailbot.shared.utils.logger import makelogger
from .whisperSetting import WhisperSetting

logger = makelogger("Whisper Engine")


class Whisper(Engine):
    def __init__(self, setting: WhisperSetting):
        self.setting = setting
        self.core = WhisperCore()
        self._successful = False

    def __str__(self):
        """
        Returns the name of the function
        """
        return self.setting.engine_name

    def __repr__(self):
        """
        Returns all the configurations and additional metadata
        """
        return self.core.__repr__()

    def transcribe(
            self,
            audio_path, payload_workspace
    ) -> List[Dict]:
        results = self.core.transcribe(audio_path, self.setting.language, self.setting.detect_speakers)
        self._successful = True
        return results

    def was_transcription_successful(self) -> bool:
        """
        Return true if transcription was successful, false otherwise.
        """
        return self._successful

    def get_engine_name(self) -> str:
        """
        Obtain the name of the current engine.

        Returns:
            (str): Name of the engine.
        """
        return self.setting.engine

    def get_supported_formats(self) -> List[str]:
        """
        Obtain a list of audio file formats that are supported.

        Returns:
            (List[str]): Supported audio file formats.
        """
        return self.core.get_supported_formats()

    def is_file_supported(self, file_path: str) -> bool:
        """
        Determine if the given file is supported by the engine.

        Args:
            file_path (str)

        Returns:
            (bool): True if file is supported. False otherwise.
        """
        return get_extension(file_path) in self.get_supported_formats()

    def get_available_models(self) -> List[str]:
        """
        Return the list of available models
        """
        return self.core.get_available_models()
