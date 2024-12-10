# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-07-24 14:34:21
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
from typing import Dict
import toml


@dataclass
class WatsonConfig(DataclassFromDict):
    """Loads data from the Watson engine configuration"""

    max_file_size_bytes: float = field_from_dict()
    regions_uris: Dict = field_from_dict()
    format_to_content: Dict = field_from_dict()
    defaults: Dict = field_from_dict()
    name: str = field_from_dict()
    workspace: str = field_from_dict()


def load_watson_config(path: str):
    """Loads data from the Watson engine configuration

    Args:
        path (str) : path to the toml file to load
    """
    d = toml.load(path)
    return WatsonConfig.from_dict(d["watson"])
