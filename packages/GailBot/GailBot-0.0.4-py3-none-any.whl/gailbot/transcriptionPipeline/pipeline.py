# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-09 10:09:26
# @Description: Implement static functions to transcribe multiple sources in parallel
from concurrent.futures import ThreadPoolExecutor, wait
from dataclasses import dataclass
from typing import List

from gailbot.payload import PayloadObject
from gailbot.shared.utils.logger import makelogger
from gailbot.sourceManager.sourceObject import SourceObject


@dataclass(init=True)
class TranscriptionResult:
    success_output: List[str]
    failure: List[str]
    invalid: List[str]


@dataclass(init=True)
class PayloadTranscriptionResult:
    success: List[PayloadObject]
    failure: List[PayloadObject]


@dataclass(init=True)
class ConvertResult:
    converted: List[PayloadObject]
    invalid: List[SourceObject]
    original_source_ids: List[str]


class GBPipeline:
    logger = makelogger("transcriptionPipeline")

    @staticmethod
    def convert(sources: List[SourceObject]) -> ConvertResult:
        """
        Convert a list of sources to payload objects

        Notes
        ----------
            This is only used for developer to write applications that use gailbot for more fine-grained
            control to the transcription process

        Parameters
        ----------
        sources:
            Each SourceObject in the list sources must be applied with a valid profile setting

        Returns
        -------
            [ConvertResult.converted] stores a list of converted payload
            [ConvertResult.invalid] stores a list of invalid SourceObject
            [ConvertResult.original_source_ids] stores the list of original source id being converted
        """
        converted: List[PayloadObject] = []
        invalid: List[SourceObject] = []
        for s in sources:
            try:
                new_payload = s.convert()
                if not new_payload:
                    invalid.append(s)
                converted.extend(new_payload)
            except Exception as e:
                GBPipeline.logger.error(f"failed to convert {s.source_path}")
                GBPipeline.logger.error(e, exc_info=True)
                invalid.append(s)
        source_ids = [s.name for s in sources]
        return ConvertResult(converted, invalid, source_ids)

    @staticmethod
    def transcribe_payloads(
        payloads: List[PayloadObject],
    ) -> PayloadTranscriptionResult:
        """
        Transcribe a given list of payloads in parallel

        Notes
        ----------
            This is only used for developer to write applications that use gailbot for more fine-grained
            control to the transcription process

        Parameters
        ----------
        payloads:
            A list of valid payload where the transcription will start when payload.start_execute function
            is evoked

        Returns
        -------
            [PayloadTranscriptionResult.success] stores a list of successfully transcribed payload
            [PayloadTranscriptionResult.failure] stores a list of failed payload
        """
        io_thread_limit = 15
        cpu_thread_limit = 1
        success = list()
        failure = list()
        futures = dict()

        cpu_bound = []
        io_bound = []

        for payload in payloads:
            if payload.profile.engine_provider.is_cpu_intensive():
                cpu_bound.append(payload)
            else:
                io_bound.append(payload)

        # use separate threadpool executor for cpu and io bound engine
        if io_bound:
            io_executor = ThreadPoolExecutor(
                max_workers=min(len(io_bound), io_thread_limit)
            )
            for payload in io_bound:
                futures[payload] = io_executor.submit(payload.start_execute)

        if cpu_bound:
            cpu_executor = ThreadPoolExecutor(max_workers=cpu_thread_limit)
            for payload in cpu_bound:
                futures[payload] = cpu_executor.submit(payload.start_execute)

        wait(list(futures.values()))
        for payload, future in futures.items():
            if future.result():
                success.append(payload)
            else:
                failure.append(payload)

        return PayloadTranscriptionResult(success=success, failure=failure)

    @staticmethod
    def transcribe(sources: List[SourceObject]) -> TranscriptionResult:
        """
        Transcribe the list of sources

        Notes
        ----------
            This is the wrapper function for convert and transcribe_payloads used by gailbot api

        Parameters
        ----------
        sources:
            Each SourceObject in the list sources must be applied with a valid profile setting

        Returns
        -------
            [TranscriptionResult.success] stores the output path to the successfully transcribed payloads
            [TranscriptionResult.fail] stores the names of failure sources
            [TranscriptionResult.invalid] stores the names of invalid sources

        """
        payload_result = GBPipeline.convert(sources)
        transcribe_result = GBPipeline.transcribe_payloads(payload_result.converted)
        return TranscriptionResult(
            [s.output_dir for s in transcribe_result.success],
            [f.name for f in transcribe_result.failure],
            [i.name for i in payload_result.invalid],
        )
