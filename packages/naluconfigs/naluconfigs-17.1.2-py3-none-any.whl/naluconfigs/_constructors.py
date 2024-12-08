"""Defines a custom loader which can be used to load NaluConfigs files
which use custom YAML tags.
"""

import typing
from functools import partial

import yaml

from . import helpers


def _include_chip(**kwargs) -> dict:
    """Tag constructor. Includes a portion of a chip file.
    Supports overriding fields.

    Args:
        from (str): The qualified name of the chip file to include.
            The first segment is the chip name, and the rest are the
            fields to include from within the chip file.
            Example: "chip_name::params::etc"
        override (dict): A dictionary of fields to override. Can be nested
            to override nested fields.
    """
    from_: str = kwargs["from"]
    override: dict = kwargs.get("override", None)
    delete: list = kwargs.get("delete", None)

    result = _load_chip_qualified(from_)
    if override:
        _apply_overrides(result, override)
    if delete:
        for key in delete:
            result.pop(key, None)
    return result


def _include_registers(
    value_count: int = 1,
    **kwargs,
) -> dict:
    """Tag constructor. Includes the registers portion of a chip file.

    Args:
        value_count (int): The number of values to include for each register.
        **kwargs: see documentation for `_include()`.
    """
    result = _include_chip(**kwargs)
    for register in result.values():
        value = register.get("value", None)
        if isinstance(value, (int, str)):
            register["value"] = [value] * value_count
    return result


def _load_chip_qualified(qualified_name: str) -> dict:
    """Loads a chip config from a qualified name.

    Args:
        qualified_name (str): The qualified name of the chip config to load.
            The first segment is the chip name, and the rest are the
            fields to include from within the chip file.
            Example: "chip_name::params::etc"

    Returns:
        dict: the loaded chip config
    """
    chip_name, *rest = qualified_name.split("::")
    result = helpers.default_chip_config(chip_name)
    for key in rest:
        result = result[key]
    return result


def _apply_overrides(target: dict, overrides: dict):
    """Recursively apply overrides to a dictionary in-place.

    Args:
        target (dict): The dictionary to apply overrides to.
        overrides (dict): The overrides to apply.

    Raises:
        KeyError: if an overriden key does not exist in the target.
    """
    for k, v in overrides.items():
        if k not in target:
            raise KeyError(f"Invalid key {k} in overrides; key does not exist in base")
        if isinstance(v, dict):
            _apply_overrides(target[k], v)
        else:
            target[k] = v


class CustomYamlLoader(yaml.CLoader):
    """Custom PyYaml loader with custom constructors. Use this for loading
    configuration files.
    """


def _mapping_constructor_callback(
    fn: typing.Callable,
    loader: yaml.Loader,
    node: yaml.nodes.MappingNode,
) -> typing.Any:
    kwargs = loader.construct_mapping(node, deep=True)
    return fn(**kwargs)


def _register(tag: str, fn: typing.Callable):
    """Registers a custom constructor for a tag.

    Args:
        tag (str): The tag to define a constructor for.
        fn (typing.Callable): The constructor function.
    """
    CustomYamlLoader.add_constructor(tag, partial(_mapping_constructor_callback, fn))


_register("!include_chip", _include_chip)
_register("!include_registers", _include_registers)
