# -*- coding: utf-8 -*-
# @Author: Joanne Fan
# @Date:   2024-01-26 17:47:47
# @Last Modified by:   Joanne Fan
# @Last Modified time: 2024-02-10 21:01:46

import pytest


@pytest.fixture()
def WATSON_API_KEY():
    WATSON_API_KEY = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
    return WATSON_API_KEY


@pytest.fixture()
def WATSON_REGION():
    WATSON_REGION = "dallas"
    return WATSON_REGION


@pytest.fixture()
def WATSON_BASE_LANG_MODEL():
    WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"
    return WATSON_BASE_LANG_MODEL


@pytest.fixture()
def WATSON_SETTING(WATSON_API_KEY, WATSON_REGION, WATSON_BASE_LANG_MODEL):
    WATSON_SETTING = {
        "engine": "watson",
        "apikey": WATSON_API_KEY,
        "region": WATSON_REGION,
        "base_model": WATSON_BASE_LANG_MODEL
    }
    return WATSON_SETTING


@pytest.fixture()
def WHISPERX_SETTING():
    WHISPERX_SETTING = {
        "engine": "whisperX",
        "language": "English"
    }
    return WHISPERX_SETTING
