# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Joanne Fan
# @Last Modified time: 2024-04-01 02:20:18
# @Description: Any file accepted by gailbot will be initially stored as an instance of SourceObject
#               SourceObject will store the Profile and Loader applied to the Source,
#               A set of SourceObjects will be managed by SourceManager
from typing import List

from gailbot.payload.payloadConverter.mediaConverter import MediaConverter
from gailbot.payload.payloadConverter.conversationDirConverter import ConversationDirConverter
from gailbot.payload.payloadConverter.mixedDirConverter import MixedDirectoryConverter
from gailbot.payload.payloadConverter.transcribedDirConverter import TranscribedDirConverter
from gailbot.payload.payloadObject import PayloadObject
from gailbot.profileManager import ProfileObject
from gailbot.sourceManager.watcher import Watcher


class SourceObject:
    converters = [TranscribedDirConverter,
                  MediaConverter,
                  ConversationDirConverter,
                  MixedDirectoryConverter]

    def __init__(self, source_id, source_path, output):
        self.source_id = source_id
        self.name = source_id
        self.source_path = source_path
        self.output_dir = output
        self.profile_name: str | None = None
        self.profile_obj: ProfileObject | None = None
        self.watchers: List[Watcher] = []
        self.converter = None
        for converter in self.converters:
            if converter.is_accepted_form(source_path):
                self.converter = converter
                break

    def link_profile(self, profile_name: str):
        """
        link the source to a profile name

        Parameters
        ----------
        profile_name : str

        Returns
        -------

        """
        self.profile_name = profile_name

    def initialize_profile(self, profile: ProfileObject):
        """
        initialize the profile object used by the source, this function must be called
        before converting the source to a payload for transcription

        Parameters
        ----------
        profile

        Returns
        -------

        """
        self.profile_obj = profile

    def add_watcher(self, watcher: Watcher):
        self.watchers.append(watcher)

    def compatible_converters(self):
        compatible = [c for c in self.converters if c.is_accepted_form(self.source_path)]
        return compatible

    def change_converter(self, converter):
        if converter.is_accepted_form(self.source_path):
            self.converter = converter
            return True
        else:
            return False

    def convert(self) -> List[PayloadObject]:
        if not self.converter:
            return []
        return self.converter.convert(self.source_path, self.output_dir, self.profile_obj, self.watchers)
