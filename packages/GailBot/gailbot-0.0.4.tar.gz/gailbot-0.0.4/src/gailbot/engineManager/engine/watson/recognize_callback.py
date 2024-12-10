# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-11 00:20:37
# Standard imports
from typing import List, Dict

# Local imports
# Third party imports
from copy import deepcopy
from ibm_watson.websocket import RecognizeCallback
from gailbot.shared.utils.logger import makelogger

logger = makelogger("callback")


class WatsonException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg


class CustomWatsonCallbacks(RecognizeCallback):
    """
    Extends the watson callback class to allow custom callbacks to be executed
    when an event occurs through the lifecycle of the websocket connection.

    Inherits:
        (RecognizeCallback)
    """

    def __init__(self) -> None:
        super().__init__()
        self.closure = self._init_closure()

    def reset(self) -> None:
        logger.info("Watson: reset recognize callback")
        self.closure = self._init_closure()

    def get_results(self) -> Dict:
        logger.info("Watson: on get result")
        return deepcopy(self.closure)

    def on_transcription(self, transcript: List) -> None:
        """
        Called after the service returns the final result for the transcription.
        """
        logger.info("Watson: on transcription")
        try:
            closure = self.closure
            closure["callback_status"]["on_transcription"] = True
            closure["results"]["transcript"].append(transcript)
        except Exception as e:
            logger.error(e, exc_info=e)

    def on_connected(self) -> None:
        """
        Called when a Websocket connection was made
        """
        logger.info("Watson: connected to watson")
        try:
            closure = self.closure
            closure["callback_status"]["on_connected"] = True
        except Exception as e:
            logger.error(e, exc_info=e)

    def on_error(self, error: str) -> None:
        """
        Called when there is an error in the Websocket connection.
        """
        logger.error(f"Watson: get error {error}")
        closure = self.closure
        closure["callback_status"]["on_error"] = True
        closure["results"]["error"] = error
        raise WatsonException(error)

    def on_inactivity_timeout(self, error: str) -> None:
        """
        Called when there is an inactivity timeout.
        """
        logger.warning("Watson: inactivity time out")
        try:
            closure = self.closure
            closure["callback_status"]["on_inactivity_timeout"] = True
            closure["results"]["error"] = error
        except Exception as e:
            logger.error(f"timeout error {e}")

    def on_listening(self) -> None:
        """
        Called when the service is listening for audio.
        """
        logger.info("Watson: is listening")
        try:
            closure = self.closure
            closure["callback_status"]["on_listening"] = True
        except Exception as e:
            logger.error(f"on listening error {e}")

    def on_hypothesis(self, hypothesis: str) -> None:
        """
        Called when an interim result is received.
        """
        logger.info(f"Watson: on hypothesis {hypothesis}")
        try:
            closure = self.closure
            closure["callback_status"]["on_hypothesis"] = True
        except Exception as e:
            logger.error(f"on hypothesis error {e}")

    def on_data(self, data: Dict) -> None:
        """
        Called when the service returns results. The data is returned unparsed.
        """
        logger.info(f"Watson: returned the results")
        try:
            closure = self.closure
            closure["callback_status"]["on_data"] = True
            closure["results"]["data"].append(data)
        except Exception as e:
            logger.error(f"on data error {e}", exc_info=True)

    def on_close(self) -> None:
        """
        Called when the Websocket connection is closed
        """
        logger.info("Watson: on close")
        try:
            closure = self.closure
            closure["callback_status"]["on_close"] = True
        except Exception as e:
            logger.error(f"on close error {e}", exc_info=True)

    def _init_closure(self) -> Dict:
        return {
            "callback_status": {
                "on_transcription": False,
                "on_connected": False,
                "on_error": False,
                "on_inactivity_timeout": False,
                "on_listening": False,
                "on_hypothesis": False,
                "on_data": False,
                "on_close": False,
            },
            "results": {
                "error": None,
                "transcript": list(),
                "hypothesis": list(),
                "data": list(),
            },
        }
