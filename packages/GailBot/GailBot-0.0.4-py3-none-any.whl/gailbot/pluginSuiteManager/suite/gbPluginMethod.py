# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-02-06 16:03:16
# @Description: This is initially an abstract class that declare a set of function
# needs to be implemented for any  plugin method, currently, there is only one
# GBPluginMethods
import os
from dataclasses import dataclass
from typing import List, Dict, Union, Any

from gailbot.engineManager.engine.engine import UttDict
from gailbot.shared.utils.general import write_csv, write_toml, write_yaml, write_json, write_txt, get_name
from gailbot.shared.utils.logger import makelogger

logger = makelogger("Plugin Method")


class Methods:
    """
    Methods that will be passed to a plugin.
    These can be custom defined and may be useful as
    a wrapper around objects
    that may want to be passed to a plugin.
    """

    def __init__(self):
        pass


class UttObj:
    def __init__(self, start: float | str, end: float | str, speaker, text):
        self.start = float(start)
        self.end = float(end)
        self.speaker = speaker
        self.text = text


@dataclass(init=True)
class GBPluginMethods(Methods):
    work_path: str
    out_path: str
    data_files: List[str]
    merged_media: str
    utterances: Dict[str, List[UttDict]]

    @property
    def format_to_out_fun(self):
        return {
            "csv": write_csv,
            "toml": write_toml,
            "yaml": write_yaml,
            "json": write_json,
            "txt": write_txt,
        }

    @property
    def temp_work_path(self):
        return self.work_path

    @property
    def output_path(self):
        return self.out_path

    @property
    def filenames(self):
        return [get_name(file) for file in self.data_files]

    def get_utterance_objects(self) -> Dict[str, List[UttObj]]:
        """
        Access and return the utterance data as utterance object
        """
        res = dict()
        for key, uttlist in self.utterances.items():
            newlist = list()
            for utt in uttlist:
                # Convert speaker to string, handle None case

                utt["speaker"] = (
                    str(utt["speaker"]) if utt["speaker"] is not None else "speaker_00"
                )
                newlist.append(UttObj(**utt))
            res[key] = newlist
        return res

    def save_item(
            self,
            data: Union[Dict[str, Any], List],
            name: str,
            temporary: bool = True,
            output_format: str = "json",
            fun: callable = None,
            kwargs=None,
    ) -> bool:
        """
        function provided for the plugin to save file

        Args:
            data (Union[Dict[str, Any], List]): the data that will be outputed
            name (str): the name of the output file
            temporary (bool, optional): if true, the file will be stored in
                                        temporary folder and discarded once the
                                        analysis process finishes. Defaults to True.
            output_format (str, optional): the format of the output file. Defaults to "json".
            fun (callable, optional): user defined function to write the
                                      output. Defaults to None.
            kwargs (dict, optional): user defined key word arguments that will
                                    be passed into user defined function.
                                    Defaults to None.

        Returns:
            bool: return true if the plugin is registered successfully , false otherwise
        """
        path = (
            os.path.join(self.work_path, name + "." + output_format)
            if temporary
            else os.path.join(self.out_path, name + "." + output_format)
        )
        if fun:
            try:
                fun(path, data, **kwargs)
                return True
            except Exception as e:
                logger.error(e, exc_info=e)
                return False
        if output_format not in self.format_to_out_fun:
            logger.error("the output format is not supported")
            return False
        try:
            self.format_to_out_fun[output_format](path, data)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
