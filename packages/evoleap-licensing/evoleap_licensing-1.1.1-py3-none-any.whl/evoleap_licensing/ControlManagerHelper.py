from typing import Callable, Tuple

from .ControlStrategy import ControlStrategy
from .RegistrationResult import *
from .SessionValidity import SessionValidity
from .control_logic import ControlLogic
from .enumerations.licensing_enumerations import *
from .states.ControlState import ControlState
from .timehandling import TimeProvider
from .timehandling.UtcDateTime import UtcDateTime
from .webservice.server_results import RegisterResultBase


def InitializeState(state: ControlState):
    if state.FirstLaunchTime is None:
        state.FirstLaunchTime = GetUtcNow()


def GetUtcNow() -> UtcDateTime:
    return TimeProvider.Current().UtcNow()


def Register(state: ControlState, registration_callback: Callable[[], RegisterResultBase]):
    InitializeState(state)
    if state.Registered:
        return RegistrationResult.GetSuccess()
    result = registration_callback()
    if result.Success:
        state.Registered = True
        state.RegisteredAt = result.FirstRegisteredAt
        state.GracePeriodForValidationFailures = result.GracePeriodForValidationFailures
        state.FailedRegistrationTimes.clear()
        state.AdditionalUpdateAfterRegistrationSuccess(result)
        return RegistrationResult.GetSuccess()
    else:
        state.FailedRegistrationTimesUnsafe.insert(0, (result.ServerTime or GetUtcNow().AsDateTime()))
        return RegistrationResult.GetError(result.ErrorMessage)


def GetUnregisteredValidity(strategy: ControlStrategy, state: ControlState,
                            current_time: UtcDateTime) -> SessionValidity:
    if ControlLogic.IsFirstLaunchTimeInvalid(state.FirstLaunchTime, current_time):
        state.LastValidationStatus = ValidationStatus.UserTamperingDetected
        return SessionValidity.Invalid(InvalidReason.UserTamperingDetected)

    if ControlLogic.IsTimeInconsistencyDetected(state.FirstLaunchTime, state.FailedRegistrationTimesUtc, current_time,
                                                False):
        state.LastValidationStatus = ValidationStatus.UserTamperingDetected
        return SessionValidity.Invalid(InvalidReason.UserTamperingDetected)

    result, expiration = ControlLogic.IsInGracePeriodForUnregisteredProduct(strategy, state.FirstLaunchTime,
                                                                            current_time)
    if result:
        return SessionValidity.UnregisteredGracePeriod(expiration)
    else:
        state.LastValidationStatus = ValidationStatus.RegistrationRequired
        return SessionValidity.Invalid(InvalidReason.InstanceNotRegistered)


class OfflineGracePeriodStatus(Enum):
    UserTamperingDetected = 0,
    NotPermitted = 1,
    Available = 2


def GetServerUnreachableValidity(state: ControlState, local_time: UtcDateTime) -> SessionValidity:
    offline_status, grace_period_expiration = CheckOfflineStatus(state, local_time)
    if offline_status is OfflineGracePeriodStatus.UserTamperingDetected:
        return SessionValidity.Invalid(InvalidReason.UserTamperingDetected)
    elif offline_status is OfflineGracePeriodStatus.NotPermitted:
        return SessionValidity.Invalid(InvalidReason.ServiceUnreachable)
    else:
        return SessionValidity.ValidationFailureGracePeriod(grace_period_expiration)


def CheckOfflineStatus(state: ControlState, local_time: UtcDateTime, update_last_validation_status: bool = True) -> \
        Tuple[OfflineGracePeriodStatus, UtcDateTime]:
    if state.LastSuccessfulValidationTime is None:
        return OfflineGracePeriodStatus.NotPermitted, None
    if state.LastValidationStatus is ValidationStatus.Success:
        if IsTimeInconsistencyDetected(state, local_time):
            if update_last_validation_status:
                state.LastValidationStatus = ValidationStatus.UserTamperingDetected
            return OfflineGracePeriodStatus.UserTamperingDetected, None
        result, expiration = ControlLogic.IsInGracePeriodForValidationFailures(state.GracePeriodForValidationFailures,
                                                                               UtcDateTime(state.FailedValidationTimes[-1]),
                                                                               local_time)
        if result:
            return OfflineGracePeriodStatus.Available, expiration
        else:
            return OfflineGracePeriodStatus.NotPermitted, None
    else:
        return OfflineGracePeriodStatus.NotPermitted, None


def LogServerReached(state: ControlState, server_time: UtcDateTime, server_state: ValidationStatus):
    state.FailedValidationTimes.clear()
    state.LastSuccessfulValidationTime = server_time
    state.LastValidationStatus = server_state


def LogServerNotReached(state: ControlState, local_time: UtcDateTime):
    state.FailedValidationTimesUnsafe.insert(0, local_time.AsDateTime())


def IsTimeInconsistencyDetected(state: ControlState, local_time: UtcDateTime) -> bool:
    return ControlLogic.IsTimeInconsistencyDetected(state.LastSuccessfulValidationTime, state.FailedValidationTimesUtc,
                                                    local_time, False)


def StatusToReason(status: ValidationStatus) -> InvalidReason:
    if status is ValidationStatus.RegistrationRequired:
        return InvalidReason.InstanceNotRegistered
    try:
        return InvalidReason[status.name]
    except KeyError:
        return InvalidReason.Unknown
