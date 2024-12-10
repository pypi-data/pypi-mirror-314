# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-02-24 10:14:02
# @Email:
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-08 22:41:25
# @Descriptions
import os
import threading
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, wait
from typing import List
from .payloadObject import PayloadObject, Progress
from ...profileManager import ProfileObject
from ...shared.utils.general import get_name, copy
from ...shared.utils.logger import makelogger
from ...shared.utils.media import AudioHandler
from ...sourceManager.watcher import Watcher
from ...workspace.directory_structure import OutputFolder, TemporaryFolder

logger = makelogger("un-transcribed payload")


class untranscribedDirPayload(PayloadObject):

    def __init__(
        self,
        original_source: str,
        data_files: List[str],
        temp_dir_struct: TemporaryFolder,
        output_path: str,
        profile: ProfileObject,
        watchers: List[Watcher],
    ):
        super().__init__(
            original_source, data_files, temp_dir_struct, output_path, profile, watchers
        )
        self.finished_files = 0
        self.finished_files_lock = threading.Lock()

    def merge_audio(self, output) -> str:
        try:
            if len(self.data_files) == 1:
                merged_path = os.path.join(output, OutputFolder.MERGED_FILE)
                copy(src_path=self.data_files[0], tgt_path=merged_path)
            else:
                audio_handler = AudioHandler()
                merged_path = audio_handler.overlay_audios(
                    self.data_files, output, OutputFolder.MERGED_FILE
                )
            return merged_path
        except Exception as e:
            logger.error(e, exc_info=True)

    def stt_transcribe(self) -> bool:
        print("IN stt transcribe in untranscribedDirPayload\n")
        if len(self.data_files) == 1:
            return self.transcribe_file(self.data_files[0])
        else:
            return self.transcribe_files(self.data_files)

    def transcribe_file(self, path: str):
        try:
            for w in self.watchers:
                w.watch(
                    Progress.Transcribing.format(
                        name=self.name, engine=self.engine.get_engine_name()
                    )
                )
            result = self.engine.transcribe(path, self.temp_dir_struct.transcribe_ws)
            assert self.transcription_result.save_data({get_name(path): result})
            return True
        except Exception as e:
            logger.error(e, exc_info=True)
            return False

    def transcribe_files(self, paths: List[str]):
        total_time = 0
        time_loaded = True
        for p in paths:
            try:
                audio: AudioSegment = AudioSegment.from_file(p)
                total_time += audio.duration_seconds
            except Exception as e:
                logger.warn(f"Failed to get the audio time", exc_info=True)
                time_loaded = False
        logger.info(f"The total audio time is {total_time} seconds")

        def report_finish(_):
            with self.finished_files_lock:
                self.finished_files += 1
                for w in self.watchers:
                    w.watch(
                        f"{self.name}: Transcribed {self.finished_files} / {len(self.data_files)} files."
                    )

        try:
            for watcher in self.watchers:
                watcher.watch(
                    Progress.Transcribing.format(
                        name=self.name, engine=self.engine.get_engine_name()
                    )
                )
            futures = dict()
            results = dict()
            with ThreadPoolExecutor(min(3, len(paths))) as executor:
                for file in paths:
                    future = executor.submit(self.transcribe_wrapper, file)
                    future.add_done_callback(report_finish)
                    futures[get_name(file)] = future
                if time_loaded:
                    wait(futures.values(), timeout=total_time * 2)
                else:
                    wait(futures.values())

            for name, future in futures.items():
                result = future.result()
                assert result != False
                results[name] = result
            assert self.transcription_result.save_data(results)
            return True
        except Exception as e:
            logger.error(e, exc_info=True)
            return False

    def transcribe_wrapper(self, file):
        try:
            return self.engine.transcribe(file, self.temp_dir_struct.transcribe_ws)
        except Exception as e:
            logger.error(e, exc_info=True)
            return False
