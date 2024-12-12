import os
import shutil
import logging
from typing import List, Tuple, Union
from io import StringIO, BytesIO
from gluepy.files.storages.base import BaseStorage

logger = logging.getLogger(__name__)


class LocalStorage(BaseStorage):
    """Storage implementation of local file system interactions"""

    MAX_CHUNK_SIZE = 4_000_000

    def touch(self, file_path: str, content: Union[StringIO, BytesIO]) -> None:
        """Create a new blob at file path.

        Args:
            file_path (str): Path to file we want to create
            content (Union[StringIO, BytesIO]): Content of file we want to generate

        Raises:
            TypeError: Raises type error if the chunk read in from the content
              stream is not a valid type.
        """
        # Local file system require directories to exist before blobs are created.
        if not self.exists(os.path.dirname(file_path)):
            self.mkdir(os.path.dirname(file_path))

        logger.debug(f"Writing file to path '{self.abspath(file_path)}'.")
        with open(self.abspath(file_path), mode="wb") as stream:
            while True:
                chunk = content.read(self.MAX_CHUNK_SIZE)
                if not chunk:
                    break

                if isinstance(chunk, str):
                    chunk = chunk.encode("utf-8")
                elif not isinstance(chunk, bytes):
                    raise TypeError("Chunk is neither bytes or string")

                stream.write(chunk)

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
        if self.isdir(src_path) and not recursive:
            raise ValueError(f"recursive must be True if '{src_path}' is a directory")
        if self.exists(dest_path) and not overwrite:
            raise FileExistsError(
                f"'{dest_path}' already exists and overwrite is False"
            )
        if not self.exists(os.path.dirname(dest_path)):
            self.mkdir(os.path.dirname(dest_path))
        shutil.copy2(
            self.abspath(src_path), self.abspath(dest_path), follow_symlinks=True
        )

    def open(self, file_path: str, mode: str = "rb") -> Union[str, bytes]:
        """Opens a blob at file_path

        Args:
            file_path (str): File path of blob we want to open
            mode (str): The read mode of the file, if should return string or bytes.

        Returns:
            bytes: Returns the string or byte content of the file.
        """
        logger.debug(f"Reading file from path '{self.abspath(file_path)}'.")
        with open(self.abspath(file_path), mode=mode) as stream:
            f = stream.read()
        return f

    def ls(self, path: str) -> Tuple[List[str], List[str]]:
        """List all files and directories at given path.

        Args:
            path (str): Path where we want to list contents of

        Raises:
            ValueError: Raises a ValueError if the isdir and isfile functions cannot
                identify if a blob is a file or a dir.

        Returns:
            Tuple[List[str], List[str]]:
              First list is files, second list is directories.
        """
        files = []
        dirs = []
        blobs = [
            self.abspath(os.path.join(path, fpath))
            for fpath in os.listdir(self.abspath(path))
        ]

        for b in blobs:
            if self.isdir(b):
                dirs.append(self.relpath(b))
            elif self.isfile(b):
                files.append(self.relpath(b))
            else:
                raise ValueError(f"File '{b}' is neither a file or directory.")

        return files, dirs

    def mkdir(self, path: str, make_parents: bool = False) -> None:
        """Make a new directory at location

        Args:
            path (str): Path of directory we want to create

        """
        os.makedirs(self.abspath(path), exist_ok=True)

    def isdir(self, path: str) -> bool:
        """Check if path is directory or not.

        Args:
            path (str): Path we want to check

        Raises:
            FileNotFoundError: Raise error if the path cannot be found.

        Returns:
            bool: True/False if path is directory or not
        """
        if not self.exists(path):
            raise FileNotFoundError(f"Path '{path}' does not exist.")

        return os.path.isdir(self.abspath(path))

    def isfile(self, path: str) -> bool:
        """Check if path is a file or not.

        Args:
            path (str): Path we want to check

        Raises:
            FileNotFoundError: Raise error if the path cannot be found.

        Returns:
            bool: True/False if path is file or not.
        """
        if not self.exists(path):
            raise FileNotFoundError(f"Path '{path}' does not exist.")

        return os.path.isfile(self.abspath(path))

    def exists(self, path: str) -> bool:
        """Check if path exists or not.

        Args:
            path (str): Path we want to check

        Returns:
            bool: True/False if path is file or not.
        """
        return os.path.exists(self.abspath(path))
