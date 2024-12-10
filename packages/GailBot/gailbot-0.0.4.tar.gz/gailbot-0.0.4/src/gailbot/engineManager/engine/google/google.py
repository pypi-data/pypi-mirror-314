# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Vivian Li 
# @Last Modified time: 2024-05-03 17:14:56

from gailbot.engineManager.engine.engine import Engine
from .googleSetting import GoogleSetting
from ..google.core import GoogleCore
from .AC import GoogleACInterface
from typing import Dict, List
from gailbot.shared.utils.logger import makelogger

logger = makelogger("google engine")


class Google(Engine):
    """
    An Engine that connect to Google Cloud STT, provide function to transcribe
    audio file with Google Cloud STT

    Inheritance:
        Engine
    """
    def __init__(self, setting: GoogleSetting):
        self.setting = setting
        self.ac = GoogleACInterface(api_key_path=self.setting.google_api_key)
        self.core = GoogleCore(self.setting)
        self.transcribe_success = False

    def __repr__(self):
        return self.setting.engine

    def transcribe(self, audio_path: str, workspace: str) -> List[Dict[str, str]]:
        """use Google engine to transcribe the audio file

        Args:
            audio_path (str): path to audio source
            workspace (str): path to a folder that is available for engine to store temporary data

        Raises:
            Err.TranscriptionError

        Returns:
            A list of dictionary that contains the utterance data of the
            audio file, each part of the audio file is stored in the format
            {speaker: , start_time: , end_time: , text: }
        """
        res = self.core.transcribe(audio_path, workspace)
        self.transcribe_success = True
        return res

    def is_file_supported(self, file_path: str) -> bool:
        """
        given a file path, return true if the file format is supported by
        the Google STT engine
        """
        return self.core.is_file_supported(file_path)

    def get_supported_formats(self) -> List[str]:
        return self.core.supported_formats

    def get_engine_name(self) -> str:
        return self.setting.engine

    def was_transcription_successful(self) -> bool:
        return self.transcribe_success

    @staticmethod
    def is_valid_google_api(google_api_key) -> bool:
        """ takes a path to a json file """
        engine = GoogleCore.is_valid_google_api(google_api_key)
        return True if engine else False
