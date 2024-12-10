# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-02-15 22:13:22
# @Description: abstract class that defines a list of method must be implemented
#  by a Plugin
from abc import ABC
from typing import Any, Dict
from gailbot.shared.utils.logger import makelogger
from gailbot.pluginSuiteManager.suite.gbPluginMethod import Methods


class Plugin(ABC):
    """
    Abstract class that defines an interface for a plugin
    """

    def __init__(self) -> None:
        self.logger = makelogger(f"Plugin-{self.__class__}")
        self.name = self.__class__
        self.successful = False

    @property
    def is_successful(self) -> bool:
        return self.successful

    def apply(
        self, dependency_outputs: Dict[str, Any], methods: Methods, *args, **kwargs
    ) -> Any:
        """
        Wrapper for plugin algorithm that has access to dependencies =,
        Args:
            dependency_outputs (Dict[str,Any]):
                Mapping from all plugins this plugin is depended on and their
                outputs.
            methods (Methods):
                Methods object that stores data for transcription
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"plugin {self.name}"
