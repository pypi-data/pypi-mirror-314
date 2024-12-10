# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:01
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-21 14:21:16
# @Description: PluginManger stores available plugin suites in a map from suite
# name to PluginSuite object, and provides method to load, delete, and reload
# plugin suite
import platform
import shutil

import sys
import os
from datetime import datetime
from typing import List, Dict
from gailbot.pluginSuiteManager.S3BucketManager import S3BucketManager

from gailbot.shared.exception.serviceException import (
    FailReportError,
    PluginSuiteNotFound,
    RemoveOfficialPlugin,
)
from gailbot.shared.utils.download import is_internet_connected
from gailbot.shared.utils.logger import makelogger
from gailbot.shared.utils.general import (
    get_subfiles,
    make_dir,
    subdirs_in_dir,
    delete,
    get_name,
    is_directory,
    num_subdirs,
)
from gailbot.configs.interfaces import get_plugin_structure_config
from gailbot.configs import PLUGIN_CONFIG
from gailbot.pluginSuiteManager.suite.suite import PluginSuite
from gailbot.pluginSuiteManager.suiteLoader import (
    PluginDirectorySuiteLoader,
    PluginURLSuiteLoader,
    PluginSuiteLoader,
)
from gailbot.pluginSuiteManager.suite.pluginData import Suite

EXPECTED_STRUCTURE = get_plugin_structure_config()
logger = makelogger("plugin_manager")


