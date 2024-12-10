from gailbot.payload.payloadObject.payloadObject import PayloadObject
import os.path
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import List
from gailbot.pluginSuiteManager.suite.gbPluginMethod import GBPluginMethods
from gailbot.profileManager import ProfileObject
from gailbot.shared.utils.general import make_dir, get_name, write_json, is_file, copy
from gailbot.shared.utils.logger import makelogger
from gailbot.sourceManager.watcher import Watcher
from gailbot.payload.result import SttTranscribeResult, AnalysisResult, FormatResult
from gailbot.workspace.directory_structure import OutputFolder, TemporaryFolder
import time


logger = makelogger("AnalysisTest")


@dataclass
class Progress:
    Start = "\u25B6 {name} : Start"
    Waiting = "\U0001F551  {name} : Waiting"
    Transcribing = "\U0001F50A {name} : Transcribing with engine {engine}"
    Finished = "\u2705 {name}: Completed"
    Transcribed = "\u2705 {name}: Transcribed"
    Error = "\U0001F6AB {name}: Error"
    Analyzing = "\U0001F4AC {name}: Applying plugin suite {suite}"
    Analyzed = "\u2705 {name}: Analyzed"
    Formatting = "\U0001F4C1 {name}: Formatting"



class Analysis():
    def __init__(
        self,
        payload_obj: PayloadObject
    ):
        self.original_source = payload_obj.original_source
        self.data_files = payload_obj.data_files
        self.temp_dir_struct = TemporaryFolder
        self.output_path = payload_obj.output_path
        self.profile  = payload_obj.profile
        self.watchers = payload_obj.watchers
        self.transcription_result = payload_obj.transcription_result
        self.plugin_suites = self.profile.plugin_suites
        self.output_dir_struct = OutputFolder(self.output_dir)
        self.merged_audio = payload_obj.merged_audio


    def analyze(self):
        """
        perform transcription analysis using the applied plugin suite

        Returns
        -------
        return true if the analysis succeed, false otherwise

        Notes
        -------
        this function will only be invoked when stt_transcribe return true,
        """
        try:
            results = dict()
            for suite, selected in self.plugin_suites.items():
                suite_output = os.path.join(self.output_dir_struct.analysis, suite.name)
                suite_ws = os.path.join(self.temp_dir_struct.analysis_ws, suite.name)
                make_dir(suite_output)
                make_dir(suite_ws)
                for watcher in self.watchers:
                    watcher.watch(
                        Progress.Analyzing.format(name=self.name, suite=suite.name)
                    )
                result = suite(
                    base_input=None,
                    methods=GBPluginMethods(
                        work_path=suite_ws,
                        out_path=suite_output,
                        data_files=self.data_files,
                        merged_media=self.merged_audio,
                        utterances=self.transcription_result.get_data(),
                    ),
                    selected_plugins=selected,
                )
                results[suite.name] = result
            # assert self.analysis_result.save_data(results)
            return results
        except Exception as e:
            logger.error(e, exc_info=True)
            return None
