from planqk.commons.runtime.json import any_to_json


class Response:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def json(self):
        return any_to_json(self)


class ErrorResponse(Response):
    """
    Represents an error to be passed back to the caller.
    """
    pass


class ResultResponse(Response):
    """
    Represents the result to be passed back to the caller.
    """
    pass


class ResponseHandler:
    def __init__(self, result):
        self.__result = result
        self.__class_name = None
        if result is not None:
            self.__class_name = result.__class__.__name__

    def is_result_response(self) -> bool:
        return self.__class_name == "ResultResponse"

    def is_error_response(self) -> bool:
        return self.__class_name == "ErrorResponse"

    def is_response(self) -> bool:
        return self.is_result_response() or self.is_error_response()

    def print_json(self):
        print(str(self))

    def __str__(self):
        if self.__result is None:
            return ""
        else:
            return f"\nPlanQK:Job:MultilineResult\n{any_to_json(self.__result)}\nPlanQK:Job:MultilineResult"
