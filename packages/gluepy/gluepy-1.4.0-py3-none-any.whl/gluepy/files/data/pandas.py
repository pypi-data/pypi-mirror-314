import logging
from io import BytesIO
import os
import pandas as pd
from gluepy.files.data import BaseDataManager
from gluepy.conf import default_settings
from gluepy.files.storages import default_storage

logger = logging.getLogger(__name__)


class PandasDataManager(BaseDataManager):
    """Data Manager that implement read and write actions for
    pandas dataframes on the currently set storage backend.
    """

    def read(self, path: str, root: bool = False, *args, **kwargs) -> pd.DataFrame:
        """Read in a pandas dataframe from path.

        Args:
            path (str): Path to file to read in.
            root (bool, optional): If path is relative to root or run folder.
                Defaults to False.

        Raises:
            ValueError: Raised if file extension is not supported.

        Returns:
            pd.DataFrame: Loaded pandas dataframe
        """
        _, ext = os.path.splitext(path)
        if ext in {".csv", ".txt"}:
            return self._read_csv(path, root, *args, **kwargs)
        elif ext in {".pq", ".parquet"}:
            return self._read_parquet(path, root, *args, **kwargs)
        elif ext in {
            ".json",
        }:
            return self._read_json(path, root, *args, **kwargs)
        else:
            raise ValueError(
                f"'{self.__class__.__name__}' does not support "
                f"reading files of extension '{ext}'"
            )

    def read_sql(self, sql: str, *args, **kwargs) -> pd.DataFrame:
        try:
            import pandas_gbq
        except ImportError:
            logger.error("Dependency 'pandas_gbq' must be installed to read SQL")
            raise
        return pandas_gbq.read_gbq(
            sql,
            project_id=default_settings.GCP_PROJECT_ID,
            use_bqstorage_api=True,
            *args,
            **kwargs,
        )

    def write(
        self, path: str, df: pd.DataFrame, root: bool = False, *args, **kwargs
    ) -> None:
        """Write pandas dataframe to path on default storage backend.

        Args:
            path (str): Path to destination of dataframe.
            df (pd.DataFrame): Dataframe to be written.
            root (bool, optional): If path is relative to root or run folder.
                Defaults to False.

        Raises:
            ValueError: Raised if file extension is not supported.
        """
        _, ext = os.path.splitext(path)
        if ext in {".csv", ".txt"}:
            self._write_csv(path, df, root, *args, **kwargs)
        elif ext in {".pq", ".parquet"}:
            self._write_parquet(path, df, root, *args, **kwargs)
        else:
            raise ValueError(
                f"'{self.__class__.__name__}' does not support "
                f"writing files of extension '{ext}'"
            )

    def _read_csv(self, path: str, root: bool = False, *args, **kwargs):
        """Implementation of reading csv file"""
        stream = BytesIO(
            default_storage.open(
                path if root is True else default_storage.runpath(path)
            )
        )
        logger.info(f"Reading file from path '{path}'.")
        return pd.read_csv(stream, *args, **kwargs)

    def _read_parquet(self, path: str, root: bool = False, *args, **kwargs):
        """Implementation of reading parquet file"""
        stream = BytesIO(
            default_storage.open(
                path if root is True else default_storage.runpath(path)
            )
        )
        logger.info(f"Reading file from path '{path}'.")
        return pd.read_parquet(stream, *args, **kwargs)

    def _read_json(self, path: str, root: bool = False, *args, **kwargs):
        """Implementation of reading json file"""
        stream = BytesIO(
            default_storage.open(
                path if root is True else default_storage.runpath(path)
            )
        )
        logger.info(f"Reading file from path '{path}'.")
        return pd.read_json(stream, *args, **kwargs)

    def _write_csv(
        self, path: str, df: pd.DataFrame, root: bool = False, *args, **kwargs
    ):
        """Implementation of writing csv file"""
        path = path if root is True else default_storage.runpath(path)
        logger.info(f"Writing file to path '{path}'.")
        stream = BytesIO()
        df.to_csv(stream, *args, **kwargs)
        stream.seek(0, os.SEEK_SET)

        default_storage.touch(file_path=path, content=stream)

    def _write_parquet(
        self, path: str, df: pd.DataFrame, root: bool = False, *args, **kwargs
    ):
        """Implementation of reading parquet file"""
        path = path if root is True else default_storage.runpath(path)
        logger.info(f"Writing file to path '{path}'.")
        stream = BytesIO()
        df.to_parquet(stream, *args, **kwargs)
        stream.seek(0, os.SEEK_SET)

        default_storage.touch(file_path=path, content=stream)
