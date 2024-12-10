# -*- coding: utf-8 -*-
# @Author: Vivian Li 
# @Date:   2024-03-29 17:10:22
# @Last Modified by:   Vivian Li 
# @Last Modified time: 2024-04-02 18:26:36
from typing import Dict, Optional

from gailbot.engineManager.engine.engine import Engine
from gailbot.engineManager.engine.engineProvider import EngineProvider
from gailbot.engineManager.engine.whisper import Whisper
from gailbot.engineManager.engine.whisper.whisperSetting import WhisperSetting


class WhisperProvider(EngineProvider):

    @staticmethod
    def load(name, data: Dict[str, str]) -> Optional[EngineProvider]:
        try:
            engine = WhisperProvider(name, data)
            assert engine.data.engine.lower() == "whisper"
            return engine
        except Exception as e:
            return None

    def __init__(self, name, data: Dict[str, str]):
        self.name = name
        self.data: WhisperSetting = WhisperSetting(**data)

    def make_engine(self) -> Engine:
        return Whisper(self.data)

    def is_cpu_intensive(self) -> bool:
        return True
