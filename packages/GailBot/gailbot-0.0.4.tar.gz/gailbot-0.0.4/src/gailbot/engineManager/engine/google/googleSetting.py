# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-03-29 17:10:22
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-05-10 13:36:14

from pydantic import BaseModel
from typing import List
from gailbot.setting_interface.formItem import FormItem, FormType
from google.cloud.speech_v1p1beta1.types import SpeechAdaptation
from gailbot.setting_interface.formItem import FormItem


class GoogleSetting(BaseModel):
    engine: str
    google_api_key: str
    language_code: str
    enable_separate_recognition_per_channel: bool
    profanity_filter: bool
    enable_word_time_offsets: bool
    enable_word_confidence: bool
    enable_automatic_punctuation: bool
    enable_spoken_punctuation: bool
    enable_spoken_emojis: bool
    use_enhanced: bool
    model: str
    phrase_sets: List[str]
    sample_rate_hertz: int
    
    

    @staticmethod
    def get_setting_config() -> list[FormItem]:
        return [
            FormItem(type=FormType.Selection, name="engine", selection_items=["google"], default_value="google"),
            FormItem(type=FormType.Selection, name="language_code", selection_items=['en-US', 'ar-KW', 'ru-RU', 'sv-SE', 'lt-LT', 'it-CH', 'en-GH', 'en-NZ', 'tn-Latn-ZA', 'ta-LK', 'ar-EG', 'ar-YE', 'kk-KZ', 'bg-BG', 'ar-PS', 'en-CA', 'es-PY', 'ar-JO', 'es-AR', 'es-DO', 'zh-CN', 'es-CR', 'ar-MA', 'uz-UZ', 'sq-AL', 'mn-MN', 'th-TH', 'hr-HR', 'uk-UA', 'rw-RW', 'pa-Guru-IN', 'bs-BA', 'en-SG', 'en-NG', 'hy-AM', 'lv-LV', 'ss-Latn-ZA', 'fr-CA', 'es-CL', 'en-TZ', 'en-IE', 'jv-ID', 'en-PH', 'bn-IN', 'ar-BH', 'ar-IQ', 'it-IT', 'es-PE', 'si-LK', 'te-IN', 'ml-IN', 'en-AU', 'zu-ZA', 'en-HK', 'bn-BD', 'es-ES', 'sw-KE', 'ar-OM', 'es-VE', 'et-EE', 'gu-IN', 'es-SV', 'ar-SY', 'ko-KR', 'tr-TR', 'es-PR', 'hu-HU', 'ur-IN', 'es-NI', 'fi-FI', 'ta-MY', 'ts-ZA', 'vi-VN', 'mr-IN', 'sl-SI', 'en-ZA', 'kn-IN', 'ur-PK', 'es-CO', 'pt-PT', 'de-AT', 'ar-IL', 'en-KE', 'yue-Hant-HK', 'nl-BE', 'ar-MR', 'mk-MK', 'id-ID', 'pl-PL', 'de-DE', 'es-PA', 'ka-GE', 'en-PK', 'ca-ES', 'hi-IN', 'km-KH', 'es-EC', 'eu-ES', 'iw-IL', 'su-ID', 'am-ET', 'fa-IR', 'ms-MY', 've-ZA', 'nl-NL', 'el-GR', 'es-MX', 'lo-LA', 'es-BO', 'en-GB', 'es-US', 'no-NO', 'fil-PH', 'en-IN', 'ar-DZ', 'ar-LB', 'zh-TW', 'gl-ES', 'es-GT', '(SouthAfrica)', 'ro-RO', 'ar-QA', 'ta-SG', 'ar-SA', 'fr-BE', 'ta-IN', 'cs-CZ', 'es-HN', 'my-MM', 'ja-JP', 'af-ZA', 'is-IS', 'ar-TN', 'az-AZ', 'fr-FR', 'pt-BR', 'sr-RS', 'sk-SK', 'da-DK', 'de-CH', 'ne-NP', 'es-UY', 'fr-CH', 'ar-AE', 'xh-ZA', 'sw-TZ'], default_value="en-US"),

            FormItem(type=FormType.File, name="google_api_key"),
            
            # booleans 
            FormItem(type=FormType.OnOff, name="enable_separate_recognition_per_channel", default_value=False),
            FormItem(type=FormType.OnOff, name="profanity_filter", default_value=False),
            FormItem(type=FormType.OnOff, name="enable_word_time_offsets", default_value=False),
            FormItem(type=FormType.OnOff, name="enable_word_confidence", default_value=False),
            FormItem(type=FormType.OnOff, name="enable_automatic_punctuation", default_value=False),
            FormItem(type=FormType.OnOff, name="enable_spoken_punctuation", default_value=False),
            FormItem(type=FormType.OnOff, name="enable_spoken_emojis", default_value=False),
            FormItem(type=FormType.OnOff, name="use_enhanced", default_value=False),

            # multi select
            FormItem(type=FormType.MultiSelect, name="phrase_sets", selection_items=[], default_value=None),

            # Selection 
            FormItem(type=FormType.Selection, name="model", selection_items=["latest_long", "latest_short", "command_and_search", "phone_call", "video", "default", "medical_conversation", "medical_dictation"], default_value="default"), 
            FormItem(type=FormType.Selection, name="sample_rate_hertz", selection_items=[8000, 16000, 22050, 32000, 44100, 48000], default_value=16000),
        ]  
