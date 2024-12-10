# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-02-24 10:12:04
# @Email:
# @Last Modified by:   Vivian Li 
# @Last Modified time: 2024-03-03 15:12:54
# @Descriptions: declare abstract class for Converter,
#                a converter convert a source to a list of payload
from abc import ABC, abstractmethod
from enum import Enum
from typing import List
from gailbot.profileManager import ProfileObject
from gailbot.payload.payloadObject import PayloadObject
from gailbot.sourceManager.watcher import Watcher


class ConverterType(Enum):
    MixedDirectory = "Mixed Directory"
    SingleMedia = "Single Media File"
    ConvDir = "Conversation Directory"
    TranscribedResult = "Previous GailBot Output"

    def __str__(self):
        return self.value


class Converter(ABC):
    accepted_forms = (
        []
    )  # a list of accepted formats that can be converted to a payload by the converter
    converter_type: ConverterType

    @staticmethod
    @abstractmethod
    def is_accepted_form(path: str) -> bool:
        """
        Return true if path is a file with the accepted form
        """
        pass

    @staticmethod
    @abstractmethod
    def convert(
            path: str, output_dir: str, profile: ProfileObject, watchers: List[Watcher]
    ) -> List[PayloadObject]:
        """
        Given the path to the original source,  the targeted output_dir of the
        transcribed result, the profile applied to the source, and the source
        watchers, convert the source to a list of payload
        """
        pass
