# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-08-01 05:37:54
from typing import TypedDict, Dict, Any
from .resultInterface import ResultInterface
from gailbot.configs import get_format_md_path
from gailbot.shared.utils.general import copy
from gailbot.shared.utils.logger import makelogger

logger = makelogger("format_result")


class FormatResultDict(TypedDict):
    process_stats: Dict[str, str]


class FormatResult(ResultInterface):
    """
    Defines a class for the format result
    """

    def __init__(self, workspace: str, data: Dict[str, Any] = None) -> None:
        super().__init__(workspace, data)
        self.data = data

    def save_data(self, data: Dict[str, Any]):
        """
        Saves the inputted data

        Args:
            data: Dict[str, ProcessingStats]: data to save, in the form
            of a dictionary mapping strings to processing stats

        Returns:
            Bool: True if successfully saved, false if not
        """
        try:
            self.data = data
            return True
        except Exception as e:
            return False

    def get_data(self):
        """
        Accesses and object's data

        Returns:
            Data in the form Dict[str, ProcessingStats]
        """
        return self.data

    def output(self, path: str) -> bool:
        """TODO: currently no data will be written as format result"""
        try:
            FORMAT_MD = get_format_md_path()
            copy(FORMAT_MD, path)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
