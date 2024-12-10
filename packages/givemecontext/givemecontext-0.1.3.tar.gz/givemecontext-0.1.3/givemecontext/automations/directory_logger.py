# ./givemecontext/automations/directory_logger.py

import os
from pathlib import Path

from givemecontext.config import get_log_file_path


class DirectoryLogger:
    """
    DirectoryLogger logs the directory structure to a specified log file,
    excluding directories and files listed in .gitignore and hidden files/folders.
    """

    @staticmethod
    def log_filtered_directory_structure(
        path: str | Path,
        log_file_name: str = "current_directory_structure.log",
    ) -> None:
        """
        Logs the directory structure to the specified log file, excluding
        directories and files listed in .gitignore and hidden files/folders.

        Args:
            path: The directory path to log the structure from.
            log_file_name: Name of the directory structure log file.
                          Defaults to "current_directory_structure.log".
        """
        log_file = get_log_file_path(log_file_name)
        path = Path(path)

        with open(log_file, "w") as file:
            # Write the root directory first
            file.write(f"{path.name}/\n")
            
            for root, dirs, files in os.walk(path):
                # Read .gitignore and exclude those directories and files
                gitignore_path = path / ".gitignore"
                if gitignore_path.exists():
                    package_dirs = {
                        line.strip()
                        for line in gitignore_path.read_text().splitlines()
                        if line.strip() and not line.startswith("#")
                    }
                else:
                    package_dirs = set()

                # Filter out hidden files, folders, __pycache__ folders,
                # and .gitignore entries
                dirs[:] = [
                    d
                    for d in dirs
                    if d not in package_dirs
                    and not d.startswith(".")
                    and d != "__pycache__"
                ]
                
                # Calculate relative path from the start path
                rel_path = Path(root).relative_to(path)
                level = len(rel_path.parts)
                indent = " " * 4 * level
                
                if level > 0:  # Skip root directory as it's already written
                    file.write(f"{indent}{os.path.basename(root)}/\n")
                    
                sub_indent = " " * 4 * (level + 1)
                for f in files:
                    if f not in package_dirs and not f.startswith("."):
                        file.write(f"{sub_indent}{f}\n")


# Always update the log when running the script
if __name__ == "__main__":
    DirectoryLogger.log_filtered_directory_structure(".")
