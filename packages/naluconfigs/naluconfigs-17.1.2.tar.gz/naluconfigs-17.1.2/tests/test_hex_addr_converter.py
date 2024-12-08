import os
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

import naluconfigs
from naluconfigs import (
    get_available_models,
    get_configuration_from_file,
    get_register_file,
)


def test_hex_addr_converter():
    """Tests conversion of converting register addresses to
    hex literals
    """
    SCRIPT_PATH = (
        Path(naluconfigs.__file__).parent.parent.parent
        / "scripts"
        / "hex_addr_converter.py"
    )
    assert os.path.exists(SCRIPT_PATH)
    for model in get_available_models():
        file_name = get_register_file(model)
        tf = NamedTemporaryFile(delete=False)

        with open(tf.name, "w") as temp_file:
            cmd = f"python {SCRIPT_PATH} -i {file_name} -o {tf.name}"
            subprocess.run(cmd)
            temp_file.seek(0)

        config = get_configuration_from_file(file_name)
        new_config = get_configuration_from_file(tf.name)
        tf.close()
        os.unlink(tf.name)
        _convert_register_addresses_to_hex(config)
        _convert_register_addresses_to_hex(new_config)
        assert config == new_config


def _convert_register_addresses_to_hex(config: dict):
    """Convert all register addresses to hex strings"""
    for register_group in config.get("registers", {}).values():
        for reg in register_group.values():
            addr = reg["address"]
            if isinstance(addr, str):
                addr = int(addr, 16)
            reg["address"] = addr
