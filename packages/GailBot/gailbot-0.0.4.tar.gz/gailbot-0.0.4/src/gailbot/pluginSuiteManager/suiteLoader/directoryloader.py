# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Vivian Li 
# @Last Modified time: 2024-02-13 19:48:09
import os
import sys

import pip
from cryptography.fernet import Fernet
from typing import List, Optional, TextIO

from .pluginSuiteLoader import PluginSuiteLoader
from gailbot.shared.utils.logger import makelogger
from gailbot.shared.utils.general import (
    get_name,
    copy,
    read_toml,
    is_directory,
    delete,
)
from gailbot.config_backend import PROJECT_ROOT
from gailbot.configs import PLUGIN_CONFIG
from pydantic import ValidationError

from ..error.errorMessage import SUITE_REGISTER_MSG
from ..suite.pluginData import ConfModel
from ..suite.suite import PluginSuite

logger = makelogger("plugin directory loader")


class PluginDirectorySuiteLoader(PluginSuiteLoader):
    """load the plugin suite from a directory that contains all source
    script implementing the plugins, and a toml file that stores
    configuration information to load the plugin
    """

    def __init__(
        self,
        suites_dir: str,
    ):
        """initialize a plugin directory loader

        Args:
            suites_dir (str): the path to the directory that stores all the
                              copies of plugins will be stored and managed
                              by plugin manager
        """
        self.suites_dir = suites_dir

    def load(self, suite_dir_path: str, f: TextIO) -> List[PluginSuite]:
        """load a plugin suite directory in"""
        missing_file = False
        if (not isinstance(suite_dir_path, str)) or (not is_directory(suite_dir_path)):
            return []

        suite_dir_name = get_name(suite_dir_path)
        tgt_path = os.path.join(self.suites_dir, get_name(suite_dir_path))
        config = None
        requirement = None
        official = None

        # search for the requirements and config file
        for root, dirs, files in os.walk(suite_dir_path):
            if PLUGIN_CONFIG.REQUIREMENT in files:
                requirement = os.path.join(root, PLUGIN_CONFIG.REQUIREMENT)
            if PLUGIN_CONFIG.CONFIG in files:
                config = os.path.join(root, PLUGIN_CONFIG.CONFIG)
            if PLUGIN_CONFIG.OFFICIAL in files:
                official = os.path.join(root, PLUGIN_CONFIG.OFFICIAL)
            if config and requirement and official:
                break
        
        if not config:
            e = SUITE_REGISTER_MSG.MISSING.format(file=PLUGIN_CONFIG.CONFIG)
            logger.error(e)
            f.write(e)
            missing_file = True


        if missing_file:
            return []

        # download required package
        try:
            if requirement:
                assert self.download_packages(requirement, PROJECT_ROOT)
        except Exception as e:
            logger.error(e, exc_info=True)
            f.write(
                SUITE_REGISTER_MSG.TEMPLATE.format(
                    cause="fail to download plugin suite dependency"
                )
            )
            return []

        # make a copy of the original plugin suite

        # NOTE: when the tgt_path already exists, will remove tgt_path
        if not is_directory(tgt_path):
            copy(suite_dir_path, tgt_path)
        elif os.path.samefile(tgt_path, suite_dir_path):
            pass
        else:
            delete(tgt_path)
            copy(suite_dir_path, tgt_path)
        sys.path.append(tgt_path)

        suite = self.load_suite_from_toml(config, suite_dir_name, self.suites_dir, f)
        if suite:
            # validate
            if self.validate_official(official):
                suite.set_to_official_suite()
            return [suite]
        else:
            sys.path.pop()
            # TODO: why??? delete(tgt_path)
            return []

    def download_packages(self, req_file, dest):
        """download packages listed under req_file to dest

        Args:
            req_file(str): a string that specifies the path to requirements.txt file
            dest (str): a string to the directory where the file will be downloaded

        Returns:
            return true if the package is downloaded successfully, else return false
        """
        if hasattr(pip, "main"):
            pip.main(["install", "-t", str(dest), "-r", req_file])
            return True
        else:
            return False

    def validate_official(self, file):
        """
        Returns:
            bool: return true if the key matches with the official gailbot plugin
        """
        if not file:
            return False
        try:
            with open(file, "r") as f:
                key = f.read()
            fernet = Fernet(PLUGIN_CONFIG.OFFICIAL_ENKEY)

            decrypt = fernet.decrypt(key)

            if decrypt == PLUGIN_CONFIG.OFFICIAL_KEY:
                return True
            else:
                return False
        except Exception as e:
            logger.error(e, exc_info=e)
            return False

    def load_suite_from_toml(
        self, conf_path: str, suite_name: str, suites_directory: str, f: TextIO
    ) -> Optional[PluginSuite]:
        """given the path to configuration file of one plugin suite, and
             the suites directory that stores all plugin suites ,
             import the plugin suite described in the configuration file

        Returns:
            PluginSuite:
        """
        conf = read_toml(conf_path)
        try:
            conf_model = ConfModel(**conf)
        except ValidationError as e:
            f.write(
                SUITE_REGISTER_MSG.TEMPLATE.format(
                    cause=f" failed to validate configuration file structure due to {e}"
                )
            )
            logger.error(
                f"plugin suite config.toml does not follow the file structure."
            )
            return None
        if conf_model.suite.name != suite_name:
            e = f"suite directory and configuration file should use the same suite name."
            f" {conf_model.suite.name} and {suite_name} are different"
            f.write(SUITE_REGISTER_MSG.TEMPLATE.format(cause=e))

        # TODO: download all plugins that are part of the suite to general plugins folder HERE
        try:
            print("about to return plugin suite from load toml\n")
            return PluginSuite(conf_model, suites_directory)
        except Exception as e:
            print("error here 201 directory loder\n")
            logger.error(e, exc_info=True)
            f.write(SUITE_REGISTER_MSG.TEMPLATE.format(cause=e))
            return None
