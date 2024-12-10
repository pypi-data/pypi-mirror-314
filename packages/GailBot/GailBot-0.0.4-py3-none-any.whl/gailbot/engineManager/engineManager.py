# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-25 18:14:59
# @Last Modified by:   Vivian Li 
# @Last Modified time: 2024-05-03 17:16:02
import os
import platform
from typing import Dict
from gailbot.shared.exception.serviceException import (
    EngineNotFound,
    DuplicateProfile,
    RemoveDefaultEngine,
)
from gailbot.engineManager.engine.google.googleSetting import GoogleSetting
from gailbot.engineManager.engine.watson.watsonSetting import WatsonSetting
from gailbot.engineManager.engine.whisperX.whisperXSetting import WhisperXSetting
from gailbot.engineManager.engine.engineProvider import EngineProvider
from gailbot.engineManager.engine.google.googleProvider import GoogleProvider
from gailbot.engineManager.engine.watson.watsonProvider import WatsonProvider
from gailbot.engineManager.engine.whisper.whisperProvider import WhisperProvider
from gailbot.engineManager.engine.whisperX.whisperXProvider import WhisperXProvider
from gailbot.setting_interface.formItem import FormItem
from gailbot.shared.utils.logger import makelogger
from gailbot.shared.utils.general import (
    is_file,
    delete,
    write_toml,
    paths_in_dir,
    get_name,
    read_toml,
    make_dir,
)


class EngineManager:
    engine_provider = {
        "google": GoogleProvider,
        "watson": WatsonProvider,
        "whisper": WhisperProvider,
        "whisperX": WhisperXProvider,
    }
    default_name = "Default"
    default_data = {"engine": "whisperX", "language": "en"}
    logger = makelogger("engine-manager")

    def __init__(self, workspace: str):
        self.workspace = workspace
        if not os.path.isdir(self.workspace):
            make_dir(self.workspace)
        self._engine_providers: Dict[str, EngineProvider] = dict()
        try:
            self._load_existing_setting()
            self._load_default_setting()
        except Exception as e:
            self.logger.error(e, exc_info=True)

    def _load_default_setting(self):
        if not self.is_engine(self.default_name):
            self.add_engine(self.default_name, self.default_data)

    def _load_existing_setting(self):
        files = paths_in_dir(self.workspace, ["toml"])
        for file in files:
            name = get_name(file)
            data = read_toml(file)
            if not self._load_engine(name, data):
                # remove the file if engine is not loaded successfully
                delete(file)

    def _load_engine(self, name: str, data: Dict[str, str]) -> EngineProvider | None:
        eng_prov = EngineManager.engine_provider[data["engine"]]
        engine = eng_prov.load(name, data)
        if engine:
            self._engine_providers[name] = engine
            return engine
        self.logger.error("not a valid engine")
        return None

    def is_engine(self, name: str) -> bool:
        return name in self._engine_providers

    def add_engine(self, name: str, data: Dict[str, str]) -> bool:
        if self.is_engine(name):
            raise DuplicateProfile(name)
        loaded_engine = self._load_engine(name, data)
        if loaded_engine:
            path = os.path.join(self.workspace, f"{name}.toml")
            if is_file(path):
                delete(path)
            write_toml(path=path, data=dict(loaded_engine.data))
            return True
        else:
            return False

    def remove_engine(self, name: str):
        if name not in self._engine_providers:
            raise EngineNotFound(name)
        if name == self.default_name:
            raise RemoveDefaultEngine()
        else:
            path = os.path.join(self.workspace, f"{name}.toml")
            if is_file(path):
                delete(path)
            del self._engine_providers[name]

    def update_engine(self, name: str, new_data: Dict[str, str]) -> bool:
        if name not in self._engine_providers:
            raise EngineNotFound(name)
        else:
            path = os.path.join(self.workspace, f"{name}.toml")
            if is_file(path):
                delete(path)
            del self._engine_providers[name]
        return self.add_engine(name, new_data)

    def get_engine_provider(self, name: str) -> EngineProvider:
        if not self.is_engine(name):
            raise EngineNotFound(name)
        else:
            return self._engine_providers[name]

    def get_engine_setting(self, name) -> Dict[str, str]:
        return self.get_engine_provider(name).engine_data()

    @property
    def available_engines(self):
        return list(self._engine_providers.keys())
    
    
def get_engine_formItem() -> Dict[str, FormItem]:
   
    return {"google": GoogleSetting.get_setting_config(),
            "watson": WatsonSetting.get_setting_config(),
            "whisperX": WhisperXSetting.get_setting_config()}
