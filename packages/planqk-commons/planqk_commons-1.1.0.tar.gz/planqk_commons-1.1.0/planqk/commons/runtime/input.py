import os
from abc import abstractmethod, ABC

from loguru import logger

from planqk.commons.runtime.file import FileReader
from planqk.commons.runtime.json import JsonEnvironmentReader


class InputFileReader(ABC):
    def __init__(self, file_path: str, base64_encoded: bool):
        self._file_path = file_path
        self._base64_encoded = base64_encoded

        logger.debug(f"Base64 encoded data? {base64_encoded}")

    def __exit__(self, resource_type, value, tb):
        pass

    def __enter__(self):
        return self

    @abstractmethod
    def read(self):
        pass


class InputDataReader(InputFileReader, ABC):
    def read(self):
        input_data = None

        if os.path.isfile(self._file_path):
            logger.info(f"Using input data from file '{self._file_path}'")
            with FileReader(["/var/input/data.json", "./input/data.json", self._file_path], self._base64_encoded) as reader:
                input_data = reader.read_to_dict()
        else:
            if "DATA_VALUE" in os.environ:
                logger.info("Using input data from environment variable 'DATA_VALUE'")
                with JsonEnvironmentReader("DATA_VALUE", self._base64_encoded) as reader:
                    input_data = reader.read()
            elif "INPUT_DATA" in os.environ:
                logger.warning("DEPRECATED: Using input data from environment variable 'INPUT_DATA'")
                with JsonEnvironmentReader("INPUT_DATA", self._base64_encoded) as reader:
                    input_data = reader.read()

        if input_data is None:
            logger.warning("No input data found, working with empty dict")
            return {}

        return input_data


class InputParamsReader(InputFileReader, ABC):
    def read(self):
        input_params = None

        if os.path.isfile(self._file_path):
            logger.info(f"Using input params from file '{self._file_path}'")
            with FileReader(["/var/input/params.json", "./input/params.json", self._file_path], self._base64_encoded) as reader:
                input_params = reader.read_to_dict()
        else:
            if "PARAMS_VALUE" in os.environ:
                logger.info("Using input params from environment variable 'PARAMS_VALUE'")
                with JsonEnvironmentReader("PARAMS_VALUE", self._base64_encoded) as reader:
                    input_params = reader.read()
            elif "INPUT_PARAMS" in os.environ:
                logger.warning("DEPRECATED: Using input params from environment variable 'INPUT_PARAMS'")
                with JsonEnvironmentReader("INPUT_PARAMS", self._base64_encoded) as reader:
                    input_params = reader.read()

        if input_params is None:
            logger.warning("No input parameters found, working with empty dict")
            return {}

        return input_params
