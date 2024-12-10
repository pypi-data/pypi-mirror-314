# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-08-01 05:34:30
from typing import List
from abc import ABC
from gailbot.pluginSuiteManager.suite.suite import PluginSuite


class PluginSuiteLoader(ABC):
    """base class for plugin loader"""

    def load(self, *args, **kwargs) -> List[PluginSuite]:
        """
        Returns:
            a list of valid plugin suite, return empty list if no valid plugin suite is loaded
        """
        raise NotImplementedError()
