from datetime import *
from .ControlState import ControlState
from ..webservice import server_results


class SessionControlState(ControlState):
    def __init__(self):
        super().__init__()
        self._sessionDuration = timedelta(hours=0)

    @staticmethod
    def fromOther(source, dest):
        if dest is None:
            dest = SessionControlState()
        dest = ControlState.fromOther(source, dest)
        if dest.Registered:
            dest._sessionDuration = source.SessionDuration
        return dest

    @property
    def SessionDuration(self):
        return self._sessionDuration

    @SessionDuration.setter
    def SessionDuration(self, value: timedelta):
        if value is None:
            raise ValueError("value must not be null")
        elif not isinstance(value, timedelta):
            raise ValueError('value must be a timedelta')
        self._sessionDuration = value

    def AdditionalUpdateAfterRegistrationSuccess(self, result: server_results.RegisterUserResult):
        self._sessionDuration = result.SessionDuration
