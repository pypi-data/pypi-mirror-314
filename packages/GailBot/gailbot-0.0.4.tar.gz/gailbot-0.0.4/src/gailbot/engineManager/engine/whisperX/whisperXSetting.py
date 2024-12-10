# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-03-29 17:10:22
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-24 19:03:12
from typing import List
from pydantic import BaseModel

from gailbot.setting_interface.formItem import FormItem, FormType



class WhisperXSetting(BaseModel):
    engine: str = "whisperX"
    output_format: str = "all"
    language: str = "en"
    interpolate_method: str = "nearest"
    min_speakers: int = 2
    max_speakers: int = 2
    temperature: float = 1
    condition_on_previous_text: bool = False
    initial_prompt: str = None
    vad_onset: float = 0.5
    vad_offset: float = 0.363
    chunk_size: int =  30
    no_speech_threshold: float = 0.6

    @staticmethod
    def get_setting_config() -> List[FormItem]:
        return [
            FormItem(type=FormType.Selection, name="engine", selection_items=["whisperX"], default_value="whisperX"),

            FormItem(type=FormType.Selection, name="language", selection_items=["af", "am", "ar", "as", "az", "ba", "be", "bg", "bn", "bo", "br", "bs", "ca", "cs", 
            "cy", "da", "de", "el", "en", "es", "et", "eu", "fa", "fi", "fo", "fr", "gl", "gu", 
            "ha", "haw", "he", "hi", "hr", "hu", "hy", "id", "is", "it", "ja", "jw", "ka", 
            "kk", "km", "kn", "ko", "la", "lb", "ln", "lo", "lt", "lv", "mg", "mi", "mk", 
            "ml", "mn", "mr", "ms", "mt", "my", "ne", "nl", "no", "nn", "oc", "pa", "pl", 
            "ps", "pt", "ro", "ru", "sa", "sd", "si", "sk", "sl", "sn", "so", "sq", "sr", 
            "sv", "sw", "ta", "te", "tg", "th", "tl", "tr", "tt", "uk", "ur", "uz", "vi", 
            "yi", "yo", "yue", "zh"], default_value= "en"),
            FormItem(type=FormType.Selection, name="interpolate_method", selection_items=["nearest", "linear", "ignore"], default_value= "nearest"),
            FormItem(type=FormType.Selection, name="min_speakers", selection_items=[1, 2, 3, 4, 5, 6], default_value= 2),
            FormItem(type=FormType.Selection, name="max_speakers", selection_items=[1, 2, 3, 4, 5, 6], default_value= 2),
            FormItem(type=FormType.Selection, name="temperature", selection_items=[0, 0.25, 0.5, 0.75, 1], default_value= 1),

            ### advanced settings:
            FormItem(type=FormType.OnOff, name="condition_on_previous_text", default_value= False),
            FormItem(type=FormType.Text, name="initial_prompt"),
            FormItem(type=FormType.Selection, name="vad_onset", selection_items=[0, 0.1, 0.2, 0.3, 0.4, 0.5], default_value= 0.5),
            FormItem(type=FormType.Selection, name="vad_offset", selection_items=[0, 0.1, 0.2, 0.363], default_value= 0.363),
            FormItem(type=FormType.Selection, name="chunk_size", selection_items=[5, 10, 15, 20, 25, 30], default_value= 30),
            FormItem(type=FormType.Selection, name="no_speech_threshold", selection_items=[0, 0.3, 0.6, 0.9], default_value= 0.6) #default is 0.6, options are iffy

        ]

    