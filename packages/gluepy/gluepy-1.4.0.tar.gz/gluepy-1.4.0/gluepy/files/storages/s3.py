import os
import logging
from typing import List, Tuple, Union
from pathlib import Path
from io import StringIO, BytesIO
from gluepy.conf import default_settings
from gluepy.exceptions import BootstrapError

try:
    import boto3
    from botocore.client import Config
    from botocore.exceptions import ClientError
except ImportError as e:
    raise BootstrapError("Could not load Boto3's S3 bindings. %s" % e)
from gluepy.files.storages.base import BaseStorage

logger = logging.getLogger(__name__)


class S3Storage(BaseStorage):
    """
    Storage backend to support S3 based storages such as
    AWS S3 or DigitalOcean Spaces.
    """

    MAX_CHUNK_SIZE = 32_000_000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._connection = None
        self._bucket = None
        self.region_name = default_settings.AWS_S3_REGION_NAME
        self.use_ssl = True
        self.endpoint_url = default_settings.AWS_S3_ENDPOINT_URL
        self.config = Config(
            s3={"addressing_style": None},
            signature_version=None,
            proxies=None,
        )
        self.verify = True
        self.access_key, self.secret_key = (
            default_settings.AWS_ACCESS_KEY_ID,
            default_settings.AWS_SECRET_ACCESS_KEY,
        )

    @property
    def connection(self):
        if self._connection is None:
            session = boto3.session.Session(
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
            )
            self._connection = session.resource(
                "s3",
                region_name=self.region_name,
                use_ssl=self.use_ssl,
                endpoint_url=self.endpoint_url,
                config=self.config,
                verify=self.verify,
            )

        return self._connection

    @property
    def bucket(self):
        if self._bucket is None:
            self._bucket = self.connection.Bucket(
                default_settings.AWS_STORAGE_BUCKET_NAME
            )
        return self._bucket

    def touch(self, file_path: str, content: Union[StringIO, BytesIO]) -> None:
        """Create a new blob at file path.

        Args:
            file_path (str): Path to file we want to create
            content (Union[StringIO, BytesIO]): Content of file we want to generate

        Raises:
            NotImplementedError: Base class raise NotImplementedError
        """
        if isinstance(content, StringIO):
            content = self._to_bytes(content)
        obj = self.bucket.Object(file_path)
        content.seek(0, os.SEEK_SET)
        obj.upload_fileobj(content)
        return file_path

    def open(self, file_path: str, mode: str = "rb") -> Union[str, bytes]:
        """Opens a blob at file_path

        Args:
            file_path (str): File path of blob we want to open

        Raises:
            NotImplementedError: Base class raise NotImplementedError
        """
        logger.debug(f"Reading file from path '{file_path}'")
        obj = self.bucket.Object(file_path)
        handler = BytesIO()
        obj.download_fileobj(handler)
        handler.seek(0, os.SEEK_SET)
        return (
            handler.read()
            if "b" in mode
            else handler.read().decode("utf-8", errors="ignore")
        )

    def ls(self, path: str) -> Tuple[List[str], List[str]]:
        """List all files and directories at given path.

        Args:
            path (str): Path where we want to list contents of

        Raises:
            NotImplementedError: Base class raise NotImplementedError

        Returns:
            Tuple[List[str], List[str]]:
              First list is files, second list is directories.
        """
        path = self.abspath(path)
        # The path needs to end with a slash, but if the root is empty, leave it.
        if path and not path.endswith("/"):
            path += "/"

        directories = []
        files = []
        paginator = self.connection.meta.client.get_paginator("list_objects")
        pages = paginator.paginate(
            Bucket=default_settings.AWS_STORAGE_BUCKET_NAME,
            Delimiter="/",
            Prefix=path,
            PaginationConfig={"PageSize": 1000},
        )
        for page in pages:
            for entry in page.get("CommonPrefixes", ()):
                directories.append(self.relpath(entry["Prefix"]))
            for entry in page.get("Contents", ()):
                key = entry["Key"]
                if key != path:
                    files.append(self.relpath(key))
        return directories, files

    def mkdir(self, path: str, make_parents: bool = False) -> None:
        """Make a new directory at location

        Args:
            path (str): Path of directory we want to create
            make_parents (bool, optional): If we should generate parents
              folders as well. Defaults to False.

        Raises:
            NotImplementedError: Base class raise NotImplementedError
        """
        self.touch(str(Path(path) / ".empty"))

    def rm(self, path: str, recursive: bool = False) -> None:
        """Delete a file

        Args:
            path (str): Path to file to delete
            recursive (bool): If allowed to delete recursive directories or not.

        """
        if recursive:
            raise NotImplementedError("`recursive` not supported")
        self.bucket.Object(path).delete()

    def cp(
        self,
        src_path: str,
        dest_path: str,
        recursive: bool = False,
        overwrite: bool = False,
    ) -> None:
        """Copy a file from source to destination

        Args:
            src_path (str): Path to file or directory to copy.
            dest_path (str): Path to file or directory to copy to.
            recursive (bool): If should copy sub directories as well.
            overwrite (bool): If should copy to destination that already exists.
        """
        if recursive or overwrite:
            raise NotImplementedError("`recursive` and `overwrite` not supported.")

        self.touch(dest_path, self.open(src_path))

    def isdir(self, path: str) -> bool:
        """Check if path is directory or not.

        Args:
            path (str): Path we want to check

        Raises:
            NotImplementedError: Base class raise NotImplementedError

        Returns:
            bool: True/False if path is directory or not
        """
        raise NotImplementedError()

    def isfile(self, path: str) -> bool:
        """Check if path is a file or not.

        Args:
            path (str): Path we want to check

        Raises:
            NotImplementedError: Base class raise NotImplementedError

        Returns:
            bool: True/False if path is file or not.
        """
        raise NotImplementedError()

    def exists(self, path: str) -> bool:
        """Check if path exists or not.

        Args:
            path (str): Path we want to check

        Raises:
            NotImplementedError: Base class raise NotImplementedError

        Returns:
            bool: True/False if path is file or not.
        """
        try:
            self.connection.meta.client.head_object(
                Bucket=default_settings.AWS_STORAGE_BUCKET_NAME, Key=path
            )
            return True
        except ClientError:
            return False
