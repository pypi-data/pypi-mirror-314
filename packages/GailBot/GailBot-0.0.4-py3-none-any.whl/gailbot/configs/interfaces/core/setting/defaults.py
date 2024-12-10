# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Lakshita Jain
# @Last Modified time: 2023-12-07 12:45:12
from dataclasses import dataclass
import os
from dict_to_dataclass import field_from_dict, DataclassFromDict
from typing import Dict, List
import toml


@dataclass
class PluginDefault(DataclassFromDict):
    suite: str = field_from_dict()
    apply_plugins: List[str] = field_from_dict()


@dataclass
class EngineDefault(DataclassFromDict):
    name: str = field_from_dict()
    whisper: Dict = field_from_dict()
    watson: Dict = field_from_dict()


@dataclass
class Default(DataclassFromDict):
    def __init__(self, plugin: PluginDefault, engine: EngineDefault) -> None:
        self.plugin: PluginDefault = plugin
        self.engine: EngineDefault = engine


def load_default_config(path: str):
    d = toml.load(path)
    engine = EngineDefault.from_dict(d["engine"])
    plugin = PluginDefault.from_dict(d["plugins"])
    return Default(plugin, engine)
