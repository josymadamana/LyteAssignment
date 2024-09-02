import os
import json
import pytest

STEPPER_TEST_CONFIG=os.path.join(os.path.dirname(__file__), 'stepper.json')

def get_config_args(file, config_name):
    with open(file) as f:
        test_config = json.load(f)
        cfg_args = [
            pytest.param(cfg["cfg"], marks=pytest.mark.JAMA(*cfg["test_ids"]))
            for cfg in test_config[config_name]
        ]
    return cfg_args
