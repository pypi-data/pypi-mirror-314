import os
from typing import Callable, List, Optional

import boto3
import botocore.client
import botocore.config

from vessl.util.path import ensure_parent_dir_exists

from .abstract_volume import AbstractVolume
from .file import VolumeFile


class S3Volume(AbstractVolume):
    def __init__(
        self,
        aws_access_key_id: str = "",
        aws_secret_access_key: str = "",
        aws_session_token: Optional[str] = None,
        bucket_name: str = "",
        base_path: str = "",
        endpoint_url: Optional[str] = None,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        self.bucket_name = bucket_name
        self.base_path = base_path
        self.endpoint_url = endpoint_url

        self._init_s3()

    def _init_s3(self):
        cfg = botocore.config.Config(region_name="ap-northeast-2")
        s3_client = boto3.client(
            "s3",
            config=cfg,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token,
            endpoint_url=self.endpoint_url,
        )
        self.s3_client = s3_client

    def list(self, path: str) -> List[VolumeFile]:
        key = os.path.join(self.base_path, path)

        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=key,
        )

        if "Contents" not in response:
            return []

        return [
            VolumeFile(path=os.path.relpath(item["Key"], key), size=item["Size"])
            for item in response["Contents"]
            if not item["Key"].endswith("/")
        ]

    def download_file(
        self,
        file: VolumeFile,
        destination: str,
        progress_callback: Optional[Callable[[int], None]] = None,
    ):
        current_bytes = 0
        if progress_callback is not None:

            def _callback(bytes_added):
                nonlocal current_bytes
                current_bytes += bytes_added
                progress_callback(current_bytes)
        else:
            _callback = None

        key = os.path.join(self.base_path, file.path)

        ensure_parent_dir_exists(destination)

        self.s3_client.download_file(
            Bucket=self.bucket_name,
            Key=key,
            Filename=destination,
            Callback=_callback,
        )

    def download_directory(
        self,
        directory: str,
        destination: str,
        progress_callback: Optional[Callable[[int, int, int, int, int], None]] = None,
    ):
        return self._download_directory_serially(directory, destination, progress_callback)

    def upload_file(
        self,
        local_file: str,
        destination: str,
        progress_callback: Optional[Callable[[int], None]] = None,
    ):
        current_bytes = 0
        if progress_callback is not None:

            def _callback(bytes_added):
                nonlocal current_bytes
                current_bytes += bytes_added
                progress_callback(current_bytes)
        else:
            _callback = None

        key = os.path.join(self.base_path, destination)

        self.s3_client.upload_file(
            Filename=local_file, Bucket=self.bucket_name, Key=key, Callback=_callback
        )
