import pytest

import naluconfigs

MODELS = [
    "aardvarcv3",
    "aodsoc_aods",
    "aodsoc_asoc",
    "aodsv2_eval",
    "asocv3",
    "hdsocv1_evalr2",
    "trbhm",
    "upac96",
]


class TestMultichip:
    @pytest.mark.parametrize("model", MODELS)
    def test_loading(self, model):
        config = naluconfigs.get_configuration(model)
        assert "features" in config
        assert "params" in config
        assert "registers" in config

    @pytest.mark.parametrize("model", MODELS)
    def test_register_value_types(self, model):
        config = naluconfigs.get_configuration(model)
        types = {
            "analog_registers": list,
            "digital_registers": list,
            "control_registers": int,
            "i2c_registers": int,
        }

        for top_name, value_type in types.items():
            for reg_name, register in config["registers"][top_name].items():
                try:
                    assert isinstance(register["value"], value_type)
                except AssertionError:
                    msg = f"{top_name}:{reg_name} in {model} has value of type \
                        {type(register['value']).__name__}, expected {value_type.__name__}"
                    raise AssertionError(msg)
