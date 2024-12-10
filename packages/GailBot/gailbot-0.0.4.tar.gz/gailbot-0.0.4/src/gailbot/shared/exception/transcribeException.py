# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-06-28 18:22:18
# @Last Modified by:   Joanne Fan
# @Last Modified time: 2024-05-16 16:29:45
from gailbot.shared.exception.gbException import GBException


class InternetConnectionError(GBException):
    def __init__(self):
        super().__init__()
        self.code = 404
        self.error_msg = " STT Connection Error"


class TranscriptionError(GBException):
    def __init__(self, error: str = None) -> None:
        super().__init__()
        self.code = 500
        self.error = error
        self.error_msg = f"Transcription error: {self.error}"


class APIKeyError(GBException):
    def __init__(self) -> None:
        super().__init__()
        self.code = 508
        self.error_msg = "API key error"


class AudioFileError(GBException):
    def __init__(self) -> None:
        super().__init__()
        self.code = 510
        self.error_msg = "Not a valid audio file"


class ModelCreateError(GBException):
    def __init__(self) -> None:
        super().__init__()
        self.code = 511
        self.error_msg = "Model creation error"


class WatsonMethodExecutionError(GBException):
    def __init__(self) -> None:
        super().__init__()
        self.code = 512
        self.error_msg = "Watson method execution error"

class WatsonModelNameTaken(GBException):
    def __init__(self) -> None:
        super().__init__()
        self.code = 513
        self.error_msg = "Watson custom model name is already taken."

class OutPutError(GBException):
    def __init__(self) -> None:
        super().__init__()
        self.code = 520
        self.error_msg = "Error writing output"


class GetUttResultError(GBException):
    def __init__(self) -> None:
        super().__init__()
        self.code = 521
        self.error_msg = "Failed to get utterance result"
