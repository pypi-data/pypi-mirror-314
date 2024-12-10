# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-08-01 05:37:45
from typing import TypedDict, Dict, List

from .resultInterface import ResultInterface
from gailbot.shared.utils.logger import makelogger

logger = makelogger("analysis-result")


class AnalysisResultDict(TypedDict):
    plugin_suite: str
    success: List[str]
    failure: List[str]


class AnalysisResult(ResultInterface):
    """
    Defines a class for the analysis result
    """

    def __init__(self, workspace: str):
        super().__init__(workspace)
        self.data: Dict[str, AnalysisResultDict] = dict()

    def save_data(self, data) -> bool:
        """
        Saves the result data

        Args:
            data: [AnalysisResultDict]: data to save, in the form
            of a dictionary mapping strings to analysis results

        Returns:
            Bool: True if successfully saved, false if not
        """
        self.data = data
        return True

    def output(self, path) -> bool:
        """NOTE: currently no data for analysis will be written"""
        try:
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return True

    def get_data(self):
        """
        Accesses object's data

        Returns:
            Data in the form Dict[str, AnalysisResultDict]
        """
        return self.data

    def get_serialized_data(self):
        return {str(k): str(v) for k, v in self.data.items()}
