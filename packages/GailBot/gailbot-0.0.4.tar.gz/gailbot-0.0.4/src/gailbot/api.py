# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-08-04 13:59:52
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-09 16:45:14
# @Description:
from typing import List, Dict, Any, Tuple, Optional
from gailbot.engineManager.engineManager import EngineManager
from gailbot.pluginSuiteManager.pluginSuiteManager import PluginSuiteManager
from gailbot.pluginSuiteManager.suite.pluginData import Suite
from gailbot.shared.exception.serviceException import (
    SourceAddError,
    FailPluginSuiteRegister,
    ProfileNotFound,
    RemoveInUseError,
    IncompatibleConverter,
)
from gailbot.sourceManager.watcher import Watcher
from gailbot.payload import ConvertFun
from gailbot.workspace import WorkspaceManager
from gailbot.shared.utils.logger import makelogger
from gailbot.profileManager.profileManager import ProfileManager, ProfileSetting
from gailbot.transcriptionPipeline.pipeline import GBPipeline, TranscriptionResult
from gailbot.sourceManager.sourceManager import SourceManager
from gailbot.configs import default_setting_loader
from tqdm import tqdm

CONFIG = default_setting_loader()
DEFAULT_SETTING_NAME = CONFIG.profile_name
logger = makelogger("gb_api")


