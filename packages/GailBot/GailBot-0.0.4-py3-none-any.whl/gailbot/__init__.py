# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-06 14:55:34
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-09 23:46:44


__version__ = "0.0.4"

## must export Plugin, Methods and GBPluginMethods
from .api import GailBot
from gailbot.shared.exception.serviceException import (
    SourceAddError,
    SourceNotFound,
    FailPluginSuiteRegister,
    PluginSuiteNotFound,
    ProfileNotFound,
    RemoveInUseError,
    EngineNotFound,
    DuplicateProfile,
    DuplicateEngine,
    DuplicatePlugin,
)
from gailbot.sourceManager.sourceObject import SourceObject
from gailbot.pluginSuiteManager.suite.plugin import Plugin
from gailbot.pluginSuiteManager.suite.gbPluginMethod import GBPluginMethods, Methods
from gailbot.shared.exception.gbException import GBException
from gailbot.profileManager.profileManager import ProfileSetting
from gailbot.payload.payloadConverter import ConverterType
