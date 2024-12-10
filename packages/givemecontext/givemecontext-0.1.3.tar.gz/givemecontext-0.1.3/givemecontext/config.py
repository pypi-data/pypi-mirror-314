# ./givemecontext/config.py

from pathlib import Path

# Default logging settings for the library
LOG_DIR_NAME = "givemecontext-logs"


def get_project_root() -> Path:
    """
    Get the root directory of the user's project (where the library is being used).

    Returns:
        Path: Path to the project root directory
    """
    return Path.cwd()


def get_logs_dir() -> Path:
    """
    Get the logs directory path in the user's project and ensure it exists.

    Returns:
        Path: Path to the logs directory
    """
    logs_dir = get_project_root() / LOG_DIR_NAME
    logs_dir.mkdir(exist_ok=True)
    return logs_dir


def get_log_file_path(log_file_name: str) -> str:
    """
    Get the full path for a log file within the user's project logs directory.

    Args:
        log_file_name (str): Name of the log file

    Returns:
        str: Full path to the log file
    """
    return str(get_logs_dir() / log_file_name)
