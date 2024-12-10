# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-21 14:31:59
import os.path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from gailbot.engineManager.engine.engineProvider import EngineProvider
from gailbot.pluginSuiteManager.pluginSuiteManager import PluginSuiteManager
from gailbot.shared.exception.serviceException import (
    ProfileNotFound,
    DuplicateProfile,
    RemoveDefaultProfile,
    EngineNotFound,
)
from gailbot.shared.utils.general import (
    is_file,
    delete,
    write_toml,
    paths_in_dir,
    get_name,
    read_toml,
)
from gailbot.shared.utils.logger import makelogger
from gailbot.engineManager.engineManager import EngineManager
from gailbot.pluginSuiteManager.suite.suite import PluginSuite


@dataclass(init=True)
class ProfileSetting:
    """
    stores the raw data for a profile setting
    """

    engine_setting_name: str
    plugin_suite_setting: Dict[str, Optional[Dict[str, List[str]] | List[str]]]


@dataclass(init=True)
class ProfileObject:
    """
    Attributes:
        name: name of the profile
        profile_data: the raw setting data
        engine_provider: an instance of EngineProvider used by current profile
        plugin_suites: a dictionary maps the plugin_suites and the selected plugins
                      (stored as a dependency graph) used by current profile
    """

    name: str
    profile_data: ProfileSetting
    engine_provider: EngineProvider
    plugin_suites: Dict[PluginSuite, Dict[str, List[str]]]


class ProfileManager:
    logger = makelogger("profileManager")
    _default_name = "Default"
    _default_data = ProfileSetting(
        engine_setting_name=EngineManager.default_name,
        plugin_suite_setting={"gb_hilab_suite": []},
    )

    def __init__(
        self,
        workspace: str,
        engine_manager: EngineManager,
        plugin_suite_manager: PluginSuiteManager,
    ):
        self.workspace = workspace
        self.engineManager = engine_manager
        self.pluginSuiteManager = plugin_suite_manager
        self.profiles: Dict[str, ProfileSetting] = dict()
        try:
            self._load_existing_profile()
            self._load_default_profile()
        except Exception as e:
            self.logger.error(e, exc_info=True)

    def add_new_profile(self, name: str, data: Dict[str, Any] | ProfileSetting):
        if self.is_profile(name):
            raise DuplicateProfile(name)

        if isinstance(data, ProfileSetting):
            profile_setting = data
            raw_data = asdict(data)
        else:
            profile_setting = ProfileSetting(**data)
            raw_data = data

        if not self.engineManager.is_engine(profile_setting.engine_setting_name):
            raise EngineNotFound(profile_setting.engine_setting_name)

        self.profiles[name] = profile_setting

        # save profile to disk
        path = os.path.join(self.workspace, f"{name}.toml")
        if is_file(path):
            delete(path)

        write_toml(path=path, data=raw_data)

    @property
    def default_profile_name(self):
        return self._default_name

    @property
    def available_profiles(self) -> List[str]:
        """
        Returns
        -------
        a list of profile names
        """
        return list(self.profiles.keys())

    def is_profile(self, name):
        return name in self.profiles

    def remove_profile(self, name):
        """
        Raises
        -------
        ProfileNotFound

        Returns
        -------
        Remove profile identified by name
        """
        if not self.is_profile(name):
            raise ProfileNotFound(name)
        if name == self.default_profile_name:
            raise RemoveDefaultProfile()

        path = os.path.join(self.workspace, f"{name}.toml")
        if is_file(path):
            delete(path)
        del self.profiles[name]

    def update_profile(self, name, data: Dict[str, Any] | ProfileSetting):
        """
        Returns
        -------
        Update the current profile identified by name with new data
        """
        if not self.is_profile(name):
            raise ProfileNotFound(name)
        path = os.path.join(self.workspace, f"{name}.toml")
        if is_file(path):
            delete(path)
        del self.profiles[name]
        self.add_new_profile(name, data)

    def get_profile_object(self, profile_name: str) -> ProfileObject:
        """
        Return the profile object that contains initialized engine and plugin suite instances
        """
        profile_setting: ProfileSetting = self.profiles[profile_name]
        engine_provider = self.engineManager.get_engine_provider(
            profile_setting.engine_setting_name
        )
        suites = {
            self.pluginSuiteManager.get_suite(suite_name): dependency
            for suite_name, dependency in profile_setting.plugin_suite_setting.items()
        }

        profile_obj = ProfileObject(
            profile_name, profile_setting, engine_provider, suites
        )
        return profile_obj

    def get_profile_setting(self, name) -> ProfileSetting:
        """
        Returns
        -------
        Returns the profile data what stores the profile setting
        """
        if not self.is_profile(name):
            raise ProfileNotFound(name)
        else:
            profile = self.profiles[name]
            return profile

    def is_suite_used_by_profile(self, suite_name: str) -> bool:
        """
        Returns
        -------
        Returns true if a suite identified by suite_name is used by any of the profiles
        """
        for profile in self.profiles.values():
            for suite in profile.plugin_suite_setting.keys():
                if suite == suite_name:
                    return True
        return False

    def is_engine_used_by_profile(self, engine_name: str) -> bool:
        """
        Returns
        -------
        Returns true if engine identified by engine_name is used by any of the profiles
        """
        for profile in self.profiles.values():
            if profile.engine_setting_name == engine_name:
                return True
        return False

    def _load_existing_profile(self):
        """
        Load existing profile on the disk
        """
        files = paths_in_dir(self.workspace, ["toml"])
        for file in files:
            name = get_name(file)
            data = read_toml(file)
            try:
                self.profiles[name] = ProfileSetting(
                    engine_setting_name=data["engine_setting_name"],
                    plugin_suite_setting=data["plugin_suite_setting"],
                )
            except Exception as e:
                delete(file)
                self.logger.error(
                    f"failed to load existing profile {name} with error {e}"
                )

    def _load_default_profile(self):
        """
        If default profile is not added, added it to profile manager
        """
        if not self.is_profile(self._default_name):
            self.add_new_profile(self._default_name, self._default_data)
