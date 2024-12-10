# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-04-09 17:02:48
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-24 19:08:53
from typing import List
from pydantic import BaseModel

from gailbot.configs import whisper_config_loader
from gailbot.setting_interface.formItem import FormItem, FormType


class WhisperSetting(BaseModel):
    engine: str
    language: str
    detect_speakers: bool = False

    @staticmethod
    def predefined_config():
        config = whisper_config_loader()
        return config

    @staticmethod
    def get_setting_config() -> List[FormItem]:
        return [
            FormItem(type=FormType.OnOff, name="detect_speaker"),
            FormItem(type=FormType.Selection, name="language", selection_items=[]),
        ]  # TODO: get the list of selectable language
