# -*- coding: utf-8 -*-
# @Author: Vivian Li 
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Vivian Li 
# @Last Modified time: 2024-02-06 16:08:36
from typing import List, TextIO

from gailbot.pluginSuiteManager.suite.suite import PluginSuite
from gailbot.pluginSuiteManager.suiteLoader.pluginSuiteLoader import PluginSuiteLoader
from gailbot.pluginSuiteManager.suiteLoader.urlloaders import ZipUrlLoader, \
    S3BucketLoader, UrlLoader


class PluginURLSuiteLoader(PluginSuiteLoader):
    url_loader_classes = [ZipUrlLoader, S3BucketLoader]

    def __init__(self, download_dir: str, suites_dir: str) -> None:
        super().__init__()
        self.download_dir = download_dir
        self.url_loaders: List[UrlLoader] = [
            ZipUrlLoader(download_dir, suites_dir),
            S3BucketLoader(download_dir, suites_dir),
        ]

    @property
    def supported_url_source(self):
        """return a list of supported url downloading source"""
        return ["github", "amazon s3"]

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        check if the url string is valid

        Args:
            url (str): a string that represent the url

        Returns:
            bool: true if the string is valid url false otherwise
        """
        for loader in PluginURLSuiteLoader.url_loader_classes:
            if loader.is_supported_url(url):
                return True
        return False

    def load(self, url: str, f: TextIO) -> List[PluginSuite]:
        for loader in self.url_loaders:
            suites = loader.load(url, f)
            if suites:
                return suites
        return []
