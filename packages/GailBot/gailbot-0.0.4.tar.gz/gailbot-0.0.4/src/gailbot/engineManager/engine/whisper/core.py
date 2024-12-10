# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 11:09:26
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-02 17:48:48


import os
from threading import Lock
import json
from typing import List, Dict
from dataclasses import asdict

import torch
import whisper_timestamped as whisper
from whisper_timestamped.transcribe import force_cudnn_initialization

from gailbot.workspace import WorkspaceManager
from .parsers import (
    parse_into_full_text,
)

from .parsers import parse_into_word_dicts
from gailbot.shared.utils.general import is_file, make_dir
from gailbot.configs import whisper_config_loader
from gailbot.shared.utils.logger import makelogger

logger = makelogger("whisper")

WHISPER_CONFIG = whisper_config_loader()
LOAD_MODEL_LOCK = Lock()


class WhisperCore:
    """
    We are using this class as an adapter for the engine so that we can use
    multiple different instances of the underlying whisper package is required.
    """

    # NOTE: Intentionally limiting the supported formats since we have
    # not tested other formats.
    _SUPPORTED_FORMATS = "wav"

    def __init__(self):
        # initialize the workspace
        self.workspace_dir = os.path.join(WorkspaceManager.engine_src, "whisper")
        self.cache_dir = os.path.join(self.workspace_dir, "cache")
        self.models_dir = os.path.join(self.cache_dir, "models")
        self.loadModelLock = Lock()
        make_dir(self.workspace_dir, overwrite=False)
        make_dir(self.cache_dir, overwrite=False)
        make_dir(self.models_dir, overwrite=False)

        # Load a GPU is it is available
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        if self.device.lower().startswith("cuda"):
            force_cudnn_initialization(self.device)
        logger.info(f"Whisper core initialized with device: {self.device}")

    def __repr__(self) -> str:
        configs = json.dumps(
            asdict(WHISPER_CONFIG.transcribe_configs), indent=2, ensure_ascii=False
        )
        return (
            f"Whisper model: {WHISPER_CONFIG.model_name}"
            f"Transcribe configs:\n{configs}"
        )

    def transcribe(
        self, audio_path: str, language: str = None, detect_speaker: bool = False
    ) -> List[Dict]:
        """
        Use the engine to transcribe an item
        """
        assert is_file(audio_path), f"ERROR: Invalid file path: {audio_path}"
        global LOAD_MODEL_LOCK
        with LOAD_MODEL_LOCK:
            whisper_model = whisper.load_model(
                name=WHISPER_CONFIG.model_name,
                device=self.device,
                download_root=self.models_dir,
            )
        logger.info(f"Whisper core using whisper model: {WHISPER_CONFIG.model_name}")

        if language is None:
            logger.info("no language specified - auto detecting language")

        # Load the audio and models, transcribe, and return the parsed result
        audio = whisper.load_audio(audio_path)

        asr_result = whisper.transcribe(
            whisper_model,
            audio,
            language=language,
            **asdict(WHISPER_CONFIG.transcribe_configs),
        )

        if WHISPER_CONFIG.transcribe_configs.verbose:
            logger.debug(parse_into_full_text(asr_result))

        res = parse_into_word_dicts(asr_result)
        return res

    def get_supported_formats(self) -> List[str]:
        return list(self._SUPPORTED_FORMATS)

    def get_available_models(self) -> List[str]:
        return whisper.available_models()
