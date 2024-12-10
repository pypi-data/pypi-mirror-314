# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-03-29 17:10:22
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-02 18:27:19
from typing import Dict, Optional

from gailbot.engineManager.engine.engineProvider import EngineProvider
from gailbot.engineManager.engine.whisperX.whisperX import WhisperX
from gailbot.engineManager.engine.whisperX.whisperXSetting import WhisperXSetting
from gailbot.shared.utils.logger import makelogger


class WhisperXProvider(EngineProvider):
    @staticmethod
    def load(name, data: Dict[str, str]) -> Optional[EngineProvider]:
        try:
            engine = WhisperXProvider(name, data)
            assert engine.data.engine.lower() == "whisperx"
            return engine
        except Exception as _:
            return None

    def __init__(self, name, data: Dict[str, str]):
        self.data: WhisperXSetting = WhisperXSetting(**data)
        self.name = name

    def make_engine(self) -> WhisperX:
        return WhisperX(self.data)

    def is_cpu_intensive(self) -> bool:
        return True
