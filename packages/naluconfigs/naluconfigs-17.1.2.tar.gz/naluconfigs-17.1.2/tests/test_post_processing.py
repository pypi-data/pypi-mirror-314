"""Tests the general post-processing functions.
See relevant modules for more specific tests.
"""
import pytest

from naluconfigs.exceptions import RangeParsingError
from naluconfigs.postprocess import (
    process_configuration,
    _insert_in_dict_or_raise,
)


def test_plain_config():
    """Tests whether a simple config that doesn't require
    special processing is the same before and after the
    post-processing operation.
    """
    config = {
        'a': 5,
        'b': [10, 20, 30],
        'c': {
            'd': 10,
            'e': {
                'f': 20
            }
        }
    }

    result = process_configuration(config)
    assert result is not config
    assert result == config


def test_processing_invalid_type():
    """Tests whether passing bad types to the post processor
    results in an error.
    """
    with pytest.raises(TypeError):
        process_configuration('bad type')
    with pytest.raises(TypeError):
        process_configuration([0, 1, 2])


def test_duplicate_insertion():
    """Tests whether inserting duplicate entries into a dictionary
    correctly raises an error
    """
    test_dict = {}
    _insert_in_dict_or_raise(test_dict, {0: 100})
    _insert_in_dict_or_raise(test_dict, {1: 100})
    _insert_in_dict_or_raise(test_dict, {2: 100})
    with pytest.raises(KeyError):
        _insert_in_dict_or_raise(test_dict, {1: 100})
