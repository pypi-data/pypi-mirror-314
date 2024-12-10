from ..enumerations.licensing_enumerations import ValidationStatus
import datetime
from ..timehandling import UtcDateTime
from typing import Optional, Union


class ControlState(object):

    _registeredAt: UtcDateTime
    _registered: bool

    def __init__(self):
        self._failedRegistrationTimes = []
        self._failedValidationTimes = []
        self._features = []
        self._registered = False
        self._registeredAt = None
        self._gracePeriodForValidationFailures = datetime.timedelta()
        self._lastSuccessfulValidationTime = None
        self._firstLaunchTime = None
        self._lastValidationStatus = ValidationStatus.RegistrationRequired

    @staticmethod
    def fromOther(source, dest):
        if dest is None:
            dest = ControlState()
        dest._firstLaunchTime = source.FirstLaunchTime
        if (source.RegisteredAt is None):
            dest._registered = False
            dest._registeredAt = None
            dest._gracePeriodForValidationFailures = datetime.timedelta()
        else:
            dest._registered = True
            dest._registeredAt = UtcDateTime.UtcDateTime(source.RegisteredAt)
            dest._gracePeriodForValidationFailures = source.GracePeriodForValidationFailures

        if not (source.LastSuccessfulValidationTime is None):
            dest._lastSuccessfulValidationTime = UtcDateTime.UtcDateTime(source.LastSuccessfulValidationTime)
        dest._lastValidationStatus = source.LastValidationStatus
        dest._failedRegistrationTimes = source.FailedRegistrationTimes
        dest._failedValidationTimes = source.FailedValidationTimes
        dest._features = source.Features
        return dest

    @property
    def Features(self):
        return self._features

    @property
    def FailedRegistrationTimes(self):
        return list(self._failedRegistrationTimes)

    # Do not use this in consuming applications
    @property
    def FailedRegistrationTimesUnsafe(self):
        """
        Do not use this property in consuming applications
        """
        return self._failedRegistrationTimes

    @property
    def FailedRegistrationTimesUtc(self):
        return [UtcDateTime.UtcDateTime(x) for x in self._failedRegistrationTimes]

    @property
    def FailedValidationTimes(self):
        return list(self._failedValidationTimes)


    @property
    def FailedValidationTimesUnsafe(self):
        """
        Do not use this property in consuming applications
        """
        return self._failedValidationTimes

    @property
    def FailedValidationTimesUtc(self):
        return [UtcDateTime.UtcDateTime(x) for x in self._failedValidationTimes]

    @property
    def LastValidationStatus(self):
        return self._lastValidationStatus

    @LastValidationStatus.setter
    def LastValidationStatus(self, value: ValidationStatus):
        self._lastValidationStatus = value

    @property
    def FirstLaunchTime(self):
        return self._firstLaunchTime

    @FirstLaunchTime.setter
    def FirstLaunchTime(self, value: UtcDateTime):
        self._firstLaunchTime = value

    @property
    def GracePeriodForValidationFailures(self):
        return self._gracePeriodForValidationFailures

    @GracePeriodForValidationFailures.setter
    def GracePeriodForValidationFailures(self, value):
        self._gracePeriodForValidationFailures = value

    @property
    def LastSuccessfulValidationTime(self):
        if self._lastSuccessfulValidationTime is None:
            return None
        else:
            return self._lastSuccessfulValidationTime.AsDateTime()

    @LastSuccessfulValidationTime.setter
    def LastSuccessfulValidationTime(self, value):
        if isinstance(value, datetime.datetime):
            self._lastSuccessfulValidationTime = UtcDateTime.UtcDateTime(value)
        else:
            self._lastSuccessfulValidationTime = value

    @property
    def Registered(self):
        return self._registered

    @Registered.setter
    def Registered(self, value):
        self._registered = value

    @property
    def RegisteredAt(self) -> Optional[datetime.datetime]:
        if self._registeredAt is None:
            return None
        else:
            return self._registeredAt.AsDateTime()

    @property
    def RegisteredAtUtc(self):
        return self._registeredAt

    @RegisteredAt.setter
    def RegisteredAt(self, value: Union[datetime.datetime, UtcDateTime.UtcDateTime, type(None)]):
        if value is None:
            self._registeredAt = None
        elif isinstance(value, datetime.datetime):
            self._registeredAt = UtcDateTime.UtcDateTime(value)
        else:
            self._registeredAt = value

    def AdditionalUpdateAfterRegistrationSuccess(self, result):
        raise NotImplementedError()
