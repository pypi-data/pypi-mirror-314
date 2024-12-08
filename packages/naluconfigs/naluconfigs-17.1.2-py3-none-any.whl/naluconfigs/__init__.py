import os
import shutil
from pathlib import Path
from typing import List, Tuple

import numpy as np
import yaml

from naluconfigs.exceptions import ConfigurationFileParsingError, InvalidBoardModelError
from naluconfigs.postprocess import process_configuration as _process_configuration

from . import _constructors
from ._version import __version__
from .helpers import CLOCKS_DIR, REGISTERS_DIR

_VALID_BOARDS = [
    "aardvarcv3",
    "aardvarcv4",
    "aodsv1",
    "aodsv2_eval",
    "asocv3",
    "asocv3s",
    "trbhm",
    'dsa-c10-8',
    "hdsocv1_evalr2",
    "hdsocv2_eval",
    "hdsocv2_evalr2",
    "hiper",
    "upac32",
    "upac96",
    "udc16",
    "aodsoc_asoc",
    "aodsoc_aods",
]


def get_available_models() -> List[str]:
    """Fetches a list of all available board models that can be
    used with NaluConfigs.

    Returns:
        A list of board models.
    """
    # Need a copy in case users want to play with the list
    return _VALID_BOARDS.copy()


def copy_config_files(destination_dir, boards=None) -> dict:
    """Copies a set of config files a given destination

    Args:
        destination_dir (str or Path): the directory to copy config files to
        boards (str or list of str): the board model or list of board models
            to copy the config files for. If None, then this will copy config
            files for all boards

    Raises:
        InvalidBoardModelError if at least one board is invalid
        FileNotFoundError if the source config files cannot be found
        PermissionError if the destination directory is not writable

    Returns:
        A dictionary of output register/clock file paths, organized by board.
        Ex:
            {
                'aardvarcv3': {
                    'registers_file': 'register file location',
                    'clock_file': 'clock file location',
                },
                'asocv2': {
                    'registers_file': 'register file location',
                    'clock_file': 'clock file location',
                },
                ...
            }
    """
    output_paths = {}

    if boards is None:
        boards = _VALID_BOARDS
    elif isinstance(boards, str):
        boards = [boards]

    # Make sure all board models are valid
    for board in boards:
        if board not in _VALID_BOARDS:
            raise InvalidBoardModelError(f'Unknown or unsupported board "{board}"')

    # Create destination directory structure
    destination_dir = Path(destination_dir).resolve()
    (destination_dir / "registers").mkdir(parents=True, exist_ok=True)
    (destination_dir / "clocks").mkdir(exist_ok=True)

    # Copy over all the files for the requested board models
    for board in boards:
        # Copy the .yml file
        try:
            src_param_file = get_register_file(board)
            dest_param_file = destination_dir / "registers" / src_param_file.name

            shutil.copyfile(src_param_file, dest_param_file)
            output_paths[board] = {"registers_file": dest_param_file}
        except:
            raise

        # Copy the clock file
        src_clock_file = get_clock_file(board)
        if src_clock_file is not None:
            try:
                dest_clock_file = destination_dir / "clocks" / src_clock_file.name
                shutil.copyfile(src_clock_file, dest_clock_file)
                output_paths[board]["clock_file"] = dest_clock_file
            except:
                raise

    return output_paths


def get_configuration(model: str) -> dict:
    """Retrieves the default configurations for a board.

    Args:
        model (str): The board model

    Returns:
        A dict containing the configuration

    Raises:
        InvalidBoardModelError if the model is not supported.
        ConfigurationFileParsingError if the config file parsing fails.
        OSError if the config file cannot be accessed
    """
    if model not in _VALID_BOARDS:
        raise InvalidBoardModelError(f'Invalid board model "{model}"')

    # Load the configs from file
    try:
        yml_file = REGISTERS_DIR / (model + ".yml")
        result = get_configuration_from_file(yml_file)
    except OSError:
        raise
    except ConfigurationFileParsingError:
        raise

    return result


def get_configuration_from_file(filename: str) -> dict:
    """Retrieves the configurations from a file.

    Args:
        filename (Path): Full path to the file.

    Returns:
        A dict containing the configuration

    Raises:
        InvalidBoardModelError if the model is not supported.
        OSError if the config file cannot be accessed
    """
    # Load the configs from file
    try:
        result = _load_yaml_file(filename)
    except (OSError, UnicodeDecodeError):
        raise
    except yaml.YAMLError:
        raise ConfigurationFileParsingError(
            f"{filename} could not be interpreted as a yml registers file."
        )

    try:
        result = _process_configuration(result)
    except (ValueError, KeyError, TypeError) as e:
        raise ConfigurationFileParsingError(f"{filename} could not be parsed.") from e

    return result


def get_register_file(model: str) -> Path:
    """Retrieves the default registers file path for a board.

    Args:
        model (str): The board model

    Returns:
        A pathlib Path to the register file for the board.

    Raises:
        InvalidBoardModelError if the model is not supported.
        FileNotFoundError if the config file cannot be found
    """
    if model not in _VALID_BOARDS:
        raise InvalidBoardModelError(f'Invalid board model "{model}"')

    yml_file = REGISTERS_DIR / (model + ".yml")
    if not yml_file.exists():
        raise FileNotFoundError(f"Could not locate the register file at {yml_file}")

    return yml_file


def get_clock(model: str) -> Tuple[list, Path]:
    """Retrieve the default clock file as a string for a board.

    Args:
        model (str): The board name

    Returns:
        A list of clock commands, and the clock file path. Will return
        (None, None) if the

    Raises:
        InvalidBoardModelError if the model is not supported.
    """
    if model not in _VALID_BOARDS:
        raise InvalidBoardModelError(f'Invalid board model "{model}"')

    clock_file_path = get_clock_file(model)

    if clock_file_path is None:
        return None, None
    else:
        return _load_clock_file(clock_file_path), clock_file_path


def get_clock_file(model: str) -> Path:
    """Retrieve the default clock file path for a board.

    Args:
        model (str): The board name

    Returns:
        The clock file path, or None if there is no supported clock file

    Raises:
        InvalidBoardModelError if the model is not supported.
    """
    if model not in _VALID_BOARDS:
        raise InvalidBoardModelError(f'Invalid board model "{model}"')

    # (wastefully) parse the params file to get the clock file name
    config = get_configuration(model)

    if "clock_file" in config["params"]:
        return CLOCKS_DIR / config["params"]["clock_file"]
    else:
        return None


def _load_yaml_file(filename) -> dict:
    """Loads a yaml file into a dict.

    Used to load boardparameters.

    Args:
        filename (str): the path of the yaml file

    Returns:
        A dict representing the yaml file

    Raises:
        OSError if file cannot be accessed.
        YAMLError if YAML file is not valid.
    """
    try:
        with open(filename, "r") as fp:
            return yaml.load(fp, Loader=_constructors.CustomYamlLoader)
    except OSError:
        raise
    except yaml.YAMLError:
        raise


def _load_clock_file(filename) -> list:
    """Turns a .txt file into a list, used for clock file loading.

    Returns:
        list of the loaded clock commands.

    Raises:
        FileNotFoundError if filename is not a valid text file.
        Error ifr loadtxt function fails for an unknown reason (The numpy function is fragile).
    """
    if not os.path.exists(filename) or not os.path.split(filename)[-1].endswith(".txt"):
        raise FileNotFoundError(
            f"File {filename} does not exist. Please provide the path to a valid clockfile."
        )

    try:
        data = np.loadtxt(filename, dtype=str, delimiter=",")
    except Exception as error_msg:
        raise
    return data
