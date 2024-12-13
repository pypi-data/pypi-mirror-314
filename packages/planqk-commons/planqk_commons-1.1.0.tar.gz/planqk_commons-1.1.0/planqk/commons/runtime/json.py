import base64
import json
import os
from typing import Dict, Union

from loguru import logger


def any_to_json(data: any) -> str:
    return json.dumps(data, default=lambda o: getattr(o, "__dict__", str(o)), sort_keys=True, indent=2)


def json_to_dict(value: str, base64_encoded: bool) -> Dict:
    if value is None:
        return {}
    decoded_value = value
    if base64_encoded:
        try:
            decoded_value = base64.urlsafe_b64decode(value).decode("utf-8")
        except Exception as e:
            raise ValueError(f"Not a base64 string? - {e}")
    try:
        return json.loads(decoded_value)
    except Exception as e:
        raise ValueError(f"Not a json string? {e}")


class JsonEnvironmentReader:
    def __init__(self, name: str, base64_encoded: bool):
        self.__name = name
        self.__base64_encoded = base64_encoded

    def __enter__(self):
        return self

    def __exit__(self, resource_type, value, tb):
        pass

    def read(self) -> Union[Dict, None]:
        value = os.environ.get(self.__name, None)
        if value is None:
            return None
        try:
            return json_to_dict(value, self.__base64_encoded)
        except ValueError as e:
            logger.error("Error reading environment variable '{}': {}", self.__name, e)
            return None
