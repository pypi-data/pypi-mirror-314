from typing import Dict, List, Optional, Union, Any
from datetime import datetime
import logging
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)


class BaseOpsBackend:
    """Backend interface for Gluepy operations.

    This class defines the interface for tracking and storing run information,
    similar to MLFlow's but tool agnostic to be extended for tool-specific
    implementations.
    """

    def create_run(
        self,
        dag: str,
        run_id: Optional[str] = None,
        config: Optional[Dict] = None,
        username: Optional[str] = "AnonymousUser",
    ) -> str:
        """Creates a new run in the backend storage.

        Args:
            dag: Name of the DAG being executed
            run_id: Optional unique identifier for the run. If not provided,
                   one will be generated.
            config: Optional dictionary containing the run configuration
            username: Optional username of the person creating the run

        Returns:
            str: The run_id of the created run

        Raises:
            NotImplementedError: Method needs to be implemented by concrete class
        """
        raise NotImplementedError

    def get_run(self, run_id: str) -> Dict:
        """Gets the run information for the specified run_id.

        Args:
            run_id: The unique identifier for the run

        Returns:
            Dict: Dictionary containing the run information

        Raises:
            NotImplementedError: Method needs to be implemented by concrete class
        """
        raise NotImplementedError

    def list_runs(
        self,
        dag: Optional[str] = None,
        username: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> List[Dict]:
        """Lists runs matching the specified criteria.

        Args:
            dag: Optional DAG name to filter runs
            username: Optional username to filter runs
            start_time: Optional start time for filtering runs
            end_time: Optional end time for filtering runs

        Returns:
            List[Dict]: List of dictionaries containing run information

        Raises:
            NotImplementedError: Method needs to be implemented by concrete class
        """
        raise NotImplementedError

    def log_metric(
        self,
        key: str,
        value: Union[float, int],
        timestamp: Optional[datetime] = None,
    ) -> None:
        """Logs a metric for a run.

        Args:
            run_id: The run to log the metric for
            key: Metric name
            value: Metric value (must be numeric)
            timestamp: Optional timestamp for the metric

        Raises:
            NotImplementedError: Method needs to be implemented by concrete class
        """
        raise NotImplementedError

    def log_param(
        self,
        key: str,
        value: str,
    ) -> None:
        """Logs a parameter for a run.

        Args:
            run_id: The run to log the parameter for
            key: Parameter name
            value: Parameter value

        Raises:
            NotImplementedError: Method needs to be implemented by concrete class
        """
        raise NotImplementedError

    def log_artifact(
        self,
        local_path: str,
        artifact_path: Optional[str] = None,
    ) -> None:
        """Logs an artifact (file) for a run.

        Args:
            run_id: The run to log the artifact for
            local_path: Path to the file to log
            artifact_path: Optional path where the artifact should be stored

        Raises:
            NotImplementedError: Method needs to be implemented by concrete class
        """
        raise NotImplementedError

    def set_terminated(
        self,
        run_id: str,
        status: str,
        end_time: Optional[datetime] = None,
    ) -> None:
        """Sets a run's status to terminated.

        Args:
            run_id: The run to terminate
            status: The final status (e.g., 'FINISHED', 'FAILED', 'KILLED')
            end_time: Optional end time for the run

        Raises:
            NotImplementedError: Method needs to be implemented by concrete class
        """
        raise NotImplementedError

    def delete_run(self, run_id: str) -> None:
        """Deletes a run and all its associated data.

        Args:
            run_id: The run to delete

        Raises:
            NotImplementedError: Method needs to be implemented by concrete class
        """
        raise NotImplementedError

    def log_input(
        self,
        df: Any,
        context: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs,
    ) -> None:
        """Logs an input source for a run.

        Args:
            df: Dataframe containing the input data
            context: Optional string providing additional context about the input
            tags: Optional dictionary of tags to associate with this input

        Raises:
            NotImplementedError: Method needs to be implemented by concrete class
        """
        raise NotImplementedError


class LoggingOpsBackend(BaseOpsBackend):
    """Simple logging-based MLOps backend that logs operations to stdout.

    This implementation provides a basic way to track ML operations by logging
    them to stdout using Python's logging module. Useful for development and
    debugging purposes.
    """

    def create_run(
        self,
        dag: str,
        run_id: Optional[str] = None,
        config: Optional[Dict] = None,
        username: Optional[str] = "AnonymousUser",
    ) -> str:
        """Creates a new run and logs its creation."""
        if run_id is None:
            run_id = str(uuid.uuid4())

        logger.info(
            "Created new run: \n"
            f"Run ID: {run_id}\n"
            f"DAG: {dag}\n"
            f"Username: {username}\n"
            f"Config: {config}"
        )
        return run_id

    def get_run(self, run_id: str) -> Dict:
        """Gets run information by logging the request."""
        logger.info(f"Retrieving run information for run_id: {run_id}")
        # In a logging-only backend, we can't actually retrieve historical data
        return {
            "run_id": run_id,
            "status": "UNKNOWN",
            "start_time": None,
            "end_time": None,
        }

    def list_runs(
        self,
        dag: Optional[str] = None,
        username: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> List[Dict]:
        """Lists runs matching criteria by logging the request."""
        logger.info(
            "Listing runs with filters:\n"
            f"DAG: {dag}\n"
            f"Username: {username}\n"
            f"Start time: {start_time}\n"
            f"End time: {end_time}"
        )
        # In a logging-only backend, we can't actually retrieve historical data
        return []

    def log_metric(
        self,
        key: str,
        value: Union[float, int],
        timestamp: Optional[datetime] = None,
    ) -> None:
        """Logs a metric by printing it to stdout."""
        current_time = timestamp or datetime.now()
        logger.info(
            f"Logging metric at {current_time}:\n" f"Key: {key}\n" f"Value: {value}"
        )

    def log_param(
        self,
        key: str,
        value: str,
    ) -> None:
        """Logs a parameter by printing it to stdout."""
        logger.info("Logging parameter:\n" f"Key: {key}\n" f"Value: {value}")

    def log_artifact(
        self,
        local_path: str,
        artifact_path: Optional[str] = None,
    ) -> None:
        """Logs an artifact by printing its path information to stdout."""
        dest_path = artifact_path or Path(local_path).name
        logger.info(
            "Logging artifact:\n"
            f"Source path: {local_path}\n"
            f"Destination path: {dest_path}"
        )

    def set_terminated(
        self,
        run_id: str,
        status: str,
        end_time: Optional[datetime] = None,
    ) -> None:
        """Sets a run's status to terminated by logging the state change."""
        current_time = end_time or datetime.now()
        logger.info(
            f"Setting run {run_id} as terminated:\n"
            f"Status: {status}\n"
            f"End time: {current_time}"
        )

    def delete_run(self, run_id: str) -> None:
        """Deletes a run by logging the deletion request."""
        logger.info(f"Deleting run: {run_id}")

    def log_input(
        self,
        df: Any,
        context: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs,
    ) -> None:
        """Logs input source information by printing to stdout."""
        logger.info(
            "Logging input source:\n"
            f"Context: {context}\n"
            f"Tags: {tags}\n"
            f"Shape: {getattr(df, 'shape', 'unknown')}"
        )
