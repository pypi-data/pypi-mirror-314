# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-03-30 11:57:13
# @Last Modified by:   Vivian Li 
# @Last Modified time: 2024-05-03 17:16:44
import os.path
from typing import Dict, Optional

from gailbot.engineManager.engine.engine import Engine
from gailbot.engineManager.engine.engineProvider import EngineProvider
from gailbot.engineManager.engine.google import Google
from gailbot.engineManager.engine.google.googleSetting import GoogleSetting
from gailbot.shared.utils.general import make_dir, copy
from gailbot.shared.utils.logger import makelogger
from gailbot.workspace import WorkspaceManager

logger = makelogger("google setting")


class GoogleProvider(EngineProvider):
    workspace = os.path.join(WorkspaceManager.engine_src, "google/api")

    def is_cpu_intensive(self) -> bool:
        return False

    @staticmethod
    def load(name, data: Dict[str, str]) -> Optional[EngineProvider]:
        try:
            engine = GoogleProvider(name, data)
            assert engine.data.engine.lower() == "google"
            return engine
        except Exception as e:
            logger.warning(e)
            return None

    def __init__(self, name, data: Dict[str, str]):
        if not os.path.isdir(self.workspace):
            make_dir(self.workspace)
        self.name = name
        self.data: GoogleSetting = GoogleSetting(**data)
        assert Google.is_valid_google_api(self.data.google_api_key)
        copied_path = os.path.join(
            self.workspace, os.path.basename(self.data.google_api_key)
        )
        if not os.path.isfile(copied_path):
            copy(src_path=self.data.google_api_key, tgt_path=copied_path)

        self.data.google_api_key = copied_path

    def make_engine(self) -> Engine:
        return Google(self.data)
