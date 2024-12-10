import logging
from typing import Dict, Union


class LoggingLevelResolver:
    """
    A class to resolve logging levels to various representations.

    This class provides methods to convert a logging level input (either as an integer,
    short name, or fully-qualified name) into different formats such as the numeric level,
    short name, or fully-qualified name.

    Usage:
        number = LoggingLevelResolver.to_number(level_input)
        name = LoggingLevelResolver.to_name(level_input)
        full_name = LoggingLevelResolver.to_full_name(level_input)
        all_reprs = LoggingLevelResolver.to_all(level_input)
    """

    @staticmethod
    def to_number(level_input: Union[str, int]) -> int:
        """
        Converts the logging level input to its numeric value.

        Parameters:
            level_input (Union[str, int]): The logging level as an integer, short name,
                                           or fully-qualified name.

        Returns:
            int: The numeric logging level.

        Raises:
            ValueError: If the input does not correspond to any known logging level.
            TypeError: If the input type is neither str nor int.
        """
        if isinstance(level_input, int):
            level_num = level_input
            level_name = logging.getLevelName(level_num)
            if level_name.startswith("Level "):
                raise ValueError(f"Unknown logging level number: {level_num}")
            return level_num
        elif isinstance(level_input, str):
            normalized_input = level_input.strip().upper()
            if normalized_input.startswith("LOGGING."):
                level_name = normalized_input[len("LOGGING.") :]
            else:
                level_name = normalized_input
            level_num = logging.getLevelName(level_name)
            if isinstance(level_num, int):
                return level_num
            else:
                raise ValueError(f"Invalid logging level name: '{level_input}'")
        else:
            raise TypeError("level_input must be an integer or string.")

    @staticmethod
    def to_name(level_input: Union[str, int]) -> str:
        """
        Converts the logging level input to its short name.

        Parameters:
            level_input (Union[str, int]): The logging level as an integer, short name,
                                           or fully-qualified name.

        Returns:
            str: The short name of the logging level (e.g., 'DEBUG').

        Raises:
            ValueError: If the input does not correspond to any known logging level.
            TypeError: If the input type is neither str nor int.
        """
        if isinstance(level_input, int):
            level_num = level_input
            level_name = logging.getLevelName(level_num)
            if level_name.startswith("Level "):
                raise ValueError(f"Unknown logging level number: {level_num}")
            return level_name
        elif isinstance(level_input, str):
            normalized_input = level_input.strip().upper()
            if normalized_input.startswith("LOGGING."):
                level_name = normalized_input[len("LOGGING.") :]
            else:
                level_name = normalized_input
            level_num = logging.getLevelName(level_name)
            if isinstance(level_num, int):
                return level_name
            else:
                raise ValueError(f"Invalid logging level name: '{level_input}'")
        else:
            raise TypeError("level_input must be an integer or string.")

    @staticmethod
    def to_full_name(level_input: Union[str, int]) -> str:
        """
        Converts the logging level input to its fully-qualified name.

        Parameters:
            level_input (Union[str, int]): The logging level as an integer, short name,
                                           or fully-qualified name.

        Returns:
            str: The fully-qualified logging level name (e.g., 'logging.DEBUG').

        Raises:
            ValueError: If the input does not correspond to any known logging level.
            TypeError: If the input type is neither str nor int.
        """
        level_name = LoggingLevelResolver.to_name(level_input)
        return f"logging.{level_name}"

    @staticmethod
    def to_all(level_input: Union[str, int]) -> Dict[str, Union[str, int]]:
        """
        Retrieves all representations of the logging level.

        Parameters:
            level_input (Union[str, int]): The logging level as an integer, short name,
                                           or fully-qualified name.

        Returns:
            Dict[str, Union[str, int]]: A dictionary containing the numeric level,
                                        short name, and fully-qualified name.

        Raises:
            ValueError: If the input does not correspond to any known logging level.
            TypeError: If the input type is neither str nor int.
        """
        return {
            "number": LoggingLevelResolver.to_number(level_input),
            "name": LoggingLevelResolver.to_name(level_input),
            "full_name": LoggingLevelResolver.to_full_name(level_input),
        }
