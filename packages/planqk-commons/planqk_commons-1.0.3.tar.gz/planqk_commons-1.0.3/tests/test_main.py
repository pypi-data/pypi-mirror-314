import os

from planqk.commons.runtime import main, ResultResponse, init_logging


def run(**kwargs) -> any:
    return ResultResponse()


def test_main():
    # set the entry point to the test function
    os.environ["ENTRY_POINT"] = "tests.test_main:run"

    init_logging()

    print()
    main()

    # reset the entry point
    os.environ["ENTRY_POINT"] = "user_code.src.program:run"


if __name__ == "__main__":
    test_main()
