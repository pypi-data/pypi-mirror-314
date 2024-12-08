"""Module for applying fancy alterations to a configuration dict
once it has been loaded from a YAML file.

The following is performed by processing a dict:
- Ranged keys (e.g. `0..31`) are expanded, and the value of
  the ranged key is duplicated for each element in the range.
  The original key is not perserved once it has been expanded.


Example of valid range strings:
- `0..5` gets expanded into [0, 1, 2, 3, 4, 5]
- `0..2, 4..5` gets expanded into [0, 1, 2, 4, 5]
- `0, 3..5` gets expanded into [0, 3, 4, 5]
- `0, 1, 2` gets expanded into [0, 1, 2]

Example of invalid range strings:
- `0..2..5` is invalid because it has more than two endpoints specified
- `0..` and `..1` are invalid because they are missing endpoints
- `0.1..5.0` is invalid because the endpoint contains a non-integer value
"""
import copy
from typing import List

from .exceptions import PostProcessingError, RangeParsingError


_RANGE_DELIMITER = '..'
_SUBRANGE_DELIMITER = ','



def process_configuration(config: dict) -> dict:
    """Applies fancy post-processing to a configuration dict.

    This includes:
    - Expanding ranged keys (e.g. `0..31`)

    Args:
        config (dict): the configuration dict.

    Returns:
        The processed configuration dict
    """
    if not isinstance(config, dict):
        raise TypeError('Configuration must be a dictionary')

    try:
        return _traverse_tree(config)
    except (KeyError, PostProcessingError) as e:
        raise PostProcessingError('Failed to apply post processing') from e


def _traverse_tree(node) -> dict:
    """Traverses every node in the tree (if a dict) and applies
    processing to entries.

    Args:
        node (object): the value of a node
        parent_key (str): the key of the parent of this node as a string.
            Used for error messages if a problem occurs.

    Returns:
        The processed node. If the node is a dict, a copy is returned.

    Raises:
        KeyError if duplicate keys are found after expanding a ranged key.
        RangeParsingError if any key ranges are found to be invalid.
    """
    if not isinstance(node, dict):
        return node

    # Need to copy over everything since we can't change
    # the size of the dict while iterating
    result_dict = {}
    for key, value in node.items():
        value = _traverse_tree(value)

        # Processing one entry can result in many being created
        new_entries = _process_single_entry(key, value)
        _insert_in_dict_or_raise(result_dict, new_entries)

    return result_dict


def _insert_in_dict_or_raise(output: dict, entries: dict):
    """Inserts one or more entries into a dictionary.
    Unlike `dict.update()`, this function does not allow the overwriting
    of old values.

    Args:
        output (dict): the output dict
        entries (dict): entries to add to the dict

    Raises:
        KeyError if the key already exists in the dictionary
    """
    for key, value in entries.items():
        if key in output:
            raise KeyError(f'Duplicate key "{key}" found in dictionary')
        output[key] = value


def _process_single_entry(key, value):
    """Performs post-processing on a single entry of a dictionary.

    Processing performed:
    - Range expansion of keys. Can create an abitrary number of
      entries with differing keys but duplicate values

    Args:
        key (any): the key of the entry
        value (any): the value of the entry

    Returns:
        A dict of any new entries. If no processing is performed on a key,
        the return dict is simply `{key: value}`.

    Raises:
        RangeParsingError if the key is an invalid range.
    """
    new_entries = {key: value}

    if _is_range_string(key):
        new_keys = _expand_range_str(key)
        if len(set(new_keys)) != len(new_keys):
            raise RangeParsingError(f'Duplicate values found in range "{key}"')
        new_entries = {k: copy.deepcopy(value) for k in new_keys}

    return new_entries


def _is_range_string(s: str) -> bool:
    """Checks if a string should be interpreted as a range.

    This function only does quick sanity checks, and does not
    fully parse the string to validate the syntax fully.

    Args:
        s (str): The string to test

    Returns:
        True if the string is probably a range
    """
    return isinstance(s, str) and (_RANGE_DELIMITER in s or _SUBRANGE_DELIMITER in s)


def _expand_range_str(s: str) -> List[int]:
    """Expands a range string into a list of elements.

    The string can contain any number of subranges/elements.

    Args:
        s (str): the range string.

    Raises:
        TypeError if the argument is not a string, or
            contains elements that cannot be represented
            as an integer
        ValueError if for any range, lower >= upper, or if
            an invalid syntax is found (e.g. `0..1..2`)

    Returns:
        A list of all elements in the range as ints.
    """
    if not isinstance(s, str):
        raise TypeError('Range string must be a string')

    range_strings = s.split(_SUBRANGE_DELIMITER)
    range_elements = []
    try:
        for string in range_strings:
            elements = _parse_range(string)
            range_elements.extend(elements)
    except (ValueError, TypeError) as e:
        raise RangeParsingError(f'Invalid range specified: {s}') from e

    return range_elements


def _parse_range(r: str) -> List[int]:
    try:
        endpoints = r.split(_RANGE_DELIMITER)
        endpoints = [int(x) for x in endpoints]
    except ValueError:
        raise TypeError('Non-integer value found in ranged key')
    if len(endpoints) > 2:
        raise ValueError('Too many endpoints in range')
    if len(endpoints) == 2:
        # max(endpoints) + 1 breaks on negative values. Tacking on the endpoint works better
        endpoints = list(range(min(endpoints), max(endpoints))) + [max(endpoints)]

    return endpoints
