from typing import Union, List

class UserLicenseResult:
    _success: bool
    _errorMessage: Union[str, type(None)]
    _licenses: List[str]

    def __init__(self, success: bool, error_message: Union[str, type(None)], licenses: List[str]):
        self._success = success
        self._errorMessage = error_message
        self._licenses = licenses.copy()

    @property
    def Success(self) -> bool:
        return self._success

    @property
    def ErrorMessage(self) -> Union[str, type(None)]:
        return self._errorMessage

    @property
    def Licenses(self) -> List[str]:
        return self._licenses

