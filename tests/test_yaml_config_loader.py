import os
import unittest

from pydantic import BaseModel, ValidationError

from yamlconfigloader.yaml_config_loader import YamlConfigLoader


class MyConfigSchema(BaseModel):
    n_splits: int
    n_trials: int
    sample_fraction: float


class TestYamlConfigLoader(unittest.TestCase):
    def setUp(self):
        self.yaml_loader = YamlConfigLoader()

    def test_load_yaml_valid(self):
        yaml_content = """
        n_splits: 5
        n_trials: 100
        sample_fraction: 0.8
        """
        file_path = "test_valid_config.yaml"

        with open(file_path, "w") as file:
            file.write(yaml_content)

        config_data = self.yaml_loader.load_yaml(file_path)
        self.assertEqual(config_data["n_splits"], 5)
        self.assertEqual(config_data["n_trials"], 100)
        self.assertEqual(config_data["sample_fraction"], 0.8)

        os.remove(file_path)

    def test_load_yaml_invalid(self):
        yaml_content = """
        n_splits: 5
        n_trials: 100
        """
        file_path = "test_invalid_config.yaml"

        with open(file_path, "w") as file:
            file.write(yaml_content)

        config_data = self.yaml_loader.load_yaml(file_path)

        # Expecting a ValidationError due to missing required field
        with self.assertRaises(ValidationError):
            self.yaml_loader.validate_yaml(config_data, MyConfigSchema)

        os.remove(file_path)

    def test_load_yaml_with_syntax_error(self):
        yaml_content = """
        n_splits: 5
        n_trials: 100
        sample_fraction: 0.8
        - another: value
        """
        file_path = "test_syntax_error.yaml"

        with open(file_path, "w") as file:
            file.write(yaml_content)

        with self.assertRaises(ValueError):
            self.yaml_loader.load_yaml(file_path)

        os.remove(file_path)

    def test_load_and_validate(self):
        yaml_content = """
        n_splits: 5
        n_trials: 100
        sample_fraction: 0.8
        """
        file_path = "test_full_valid_config.yaml"

        with open(file_path, "w") as file:
            file.write(yaml_content)

        config = self.yaml_loader.load_and_validate(file_path, MyConfigSchema)
        self.assertIsInstance(config, MyConfigSchema)
        self.assertEqual(config.n_splits, 5)
        self.assertEqual(config.n_trials, 100)
        self.assertEqual(config.sample_fraction, 0.8)

        os.remove(file_path)


if __name__ == "__main__":
    unittest.main()
