from typing import Union, Dict, List

from loguru import logger

from planqk.commons.runtime.json import json_to_dict


class FileReader:
    def __init__(self, file_paths: List[str], base64_encoded: bool = False):
        self.__file_paths = file_paths
        self.__base64_encoded = base64_encoded

        self.__file_path = None
        self.__file_object = None

    def __enter__(self):
        # open first file in list that exists
        for file_path in self.__file_paths:
            try:
                self.__file_path = file_path
                self.__file_object = open(file_path, "r")
                return self
            except FileNotFoundError:
                continue

        raise FileNotFoundError(f"No file found in paths: {self.__file_paths}")

    def __exit__(self, resource_type, value, tb):
        self.__file_object.close()

    def file(self):
        if self.__file_path is None or self.__file_object is None or self.__file_object.closed:
            raise RuntimeError("FileReader must be used with the 'with' keyword")
        return self.__file_object

    def read_to_string(self) -> Union[str, None]:
        try:
            return self.file().read()
        except Exception as e:
            logger.error("Error reading file '{}': {}", self.__file_path, e)
            return None

    def read_to_dict(self) -> Union[Dict, None]:
        data = self.read_to_string()
        try:
            return json_to_dict(data, self.__base64_encoded)
        except ValueError as e:
            logger.error("Error reading file '{}': {}", self.__file_path, e)
            return None
