import logging
import os
from typing import List, Tuple, Union
from io import StringIO, BytesIO
from gluepy.files.storages.base import BaseStorage

logger = logging.getLogger(__name__)


class MemoryStorage(BaseStorage):
    """In memory file storage, used for test suite
    and other non production workloads.
    """

    def __init__(self) -> None:
        self.FILE_SYSTEM = dict()
        super().__init__()

    def touch(self, file_path: str, content: Union[StringIO, BytesIO]) -> None:
        """Create a new blob at file path.

        Args:
            file_path (str): Path to file we want to create
            content (Union[StringIO, BytesIO]): Content of file we want to generate
        """
        if not self.exists(os.path.dirname(file_path)):
            self.mkdir(os.path.dirname(file_path))

        paths = self.abspath(file_path).split(self.separator)
        directory = self.FILE_SYSTEM
        for idx, path in enumerate(paths):
            if path not in directory and idx < len(paths) - 1:
                directory[path] = dict()

            if idx == len(paths) - 1:
                directory[path] = content
            else:
                directory = directory[path]

    def open(self, file_path: str, mode: str = "rb") -> Union[str, bytes]:
        """Opens a blob at file_path

        Args:
            file_path (str): File path of blob we want to open

        Raises:
            NotImplementedError: Base class raise NotImplementedError
        """
        paths = self.abspath(file_path).split(self.separator)
        directory = self.FILE_SYSTEM
        for idx, path in enumerate(paths):
            if path not in directory:
                raise FileNotFoundError

            if idx == len(paths) - 1:
                return directory[path].read()

            directory = directory[path]

    def rm(self, path: str, recursive: bool = False) -> None:
        """Delete a file

        Args:
            path (str): Path to file to delete
            recursive (bool): If allowed to delete recursive directories or not.
        """
        paths = self.abspath(path).split(self.separator)
        directory = self.FILE_SYSTEM
        for idx, path in enumerate(paths):
            if path not in directory:
                raise FileNotFoundError

            if idx == len(paths) - 1:
                if (
                    isinstance(directory[path], dict)
                    and not recursive
                    and directory[path]
                ):
                    raise ValueError("Trying to delete directory without recursive")
                del directory[path]
                return

            directory = directory[path]

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

        contents = self.open(src_path)
        contents = (
            StringIO(contents.decode("utf-8"))
            if isinstance(contents, bytes)
            else StringIO(contents)
        )
        self.touch(dest_path, contents)

    def ls(self, path: str) -> Tuple[List[str], List[str]]:
        """List all files and directories at given path.

        Args:
            path (str): Path where we want to list contents of

        Returns:
            Tuple[List[str], List[str]]:
              First list is files, second list is directories.
        """
        paths = self.abspath(path).split(self.separator)
        directory = self.FILE_SYSTEM
        for idx, path in enumerate(paths):
            if path not in directory:
                raise FileNotFoundError

            if idx == len(paths) - 1:
                # Its a file, ls return nothing
                if not isinstance(directory[path], dict):
                    return ([path], [])

                else:
                    return (
                        [
                            child
                            for child in directory[path]
                            if self.isfile(os.path.join(path, child))
                        ],
                        [
                            child
                            for child in directory[path]
                            if self.isdir(os.path.join(path, child))
                        ],
                    )

            directory = directory[path]

    def mkdir(self, path: str, make_parents: bool = False) -> None:
        """Make a new directory at location

        Args:
            path (str): Path of directory we want to create
            make_parents (bool, optional): If we should generate parents
            folders as well. Defaults to False.
        """
        paths = self.abspath(path).split(self.separator)
        directory = self.FILE_SYSTEM
        for path in paths:
            if path not in directory:
                directory[path] = dict()

            directory = directory[path]

    def isdir(self, path: str) -> bool:
        """Check if path is directory or not.

        Args:
            path (str): Path we want to check

        Returns:
            bool: True/False if path is directory or not
        """
        paths = self.abspath(path).split(self.separator)
        directory = self.FILE_SYSTEM
        for idx, path in enumerate(paths):
            if path not in directory:
                raise FileNotFoundError

            if idx == len(paths) - 1:
                return isinstance(directory[path], dict)

            directory = directory[path]

    def isfile(self, path: str) -> bool:
        """Check if path is a file or not.

        Args:
            path (str): Path we want to check

        Returns:
            bool: True/False if path is file or not.
        """
        paths = self.abspath(path).split(self.separator)
        directory = self.FILE_SYSTEM
        for idx, path in enumerate(paths):
            if path not in directory:
                raise FileNotFoundError

            if idx == len(paths) - 1:
                return not isinstance(directory[path], dict)

            directory = directory[path]

    def exists(self, path: str) -> bool:
        """Check if path exists or not.

        Args:
            path (str): Path we want to check

        Returns:
            bool: True/False if path is file or not.
        """
        paths = self.abspath(path).split(self.separator)
        directory = self.FILE_SYSTEM
        for path in paths:
            if path not in directory:
                return False

            directory = directory[path]

        return True
