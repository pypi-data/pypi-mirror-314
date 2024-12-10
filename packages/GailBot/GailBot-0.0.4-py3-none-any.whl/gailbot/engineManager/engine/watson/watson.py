# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:43:29
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-08-01 05:32:12
from typing import Dict, List
from .core import WatsonCore
from .lm import WatsonLMInterface
from .am import WatsonAMInterface
from gailbot.engineManager.engine.engine import Engine
from gailbot.shared.exception.transcribeException import TranscriptionError
from gailbot.configs import watson_config_loader
from gailbot.shared.utils.logger import makelogger
from .watsonSetting import WatsonSetting

WATSON_CONFIG = watson_config_loader()

logger = makelogger("watson")


class Watson(Engine):
    """
    An Engine that connect to IBM Watson STT, provide function to transcribe
    audio file with IBM Watson STT

    Inheritance:
        Engine
    """

    def __init__(
            self,
            setting: WatsonSetting
    ):
        self.setting = setting
        apikey = self.setting.apikey
        region = self.setting.region
        self.core = WatsonCore(apikey, region, setting)
        self.lm = WatsonLMInterface(apikey, region)
        self.am = WatsonAMInterface(apikey, region)
        self.is_transcribe_success = False

    def __str__(self):
        return WATSON_CONFIG.name

    def __repr__(self):
        """
        Returns all the configurations and additional metadata
        """
        return self.core.__repr__()

    @staticmethod
    def validate_api(apikey: str, region: str):
        return WatsonCore.valid_region_api(apikey, region)

    @property
    def supported_formats(self) -> List[str]:
        """
        A list of supported format that can be transcribe with the STT engine
        """
        return self.core.supported_formats

    @property
    def regions(self) -> Dict:
        """
        A dictionary of the supported regions and the regions url
        """
        return self.core.regions

    @property
    def defaults(self) -> Dict:
        """
        A dictionary that contains the default settings that will be
        applied to the IBM Watson STT engine
        """
        return self.core.defaults

    def transcribe(
            self,
            audio_path: str,
            payload_workspace: str,
    ) -> List[Dict]:
        try:
            utterances = self.core.transcribe(
                audio_path,
                payload_workspace,
                self.setting.base_model,
                self.setting.language_customization_id,
                self.setting.acoustic_customization_id,
                self.setting
            )
            self.is_transcribe_success = True
            return utterances
        except Exception as e:
            logger.error(e, exc_info=e)
            raise TranscriptionError(e)

    def language_customization_interface(self) -> WatsonLMInterface:
        """
        Return the watson customized language model interface
        """
        return self.lm

    def acoustic_customization_interface(self) -> WatsonAMInterface:
        """
        Return the watson customized acoustic model interface
        """
        return self.am

    def get_engine_name(self) -> str:
        """
        Return the name of the watson engine
        """
        return "watson"

    def get_supported_formats(self) -> List[str]:
        """
        Return a list of supported format that can be
        transcribed with the STT engine
        """
        return self.core.supported_formats

    def is_file_supported(self, file_path: str) -> bool:
        """
        Given a file path, return true if the file format is supported by
        the Watson STT engine

        Args:
            file_path: str
                a path to the file of which to check if supported
        """
        return self.core.is_file_supported(file_path)

    def was_transcription_successful(self) -> bool:
        """
        Return true if the transcription is finished and successful,
        false otherwise
        """
        return self.is_transcribe_success
