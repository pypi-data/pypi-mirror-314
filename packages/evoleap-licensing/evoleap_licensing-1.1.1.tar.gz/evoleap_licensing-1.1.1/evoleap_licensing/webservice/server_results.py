from datetime import *
from typing import List, Optional
from ..enumerations.licensing_enumerations import ValidationStatus
from uuid import UUID, uuid4


class ServerResult(object):
    def __init__(self):
        self._errorMessage = ''

    @property
    def ErrorMessage(self):
        return self._errorMessage

    @ErrorMessage.setter
    def ErrorMessage(self, value: str):
        self._errorMessage = value


class TimedServerResult(ServerResult):
    def __init__(self):
        super().__init__()
        self._serverTime = None

    @property
    def ServerTime(self):
        return self._serverTime

    @ServerTime.setter
    def ServerTime(self, value: datetime):
        self._serverTime = value


class RegisterResultBase(TimedServerResult):
    def __init__(self):
        super().__init__()
        self._firstRegisteredAt = None
        self._gracePeriodForValidationFailures = timedelta(hours=0)
        self._success = False

    @property
    def Success(self):
        """ Gets whether registration was successful. """
        return self._success

    @Success.setter
    def Success(self, value: bool):
        self._success = value

    @property
    def GracePeriodForValidationFailures(self):
        """Gets the grace period allowed for validation failures."""
        return self._gracePeriodForValidationFailures

    @GracePeriodForValidationFailures.setter
    def GracePeriodForValidationFailures(self, value: timedelta):
        self._gracePeriodForValidationFailures = value

    @property
    def FirstRegisteredAt(self):
        """
        Gets the time at which this instance and/or user was *first* registered.  Multiple registrations
        of an instance are valid and will succeed, but this property will always return
        the time of the very first registration.  This is useful for determining the length
        of trial periods, for example.
        """
        return self._firstRegisteredAt

    @FirstRegisteredAt.setter
    def FirstRegisteredAt(self, value: Optional[datetime]):
        self._firstRegisteredAt = value


class RegisterInstanceResult(RegisterResultBase):

    def __init__(self):
        super().__init__()
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, value: UUID):
        self._InstanceId = value


class RegisterResultWithSessionDuration(RegisterResultBase):

    def __init__(self):
        super().__init__()
        self._SessionDuration = timedelta(hours=0)

    @property
    def SessionDuration(self):
        return self._SessionDuration

    @SessionDuration.setter
    def SessionDuration(self, value: timedelta):
        self._SessionDuration = value


class RegisterUserResult(RegisterResultWithSessionDuration):

    def __init__(self):
        super().__init__()
        self._UserId = None

    @property
    def UserId(self):
        return self._UserId

    @UserId.setter
    def UserId(self, value: UUID):
        self._UserId = value


class RegisterAppResult(RegisterUserResult):

    def __init__(self):
        super().__init__()
        self._InstanceId = None

    @property
    def InstanceId(self):
        return self._InstanceId

    @InstanceId.setter
    def InstanceId(self, value: UUID):
        self._InstanceId = value

class GetUserLicenseServerResult(TimedServerResult):
    def __init__(self):
        super().__init__()
        self._LicenseKeys = []
    
    @property
    def LicenseKeys(self):
        return self._LicenseKeys

    @LicenseKeys.setter
    def LicenseKeys(self, value: List[str]):
        self._LicenseKeys = value

class ValidatedResult(TimedServerResult):

    def __init__(self):
        super().__init__()
        self._Status = ValidationStatus.RegistrationRequired

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, value: ValidationStatus):
        self._Status = value


class ValidatedSessionResult(ValidatedResult):

    def __init__(self):
        super().__init__()
        self._SessionDuration = timedelta(hours=0)
        self._GracePeriodForValidationFailures = timedelta(days=0)
        self._Features = []
        self._AuthToken = ''

    @property
    def AuthToken(self):
        return self._AuthToken

    @AuthToken.setter
    def AuthToken(self, value: str):
        self._AuthToken = value

    @property
    def Features(self):
        return self._Features

    @Features.setter
    def Features(self, value: List[str]):
        self._Features = value

    @property
    def GracePeriodForValidationFailures(self):
        return self._GracePeriodForValidationFailures

    @GracePeriodForValidationFailures.setter
    def GracePeriodForValidationFailures(self, value: timedelta):
        self._GracePeriodForValidationFailures = value

    @property
    def SessionDuration(self):
        return self._SessionDuration

    @SessionDuration.setter
    def SessionDuration(self, value: timedelta):
        self._SessionDuration = value


class ValidateInstanceResult(ValidatedResult):

    def __init__(self):
        super().__init__()
        self._Features = []
        self._GracePeriodForValidationFailures = []

    @property
    def GracePeriodForValidationFailures(self):
        return self._GracePeriodForValidationFailures

    @GracePeriodForValidationFailures.setter
    def GracePeriodForValidationFailures(self, value: timedelta):
        self._GracePeriodForValidationFailures = value

    @property
    def Features(self):
        return self._Features

    @Features.setter
    def Features(self, value):
        self._Features = value


class BeginSessionResult(ValidatedSessionResult):

    def __init__(self):
        super().__init__()
        self._SessionKey = ''

    @property
    def SessionKey(self):
        return self._SessionKey

    @SessionKey.setter
    def SessionKey(self, value):
        self._SessionKey = value


class BeginAppSessionResult(BeginSessionResult):

    def __init__(self):
        super().__init__()
        self._Components = []
        self._ComponentEntitlements = []

    @property
    def Components(self):
        return self._Components

    @Components.setter
    def Components(self, value):
        self._Components = value

    @property
    def ComponentEntitlements(self):
        return self._ComponentEntitlements

    @ComponentEntitlements.setter
    def ComponentEntitlements(self, value):
        self._ComponentEntitlements = value


class CheckOutComponentResult(ValidatedResult):

    def __init__(self):
        super().__init__()
        self._Components = []
        self._ComponentEntitlements = []

    @property
    def Components(self):
        return self._Components

    @Components.setter
    def Components(self, value):
        self._Components = value

    @property
    def ComponentEntitlements(self):
        return self._ComponentEntitlements

    @ComponentEntitlements.setter
    def ComponentEntitlements(self, value):
        self._ComponentEntitlements = value


class EndSessionResult(TimedServerResult):

    def __init__(self):
        super().__init__()
        self._Success = False

    @property
    def Success(self):
        return self._Success

    @Success.setter
    def Success(self, value):
        self._Success = value


class ComponentsStatusResult(ServerResult):

    def __init__(self):
        super().__init__()
        self._ComponentEntitlements = []
        self._Components = []
        self._Success = False

    @property
    def Success(self):
        return self._Success

    @Success.setter
    def Success(self, value):
        self._Success = value

    @property
    def Components(self):
        return self._Components

    @Components.setter
    def Components(self, value):
        self._Components = value

    @property
    def ComponentEntitlements(self):
        return self._ComponentEntitlements

    @ComponentEntitlements.setter
    def ComponentEntitlements(self, value):
        self._ComponentEntitlements = value
