import logging
import os
import sys
import traceback

from loguru import logger

from planqk.commons import __version__
from planqk.commons.runtime.input import InputDataReader, InputParamsReader
from planqk.commons.runtime.logging import LogHandler
from planqk.commons.runtime.response import ResponseHandler
from planqk.commons.runtime.string import str_to_bool
from planqk.commons.runtime.user_code import run


def main():
    logging_level = os.environ.get("LOG_LEVEL", "DEBUG")
    logging.getLogger().handlers = [LogHandler()]
    logging.getLogger().setLevel(logging_level)
    logger.configure(handlers=[{"sink": sys.stdout, "level": logging_level}])

    logging.debug(f"Template Version: {__version__}")

    entry_point = os.environ.get("ENTRY_POINT", "user_code.src.program:run")
    logging.debug(f"Entry Point: {entry_point}")

    data_file = os.environ.get("DATA_FILE", "/var/input/data.json")
    params_file = os.environ.get("PARAMS_FILE", "/var/input/params.json")
    base64_encoded = str_to_bool(os.environ.get("BASE64_ENCODED", "true"))
    data_base64_encoded = str_to_bool(os.environ.get("DATA_BASE64_ENCODED", "true"))
    params_base64_encoded = str_to_bool(os.environ.get("PARAMS_BASE64_ENCODED", "true"))

    with InputDataReader(data_file, data_base64_encoded and base64_encoded) as reader:
        input_data = reader.read()

    with InputParamsReader(params_file, params_base64_encoded and base64_encoded) as reader:
        input_params = reader.read()

    response = None
    try:
        response = run(entry_point, input_data, input_params)
    except Exception as e:
        logging.error(f"Error executing user code: {e}")
        traceback.print_exc()
        exit(1)

    response_handler = ResponseHandler(response)

    if not response_handler.is_response():
        logging.warning("Result type is not one of ResultResponse or ErrorResponse")

    response_handler.print_json()

    if response_handler.is_error_response():
        exit(1)


if __name__ == "__main__":
    main()
