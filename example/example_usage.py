import os
from typing import Any, Dict

from pydantic import BaseModel

from yamlconfigloader.yaml_config_loader import YamlConfigLoader


class ConfigSchema(BaseModel):
    random_state: int
    n_splits: int
    n_trials: int
    n_jobs: int  # Number of CPUs to use
    sample_size: float  # Fraction of the whole dataset to use to test the script
    verbosity: Dict[
        str, str
    ]  # Contains verbosity levels for optuna, catboost, and general
    output_paths: Dict[str, str]  # Directories for saving models and logs
    catboost_params: Dict[
        str, Any
    ]  # Parameters for CatBoost, supporting both lists and scalar values


# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the config.yaml file
config_file_path = os.path.join(script_dir, "config.yaml")

# Example usage
yaml_loader = YamlConfigLoader()
try:
    config = yaml_loader.load_and_validate(config_file_path, ConfigSchema)
    print(config)
except ValueError as e:
    print(f"Error: {e}")
