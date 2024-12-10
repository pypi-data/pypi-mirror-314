import logging
import subprocess
import os

log = logging.getLogger("rich")


def execute_command_in_directory(
    command: list[str], directory: str, parameter: list[str]
) -> int:
    """
    Execute a command in a specified directory with a given parameter.

    :param command: The command to execute (as a list of arguments).
    :param directory: The directory in which to execute the command.
    :param parameter: The parameter to pass to the command.
    """
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"The specified directory does not exist: {directory}")
    command.extend(parameter)
    log.info(f"⏳ Executing command: [{' '.join(command)}]...")
    result = subprocess.run(
        command,
        cwd=directory,
    )
    return result.returncode


def get_absolute_path(path: str) -> str:
    if os.path.isabs(path):
        return path
    return os.path.join(os.getcwd(), path)
