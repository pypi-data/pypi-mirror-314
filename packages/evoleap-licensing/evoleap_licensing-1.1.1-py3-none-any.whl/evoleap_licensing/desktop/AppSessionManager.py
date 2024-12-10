from datetime import timedelta
from typing import Optional, Tuple, List, Callable
from uuid import UUID

from .enumerations import ValidationResult
from .offline_session_info_helper import OfflineSessionInfoHelper
from .. import ControlManagerHelper
from ..ComponentCheckoutResult import ComponentCheckoutResult
from ..ComponentInfo import ComponentInfo
from ..ComponentsStatus import ComponentsStatus
from ..InstanceIdentity import InstanceIdentity
from ..SessionValidity import SessionValidity
from ..UserIdentity import UserIdentity
from ..control_logic import ControlLogic
from ..enumerations.licensing_enumerations import *
from ..states.ControlState import ControlState
from ..states.ValidatedSessionState import ValidatedSessionState
from ..states.ValidationState import ValidationState
from ..timehandling import TimeProvider
from ..timehandling.UtcDateTime import UtcDateTime
from ..webservice.LicensingWebService import LicensingWebService
from ..webservice.server_results import BeginAppSessionResult, ValidatedSessionResult, CheckOutComponentResult


class AppSessionManager(object):
    _webService: LicensingWebService
    _productId: UUID
    _version: str
    _validationState: ValidationState
    _sessionState: ValidatedSessionState
    _instanceIdentity: InstanceIdentity
    _userIdentity: UserIdentity

    def __init__(self, web_service: LicensingWebService, product_id: UUID, version: str,
                 validation_state: ValidationState, validated_session_state: ValidatedSessionState,
                 instance_identity: Optional[InstanceIdentity] = None,
                 user_identity: Optional[UserIdentity] = None):
        self._webService = web_service
        self._productId = product_id
        self._version = version
        self._validationState = validation_state
        self._sessionState = validated_session_state
        self._instanceIdentity = instance_identity
        self._userIdentity = user_identity

    @staticmethod
    def Now() -> UtcDateTime:
        return TimeProvider.Current().UtcNow()

    def BeginSession(self, requested_session_duration: Optional[timedelta] = None):
        if self._sessionState.SessionState != SessionState.NotStarted:
            raise RuntimeError()

        web_result = self.BeginWebSession(requested_session_duration)
        validity, result = self.ProcessWebResultIntoValidity(web_result)
        if result is ValidationResult.OnlineSuccess:
            self._sessionState.SessionState = SessionState.Active
        elif result is ValidationResult.OfflineSuccess:
            self._sessionState.SessionState = SessionState.ActiveOffline
            OfflineSessionInfoHelper.BeginOfflineSession(self._validationState, self._sessionState, self.Now(), None)
        return validity

    def BeginWebSession(self, requested_session_duration: Optional[timedelta] = None) -> BeginAppSessionResult:
        result = self._webService.BeginAppSessionAsync(self._productId, self._validationState.InstanceId,
                                                       self._version, self._validationState.UserId,
                                                       self._instanceIdentity, self._userIdentity,
                                                       requested_session_duration)
        if result.Status is ValidationStatus.Success:
            self.UpdateCommonSessionState(result)
            self._sessionState.SessionKey = result.SessionKey
            self._validationState.Components.clear()
            [self._validationState.Components.append(x) for x in result.Components]
            self._validationState.ComponentsLoaded = True
            self._validationState.ComponentEntitlements.clear()
            [self._validationState.ComponentEntitlements.append(x) for x in result.ComponentEntitlements]
            self._validationState.ComponentEntitlementsLoaded = True
        return result

    def UpdateCommonSessionState(self, result: ValidatedSessionResult):
        self._sessionState.AuthToken = result.AuthToken
        self._validationState.GracePeriodForValidationFailures = result.GracePeriodForValidationFailures
        self._validationState.SessionDuration = result.SessionDuration
        features = ControlState.Features.__get__(self._validationState)
        features.clear()
        [features.append(x) for x in result.Features]

    def ProcessWebResultIntoValidity(self, web_result: ValidatedSessionResult) -> \
            Tuple[SessionValidity, ValidationResult]:
        if (web_result.Status == ValidationStatus.ServiceUnreachable or
                web_result.Status == ValidationStatus.GeneralError):
            ControlManagerHelper.LogServerNotReached(self._validationState, self.Now())
            status, expiration = ControlManagerHelper.CheckOfflineStatus(self._validationState, self.Now())
            if status is ControlManagerHelper.OfflineGracePeriodStatus.NotPermitted:
                return SessionValidity.Invalid(InvalidReason.ServiceUnreachable,
                                               False), ValidationResult.OfflineFailure
            elif status is ControlManagerHelper.OfflineGracePeriodStatus.UserTamperingDetected:
                return SessionValidity.Invalid(InvalidReason.UserTamperingDetected,
                                               False), ValidationResult.OfflineFailureUserTampering
            else:
                return SessionValidity.ValidationFailureGracePeriod(expiration), ValidationResult.OfflineSuccess
        else:
            ControlManagerHelper.LogServerReached(self._validationState, web_result.ServerTime, web_result.Status)
            if web_result.Status == ValidationStatus.Success:
                return SessionValidity.Valid(self._validationState.SessionDuration), ValidationResult.OnlineSuccess
            else:
                return SessionValidity.Invalid(ControlManagerHelper.StatusToReason(web_result.Status),
                                               False), ValidationResult.OnlineFailure

    def ExtendSession(self, requested_extension_duration: timedelta) -> SessionValidity:

        session_state = self._sessionState.SessionState
        if session_state is SessionState.Active or session_state is not SessionState.ActiveOfflineWithOnlineSession:
            web_result = self.ExtendWebSession(requested_extension_duration)
        elif session_state is SessionState.ActiveOffline:
            web_result = self.BeginWebSession(requested_extension_duration)
        else:
            raise ValueError('There is no active session to extend')

        validity, result = self.ProcessWebResultIntoValidity(web_result)
        if result is ValidationResult.OnlineSuccess:
            self._sessionState.SessionState = SessionState.Active
        elif result is ValidationResult.OfflineSuccess:
            if session_state is SessionState.Active:
                OfflineSessionInfoHelper.BeginOfflineSession(self._validationState, self._sessionState, None,
                                                             self._sessionState.SessionKey)
            if session_state is SessionState.Active or session_state is SessionState.ActiveOfflineWithOnlineSession:
                self._sessionState.SessionState = SessionState.ActiveOfflineWithOnlineSession
            else:
                self._sessionState.SessionState = SessionState.ActiveOffline
        else:
            self._sessionState.SessionState = SessionState.Ended
        return validity

    def ExtendWebSession(self, requested_extension_duration: timedelta) -> ValidatedSessionResult:
        result = self._webService.ExtendSession(self._productId, self._sessionState.AuthToken,
                                                requested_extension_duration)
        if result.Status is ValidationStatus.Success:
            self.UpdateCommonSessionState(result)
        return result

    def CheckOutComponents(self, components: List[str]) -> ComponentCheckoutResult:
        return self.CheckOutComponentsCommon(components, lambda: self._webService.CheckOutComponents(self._productId, self._sessionState.SessionKey, components))

    def CheckOutConsumableComponent(self, component: str, token_count: Optional[int]) -> ComponentCheckoutResult:
        return self.CheckOutComponentsCommon([component], lambda: self._webService.CheckOutConsumableComponent(self._productId, self._sessionState.SessionKey, component, token_count))

    def CheckOutComponentsCommon(self, components: List[str], web_result_provider: Callable[[], CheckOutComponentResult]) -> ComponentCheckoutResult:
        session_state = self._sessionState.SessionState
        if session_state is SessionState.NotStarted or \
                session_state is SessionState.Ended:
            raise ValueError('A session is not active')
        if session_state is SessionState.Active:
            web_result = web_result_provider()
            if (web_result.Status == ValidationStatus.ServiceUnreachable or
                    web_result.Status == ValidationStatus.GeneralError):
                failure_reason = ComponentCheckoutFailureReason.ServiceUnreachable if \
                    web_result.Status == ValidationStatus.ServiceUnreachable else ComponentCheckoutFailureReason.Unknown
                return self.CheckOutFreeComponentsOffline(components, failure_reason)
            else:
                if web_result.Status is ValidationStatus.Success:
                    return ComponentCheckoutResult.GetSuccess(False)
                elif web_result.Status is ValidationStatus.NoSeatsAvailable:
                    return ComponentCheckoutResult.GetFailure(ComponentCheckoutFailureReason.InsufficientSessions,
                                                              False)
                elif web_result.Status is ValidationStatus.InsufficientTokens:
                    return ComponentCheckoutResult.GetFailure(ComponentCheckoutFailureReason.InsufficientTokens, False)
                elif web_result.Status is ValidationStatus.InvalidComponent:
                    return ComponentCheckoutResult.GetFailure(ComponentCheckoutFailureReason.InvalidComponent, False)
                else:
                    return ComponentCheckoutResult.GetFailure(ComponentCheckoutFailureReason.Unknown, False)
        elif session_state is SessionState.ActiveOffline or \
                session_state is SessionState.ActiveOfflineWithOnlineSession:
            return self.CheckOutFreeComponentsOffline(components, ComponentCheckoutFailureReason.ServiceUnreachable)
        else:
            raise ValueError('A session is not active')

    def CheckOutFreeComponentsOffline(self, components: List[str],
                                      failure_reason: ComponentCheckoutFailureReason) -> ComponentCheckoutResult:
        if ControlLogic.IsTimeInconsistencyDetected(self._validationState.LastSuccessfulValidationTime,
                                                    self._validationState.FailedValidationTimesUtc, self.Now(), False):
            return ComponentCheckoutResult.GetFailure(ComponentCheckoutFailureReason.UserTamperingDetected, True)

        if self._validationState.LastSuccessfulValidationTime is not None:
            return ComponentCheckoutResult.GetFailure(failure_reason, True)

        if not self._validationState.ComponentsLoaded:
            return ComponentCheckoutResult.GetFailure(failure_reason, True)

        failed = False
        for name in components:
            component_info: ComponentInfo = next(
                (c for c in self._validationState.Components if c.Name.casefold() == name.casefold()), None)
            if component_info is None:
                failed = True
                break

            bad = True
            if component_info.LicenseModel is ComponentLicenseModel.Nothing:
                bad = False
            elif component_info.LicenseModel is ComponentLicenseModel.Token:
                effective_tokens = component_info.TokensRequiredAt(self.Now())
                if effective_tokens == 0:
                    bad = False
            if bad:
                failed = True
                break

        if failed:
            return ComponentCheckoutResult.GetFailure(failure_reason, True)
        else:
            return ComponentCheckoutResult.GetSuccess(True)

    def GetComponentsStatus(self) -> ComponentsStatus:
        if self._sessionState.SessionState is SessionState.NotStarted or \
                self._sessionState.SessionState is SessionState.Ended:
            raise ValueError('A session is not active')
        elif self._sessionState.SessionState is SessionState.ActiveOffline:
            ret = ComponentsStatus()
            ret.Success = False
            ret.Components = self._validationState.ComponentsIfLoaded()
            ret.ComponentEntitlements = self._validationState.ComponentEntitlementsIfLoaded()
            return ret
        else:
            web_result = self._webService.GetComponentStatus(self._productId, self._sessionState.SessionKey)
            if web_result.Success:
                self._validationState.Components.clear()
                [self._validationState.Components.append(x) for x in web_result.Components]
                self._validationState.ComponentsLoaded = True
                self._validationState.ComponentEntitlements.clear()
                [self._validationState.ComponentEntitlements.append(x) for x in web_result.ComponentEntitlements]
                self._validationState.ComponentEntitlementsLoaded = True
                ret = ComponentsStatus()
                ret.Success = False
                ret.Components = self._validationState.Components
                ret.ComponentEntitlements = self._validationState.ComponentEntitlements
                return ret
            else:
                ret = ComponentsStatus()
                ret.Success = False
                ret.Components = self._validationState.ComponentsIfLoaded
                ret.ComponentEntitlements = self._validationState.ComponentEntitlementsIfLoaded
                return ret

    def CurrentOfflineSessionID(self) -> Optional[UUID]:
        if self._sessionState.SessionState is SessionState.ActiveOffline or \
                self._sessionState.SessionState is SessionState.ActiveOfflineWithOnlineSession:
            return self._sessionState.OfflineSessionID
        else:
            return None

    def EndSession(self) -> bool:
        session_state = self._sessionState.SessionState
        if session_state is SessionState.NotStarted or \
                session_state is SessionState.Ended:
            raise ValueError('A session is not active')
        elif session_state is SessionState.Active or session_state is SessionState.ActiveOfflineWithOnlineSession:
            result = self._webService.EndSession(self._productId, self._sessionState.AuthToken)
            if result.Success:
                if session_state is SessionState.ActiveOfflineWithOnlineSession:
                    OfflineSessionInfoHelper.EndOfflineSession(self._validationState, self._sessionState, None)
                self._sessionState.SessionState = SessionState.Ended
                return True
            else:
                return False
        else:
            OfflineSessionInfoHelper.EndOfflineSession(self._validationState, self._sessionState, self.Now())
            self._sessionState.SessionState = SessionState.Ended
            return True
