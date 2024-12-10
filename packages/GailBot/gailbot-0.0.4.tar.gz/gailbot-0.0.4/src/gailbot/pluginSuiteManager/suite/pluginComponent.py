# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-02-06 16:08:45
# @Description: a wrapper around Plugin object, PluginComponent will eventually
#  be sent to Pipeline, which accepts executable function stored in component object
import time
from typing import Dict, Any

from gailbot.shared.pipeline import Component, ComponentResult, ComponentState
from gailbot.shared.utils.logger import makelogger
from gailbot.pluginSuiteManager.suite.plugin import Plugin


class PluginResult(ComponentResult):
    state: ComponentState = ComponentState.FAILED
    result: Any = None
    runtime: float = 0


class PluginComponent(Component):
    """
    This is an adapter because the Plugin expects different args as compared
    to transcriptionPipeline components.
    This is needed to so that ComponentResult component is not passed to the user.
    """

    logger = makelogger("pluginSuite")

    def __init__(self, plugin: Plugin):
        super().__init__()
        self.plugin = plugin

    def __repr__(self):
        return str(self.plugin)

    def __call__(
        self,
        dependency_outputs: Dict[str, ComponentResult] = None,
        methods=None,
        *args,
        **kwargs,
    ):
        """
        In addition to dependency outputs, this expects methods which can be
        passed to the individual plugins.
        """
        if not dependency_outputs:
            dependency_outputs = None
        # Extract the actual dependency results
        dep_outputs = {k: v.result for k, v in dependency_outputs.items()}
        # Simply call the plugin and return its results
        start = time.time()
        try:
            result = self.plugin.apply(dep_outputs, methods)
        except Exception as e:
            result = f"Error: {e}"
            self.logger.error(e, exc_info=e)

        elapsed = time.time() - start

        return PluginResult(
            state=(
                ComponentState.SUCCESS
                if self.plugin.is_successful
                else ComponentState.FAILED
            ),
            result=result,
            runtime=elapsed,
        )
