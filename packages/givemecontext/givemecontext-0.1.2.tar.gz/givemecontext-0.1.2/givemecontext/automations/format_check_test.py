import tempfile
from importlib.resources import files
from pathlib import Path

from givemecontext.config import LOG_DIR_NAME, get_log_file_path, get_logs_dir
from givemecontext.utils.shell_script_runner import ShellScriptRunner


class CodeQualityAutomation:
    """
    CodeQualityAutomation runs automated code quality checks using the following tools:

    1. **black**: For code formatting.
    2. **ruff**: For linting and fixing Python code style issues.
    3. **pytest**: For running unit tests and ensuring code correctness.

    It provides two primary methods:
    - `run_script`: Executes the shell script and captures the output.
    - `run_with_log`: Executes the shell script and logs the output to a given log file.

    Usage:
    - Directly call `run_script` to run the shell commands and capture output.
    - Use `run_with_log` to run the shell commands and log the output.

    Example:
    CodeQualityAutomation.run_script()
    """

    DEFAULT_LOG_FILENAME = "format_check_test_output.log"

    @classmethod
    def _get_script_path(cls) -> str:
        """
        Gets the path to the shell script, handling both development and installed package scenarios.

        Returns:
            str: Path to the shell script
        """
        # Create a temporary file to store the script
        temp_dir = Path(tempfile.gettempdir()) / "givemecontext"
        temp_dir.mkdir(exist_ok=True)
        temp_script = temp_dir / "format_check_test.sh"

        # Get the script content from package resources
        script_content = (
            files("givemecontext.automations")
            .joinpath("format_check_test.sh")
            .read_text()
        )

        # Write the script to the temporary file
        temp_script.write_text(script_content)

        # Make the script executable
        temp_script.chmod(0o755)

        return str(temp_script)

    @classmethod
    def _get_environment_vars(cls, log_file_path: str = None) -> dict:
        """
        Prepares the environment variables for the shell script.

        Args:
            log_file_path: Optional path to the log file.

        Returns:
            dict: Dictionary of environment variables.
        """
        # Get absolute paths for logging using config values
        logs_dir = get_logs_dir()

        env_vars = {
            "GIVEMECONTEXT_LOG_DIR": str(logs_dir.resolve()),
            "PYTHONPATH": str(Path.cwd()),
            "GIVEMECONTEXT_LOG_DIR_NAME": LOG_DIR_NAME,  # Pass the directory name from config
        }

        if log_file_path:
            env_vars.update(
                {
                    "GIVEMECONTEXT_LOG_FILE": str(Path(log_file_path).resolve()),
                    "GIVEMECONTEXT_LOG_FILENAME": cls.DEFAULT_LOG_FILENAME,
                }
            )

        return env_vars

    @classmethod
    def run_script(cls, path: str | Path | None = None) -> str:
        """
        Executes the shell script and returns the command output.

        Args:
            path: Optional path to run checks on. Defaults to current directory.

        Returns:
            str: The output of the shell command execution.
        """
        try:
            # Get script path and prepare environment variables
            script_path = cls._get_script_path()
            log_file_path = get_log_file_path(cls.DEFAULT_LOG_FILENAME)
            env_vars = cls._get_environment_vars(log_file_path)

            # Initialize and run the shell script
            runner = ShellScriptRunner(script_path, env_vars=env_vars)
            check_path = str(Path(path).resolve()) if path else "."
            return runner.run([check_path])
        except Exception as e:
            print(f"Error while executing the shell script: {e}")
            return str(e)

    @classmethod
    def run_with_log(cls, path: str | Path | None = None, log_file_name: str = DEFAULT_LOG_FILENAME) -> None:
        """
        Executes the shell script and logs the output to a specified log file.

        Args:
            path: Optional path to run checks on. Defaults to current directory.
            log_file_name: Name of the log file where output will be logged.
                          Default is "format_check_test_output.log".
        """
        try:
            # Get script path and prepare environment variables
            script_path = cls._get_script_path()
            log_file_path = get_log_file_path(log_file_name)
            env_vars = cls._get_environment_vars(log_file_path)

            # Initialize and run the shell script with logging
            runner = ShellScriptRunner(script_path, env_vars=env_vars)
            check_path = str(Path(path).resolve()) if path else "."
            runner.run_with_log(log_file_path, args=[check_path])
        except Exception as e:
            print(f"Error while executing the shell script: {e}")
            raise
