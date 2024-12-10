# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Joanne Fan
# @Last Modified time: 2024-04-01 02:20:18
from typing import Dict, List

from gailbot.shared.exception.serviceException import SourceNotFound
from gailbot.shared.utils.general import get_name
from gailbot.sourceManager.sourceObject import SourceObject, Watcher
from gailbot.payload.payloadConverter import (ConversationDirConverter,
                                              MediaConverter,
                                              TranscribedDirConverter,
                                              MixedDirectoryConverter,
                                              ConverterType)


class SourceManager:
    def __init__(self):
        self._sources: Dict[str, SourceObject] = dict()
        self._converters = {
            ConverterType.ConvDir: ConversationDirConverter,
            ConverterType.SingleMedia: MediaConverter,
            ConverterType.TranscribedResult: TranscribedDirConverter,
            ConverterType.MixedDirectory: MixedDirectoryConverter
        }

    def available_converters(self) -> List[ConverterType]:
        return list(self._converters.keys())

    def un_transcribed_sources(self) -> Dict[str, SourceObject]:
        return self._sources

    def add_source(self, source: str, output: str) -> str:
        source_id = get_name(source)
        if source_id in self._sources:
            counter = 1
            temp = source_id + f"({counter})"
            while temp in self._sources:
                counter += 1
                temp = source_id + f"({counter})"
            source_id = temp
        self._sources[source_id] = SourceObject(source_id, source, output)
        return source_id

    def is_source(self, source_id: str):
        return source_id in self._sources

    def get_source_output(self, source_id: str):
        if not self.is_source(source_id):
            raise SourceNotFound(source_id)
        return self._sources[source_id].output_dir

    def remove_source(self, source_id: str):
        if source_id not in self._sources:
            raise SourceNotFound(source_id)
        else:
            self._sources.pop(source_id)

    def apply_profile_to_source(self, source_id: str, profile: str):
        if source_id not in self._sources:
            raise SourceNotFound(source_id)
        else:
            self._sources[source_id].link_profile(profile)

    def get_source_profile(self, source_id: str) -> str:
        if not self.is_source(source_id):
            raise SourceNotFound(source_id)
        else:
            return self._sources[source_id].profile_name

    def get_source(self, source_id) -> SourceObject:
        if not self.is_source(source_id):
            raise SourceNotFound(source_id)
        else:
            return self._sources[source_id]

    def profile_used_by_source(self, profile_name: str) -> bool:
        """
        return true if [profile_name] is used by any source, false otherwise
        """
        for source in self._sources.values():
            if source.profile_obj == profile_name:
                return True
        else:
            return False

    def add_progress_watcher(self, source_id: str, watcher: Watcher):
        if not self.is_source(source_id):
            raise SourceNotFound(source_id)
        else:
            self._sources[source_id].add_watcher(watcher)

    def change_source_converter(self, source_id: str, converter: ConverterType):
        converter = self._converters[converter]
        return self._sources[source_id].change_converter(converter)

    def get_source_converter(self, source_id: str) -> ConverterType:
        return self.get_source(source_id).converter.converter_type

    def compatible_converters(self, source_id: str) -> List[ConverterType]:
        compatible = self._sources[source_id].compatible_converters()
        return [key for key, value in self._converters.items() if value in compatible]