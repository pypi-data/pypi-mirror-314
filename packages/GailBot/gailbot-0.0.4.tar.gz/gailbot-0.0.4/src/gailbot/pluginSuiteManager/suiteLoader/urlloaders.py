# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-08-01 05:34:44
import os
import re
import boto3
import requests
from botocore.exceptions import ParamValidationError
from cryptography.fernet import Fernet
from typing import List, IO, TextIO
from abc import ABC
from .directoryloader import PluginDirectorySuiteLoader
from gailbot.shared.utils.logger import makelogger
from gailbot.shared.utils.general import read_toml, delete
from gailbot.configs import PLUGIN_CONFIG
from gailbot.shared.utils.download import download_from_urls

from ..suite.pluginData import ConfModel
from ..suite.suite import PluginSuite

logger = makelogger("url_loader")


class UrlLoader(ABC):
    """base class for loading plugin from url"""

    def __init__(self, download_dir, suites_dir) -> None:
        self.download_dir = download_dir
        self.suites_dir = suites_dir
        self.dir_loader = PluginDirectorySuiteLoader(suites_dir)
        super().__init__()

    @staticmethod
    def is_supported_url(url: str) -> bool:
        """
        check if the url is supported
        """
        raise NotImplementedError

    def load(self, url: str, f: IO) -> List[PluginSuite]:
        """load the source from the url"""
        raise NotImplementedError


class ZipUrlLoader(UrlLoader):
    """load plugin from an url source"""

    def __init__(self, download_dir, suites_dir) -> None:
        """initialize the plugin loader

        Args:
            download_dir (str): path to where the plugin suite will be downloaded
            suites_dir (str): path to where the plugin will be stored after
                              download
        """
        super().__init__(download_dir, suites_dir)

    @staticmethod
    def is_supported_url(url: str) -> bool:
        try:
            response = requests.head(url)
            content_type = response.headers.get('content-type', '')
            # Check if the content type indicates a zip file
            return content_type.lower() == 'application/zip' or url.lower().endswith('.zip')
        except requests.RequestException as e:
            return False

    def load(self, url: str, f: TextIO) -> [PluginSuite]:
        if not self.is_supported_url(url):
            return []

        download_path = download_from_urls(
            urls=[url], download_dir=self.download_dir, unzip=True
        )[0]

        suite_name = None
        suite_path = None

        # get the suite name from the toml file
        for root, dirs, files in os.walk(download_path):
            if PLUGIN_CONFIG.CONFIG in files:
                config = os.path.join(root, PLUGIN_CONFIG.CONFIG)
                suite_name = ConfModel(**read_toml(config)).suite.name
                break

        # get the suite directory
        for dirpath, dirnames, filename in os.walk(download_path):
            if suite_name in dirnames:
                suite_path = os.path.join(dirpath, suite_name)
                logger.info(f"the directory path is {suite_path}")
                break

        if not suite_name:
            f.write(f"{url} does not store a valid {PLUGIN_CONFIG.CONFIG} configuration file\n")
            return []
        if not suite_path:
            f.write(f"{suite_path} does not exist\n")
            return []

        suites = self.dir_loader.load(suite_path, f)
        delete(download_path)
        return suites


class S3BucketLoader(UrlLoader):
    """load plugin from an url source"""
    fernet = Fernet(PLUGIN_CONFIG.EN_KEY)
    aws_api_key = fernet.decrypt(PLUGIN_CONFIG.ENCRYPTED_API_KEY).decode()
    aws_id = fernet.decrypt(PLUGIN_CONFIG.ENCRYPTED_API_ID).decode()

    def __init__(self, download_dir, suites_dir) -> None:
        """initialize the plugin loader

        Args:
            download_dir (str): path to where the plugin suite will be downloaded
            suites_dir (str): path to where the plugin will be stored after
                              download
        """
        super().__init__(download_dir, suites_dir)
        self.download_dir = download_dir
        self.suites_dir = suites_dir

    @staticmethod
    def is_supported_url(bucket: str) -> bool:
        try:
            r3 = boto3.resource(
                "s3", aws_access_key_id=S3BucketLoader.aws_id, aws_secret_access_key=S3BucketLoader.aws_api_key
            )
            r3.meta.client.head_bucket(Bucket=bucket)
            return True
        except ParamValidationError:
            return False
        except Exception as e:
            return False

    def load(self, bucket: str, f: TextIO) -> List[PluginSuite]:
        if not self.is_supported_url(bucket):
            return []

        s3 = boto3.client(
            "s3", aws_access_key_id=self.aws_id, aws_secret_access_key=self.aws_api_key
        )

        plugin_suites = []
        # get all object from teh bucket

        objects = s3.list_objects_v2(Bucket=bucket)["Contents"]
        for obj in objects:
            key = obj["Key"]
            if "zip" in key:
                # Generate a pre-signed URL for the object
                url = s3.generate_presigned_url(
                    "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600
                )
                url = url[0: url.index("?")]
                logger.info(f"loading plugin from url {url}")
                ZipLoader = ZipUrlLoader(self.download_dir, self.suites_dir)
                plugin_suites.extend(ZipLoader.load(url, f))
        return plugin_suites
