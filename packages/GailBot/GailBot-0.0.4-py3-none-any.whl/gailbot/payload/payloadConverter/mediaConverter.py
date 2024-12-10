# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-02-24 10:12:13
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-05-10 13:36:52
# @Description : convert a single audio file to a singleton list of one
#                audio payload
from datetime import datetime
from typing import List
from .converterFun import ConvertFun
from ..payloadObject import PayloadObject
from ..payloadObject.untranscribedDirPayload import untranscribedDirPayload
from ...profileManager import ProfileObject
from ...shared.utils.general import get_extension, get_name
from ...sourceManager.watcher import Watcher
from ...workspace.directory_structure import TemporaryFolder
from .converter import Converter, ConverterType


class MediaConverter(Converter):
    accepted_forms = list(ConvertFun.convert_funs.keys())
    converter_type = ConverterType.SingleMedia

    @staticmethod
    def is_accepted_form(path: str) -> bool:
        """
        Return true if path is an audio file with accepted format
        """
        format = get_extension(path)
        return format.lower() in MediaConverter.accepted_forms

    @staticmethod
    def convert(
        path: str, output_dir: str, profile: ProfileObject, watchers: List[Watcher]
    ) -> List[PayloadObject]:
        """
        convert path to a list of one AudioPayloadObject

        Parameters
        ----------
        path
        output_dir
        profile
        watchers

        Returns
        -------
        A list of one audio payload object
        """

        name = get_name(path)
        time = datetime.now().strftime("%m%d_%H_%M_%S_%f")
        temp_path = TemporaryFolder(f"{name}_{time}")
        audio_path: List[str] = ConvertFun.convert_to_wav(path, temp_path.data_copy)

        return [
            untranscribedDirPayload(
                original_source=path,
                data_files=audio_path,
                temp_dir_struct=temp_path,
                output_path=output_dir,
                profile=profile,
                watchers=watchers,
            )
        ]
