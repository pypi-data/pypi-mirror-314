# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-02-24 10:14:11
# @Email:
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-02-28 19:06:07
# @Descriptions
import os.path
from .payloadObject import PayloadObject, OutputFolder
from ...shared.utils.general import copy
from ...shared.utils.logger import makelogger

logger = makelogger("transcribed directory loader")


class TranscribedDirPayload(PayloadObject):
    def merge_audio(self, output) -> str:
        for root, dirs, files in os.walk(self.data_files[0]):
            for file in files:
                file_name = os.path.basename(file)
                if file_name == OutputFolder.MERGED_FILE:
                    merged_path = copy(
                        os.path.join(root, file), os.path.join(self.output_dir_struct.media, OutputFolder.MERGED_FILE)
                    )
                    return merged_path
        logger.warning(f"{OutputFolder.MERGED_FILE} is not found")
        return ""

    def stt_transcribe(self):
        print("IN stt transcribe in transcribedDirPayload\n")
        return self.transcription_result.load_result(
            OutputFolder.get_transcribe_dir(self.data_files[0])
        )