class GailBot:
    def __init__(self):
        """
        initialize a gailbot object that provides a suite of functions
            to interact with gailbot
        """
        tqdm(disable=True, total=0)
        self.ws_manager: WorkspaceManager = WorkspaceManager()
        self._init_workspace()
        self.plugin_suite_manager = PluginSuiteManager(WorkspaceManager.plugin_src)
        self.engine_manager = EngineManager(WorkspaceManager.engine_setting_src)
        self.profile_manager = ProfileManager(
            WorkspaceManager.profile_src, self.engine_manager, self.plugin_suite_manager
        )
        self.source_manager = SourceManager()
        self.pipeline_service = GBPipeline
        self.transcribed = set()

    def _init_workspace(self) -> bool:
        """
        Resets the workspace: clears the old workspace and initializes a new one.

        Returns
        -------
        Bool:
            True if the workspace is initialized successful, false otherwise.
        """
        try:
            self.ws_manager.clear_gb_temp_dir()
            self.ws_manager.init_workspace()
            return True
        except Exception as e:
            logger.error(f"failed to reset workspace due to the error {e}", exc_info=e)
            return False

    def clear_workspace(self) -> bool:
        """
        Clears current workspace.

        Returns
        -------
        Bool:
            True if the workspace is cleared, false otherwise.
        """
        try:
            self.ws_manager.clear_gb_temp_dir()
            return True
        except Exception as e:
            logger.error(f"failed to reset workspace due to the error {e}", exc_info=e)
            return False

    def reset_workspace(self) -> bool:
        """
        Reset the gailbot workspace.

        Returns
        -------
        Bool:
            True if workspace successfully reset; false otherwise.
        """
        return self.ws_manager.reset_workspace()

    def add_source(self, source_path: str, output_dir: str) -> str:
        """
        Adds a given source.

        Parameters
        ----------
        source_path: str
            Full path of the source to add.
        output_dir: str
            Path to the directory where gailbot should place output files.

        Returns
        -------
        str:
            the id of the added source

        Raises
        ------
        SourceAddError
        """
        try:
            name = self.source_manager.add_source(source_path, output_dir)
            self.source_manager.apply_profile_to_source(
                name, self.profile_manager.default_profile_name
            )
            return name
        except Exception as e:
            raise SourceAddError(source_path, e)

    def add_sources(
        self, src_output_pairs: List[Tuple[str, str]]
    ) -> Dict[str, Tuple[str, str]]:
        """
        Adds a given list of sources.

        Parameters
        ----------
        src_output_pairs: List[Tuple[str, str]]
            A list of (source_path, output_directory_path) tuples.

        Returns
        -------
        Dict[str, Tuple[str, str]]:
            A dictionary mapping from source id to the corresponding
            (source_path, output_directory_path) tuple.

        Raises
        -------
        SourceAddError
        """
        res = dict()
        for source_path, output in src_output_pairs:
            source_id = self.add_source(source_path, output)
            res[source_id] = (source_path, output)
        return res

    def is_source(self, source_id: str) -> bool:
        """
        Determines if a given name corresponds to an existing source.

        Parameters
        ----------
        source_id: str
            Name of the source to look for; or path.

        Returns
        -------
        Bool:
            True if the given name corresponds to an existing source,
            false if not.
        """
        return self.source_manager.is_source(source_id)

    def remove_source(self, source_id: str):
        """
        Removes the given source.

        Parameters
        ----------
        source_id: str
            Name of the existing source to remove; without extension.

        Returns
        -------
        None

        Raises
        ------
        SourceNotFound
        """
        self.source_manager.remove_source(source_id)

    def remove_sources(self, source_ids: List[str]):
        """
        Removes the given list of named sources.

        Parameters
        ----------
        source_ids: List[str]
            List of names of the existing sources to remove

        Returns
        -------
        None

        Raises
        ------
        SourceNotFound
        """
        for name in source_ids:
            self.source_manager.remove_source(name)

    def source_profile_setting(self, source_id: str) -> ProfileSetting:
        """
        Access the contents of the profile assigned to a given source.

        Parameters
        ----------
        source_id: str
            The name of the source; or path

        Returns
        -------
        Dict:
            A dictionary storing the data of the source's profile

        Raises
        -------
        SourceNotFound
        """
        profile_name = self.source_manager.get_source_profile(source_id)
        profile = self.profile_manager.get_profile_setting(profile_name)
        return profile

    def source_profile_name(self, source_id: str) -> str:
        """
        Access the name of the profile applied to the given source.

        Parameters
        ----------
        source_id: str
            The name of the source file; without extensions.

        Returns
        -------
        str:
            The name of the profile applied to the source.

        Raises
        ---------
        SourceNotFound
        """
        return self.source_manager.get_source_profile(source_id)

    def change_source_converter(self, source_id, converter):
        """
        Parameters
        ----------
        source_id
        converter

        Returns
        -------
        true if the source [converter] can convert the source, false otherwise
        """
        if not self.source_manager.change_source_converter(source_id, converter):
            raise IncompatibleConverter(source_id, converter.value)

    def available_converters(self):
        """
        Returns
        -------
        A list of available converters' names
        """
        return self.source_manager.available_converters()

    def get_source_converter(self, source_id):
        """
        get the converter currently applied to the source identified by source_id

        Parameters
        ----------
        source_id

        Returns
        -------

        Raises
        -------
        SourceNotFoundError
        """
        return self.source_manager.get_source_converter(source_id)

    def compatible_converters(self, source_id):
        """
        get all converters that are compatible with the type of the
        source identified by source_id

        Parameters
        ----------
        source_id

        Returns
        -------

        Raises
        -------
        SourceNotFoundError
        """
        return self.source_manager.compatible_converters(source_id)

    def transcribe(self, source_ids: Optional[List[str]] = None) -> TranscriptionResult:
        """
        Given a list of source IDs, transcribe the sources.

        Parameters
        ----------
        source_ids: List[str]
            A list of source IDs to transcribe.

        Returns
        -------
        TranscriptionResult:
            The path to the successful transcriptions' outputs will be stored in [TranscriptionResult.success_output]
            The source name for the invalid and failure transcription will be stored in [TranscriptionResult.invalid]
            and [Transcription.fail]

        Raises
        ------
        """
        sources = []
        if not source_ids:
            source_ids = list(self.source_manager.un_transcribed_sources().keys())
        # get source object from source id
        for src_id in source_ids:
            sources.append(self.get_source_obj(src_id))

        print("sources is ", sources)
        # transcribe source
        result = self.pipeline_service.transcribe(sources)

        # set source to be transcribed
        for src_id in source_ids:
            self.source_manager.remove_source(src_id)
        self.ws_manager.clear_gb_temp_dir()
        return result

    def create_profile(self, name: str, setting: Dict[str, str] | ProfileSetting):
        """
        Create a new profile.

        Parameters
        ----------
        name: str
            The name of the profile.
        setting: Dict[str, str]
            The profile content.

        Raises
        ----------
        DuplicateProfile
        EngineNotFound
        """
        self.profile_manager.add_new_profile(name, setting)

    def get_profile_setting(self, name: str) -> ProfileSetting:
        """
        Given a profile name, returns the profile's content.

        Parameters
        ----------
        name: str
            Name of a profile.

        Returns
        -------
        Dict[str, Any]:
            A dictionary with the content of the profile.

        Raises
        ------
        ProfileNotFound
        """
        return self.profile_manager.get_profile_setting(name)

    def available_profiles(self) -> List[str]:
        """
        Get the names of all available profiles.

        Returns
        -------
        List[str]:
            A list of available profiles' names
        """
        return self.profile_manager.available_profiles

    def update_profile(
        self, profile_name: str, new_setting: Dict[str, Any] | ProfileSetting
    ):
        """
        Updates a given profile to a newly given structure.

        Parameters
        ----------
        profile_name: str
            Name of the profile to update.
        new_setting: Dict[str, Any] | ProfileSetting
            Either dictionary or ProfileSetting object that stores the updated profile setting

        Returns
        -------
        None

        Raises
        ------
        ProfileNotFound

        """
        self.profile_manager.update_profile(profile_name, new_setting)

    def remove_profile(self, profile_name: str):
        """
        Removes the given profile.

        Parameters
        ----------
        profile_name: str
            Name of the profile to remove.

        Returns
        -------
        None

        Raises
        ------
        RemoveInUseError
        ProfileNotFound
        """
        if self.source_manager.profile_used_by_source(profile_name):
            raise RemoveInUseError(profile_name)
        else:
            self.profile_manager.remove_profile(profile_name)

    def is_profile(self, name: str) -> bool:
        """
        Determines if the given name corresponds to an existing profile.

        Parameters
        ----------
        name: str
            Name of the profile to search for.

        Returns
        -------
        Bool:
            True if given profile is an existing profile, false if not
        """
        return self.profile_manager.is_profile(name)

    def apply_profile_to_source(self, source_id: str, profile_name: str):
        """
        Applies a given profile to a given source.

        Parameters
        ----------
        source_id: str
            Name of the source to which to apply the given profile
        profile_name: str
            Name of the profile to apply to the given source.

        Returns
        -------
        None

        Raises
        -------
        ProfileNotFound
        SourceNotFound
        """
        if self.profile_manager.is_profile(profile_name):
            self.source_manager.apply_profile_to_source(source_id, profile_name)
        else:
            raise ProfileNotFound(profile_name)

    def apply_profile_to_sources(self, source_ids: List[str], profile_name: str):
        """
        Applies a given profile to a given list of sources.

        Parameters
        ----------
        source_ids: List[str]
            List of names of the sources to which to apply the given profile.
        profile_name: str
            The profile to be applied.

        Returns
        -------
        None

        Raises
        -------
        ProfileNotFound
        SourceNotFound
        """
        for source in source_ids:
            self.apply_profile_to_source(source, profile_name)

    def default_profile_name(self) -> str:
        """
        Get the name of current default profile.

        Returns
        -------
        str:
            The name of current default profile.
        """
        return self.profile_manager.default_profile_name

    def suite_has_new_version(self, suite_name: str) -> bool:
        """
        Check if a suite has a new version that can be updated

        Parameters
        ----------
        suite_name

        Returns
        -------
        bool
        """
        return self.plugin_suite_manager.has_new_version(suite_name)

    def modified_files_in_suite(self, suite_name: str) -> List[str]:
        """
        Check if a suite has been modified locally

        Parameters
        ----------
        suite_name

        Returns
        -------
        bool
        """
        return self.plugin_suite_manager.modified_files_in_suite(suite_name)

    def suite_copy_modified_suite(self, suite_name: str):
        return self.plugin_suite_manager.copy_modified_suite(suite_name)

    def register_suite(self, plugin_path: str) -> List[str]:
        """
        Registers a gailbot plugin suite.

        Parameters
        ----------
        plugin_path: str
            Path of the plugin suite to register.

        Returns
        -------
        List[str]:
            A list of plugin names if the plugin is registered.

        Raises
        -------
        FailPluginRegister
        """
        registered = self.plugin_suite_manager.register_suite(plugin_path)
        if not registered:
            raise FailPluginSuiteRegister(
                plugin_path,
                self.plugin_suite_manager.report_registration_err(plugin_path),
            )
        else:
            return registered

    def is_suite(self, name: str) -> bool:
        """
        Determines if a given name is an existing plugin suite.

        Parameters
        ----------
        name: str
            Name of the plugin suite to search for.

        Returns
        -------
        Bool:
            True if given plugin suite exists, false if not
        """
        return self.plugin_suite_manager.is_suite(name)

    def remove_suite(self, name: str):
        """
        Removes the given plugin suite.

        Parameters
        ----------
        name: str
            Name of the plugin suite to delete.

        Returns
        -------
        None

        Raises
        -------
        PluginSuiteNotFound
        RemoveInUseError
        """
        if self.profile_manager.is_suite_used_by_profile(name):
            raise RemoveInUseError(name)
        self.plugin_suite_manager.delete_suite(name)

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
        return self.plugin_suite_manager.get_selectable_plugins(suite_name)

    def available_suites(self) -> List[str]:
        """
        Get the names of available plugin suites.

        Returns
        -------
        List[str]:
            A list of available plugin suites name.
        """
        return self.plugin_suite_manager.get_all_suites_name()

    def suite_metadata(self, suite_name: str) -> Suite:
        """
        Get the metadata of a plugin suite identified by suite name.

        Parameters
        ----------
        suite_name: str
            The name of the suite.

        Returns
        -------
        MetaData: a MetaData object that stores the suite's metadata

        Raises
        ------
        PluginSuiteNotFound
        """
        return self.plugin_suite_manager.get_suite_metadata(suite_name)

    def suite_dependency_graph(self, suite_name: str) -> Dict[str, List[str]]:
        """
        Get the dependency map of the plugin suite identified by suite_name

        Parameters
        ----------
        suite_name: str
            The name of the suite.

        Returns
        -------
        Dict[str, List[str]]:
            The dependency graph of the suite.

        Raises
        -------
        PluginSuiteNotFound
        """
        return self.plugin_suite_manager.get_suite_dependency_graph(suite_name)

    def suite_documentation_path(self, suite_name: str) -> str:
        """
        Get the path to the documentation map of the plugin suite identified
        by suite_name.

        Parameters
        ----------
        suite_name: str
            The name of the suite.

        Returns
        -------
        str:
            The path to the documentation file.

        Raises
        -------
        PluginSuiteNotFound
        """
        return self.plugin_suite_manager.get_suite_documentation_path(suite_name)

    def is_active_suite(self, suite_name: str) -> bool:
        """
        Given a suite name, check if this suite is used in any of the profiles.

        Parameters
        ----------
        suite_name: str
            The name of the plugin suite.

        Returns
        -------
        bool:
            Return true if the suite is used in any of the profiles,
            false otherwise (including if the provided suite name doesn't exist).
        """
        return self.profile_manager.is_suite_used_by_profile(suite_name)

    def is_official_suite(self, suite_name: str) -> bool:
        """
        Check if the suite identified by the given suite name is official.

        Parameters
        ----------
        suite_name: str
            The name of the suite.

        Returns
        -------
        bool:
            True if the suite is official, false otherwise.

        Raises
        ------
        PluginSuiteNotFound
        """
        return self.plugin_suite_manager.is_official_suite(suite_name)

    def suite_code_path(self, suite_name: str) -> str:
        """
        Given the name of a plugin suite, return the path to the source
        code of the suite.
        If the suite name doesn't correspond to a valid directory,
        the key value pair is erased from the list of suite names
        and corresponding PluginSuite objects. TODO: Does this happen?

        Parameters
        ----------
        suite_name: str
            The name of the suite.

        Returns
        -------
        string:
            String representing path to the suite source code.

        Raises
        -----
        PluginSuiteNotFound
        """
        return self.plugin_suite_manager.get_suite_path(suite_name)

    def report_suite_registration_error(self, suite_source) -> str:
        """
        Given the original suite_source that is used during suite registration,
        return the error string that causes the string registration failure

        Parameter
        ---------
            suite_source (str): a string to the initial source of the suite

        Returns
        --------
            str: a string that describes the error that causes the suite registration to fail

        Raises
        --------
        FailReportError
        """
        return self.plugin_suite_manager.report_registration_err(suite_source)

    def available_engines(self) -> List[str]:
        """
        Get the names of all available engines.

        Returns
        ----------
        List[str]:
            A list of all available engine names.
        """
        return self.engine_manager.available_engines

    def add_engine(self, name: str, setting: Dict[str, str]) -> bool:
        """
        Add a new engine.

        Parameters
        ----------
        name: str
            The name of the new engine
        setting: Dict[str, str]
            Settings for the new engine

        Returns
        ----------
        bool:
            True if the engine is successfully created, false otherwise
        """
        return self.engine_manager.add_engine(name, setting)

    def remove_engine(self, name: str):
        """
        Remove the engine identified by name

        Parameters
        ----------
        name: str
            the name of the engine to be removed

        Returns
        ----------
        bool:
            True if the engine is successfully removed

        Raises
        ----------
        EngineNotFound
        RemoveInUseError
        """
        if self.profile_manager.is_engine_used_by_profile(name):
            raise RemoveInUseError(name)
        self.engine_manager.remove_engine(name)

    def update_engine(self, name: str, new_setting: Dict[str, str]) -> bool:
        """
        Update an engine's setting

        Parameters
        ----------
        name: str
            the name of the engine
        new_setting: Dict[str, str]
            the new setting of the engine

        Returns
        ----------
        bool:
            True if the engine's setting is successfully updated,
            false otherwise.

        Raises
        -----------
        EngineNotFound
        """
        return self.engine_manager.update_engine(name, new_setting)

    def get_engine_setting(self, name: str) -> Dict[str, str]:
        """
        Access the setting data of the given engine.

        Parameters
        ----------
        name: str
            the name of the engine

        Returns
        ----------
        Dict[str, str]:
            The content of the engine's setting stored in a dictionary

        Raises
        ------
        EngineNotFound
        """
        return self.engine_manager.get_engine_setting(name)

    def is_engine(self, name: str) -> bool:
        """
        Check if the given name is an existing engine

        Parameters
        ----------
        name: str
            the engine name to search for.

        Returns
        ----------
        bool:
            True if provided engine name is a valid engine, false otherwise
        """
        return self.engine_manager.is_engine(name)

    def default_engine_name(self) -> str:
        """
        Get the default engine's name

        Returns
        -------
        str:
            The default engine's name
        """
        return self.engine_manager.default_name

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
        self.plugin_suite_manager.reload_suite(suite_name)

    @staticmethod
    def compatible_media_formats() -> List[str]:
        """
        Returns
        -------
        A list of media file formats supported by gailbot
        """
        return ConvertFun.compatible_formats()

    @staticmethod
    def compatible_audio_formats():
        """
        Returns
        -------
        A list of audio file formats supported by gailbot
        """
        return ConvertFun.compatible_audio_formats()

    @staticmethod
    def compatible_video_formats():
        """
        Returns
        -------
        A list of video file formats supported by gailbot
        """
        return ConvertFun.compatible_video_formats()

    def add_progress_watcher(self, source_id: str, watcher: Watcher):
        """
        Add a function displayer to track for the progress of source.

        Parameters
        ----------
        source_id: str
            The name of the source.
        watcher: Watcher
            Displayer is a function that takes in a string as argument, and the
            string encodes the progress of the source.

        Returns
        -------
        None

        Raises
        ------
        SourceNotFound
        """
        self.source_manager.add_progress_watcher(source_id, watcher)

    def get_source_obj(self, source_id: str):
        """
        return the source object identified by source_id
        Parameters
        ----------
        source_id

        Returns
        -------

        Raises
        ------
        SourceNotFound

        """
        src_obj = self.source_manager.get_source(source_id)
        if self.profile_manager.is_profile(src_obj.profile_name):
            applied_profile_name = src_obj.profile_name
        else:
            logger.warning(
                f"Applied profile {src_obj.profile_name} is deleted, use default profile instead"
            )
            applied_profile_name = self.profile_manager.default_profile_name
            self.apply_profile_to_source(
                source_id=source_id, profile_name=applied_profile_name
            )
        profile = self.profile_manager.get_profile_object(applied_profile_name)
        src_obj.initialize_profile(profile)
        return src_obj
