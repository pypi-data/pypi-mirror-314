from typing import Any


class BaseDataManager:
    """Base abstract class for data managers
    that define interface.
    """

    def read(self, path: str, root: bool = False, *args, **kwargs) -> Any:
        """Read dataframe from a file.

        Args:
            path (str): Path to file located on :setting:`STORAGE_BACKEND`.
            root (bool, optional): Is path relative to root or run folder.
                Defaults to False.

        Returns:
            Any: Dataframe depending on implementation.

        """
        raise NotImplementedError()

    def read_sql(self, sql: str, *args, **kwargs) -> Any:
        """Read dataframe from SQL query

        Args:
            sql (str): SQL query to execute to get dataframe.

        Returns:
            Any: Dataframe depending on implementation
        """
        raise NotImplementedError()

    def write(self, path: str, df: Any, root: bool = False, *args, **kwargs) -> None:
        """Write dataframe to file.

        Args:
            path (str): Path to where to write dataframe
            df (Any): Dataframe to be written
            root (bool, optional): If path relatove to root or run folder.
                Defaults to False.

        """
        raise NotImplementedError()
