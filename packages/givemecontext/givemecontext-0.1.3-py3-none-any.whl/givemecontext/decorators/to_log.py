# ./givemecontext/decorators/to_log.py

import io
import logging
import sys
from datetime import datetime
from functools import wraps
from logging.handlers import RotatingFileHandler

# Import the centralized config
from givemecontext.config import get_log_file_path
from givemecontext.utils.logging_level_resolver import LoggingLevelResolver


def to_log(
    log_file_name="main_output.log",
    log_level=logging.INFO,
    mode="a",
    to_console=True,
    max_bytes=1024 * 1024,
    backup_count=3,
):
    """
    A decorator to log the output and performance of a function, with configurable logging levels,
    file output, console output, log rotation, and error handling.

    Args:
        log_file_name (str): Name of the log file. Defaults to 'main_output.log'.
        log_level (int): Logging level. Set to one of logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                         Defaults to logging.INFO.
        mode (str): File open mode. 'a' for append and 'w' for overwrite. Defaults to 'a'.
        to_console (bool): Whether to log output to the console. Defaults to True.
        max_bytes (int): Maximum size of the log file in bytes before rotation occurs. Defaults to 1MB.
        backup_count (int): The number of backup log files to retain when log rotation occurs. Defaults to 3.

    Returns:
        func: A decorated function that logs its stdout, error messages, execution time, and result.
    """
    log_file_path = get_log_file_path(log_file_name)

    log_level = LoggingLevelResolver.to_number(log_level)

    # Clear the log file if mode is 'w' (overwrite)
    if mode == "w":
        with open(log_file_path, "w"):
            pass  # This effectively clears the file by opening in write mode

    # Create or fetch the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Clear existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a rotating file handler to handle log rotation
    file_handler = RotatingFileHandler(
        log_file_path, mode=mode, maxBytes=max_bytes, backupCount=backup_count
    )
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    # Optionally add a console handler to also log to the console
    if to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)

    def decorator(func):
        """
        The actual decorator function which wraps the target function.

        Args:
            func (Callable): The function to be decorated and logged.

        Returns:
            Callable: The wrapped function with logging enabled.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper function that captures stdout, logs function start/end, and logs any errors.

            Args:
                *args: Positional arguments passed to the decorated function.
                **kwargs: Keyword arguments passed to the decorated function.

            Returns:
                Any: The result of the decorated function, if successful.

            Raises:
                Any: Re-raises any exception that occurs within the function, after logging the error.
            """
            # Capture stdout to ensure print statements are logged
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            start_time = datetime.now()
            logger.info(
                f"Starting function '{func.__name__}' with args: {args}, kwargs: {kwargs}"
            )

            try:
                # Execute the function
                result = func(*args, **kwargs)
                logger.info(f"Function '{func.__name__}' executed successfully.")
            except Exception as e:
                # Log any exceptions with full traceback
                logger.error(f"Error in function '{func.__name__}': {e}", exc_info=True)
                raise
            finally:
                # Restore original stdout and log any printed output
                sys.stdout = old_stdout
                log_output = new_stdout.getvalue()
                if log_output:
                    logger.info(log_output)

                # Log the function's execution time
                end_time = datetime.now()
                elapsed_time = (end_time - start_time).total_seconds()
                logger.info(
                    f"Execution time for '{func.__name__}': {elapsed_time:.2f} seconds"
                )

            return result

        return wrapper

    return decorator
