import os
import subprocess
from typing import Optional, List, Union


class ShellScriptRunner:
    """
    A class to execute shell scripts with options to capture output and log execution details.

    This class provides methods to run shell scripts and optionally log their outputs to a specified file.
    It ensures robust error handling and offers clear interfaces for seamless integration into automation workflows.

    ### Usage:
        # Initialize the runner with the path to the shell script
        runner = ShellScriptRunner(script_path="./scripts/deploy.sh")

        # Run the script and capture the output
        output = runner.run()
        print(output)

        # Run the script with arguments
        output = runner.run(["arg1", "arg2"])

        # Run the script and log the output to a file
        runner.run_with_log(log_file="./logs/deploy_output.log", args=["arg1", "arg2"])
    """

    def __init__(self, script_path: str, env_vars: dict = None):
        """
        Initializes the ShellScriptRunner with the specified shell script path.

        :param script_path: Path to the shell script to be executed.
        :param env_vars: Dictionary of environment variables to pass to the script.
        :raises FileNotFoundError: If the script_path does not point to an existing file.
        :raises PermissionError: If the script is not executable.
        :raises TypeError: If the script_path is not a string.
        """
        if not isinstance(script_path, str):
            raise TypeError(
                "script_path must be a string representing the path to the shell script."
            )

        self.script_path = os.path.realpath(script_path)
        self.env_vars = env_vars or {}

        if not os.path.isfile(self.script_path):
            raise FileNotFoundError(
                f"The script path '{self.script_path}' does not point to a valid file."
            )

        if not os.access(self.script_path, os.X_OK):
            raise PermissionError(f"The script '{self.script_path}' is not executable.")

    def _get_environment(self) -> dict:
        """
        Prepare the environment variables for the script execution.

        :return: Dictionary containing the environment variables.
        """
        env = os.environ.copy()
        env.update(self.env_vars)
        return env

    def _get_command(self, args: List[str] = None) -> List[str]:
        """
        Prepare the command to be executed with optional arguments.

        Args:
            args: Optional list of arguments to pass to the script.

        Returns:
            List of command components including the script path and any arguments.
        """
        command = [self.script_path]
        if args:
            command.extend(args)
        return command

    def run(self, args: List[str] = None) -> str:
        """
        Executes the shell script and returns its standard output.

        Args:
            args: Optional list of arguments to pass to the script.

        Returns:
            The standard output from the shell script execution.

        Raises:
            subprocess.CalledProcessError: If the shell script exits with a non-zero status.
        """
        try:
            print(f"Executing shell script: {self.script_path}")
            command = self._get_command(args)
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                shell=False,  # Avoid using shell=True for security reasons
                env=self._get_environment(),
            )
            print("Shell script executed successfully.")
            return result.stdout
        except subprocess.CalledProcessError as e:
            error_message = (
                f"Error executing shell script '{self.script_path}':\n"
                f"Return Code: {e.returncode}\n"
                f"Output: {e.output}\n"
                f"Error: {e.stderr}"
            )
            print(error_message)
            raise subprocess.CalledProcessError(
                returncode=e.returncode, cmd=e.cmd, output=e.output, stderr=e.stderr
            ) from e

    def run_with_log(self, log_file: Optional[str] = None, args: List[str] = None) -> None:
        """
        Executes the shell script and logs the output to a specified log file.

        If no log_file is provided, the output will be logged in the same directory
        as the script with a default name based on the script's name.

        Args:
            log_file: Optional path to the log file where output will be recorded.
                     If None, defaults to "<script_directory>/<script_name>_output.log".
            args: Optional list of arguments to pass to the script.

        Raises:
            subprocess.CalledProcessError: If the shell script exits with a non-zero status.
            IOError: If the log file cannot be written.
        """
        if log_file is None:
            script_dir = os.path.dirname(self.script_path)
            script_name = os.path.splitext(os.path.basename(self.script_path))[0]
            log_file = os.path.join(script_dir, f"{script_name}_output.log")
        else:
            log_file = os.path.realpath(log_file)
            log_dir = os.path.dirname(log_file)
            if not os.path.isdir(log_dir):
                os.makedirs(log_dir, exist_ok=True)

        try:
            print(f"Executing shell script: {self.script_path}")
            print(f"Logging output to: {log_file}")
            command = self._get_command(args)
            with open(log_file, "w") as log:
                subprocess.run(
                    command,
                    check=True,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    shell=False,  # Avoid using shell=True for security reasons
                    env=self._get_environment(),
                )
            print("Shell script executed and logged successfully.")
        except subprocess.CalledProcessError as e:
            error_message = (
                f"Error executing shell script '{self.script_path}'. "
                f"See log file '{log_file}' for details."
            )
            print(error_message)
            raise subprocess.CalledProcessError(
                returncode=e.returncode, cmd=e.cmd, output=e.output, stderr=e.stderr
            ) from e
        except IOError as io_err:
            error_message = f"Failed to write to log file '{log_file}': {io_err}"
            print(error_message)
            raise IOError(error_message) from io_err
