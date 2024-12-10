# -*- coding: utf-8 -*-
# @Author: Erin & Joanne
# @Date:   2024-02-11 13:26:17
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-02-18 14:53:37
# @Description: Provides method retrieve metadata from aws buckets and objects.

import boto3
import os
from cryptography.fernet import Fernet
from gailbot.configs import PLUGIN_CONFIG


class S3BucketManager:
    fernet = Fernet(PLUGIN_CONFIG.EN_KEY)
    aws_api_key = fernet.decrypt(PLUGIN_CONFIG.ENCRYPTED_API_KEY).decode()
    aws_api_id = fernet.decrypt(PLUGIN_CONFIG.ENCRYPTED_API_ID).decode()

    def __init__(self):

        pass

    # Retrieve and return the version of the bucket
    # TODO: exceptions are not catched here. Caller expected to catch exceptions
    def get_remote_version(self, bucket_name, object_name) -> str:
        """
        If bucket_name and object_name identifies an existing object in aws s3 bucket, and the
        object has s3 remote metadata for version, returns the updated version of the object

        Parameters
        ----------
        bucket_name
        object_name

        Returns
        -------
        str

        Raises
        -------

        """
        s3 = boto3.client(
            "s3",
            aws_access_key_id=S3BucketManager.aws_api_id,
            aws_secret_access_key=S3BucketManager.aws_api_key,
        )

        s3_object = s3.head_object(Bucket=bucket_name, Key=object_name)
        object_metadata = s3_object["Metadata"]

        return object_metadata["version"]
    

    def download_plugin(self, bucket_name: str, prefix: str, local_dir: str) -> None:
        """
        Download all objects under a specific prefix from the S3 bucket to the given local directory.

        Parameters
        ----------
        bucket_name : str
            Name of the S3 bucket.
        prefix : str
            Prefix in the bucket (like a folder path) leading to a specififc plugin folder.
            should be in the form "plugins/{creator_id}/{plugin id}"
        local_dir : str
            Local directory where the downloaded files will be stored.
            should lead to "plugin id" as well

        Raises
        ------
        Exception
            If download fails for any file, an error will be logged or raised.
        """

        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        # List all objects under the given prefix (e.g., "plugins/")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=S3BucketManager.aws_api_id,
            aws_secret_access_key=S3BucketManager.aws_api_key,
        )
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' not in response:
            print(f"No files found under prefix '{prefix}' in bucket '{bucket_name}'.")
            return

        # Iterate over each object and download it
        for obj in response['Contents']:
            object_key = obj['Key']

            # Create full local path by appending the object's relative path
            relative_path = os.path.relpath(object_key, prefix)  # Keeps directory structure intact
            local_path = os.path.join(local_dir, relative_path)

            # Ensure the directories in the local path exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            print(f"Downloading {object_key} to {local_path}...")
            try:
                s3.download_file(bucket_name, object_key, local_path)
            except Exception as e:
                print(f"Failed to download {object_key}: {e}")