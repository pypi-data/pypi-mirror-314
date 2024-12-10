# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 15:37:50
# @Last Modified by:   Vivian Li
# @Description: provide function to load dataclasses that stores gailbot
# configuration data, which are parsed form raw toml file stored in
# ./config_backend

from .interfaces import (
    watson_config_loader,
    google_config_loader,
    whisper_config_loader,
    log_config_loader,
    workspace_config_loader,
    service_config_loader,
    default_setting_loader,
    PATH,
    PROJECT_ROOT,
    TemporaryFolder,
    OutputFolder,
    PLUGIN_CONFIG,
    get_format_md_path,
)
