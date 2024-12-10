# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-23 08:04:39
# @Last Modified by:   Vivian Li 
# @Last Modified time: 2024-03-03 15:39:24
from gailbot.shared.exception.gbException import GBException


class RemoveDefaultEngine(GBException):
    def __init__(self):
        self.code = 14
        self.error_msg = "Default Engine cannot be removed"


class RemoveDefaultProfile(GBException):
    def __init__(self):
        self.code = 14
        self.error_msg = "Default Profile cannot be removed"


class RemoveOfficialPlugin(GBException):
    def __init__(self):
        self.code = 32
        self.error_msg = "Official Plugin Suite cannot be removed"


class NotFound(GBException):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.error_msg = f"{self.name} not found."


class AddError(GBException):
    def __init__(self, name: str, cause: Exception):
        super().__init__()
        self.name = name
        self.cause = cause
        self.error_msg = f"Fail to add {self.name} due to {self.cause.__cause__}"


class Duplicate(GBException):
    def __init__(self, name):
        super().__init__()
        self.code = 13
        self.name = name
        self.error_msg = f"{self.name} already exists"


class DuplicatePlugin(Duplicate):
    def __init__(self, name):
        super().__init__(name)
        self.code = 44  # undocumented


class DuplicateEngine(Duplicate):
    def __init__(self, name):
        super().__init__(name)


class DuplicateProfile(Duplicate):
    def __init__(self, name):
        super().__init__(name)


# TODO: improve naming?
class RemoveInUseError(GBException):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.error_msg = f"Fail to remove {self.name} that is being used."


class SourceAddError(AddError):
    def __init__(self, name: str, cause: Exception):
        super().__init__(name, cause)
        self.code = 7


class ProfileAddError(AddError):
    def __init__(self, name: str, cause: Exception):
        super().__init__(name, cause)
        self.code = 16


class EngineAddError(AddError):
    def __init__(self, name: str, cause: Exception):
        super().__init__(name, cause)
        self.code = 23


class SourceNotFound(NotFound):
    def __init__(self, name):
        self.code = 4
        super().__init__(name)


class ProfileNotFound(NotFound):
    def __init__(self, name):
        self.code = 19
        super().__init__(name)


class EngineNotFound(NotFound):
    def __init__(self, name):
        self.code = 26
        super().__init__(name)


class PluginSuiteNotFound(NotFound):
    def __init__(self, name):
        self.code = 40  # not documented
        super().__init__(name)


class FailPluginSuiteRegister(GBException):
    def __init__(self, path: str, cause: str):
        super().__init__()
        self.cause = cause
        self.code = 35
        self.path = path
        self.error_msg = (
            f"Fail to register plugin suite at {path} due to : {self.cause}"
        )

    def __str__(self):
        return self.cause


class FailPluginSuiteReload(GBException):
    def __init__(self, name: str, cause: Exception):
        super().__init__()
        self.name = name
        self.code = 41  # undocumented
        self.cause = cause
        self.error_msg = (
            f"Fail to reload plugin suite {self.name} due to : {self.cause}"
        )


class FailReportError(GBException):
    def __init__(self, name: str, cause: Exception):
        super().__init__()
        self.name = name
        self.code = 45  # undocumented
        self.cause = cause
        self.error_msg = f"Fail to report suite registration error for {self.name} due to : {self.cause}"


class IncompatibleConverter(GBException):
    def __init__(self, source_name: str, converter: str):
        super().__init__()
        self.code = 100  # undocumented
        self.error_msg = f"{converter} is not compatible with {source_name}"


class IncompatibleFileFormat(GBException):
    def __init__(self, filepath: str, extension: str):
        super().__init__()
        self.code = 101  # undocumented
        self.error_msg = f"Content of {filepath} is not compatible with {extension}"
