# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-31 16:21:27
# @Last Modified by:   Hannah Shader
# @Last Modified time: 2023-11-20 12:47:28
from abc import ABC, abstractmethod

from typing import Dict

from pydantic import BaseModel

from gailbot.engineManager.engine.engine import Engine


class EngineProvider(ABC):
    """
    A factory class to provide a engine based on the engine setting
    """
    engine: str
    name: str
    data: BaseModel

    @staticmethod
    @abstractmethod
    def load(name: str, data: Dict[str, str]):
        raise NotImplementedError()

    @abstractmethod
    def make_engine(self) -> Engine:
        raise NotImplementedError()

    @abstractmethod
    def is_cpu_intensive(self) -> bool:
        raise NotImplementedError()

    def engine_data(self) -> Dict[str, str]:
        return self.data.model_dump()
