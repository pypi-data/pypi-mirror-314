# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-02-06 15:54:56
# @Description: predefined error message for different reasons when plugin suite is not loaded correctly
from dataclasses import dataclass


@dataclass
class SUITE_REGISTER_MSG:
    """
    a data class that stores the message to report any plugin suite registration error
    """
    INVALID_URL = "The given url is not supported by gailbot\n"
    MODULE_ERROR = "Fail to load import plugin module\n"
    INVALID_INPUT = "The plugin suite source can only be URL, a valid Amazon S3 Bucket name, or path to directory\n"
    TEMPLATE = "ERROR: {cause}\n"
    MISSING = "ERROR: missing file {file}\n"
    FAIL_LOAD_PLUGIN = "ERROR: failed to load plugin {plugin} due to {cause}\n"
    INFO = "INFO: \n"
