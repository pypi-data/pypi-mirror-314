# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-02-24 10:12:37
# @Email:
# @Last Modified by:   Vivian Li 
# @Last Modified time: 2024-03-03 15:13:58
# @Descriptions: convert a transcribed directory source to a singleton list of
#   one payload


import os.path
from datetime import datetime
from typing import List

from .converter import Converter, ConverterType
from ..payloadObject import PayloadObject
from ..payloadObject.transcribedDirPayload import TranscribedDirPayload
from ...profileManager import ProfileObject
from ...shared.utils.general import get_name, copy
from ...shared.utils.logger import makelogger
from ...sourceManager.watcher import Watcher
from ...workspace.directory_structure import OutputFolder, TemporaryFolder

logger = makelogger("converter")


class TranscribedDirConverter(Converter):
    accepted_forms = ["/"]
    converter_type = ConverterType.TranscribedResult

    @staticmethod
    def is_accepted_form(path: str):
        return os.path.isdir(path) and os.path.isfile(
            os.path.join(path, OutputFolder.GB_RESULT_SIGNATURE)
        )

    @staticmethod
    def convert(
            path: str, output_dir: str, profile: ProfileObject, watchers: List[Watcher]
    ) -> List[PayloadObject]:
        name = get_name(path)
        time = datetime.now().strftime("%H-%M-%S")
        temp_path = TemporaryFolder(f"{name}_{time}")
        copy_path = os.path.join(temp_path.data_copy, name)
        copy(path, copy_path)

        return [TranscribedDirPayload(original_source=path,
                                      data_files=[copy_path],
                                      temp_dir_struct=temp_path,
                                      output_path=output_dir,
                                      profile=profile,
                                      watchers=watchers)]
