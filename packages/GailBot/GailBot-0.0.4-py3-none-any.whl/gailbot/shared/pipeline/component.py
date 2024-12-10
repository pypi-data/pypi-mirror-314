# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:54:35
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-02-06 16:10:12
# @Description: Component is a wrapper around an executable function which
# will be accepted by Pipeline


from abc import ABC
from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict


class ComponentState(Enum):
    """
    Class containing the status of a component object.
    """

    READY = 0
    SUCCESS = 1
    FAILED = 2


@dataclass
class ComponentResult:
    """
    Class containing the result of a component object.
    """

    state: ComponentState = ComponentState.FAILED
    result: Any = None
    runtime: float = 0


class Component(ABC):
    """
    Wrapper for a function that is run in the transcriptionPipeline.
    Should be subclassed.
    """

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        raise NotImplementedError()

    def __call__(
        self, dependency_outputs: Dict[str, ComponentResult], *args, **kwargs
    ) -> ComponentState:
        raise NotImplementedError()
