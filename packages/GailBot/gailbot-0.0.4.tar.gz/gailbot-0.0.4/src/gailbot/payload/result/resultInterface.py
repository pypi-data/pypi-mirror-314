# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-08-01 05:38:05
from typing import Dict
from .processingStatus import ProcessingStats
from gailbot.shared.utils.logger import makelogger
from gailbot.shared.utils.general import write_json

logger = makelogger("result_interface")
""" .pickle , use efficient way to save the file """


class ResultInterface:
    """
    Defines a class containing the logic for transcription, format, and analysis results
    """

    def __init__(self, workspace: str, data=None) -> None:
        self.workspace = workspace
        self.data = data
        self.processingStats = None

    def set_processing_stats(self, stats: ProcessingStats):
        """
        Sets an object's processing stats

        Args:
            stats: ProcessingStats: ProcessingStats to set

        Returns:
            bool: True if successfully set, false if not
        """
        try:
            assert stats
            self.processingStats: ProcessingStats = stats
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False

    def output_processing_stats(self, output: str):
        """
        Outputs an object's processing stats to the output directory

        Args:
            output: str: Path of the output directory

        Returns:
            bool: True if successfully set, false if not
        """
        try:
            write_json(output, self.processingStats.__dict__)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False

    def save_data(self, data) -> bool:
        raise NotImplementedError

    def output(self, path: str) -> bool:
        raise NotImplementedError

    def get_data(self) -> Dict:
        raise NotImplementedError
