# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-07-24 14:34:19
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
from typing import Dict
import toml


@dataclass
class GoogleConfig(DataclassFromDict):
    """Loads data from the Google STT configuration"""

    defaults: Dict = field_from_dict()
    name: str = field_from_dict()
    workspace: str = field_from_dict()
    maximum_size: int = field_from_dict()
    maximum_duration: int = field_from_dict()


def load_google_config(path: str):
    """
    Loads data from the Google STT configuration

    Args:
        path (str) : path to the toml file to load
    """
    d = toml.load(path)
    return GoogleConfig.from_dict(d["google"])
