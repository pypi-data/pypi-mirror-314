# -*- coding: utf-8 -*-
# @Author: Dan Bergen
# @Date:   2023-06-06 14:36:00
# @Last Modified by:   Your Name
# @Last Modified time: Your Time

# EXCELLENT RESOURCE FOR UNDERSTANDING: https://cloud.google.com/speech-to-text/docs/adaptation-model#improve_transcription_results_using_a_customclass

# Standard library imports
from typing import Any, List, Dict, Tuple, Callable

# Local imports

# Third party imports
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIError
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2

import logging, os

logger = logging.getLogger(__name__)

class GoogleACInterface:
    def __init__(self, api_key_path: str = None, api_key_str: str = None):
        """
        Initialize the GoogleCCInterface with API credentials.

        Args:
            api_key_path (str): Path to the JSON file containing the service account key.

        Raises:
            Exception: If the API key is invalid.
        """
        # Set up the Google Cloud credentials
       

        try:
            if (api_key_str == None) :
                self.credentials = service_account.Credentials.from_service_account_file(api_key_path)
            else: 
                self.credentials = service_account.Credentials.from_service_account_info(api_key_str)
            self.project_id = self.credentials.project_id
            print(self.project_id)
            self.client = speech.AdaptationClient(credentials=self.credentials)
        except:
            raise Exception("Connect to STT failed")

    def create_custom_class(self, custom_class_id: str, phrases: List[str]) -> Dict[str, Any]:
        """
        Create a new custom class with the given phrases.

        Args:
            custom_class_id (str): ID for the custom class.
            phrases (List[str]): List of phrases to be included in the custom class.

        Returns:
            Dict[str, Any]: The created custom class resource.

        Raises:
            GoogleAPIError: If the request fails.
        """
        parent = f"projects/{self.project_id}/locations/global"
        custom_class = speech.CustomClass(
            items=[speech.CustomClass.ClassItem(value=phrase) for phrase in phrases]
        )
        response = self._execute_google_method(self.client.create_custom_class, parent=parent, custom_class=custom_class, custom_class_id=custom_class_id)
        logger.info(f"Created Custom Class: {response.name}")
        return response

    def get_custom_class(self, custom_class_id: str) -> Dict[str, Any]:
        """
        Retrieve a custom class by its ID.

        Args:
            custom_class_id (str): ID of the custom class to retrieve.

        Returns:
            Dict[str, Any]: The retrieved custom class resource.

        Raises:
            GoogleAPIError: If the request fails.
        """
        name = f"projects/{self.project_id}/locations/global/customClasses/{custom_class_id}"
        custom_class = self._execute_google_method(self.client.get_custom_class, name=name)
        return custom_class

    def delete_custom_class(self, custom_class_id: str) -> None:
        """
        Delete a custom class by its ID.

        Args:
            custom_class_id (str): ID of the custom class to delete.

        Returns:
            None

        Raises:
            GoogleAPIError: If the request fails.
        """
        name = f"projects/{self.project_id}/locations/global/customClasses/{custom_class_id}"
        self._execute_google_method(self.client.delete_custom_class, name=name)
        logger.info(f"Deleted Custom Class: {name}")

    def update_custom_class(self, custom_class_id: str, phrases: List[str]) -> Dict[str, Any]:
        """
        Update an existing custom class with new phrases.

        Args:
            custom_class_id (str): ID of the custom class to update.
            phrases (List[str]): New list of phrases to include in the custom class.

        Returns:
            Dict[str, Any]: The updated custom class resource.

        Raises:
            GoogleAPIError: If the request fails.
        """
        name = f"projects/{self.project_id}/locations/global/customClasses/{custom_class_id}"
        custom_class = self.get_custom_class(custom_class_id)
        custom_class.items = [speech.CustomClass.ClassItem(value=phrase) for phrase in phrases]
        update_mask = field_mask_pb2.FieldMask(paths=['items'])
        response = self._execute_google_method(self.client.update_custom_class, custom_class=custom_class, update_mask=update_mask)
        logger.info(f"Updated Custom Class: {response.name}")
        return response

    def list_custom_classes(self) -> List[Dict[str, Any]]:
        """
        List all custom classes in the project.

        Returns:
            List[Dict[str, Any]]: A list of all custom class resources.

        Raises:
            GoogleAPIError: If the request fails.
        """
        parent = f"projects/{self.project_id}/locations/global"
        custom_classes = self._execute_google_method(self.client.list_custom_classes, parent=parent)
        return list(custom_classes)
    
    def create_phrase_set(self, phrase_set_id: str, phrases: List[Tuple[str, int]]) -> Dict[str, Any]:
        """
        Create a new phrase set with the given phrases.

        Args:
            phrase_set_id (str): ID for the phrase set.
            phrases (List[Tuple[str, int]]): List of tuples where each tuple contains a phrase and a boost value.

        Returns:
            Dict[str, Any]: The created phrase set resource.

        Raises:
            GoogleAPIError: If the request fails.
        """
        parent = f"projects/{self.project_id}/locations/global"
        phrase_set = speech.PhraseSet(
            phrases=[speech.PhraseSet.Phrase(value=phrase, boost=boost) for phrase, boost in phrases]
        )
        response = self._execute_google_method(self.client.create_phrase_set, parent=parent, phrase_set=phrase_set, phrase_set_id=phrase_set_id)
        logger.info(f"Created Phrase Set: {response.name}")
        return response


    def get_phrase_set(self, phrase_set_id: str) -> Dict[str, Any]:
        """
        Retrieve a phrase set by its ID.

        Args:
            phrase_set_id (str): ID of the phrase set to retrieve.

        Returns:
            Dict[str, Any]: The retrieved phrase set resource.

        Raises:
            GoogleAPIError: If the request fails.
        """
        name = f"projects/{self.project_id}/locations/global/phraseSets/{phrase_set_id}"
        phrase_set = self._execute_google_method(self.client.get_phrase_set, name=name)
        return phrase_set

    def delete_phrase_set(self, phrase_set_id: str) -> None:
        """
        Delete a phrase set by its ID.

        Args:
            phrase_set_id (str): ID of the phrase set to delete.

        Returns:
            None

        Raises:
            GoogleAPIError: If the request fails.
        """
        name = f"projects/{self.project_id}/locations/global/phraseSets/{phrase_set_id}"
        self._execute_google_method(self.client.delete_phrase_set, name=name)
        logger.info(f"Deleted Phrase Set: {name}")

    def update_phrase_set(self, phrase_set_id: str, phrases: List[Tuple[str, int]]) -> Dict[str, Any]:
        """
        Update an existing phrase set with new phrases.

        Args:
            phrase_set_id (str): ID of the phrase set to update.
            phrases (List[Tuple[str, int]]): New list of tuples where each tuple contains a phrase and a boost value.

        Returns:
            Dict[str, Any]: The updated phrase set resource.

        Raises:
            GoogleAPIError: If the request fails.
        """
        name = f"projects/{self.project_id}/locations/global/phraseSets/{phrase_set_id}"
        phrase_set = self.get_phrase_set(phrase_set_id)
        phrase_set.phrases = [speech.PhraseSet.Phrase(value=phrase, boost=boost) for phrase, boost in phrases]
        update_mask = field_mask_pb2.FieldMask(paths=['phrases'])       
        response = self._execute_google_method(self.client.update_phrase_set, phrase_set=phrase_set, update_mask=update_mask)
        logger.info(f"Updated Phrase Set: {response.name}")
        return response

    def list_phrase_sets(self) -> List[Dict[str, Any]]:
        """
        List all phrase sets in the project.

        Returns:
            List[Dict[str, Any]]: A list of all phrase set resources.

        Raises:
            GoogleAPIError: If the request fails.
        """
        parent = f"projects/{self.project_id}/locations/global"
        phrase_sets = self._execute_google_method(self.client.list_phrase_set, parent=parent)
        return list(phrase_sets)

    def _execute_google_method(
        self,
        method: Callable,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        """
        Execute a Google API method and handle exceptions.

        Args: n
            method (Callable): Google API method to execute.
            args (Any): Positional arguments to pass to the method.
            kwargs (Any): Keyword arguments to pass to the method.

        Returns:
            Any: The result of the method call if successful.

        Raises:
            GoogleAPIError: If the method call fails.
        """
        try:
            response = method(*args, **kwargs)
            return response
        except GoogleAPIError as e:
            logger.error(f"Google API method execution failed: {e}", exc_info=e)
            raise e