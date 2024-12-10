# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-02-24 10:13:06
# @Email:
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-07 09:47:25
# @Descriptions: convert a conversation directory source to a singleton list of payload

import os.path
from datetime import datetime
from typing import List

from .converterFun import ConvertFun
from .mediaConverter import MediaConverter
from .converter import Converter, ConverterType
from ..payloadObject import PayloadObject
from ..payloadObject.untranscribedDirPayload import untranscribedDirPayload
from ...profileManager import ProfileObject
from ...shared.utils.general import paths_in_dir, get_name
from ...sourceManager.watcher import Watcher
from ...workspace.directory_structure import TemporaryFolder


class ConversationDirConverter(Converter):
    accepted_forms = ["/"]
    converter_type = ConverterType.ConvDir

    @staticmethod
    def is_accepted_form(path: str):
        if not os.path.isdir(path):
            return False
        supported_format = MediaConverter.accepted_forms
        sub_paths = paths_in_dir(path, supported_format, recursive=False)
        if len(sub_paths) == 0:
            return False
        return True

    @staticmethod
    def convert(
        path: str, output_dir: str, profile: ProfileObject, watchers: List[Watcher]
    ) -> List[PayloadObject]:
        name = get_name(path)
        time = datetime.now().strftime("%H-%M-%S-%f")
        temp_path = TemporaryFolder(f"{name}_{time}")
        accepted_files = paths_in_dir(
            path, MediaConverter.accepted_forms, recursive=False
        )
        data_files = []
        for f in accepted_files:
            data_files.extend(ConvertFun.convert_to_wav(f, temp_path.data_copy))

        return [
            untranscribedDirPayload(
                original_source=path,
                data_files=data_files,
                temp_dir_struct=temp_path,
                output_path=output_dir,
                profile=profile,
                watchers=watchers,
            )
        ]