class PluginSuiteManager:
    """
    Manage multiple plugins suites that can be registered, including
    storing the plugin files, parsing the config files, and instantiating
    plugin objects from files.
    """

    def __init__(self, workspace: str):
        """
        Args:
        workspace (str) : the path to plugin workspace
        loading_existing: if true, load the existing plugin from plugin workspace
        """

        self.workspace = workspace
        self._init_workspace()
        self.suites = dict()
        self.logs = dict()  # map source string to registration log
        self.loaders: List[PluginSuiteLoader] = [
            PluginURLSuiteLoader(self.download_dir, self.suites_dir),
            PluginDirectorySuiteLoader(self.suites_dir),
        ]

        # download all the suites in HiLab bucket upon first launch of gailbot
        try:
            self._load_existing_suite_from_workspace()
            if num_subdirs(self.suites_dir) == 0 and is_internet_connected():
                self._load_hilab_bucket_suite()  # NOTE: This is a special case to preload hilab suite bucket
        except Exception as e:
            logger.error(e, exc_info=True)
        self.paths_to_existing_suites = subdirs_in_dir(self.suites_dir, recursive=True)

    def _load_existing_suite_from_workspace(self):
        #TODO: this function currently downloads all the suites in self.suites_dir, 
        # but we need it to only download the default HiLabSuite and gb_hilab_suite
        # or we can change it to take in the name of the suite to download
        
        subdirs = subdirs_in_dir(self.suites_dir, recursive=False)
        directory_loader = PluginDirectorySuiteLoader(self.suites_dir)

        for plugin_source in subdirs:
            register_file = os.path.join(
                self.log_dir, "log" + datetime.now().strftime("%m-%d-%H-%M-%f")
            )
            self.logs[plugin_source] = register_file
            f = open(register_file, "a")
            suites = directory_loader.load(plugin_source, f=f)
            if not suites:
                logger.error(f"{get_name(plugin_source)} cannot be registered")
            else:
                for suite in suites:
                    if isinstance(suite, PluginSuite):
                        self.suites[suite.name] = suite
            f.close()

    def _load_hilab_bucket_suite(self):
        try:
            self.register_suite(PLUGIN_CONFIG.HILAB_BUCKET)
        except Exception as e:
            logger.error(e, exc_info=e)

    # Returns true if aws has a newer version of the given suite. Otherwise,
    # false.
    def has_new_version(self, suite_name) -> bool:
        if not is_internet_connected():
            return False
        try:
            bucket_metadata = S3BucketManager()
            local_metadata = self.get_suite_metadata(suite_name)
            remote_version = bucket_metadata.get_remote_version(
                local_metadata.BucketName, local_metadata.ObjectName
            )

            return remote_version != local_metadata.Version
        except Exception as e:
            logger.error(e, exc_info=e)
            return False

    # Returns the names of the files in the suite directory that were modified
    # after initial creation time.
    def modified_files_in_suite(self, suite_name) -> List[str]:
        ignore_files = ["__pycache__", ".DS_Store", "config.toml"]
        try:
            suite_path = os.path.join(self.suites_dir, suite_name)
            suite_file = os.stat(suite_path)

            if platform.system() == "Windows":
                creation_time = suite_file.st_mtime
            else:
                creation_time = suite_file.st_birthtime
            suite_creation_time_datetime = datetime.fromtimestamp(
                creation_time
            ).replace(second=0, microsecond=0)
            modified_files = []
            # Store the names of the files that have been changed after creation.
            for file_path in get_subfiles(path=suite_path):
                if any(ignore in file_path for ignore in ignore_files):
                    continue  # Skip this file if it matches any ignore pattern
                file_timestamp = os.path.getmtime(file_path)
                file_modification_datetime = datetime.fromtimestamp(
                    file_timestamp
                ).replace(second=0, microsecond=0)
                if suite_creation_time_datetime != file_modification_datetime:
                    modified_files.append(file_path)

            return modified_files
        except Exception as e:
            logger.error(e, exc_info=e)
            return []

    # Makes a copy of the given suite in the suite_copies folder.
    def copy_modified_suite(self, suite_name):
        source_dir = os.path.join(self.suites_dir, suite_name)
        base_destination_dir_name = "modified-" + suite_name
        destination_dir = os.path.join(self.copy_suite_dir, base_destination_dir_name)

        counter = 1
        while os.path.exists(destination_dir):
            versioned_destination_dir_name = f"{base_destination_dir_name}-{counter}"
            destination_dir = os.path.join(
                self.copy_suite_dir, versioned_destination_dir_name
            )
            counter += 1
        try:
            shutil.copytree(source_dir, destination_dir)
        except Exception as e:
            logger.error(e, exc_info=e)

    def reload_suite(self, suite_name):
        """
        re-load the suite from the original source

        Parameters
        ----------
        suite_name: str
            the name of the suite

        Returns
        ----------

        Raises
        ------
        FailPluginSuiteReload
        """
        try:
            object_url = self.get_suite_metadata(suite_name).ObjectUrl
            self.register_suite(object_url)
            self.paths_to_existing_suites = subdirs_in_dir(
                self.suites_dir, recursive=True
            )
        except Exception as e:
            logger.error(e, exc_info=e)

    def get_all_suites_name(self) -> List[str]:
        return list(self.suites.keys())

    def is_suite(self, suite_name: str) -> bool:
        return suite_name in self.suites

    def register_suite(self, plugin_source: str) -> List[str]:
        """
        Register a plugin suite from the given source, which can be
        a plugin directory, an url, a conf file, or a dictionary configuration.
        """
        register_file = os.path.join(
            self.log_dir, "log" + datetime.now().strftime("%m-%d-%H-%M-%f")
        )
        self.logs[plugin_source] = register_file
        f = open(register_file, "a")

        registered = []
        try:
            # self.loader holds PluginURLLoader and PluginDirectoryLoader
            for loader in self.loaders:
                suites = loader.load(plugin_source, f)
                # PluginURLLoader's load function isn't implemented
                # PluginDirectoryLoader returns a list with one item
                # when load is called with PluginDirectory loader, the following happens:
                # 1) gets and loads requirements
                # 2) make a copy of the original plugin suite and saves
                # it as suite, the function returns [suite]
                # 3) validates the suite
                # if the anything fails (ex: the directory doesn't exist)
                # boolean false value is returned
                if suites:
                    for suite in suites:
                        if isinstance(suite, PluginSuite):
                            self.suites[suite.name] = suite
                            registered.append(suite.name)
            f.close()
            return registered
        except Exception as e:
            f.write(f"{e}\n")
            f.close()
            logger.error(e)
            return []

    def get_selectable_plugins(self, suite_name: str) -> List[str]:
        """
        Given a suite_name, returns a list of selectable plugins from that
        suite
        Parameters
        ----------
        suite_name

        Returns
        -------

        Raises
        ------
        PluginSuiteNotFound
        """
        return self.get_suite(suite_name).optional_plugins

    def get_suite(self, suite_name: str) -> PluginSuite:
        """Given a suite name, return the plugin suite object

        Parameters
        ----------
            suite_name (str): the name that identifies the plugin suite

        Returns
        -------
            PluginSuite: the plugin suite object identified by suite name

        Raises
        -------
        PluginSuiteNotFound
        """
        if not self.is_suite(suite_name):
            raise PluginSuiteNotFound(suite_name)
        return self.suites[suite_name]

    def is_official_suite(self, suite_name) -> bool:
        """
        given a suite name, checks if it is an official suite

        Parameters
        ----------
        suite_name: str: the name of the suite

        Returns
        -------
        bool: True if the suite is official

        Raises
        -------
        PluginSuiteNotFound
        """
        if not self.is_suite(suite_name):
            raise PluginSuiteNotFound(suite_name)
        return self.suites[suite_name].is_official

    def get_suite_metadata(self, suite_name: str) -> Suite:
        """
        given a suite name, returns its metadata

        Parameters
        ----------
        suite_name: str: the name of the suite

        Returns
        -------
        MetaData: the metadata or None if unsuccessful

        Raises
        -------
        PluginSuiteNotFound
        """
        if not self.is_suite(suite_name):
            raise PluginSuiteNotFound(suite_name)
        return self.suites[suite_name].get_meta_data()

    def get_suite_dependency_graph(self, suite_name: str) -> Dict[str, List[str]]:
        """
        given a suite name, returns its dependency graph

        Parameters
        ----------
        suite_name: str: the name of the suite

        Returns
        -------
        Dict[str, List[str]]: the dependency graph

        Raises
        -------
        PluginSuiteNotFound
        """
        if not self.is_suite(suite_name):
            raise PluginSuiteNotFound(suite_name)
        return self.suites[suite_name].dependency_graph()

    def get_suite_documentation_path(self, suite_name) -> str:
        """
        given a suite name, returns its documentation path

        Parameters
        ----------
        suite_name: str: the name of the suite

        Returns
        -------
        str: the path to the documentation

        Raises
        -------
        PluginSuiteNotFound
        """
        if not self.is_suite(suite_name):
            raise PluginSuiteNotFound(suite_name)
        return self.suites[suite_name].document_path

    def _init_workspace(self):
        """
        Init workspace and load plugins from the specified sources.
        """
        self.suites_dir = os.path.join(self.workspace, "suites")
        self.copy_suite_dir = os.path.join(self.workspace, "suite_copies")
        self.download_dir = os.path.join(self.workspace, "download")
        self.log_dir = os.path.join(self.workspace, "register_log")
        self.suites: Dict[str, PluginSuite] = dict()

        # appending the path of suite directory root in order for python to import
        # plugin packages
        sys.path.append(self.suites_dir)

        # Make the directory
        make_dir(self.workspace, overwrite=False)
        make_dir(self.suites_dir, overwrite=False)
        make_dir(self.download_dir, overwrite=True)
        make_dir(self.log_dir, overwrite=True)

    def delete_suite(self, name: str):
        """
        given a suite name, delete the plugin suite

        Parameters
        ----------
        name: str: the name of the suite to delete

        Returns
        -------
        bool: true if successfully removed, false otherwise

        Raises
        -------
        PluginSuiteNotFound
        """
        if not self.is_suite(name):
            raise PluginSuiteNotFound(name)
        if self.is_official_suite(name):
            raise RemoveOfficialPlugin()

        delete(os.path.join(self.suites_dir, name))
        del self.suites[name]

    def delete_suites(self, suite_names: List[str]):
        """
        given a list of suite names, delete each plugin suite
        """
        for suite_name in suite_names:
            if not self.delete_suite(suite_name):
                return False
        return True

    def get_suite_path(self, name: str) -> str:
        """
        Given a name of the suite, return the suite path that is internally
        managed by the suite manager

        Parameters
        ----------
        name: str: the name of the suite path

        Returns
        -------
        str: the path of the suite

        Raises
        -------
        PluginSuiteNotFound
        """
        if self.is_suite(name):
            path = os.path.join(self.suites_dir, name)
            if is_directory(path):
                return path
            else:
                raise PluginSuiteNotFound(name)
        else:
            raise PluginSuiteNotFound(name)

    def report_registration_err(self, suite_source: str) -> str:
        """report plugin registration error

        Parameter
        --------
            suite_source (str): the path to the suite source

        Return
        -------
            str: a string that report the plugin registration error

        Raises
        -------
        FailReportError
        """
        try:
            log = self.logs[suite_source]
            with open(log, "r") as f:
                s = f.read()
            return s
        except Exception as e:
            raise FailReportError(suite_source, e)
