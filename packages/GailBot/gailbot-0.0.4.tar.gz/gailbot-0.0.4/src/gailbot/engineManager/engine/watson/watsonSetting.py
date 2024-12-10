# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-04-24 19:17:48
# @Last Modified by:   Sophie Clemens, Dan Bergen, Eva Caro
# @Last Modified time: 2024-05-28 14:34:00
from typing import List
from pydantic import BaseModel
from gailbot.setting_interface.formItem import FormItem, FormType
from gailbot.setting_interface.formItem import FormItem
from gailbot.engineManager.engine.watson.lm import WatsonLMInterface


class WatsonSetting(BaseModel):
    engine: str
    apikey: str
    region: str
    base_model: str
    custom_model: str
    
    ssl_verification: bool
    interim_results: bool
    word_confidence: bool
    timestamps: bool
    profanity_filter: bool
    smart_formatting: bool
    redaction: bool
    processing_metrics: bool
    audio_metrics: bool
    split_transcript_at_phrase_end: bool
    language_customization_id: str = None
    acoustic_customization_id: str = None

    inactivity_timeout: int
    keyword_threshold: float
    max_alternatives: int
    processing_metrics_interval: float
    end_of_phrase_silence_time: float
    speech_detector_sensitivity: float
    background_audio_supression: float

    @staticmethod
    def get_setting_config() -> List[FormItem]:

        return [ 
            FormItem(type=FormType.Selection, name="engine", selection_items=["watson"]),
            FormItem(type=FormType.Text, name="apikey"),
            FormItem(type=FormType.Selection, name="region", selection_items=["dallas", "washington", "frankfurt", "sydney", "tokyo", "london", "seoul"]),
            FormItem(type=FormType.Selection, name="base_model", selection_items=['en-US_BroadbandModel', 'pt-BR_BroadbandModel', 'ja-JP_BroadbandModel', 'es-CL_BroadbandModel', 'es-MX_BroadbandModel', 'zh-CN_BroadbandModel', 'es-ES_BroadbandModel', 'es-CO_BroadbandModel', 'en-US_Telephony', 'es-AR_BroadbandModel', 'es-PE_BroadbandModel', 'it-IT_Telephony', 'en-GB_BroadbandModel', 'nl-NL_NarrowbandModel', 'ko-KR_Multimedia', 'en-GB_NarrowbandModel', 'hi-IN_Telephony', 'sv-SE_Telephony', 'ar-MS_BroadbandModel', 'ja-JP_Multimedia', 'nl-NL_Multimedia', 'nl-NL_Telephony', 'pt-BR_Telephony', 'it-IT_Multimedia', 'fr-FR_BroadbandModel', 'de-DE_NarrowbandModel', 'it-IT_BroadbandModel', 'ko-KR_NarrowbandModel', 'en-GB_Telephony', 'en-US_Multimedia', 'es-PE_NarrowbandModel', 'de-DE_BroadbandModel', 'en-AU_Multimedia', 'es-ES_Telephony', 'en-AU_BroadbandModel', 'fr-CA_NarrowbandModel', 'de-DE_Telephony', 'es-LA_Telephony', 'ja-JP_NarrowbandModel', 'de-DE_Multimedia', 'nl-NL_BroadbandModel', 'es-CO_NarrowbandModel', 'en-GB_Multimedia', 'ko-KR_BroadbandModel', 'en-US_ShortForm_NarrowbandModel', 'es-MX_NarrowbandModel', 'fr-CA_BroadbandModel', 'cs-CZ_Telephony', 'es-ES_NarrowbandModel', 'es-CL_NarrowbandModel', 'fr-CA_Multimedia', 'fr-FR_Telephony', 'fr-FR_NarrowbandModel', 'en-AU_NarrowbandModel', 'en-US_NarrowbandModel', 'en-WW_Medical_Telephony', 'es-AR_NarrowbandModel', 'zh-CN_Telephony', 'it-IT_NarrowbandModel', 'pt-BR_NarrowbandModel', 'en-AU_Telephony', 'ko-KR_Telephony', 'fr-FR_Multimedia', 'es-ES_Multimedia', 'en-IN_Telephony', 'ja-JP_Telephony', 'zh-CN_NarrowbandModel', 'ar-MS_Telephony', 'fr-CA_Telephony', 'pt-BR_Multimedia', 'nl-BE_Telephony'], default_value= "en-US_BroadbandModel"),
            FormItem(type=FormType.Selection, name="custom_model", selection_items=["None"]),

            # Booleans
            FormItem(type=FormType.OnOff, name="ssl_verification", default_value= False),
            FormItem(type=FormType.OnOff, name="interim_results", default_value= False),
            FormItem(type=FormType.OnOff, name="word_confidence", default_value= False),
            FormItem(type=FormType.OnOff, name="timestamps", default_value= False),
            FormItem(type=FormType.OnOff, name="profanity_filter", default_value= True),
            FormItem(type=FormType.OnOff, name="smart_formatting", default_value= False),
            FormItem(type=FormType.OnOff, name="redaction", default_value= False),
            FormItem(type=FormType.OnOff, name="processing_metrics", default_value= False),
            FormItem(type=FormType.OnOff, name="audio_metrics", default_value= False),
            FormItem(type=FormType.OnOff, name="split_transcript_at_phrase_end", default_value= True),
            # Select
            FormItem(type=FormType.Selection, name="inactivity_timeout", selection_items=[-1, 0, 1, 5, 10, 30], default_value= 30),
            FormItem(type=FormType.Selection, name="keyword_threshold", selection_items=[0.1, 0.5, 0.8, 0.9], default_value= None),
            FormItem(type=FormType.Selection, name="max_alternatives", selection_items=[1, 2, 3], default_value= 1),
            FormItem(type=FormType.Selection, name="processing_metrics_interval", selection_items=[0.5, 1.0, 2.0], default_value= None),
            FormItem(type=FormType.Selection, name="end_of_phrase_silence_time", selection_items=[0.5, 0.8, 1.0], default_value= 0.8),
            FormItem(type=FormType.Selection, name="speech_detector_sensitivity", selection_items=[0.3, 0.5, 0.7], default_value= 0.5),
            FormItem(type=FormType.Selection, name="background_audio_supression", selection_items=[0.0, 0.1, 0.2]),
    
        ]
    