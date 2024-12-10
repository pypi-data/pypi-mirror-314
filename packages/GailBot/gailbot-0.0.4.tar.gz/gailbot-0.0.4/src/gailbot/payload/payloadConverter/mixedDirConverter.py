# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-02-24 10:13:16
# @Email:
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-02 18:01:08
# @Descriptions: convert a directory source to a list of corresponding payloads


import os.path
from typing import List

from gailbot.payload.payloadConverter.mediaConverter import MediaConverter
from gailbot.payload.payloadConverter.conversationDirConverter import (
    ConversationDirConverter,
)
from gailbot.payload.payloadConverter.converter import Converter, ConverterType
from gailbot.payload.payloadConverter.transcribedDirConverter import (
    TranscribedDirConverter,
)
from gailbot.payload.payloadObject import PayloadObject
from gailbot.profileManager import ProfileObject
from gailbot.shared.utils.general import paths_in_dir
from gailbot.sourceManager.watcher import Watcher


class MixedDirectoryConverter(Converter):
    accepted_forms = ["/"]
    converter_type = ConverterType.MixedDirectory

    @staticmethod
    def convert(
        path: str, output_dir: str, profile: ProfileObject, watchers: List[Watcher]
    ) -> List[PayloadObject]:
        converters: List = [
            TranscribedDirConverter,
            ConversationDirConverter,
            MediaConverter,
            MixedDirectoryConverter,
        ]
        payloads = []
        subpaths = paths_in_dir(path)
        for p in subpaths:
            for converter in converters:
                if converter.is_accepted_form(p):
                    payloads.extend(converter.convert(p, output_dir, profile, watchers))
                    break
        return payloads

    @staticmethod
    def is_accepted_form(path: str) -> bool:
        supported_format = MediaConverter.accepted_forms
        return (
            os.path.isdir(path)
            and paths_in_dir(path, supported_format, True) != 0
            and not TranscribedDirConverter.is_accepted_form(path)
        )
