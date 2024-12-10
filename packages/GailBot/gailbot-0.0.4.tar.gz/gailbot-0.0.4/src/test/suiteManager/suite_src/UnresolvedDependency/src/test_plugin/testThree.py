# -*- coding: utf-8 -*-
# @Author: Hannah Shader, Jason Wu, Jacob Boyar
# @Date:   2023-06-27 12:16:07
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-02-17 08:57:01
from gailbot import Plugin
from gailbot import GBPluginMethods
from typing import Dict, Any


###############################################################################
# CLASS DEFINITIONS                                                           #
###############################################################################
class TestThree(Plugin):
    """
    Wrapper class for the Gaps plugin. Contains functionality that inserts
    gap markers
    """

    def __init__(self) -> None:
        super().__init__()
        """
        Initializes the gap plugin

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        """
        Parameters
        ----------
        dependency_outputs: a list of dependency outputs
        methods: the methods being used, currently GBPluginMethods

        Returns
        -------
        A structure interact instance
        """
        self.successful = True
        return "TestThree"
