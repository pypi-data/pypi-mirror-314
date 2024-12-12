import os
from typing import List, Tuple, Union
from pathlib import Path
from io import StringIO, BytesIO
from gluepy.conf import default_settings, default_context


class BaseStorage:
    """Base class of a Storage implementation"""

    MAX_CHUNK_SIZE = 1_000_000
    separator = os.sep

    def abspath(self, path: str) -> str:
        """Get absolute path to file including STORAGE_ROOT"""
        return str(Path(default_settings.STORAGE_ROOT) / path)

    def relpath(self, path: str) -> str:
        """Get relative path to file, relative to STORAGE_ROOT"""
        return str(Path(path).relative_to(default_settings.STORAGE_ROOT))

    def runpath(self, path: str) -> str:
        """Get the path appended to the current context's :ref:`context_run_folder`"""
        return str(Path(default_context.gluepy.run_folder) / path)

    def _to_bytes(self, content: StringIO):
        """Write a StringIO stream to BytesIO"""
        io = BytesIO()
        while True:
            chunk = content.read(self.MAX_CHUNK_SIZE)
            if not chunk:
                break

            io.write(bytes(chunk.encode("utf-8")))

        io.seek(0, os.SEEK_SET)
        return io

    def touch(self, file_path: str, content: Union[StringIO, BytesIO]) -> None:
        """Create a new blob at file path.

        Args:
            file_path (str): Path to file we want to create
            content (Union[StringIO, BytesIO]): Content of file we want to generate
        """
        raise NotImplementedError()

    def open(self, file_path: str, mode: str = "rb") -> Union[str, bytes]:
        """Opens a blob at file_path

        Args:
            file_path (str): File path of blob we want to open

        Raises:
            NotImplementedError: Base class raise NotImplementedError
        """
        raise NotImplementedError()

    def rm(self, path: str, recursive: bool = False) -> None:
        """Delete a file

        Args:
            path (str): Path to file to delete
            recursive (bool): If allowed to delete recursive directories or not.
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

    def ls(self, path: str) -> Tuple[List[str], List[str]]:
        """List all files and directories at given path.

        Args:
            path (str): Path where we want to list contents of

        Returns:
            Tuple[List[str], List[str]]:
              First list is files, second list is directories.
        """
        raise NotImplementedError()

    def mkdir(self, path: str, make_parents: bool = False) -> None:
        """Make a new directory at location

        Args:
            path (str): Path of directory we want to create
            make_parents (bool, optional): If we should generate parents
            folders as well. Defaults to False.
        """
        raise NotImplementedError()

    def isdir(self, path: str) -> bool:
        """Check if path is directory or not.

        Args:
            path (str): Path we want to check

        Returns:
            bool: True/False if path is directory or not
        """
        raise NotImplementedError()

    def isfile(self, path: str) -> bool:
        """Check if path is a file or not.

        Args:
            path (str): Path we want to check

        Returns:
            bool: True/False if path is file or not.
        """
        raise NotImplementedError()

    def exists(self, path: str) -> bool:
        """Check if path exists or not.

        Args:
            path (str): Path we want to check

        Returns:
            bool: True/False if path is file or not.
        """
        raise NotImplementedError()
