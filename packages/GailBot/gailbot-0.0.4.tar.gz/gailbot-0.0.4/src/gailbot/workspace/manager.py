# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-06-15 15:27:03
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-09 18:39:41
import os.path
from dataclasses import dataclass

import userpaths

from gailbot.shared.utils.general import is_directory, make_dir, delete
from gailbot.shared.utils.logger import makelogger

logger = makelogger("workspace")


@dataclass
class WorkspaceManager:
    """store the path data of the workspace, provide utility function to
    create temporary and output directories
    """

    _last_update = 1708863997.0  # any GailBot folder older than this timestamp will be reinitialized
    gb_root = os.path.join(userpaths.get_profile(), "GailBot")
    gb_ws = os.path.join(gb_root, "gailbot_workspace")
    temporary_ws = os.path.join(gb_ws, "temporary")
    gb_data = os.path.join(gb_ws, "gailbot_data")
    plugin_src = os.path.join(gb_data, "plugin_source")
    suites = os.path.join(plugin_src, "suites")
    plugins = os.path.join(plugin_src, "plugins")
    engine_src = os.path.join(gb_data, "engine_source")
    engine_setting_src = os.path.join(engine_src, "engine_setting")
    profile_src = os.path.join(gb_data, "profile_source")
    paths = [gb_root, gb_ws, temporary_ws, gb_data, plugin_src, engine_src, profile_src]

    def init_workspace(self):
        """
        Initializes the workspace
        """
        if (
            is_directory(self.gb_root)
            and os.path.getctime(self.gb_root) < self._last_update
        ):
            delete(self.gb_root)
        for path in self.paths:
            if not is_directory(path):
                make_dir(path, True)

    def reset_workspace(self):
        """
        Resets the given workspace

        Returns
        -------
        True if successful, false otherwise
        """
        try:
            if is_directory(self.gb_root):
                delete(self.gb_root)
            self.init_workspace()
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False

    def clear_gb_temp_dir(self):
        """
        Clears the temporary workspace directory

        Returns
        -------
        False if exception is raised
        """
        try:
            if is_directory(self.temporary_ws):
                delete(self.temporary_ws)
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
