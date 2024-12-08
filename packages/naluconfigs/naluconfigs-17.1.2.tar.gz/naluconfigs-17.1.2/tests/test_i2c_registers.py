import pytest

from naluconfigs import get_available_models, get_configuration

EXCLUDE_MODELS = ["asoc"]


@pytest.fixture
def all_configs() -> dict:
    """Dict of {model: config} for all boards supporting I2C"""
    configs = {}
    models = get_available_models()
    for model in models:
        config = get_configuration(model)
        if model in EXCLUDE_MODELS:
            continue
        if "i2c_registers" in config["registers"]:
            configs[model] = config
    return configs


def test_i2c_response_addrs(all_configs: dict):
    """Make sure all the response registers have the correct
    addresses. Addresses should be NGPR+8 to NGPR+11.
    """
    for model, config in all_configs.items():
        i2c_regs = config["registers"]["i2c_registers"]
        ngpr = config["params"]["numregs"]  # numregs is NGPR

        offset = 8
        if model in ["upac96"]:  # defined differently in the UPAC96 firmware
            offset = 0

        for i, offset in enumerate(range(offset, offset + 4)):
            reg_addr = i2c_regs[f"response{i}"]["address"]
            expected = ngpr + offset

            try:
                assert reg_addr == expected
            except AssertionError as e:
                raise AssertionError(f"Wrong response address for {model}") from e


def test_reg_existence(all_configs):
    """Tests for the existence of expected in registers in all
    boards that support I2C.
    """
    needed_regs = [
        "i2c_en",
        "i2c_addr",
        "i2c_words",
        *[f"i2c_data{i}" for i in range(4)],
        *[f"response{i}" for i in range(4)],
    ]
    for model, config in all_configs.items():
        i2c_regs = config["registers"]["i2c_registers"]

        for regname in needed_regs:
            try:
                assert regname in i2c_regs
            except AssertionError as e:
                raise AssertionError(f"Missing register for {model}") from e


def test_for_segmented_registers(all_configs):
    """Tests for the existence of register addresses on the FPGA that are split
    between control and i2c registers (BAD!). This is important because writing to i2c
    registers on such addresses will set all control registers on the same address
    to zero.
    """
    for model, config in all_configs.items():
        control_reg_addresses = set(
            [
                _get_register_addr(reg)
                for reg in config["registers"]["control_registers"].values()
            ]
        )
        for name, i2c_reg in config["registers"]["i2c_registers"].items():
            i2c_reg_addr = _get_register_addr(i2c_reg)
            try:
                assert i2c_reg_addr not in control_reg_addresses
            except AssertionError:
                raise AssertionError(
                    f"I2C register {name} for {model} shares address 0x{i2c_reg_addr:02x} with one or more control registers"
                )


def _get_register_addr(reg: dict) -> int:
    """Get the address from for a register as an int."""
    addr = reg["address"]
    if isinstance(addr, str):
        addr = int(reg["address"], 16)
    return addr
