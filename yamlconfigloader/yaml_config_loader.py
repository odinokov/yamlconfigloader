import re
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, ValidationError
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError


class YamlConfigLoader:
    _FLOAT_PATTERN = re.compile(
        r"""^(?:[-+]?[0-9]*\.[0-9]+(?:[eE][-+]?[0-9]+)?
              |[-+]?[0-9]+(?:\.[0-9]*)?(?:[eE][-+]?[0-9]+)?
              |[-+]?\.?(?:inf|Inf|INF)
              |\.(?:nan|NaN|NAN))$""",
        re.VERBOSE,
    )

    def __init__(self, float_pattern: Optional[re.Pattern] = None):
        self.float_pattern = float_pattern or self._FLOAT_PATTERN

    def load_yaml(self, file_path: str) -> Dict[str, Any]:
        yaml = YAML(typ="safe")
        try:
            with open(file_path, "r") as stream:
                return yaml.load(stream)
        except (YAMLError, OSError) as e:
            raise ValueError(f"Error loading YAML file: {e}")

    def validate_yaml(self, data: Dict[str, Any], schema: Type[BaseModel]) -> BaseModel:
        try:
            return schema(**data)
        except ValidationError as e:
            raise e  # Raise the original ValidationError instead of converting it

    def load_and_validate(self, file_path: str, schema: Type[BaseModel]) -> BaseModel:
        return self.validate_yaml(self.load_yaml(file_path), schema)
