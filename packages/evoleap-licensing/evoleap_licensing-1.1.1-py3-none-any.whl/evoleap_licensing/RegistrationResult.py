from typing import Union

class RegistrationResult:
    _success: bool
    _errorMessage: Union[str, type(None)]

    def __init__(self, success: bool, error_message: Union[str, type(None)]):
        self._success = success
        self._errorMessage = error_message

    @property
    def Success(self) -> bool:
        return self._success

    @property
    def ErrorMessage(self) -> Union[str, type(None)]:
        return self._errorMessage

    @classmethod
    def GetSuccess(cls):
        return cls(True, None)

    @classmethod
    def GetError(cls, error_message: str):
        return cls(False, error_message)
