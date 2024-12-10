from pathlib import Path
import inspect
import os

from givemecontext.automations.directory_logger import DirectoryLogger
from givemecontext.automations.format_check_test import CodeQualityAutomation
from givemecontext.config import get_logs_dir


class GiveMeContext:
    """
    GiveMeContext provides a unified interface for running all givemecontext automations.
    It follows the singleton pattern to ensure consistent state across the application.

    Example usage:
        from givemecontext import context, to_log

        @to_log
        def my_function():
            pass

        # Run all automations with default path (caller's directory)
        context.run()

        # Run with specific path
        context.run(path="./src")

        # Or run specific automations
        context.run_code_quality()
        context.run_directory_logger()
    """

    _instance = None
    _base_path = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the GiveMeContext instance."""
        # Ensure logs directory exists
        get_logs_dir()
        self._base_path = None

    def _get_caller_path(self) -> Path:
        """Get the directory path of the file that called this library."""
        # Get the caller's frame (skip this function and run())
        frame = inspect.currentframe()
        while frame:
            # Skip frames from this file
            if frame.f_code.co_filename != __file__:
                caller_file = frame.f_code.co_filename
                return Path(caller_file).parent
            frame = frame.f_back
        return Path(os.getcwd())

    def run(self, code_quality: bool = True, directory_logger: bool = True, path: str | Path | None = None) -> None:
        """
        Run all enabled automations.

        Args:
            code_quality (bool): Whether to run code quality checks. Defaults to True.
            directory_logger (bool): Whether to log directory structure. Defaults to True.
            path (str | Path | None): Custom path to run checks on. If None, uses caller's directory.
        """
        try:
            # Set base path for this run
            self._base_path = Path(path) if path else self._get_caller_path()

            if code_quality:
                self.run_code_quality()

            if directory_logger:
                self.run_directory_logger()
        except Exception as e:
            print(f"Error running GiveMeContext automations: {e}")
            raise

    def run_code_quality(self, path: str | Path | None = None) -> None:
        """
        Run code quality checks (black, ruff, pytest).
        
        Args:
            path (str | Path | None): Custom path to run checks on. If None, uses base path or caller's directory.
        """
        try:
            check_path = Path(path) if path else (self._base_path or self._get_caller_path())
            CodeQualityAutomation.run_with_log(check_path)
        except Exception as e:
            print(f"Error running code quality checks: {e}")
            raise

    def run_directory_logger(self, path: str | Path | None = None) -> None:
        """
        Log the filtered directory structure.
        
        Args:
            path (str | Path | None): Custom path to log structure from. If None, uses base path or caller's directory.
        """
        try:
            log_path = Path(path) if path else (self._base_path or self._get_caller_path())
            DirectoryLogger.log_filtered_directory_structure(log_path)
        except Exception as e:
            print(f"Error logging directory structure: {e}")
            raise

    @property
    def logs_dir(self) -> Path:
        """Get the path to the logs directory."""
        return get_logs_dir()

    @property
    def base_path(self) -> Path:
        """Get the current base path being used for checks."""
        return self._base_path or self._get_caller_path()
