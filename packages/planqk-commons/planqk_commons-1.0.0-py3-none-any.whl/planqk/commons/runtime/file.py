import logging
from typing import Union, Dict

from planqk.commons.runtime.json import json_to_dict


class JsonFileReader:
    def __init__(self, file_path: str, base64_encoded: bool):
        self.__file_path = file_path
        self.__file_object = None
        self.__base64_encoded = base64_encoded

    def __enter__(self):
        self.__file_object = open(self.__file_path, "r")
        return self

    def __exit__(self, resource_type, value, tb):
        self.__file_object.close()

    def read(self) -> Union[Dict, None]:
        data = self.__file_object.read()
        try:
            return json_to_dict(data, self.__base64_encoded)
        except ValueError as e:
            logging.error(f"Error parsing JSON file content (file={self.__file_path}): {e}")
            return None
