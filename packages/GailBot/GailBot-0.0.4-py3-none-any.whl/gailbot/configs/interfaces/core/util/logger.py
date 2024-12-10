# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-07-24 14:34:31
import os
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml


@dataclass
class LogConfig(DataclassFromDict):
    formatter: str = field_from_dict()
    sub_dir_prefix: str = field_from_dict()
    log_dir: str = field_from_dict()


def load_log_config(path):
    d = toml.load(path)
    return LogConfig.from_dict(d["log"])
