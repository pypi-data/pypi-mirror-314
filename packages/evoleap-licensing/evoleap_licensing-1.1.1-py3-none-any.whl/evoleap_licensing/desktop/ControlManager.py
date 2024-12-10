from datetime import timedelta
from typing import Optional, List
from uuid import UUID

from .AppSessionManager import AppSessionManager
from .. import ControlManagerHelper
from ..ComponentCheckoutResult import ComponentCheckoutResult
from ..ControlStrategy import ControlStrategy
from ..InstanceIdentity import InstanceIdentity
from ..RegistrationResult import RegistrationResult
from ..SessionValidity import SessionValidity
from ..UserIdentity import UserIdentity
from ..UserInfo import UserInfo
from ..UserLicenseResult import UserLicenseResult
from ..enumerations.licensing_enumerations import SessionState
from ..states.ValidatedSessionState import ValidatedSessionState, fromOther as fromOtherValidatedSessionState
from ..states.ValidationState import ValidationState
from ..timehandling import TimeProvider
from ..webservice.LicensingWebService import LicensingWebService
from ..webservice.server_results import RegisterResultBase


class ControlManager:
    _state: ValidationState
    _sessionState: ValidatedSessionState
    _productId: UUID
    _version: str
    _sessionManager: AppSessionManager
    _webService: LicensingWebService
    _userIdentity: UserIdentity
    _instanceIdentity: InstanceIdentity
    _strategy: ControlStrategy

    @property
    def State(self) -> ValidationState:
        return self._state

    @property
    def SessionState(self) -> ValidatedSessionState:
        return self._sessionState

    @property
    def ProductId(self) -> UUID:
        return self._productId

    @property
    def Version(self) -> str:
        return self._version

    @property
    def SessionManager(self) -> AppSessionManager:
        return self._sessionManager

    @property
    def WebService(self) -> LicensingWebService:
        return self._webService

    @property
    def UserIdentity(self) -> UserIdentity:
        return self._userIdentity

    @property
    def InstanceIdentity(self) -> InstanceIdentity:
        return self._instanceIdentity

    @property
    def strategy(self) -> ControlStrategy:
        return self._strategy

    def __init__(self, product_id: UUID, version: str, public_key: str, user_identity: UserIdentity,
                 instance_identity: InstanceIdentity, strategy: ControlStrategy = None,
                 saved_state: ValidationState = None, session_state: ValidatedSessionState = None):
        self._state = ValidationState.fromOther(saved_state, None)
        self._sessionState = fromOtherValidatedSessionState(session_state)
        self._productId = product_id
        self._version = version
        self._userIdentity = user_identity
        self._instanceIdentity = instance_identity
        self._strategy = strategy or ControlStrategy()
        self._strategy.Lock()
        self._webService = LicensingWebService(public_key)
        self._sessionManager = None

    def Register(self, license_key: str, user_info: UserInfo) -> RegistrationResult:
        user_info.Verify()
        return ControlManagerHelper.Register(self._state, lambda: self.RegisterCore(license_key, user_info))

    def RegisterCore(self, license_key: str, user_info: UserInfo) -> RegisterResultBase:
        return self._webService.RegisterAppAsync(self._productId, license_key, user_info, self._instanceIdentity,
                                                 self._userIdentity)

    def ValidateSession(self, requested_session_duration: Optional[timedelta] = None) -> SessionValidity:
        ControlManagerHelper.InitializeState(self._state)
        if not self._state.Registered:
            return ControlManagerHelper.GetUnregisteredValidity(self._strategy, self._state,
                                                                TimeProvider.Current().UtcNow())
        self.EnsureWebSessionManagerCreated()
        session_state = self._sessionState.SessionState
        if session_state is SessionState.NotStarted:
            return self._sessionManager.BeginSession(requested_session_duration)
        elif session_state is SessionState.Ended:
            raise ValueError('The current session has already ended')
        else:
            return self._sessionManager.ExtendSession(requested_session_duration)

    def EnsureWebSessionManagerCreated(self):
        if self._sessionManager is None:
            self._sessionManager = AppSessionManager(self._webService, self._productId, self._version, self._state,
                                                     self._sessionState, self._instanceIdentity, self._userIdentity)

    def EndSession(self) -> bool:
        if self._sessionManager is None or \
                self._sessionState.SessionState is SessionState.NotStarted or \
                self._sessionState.SessionState is SessionState.Ended:
            return True
        return self._sessionManager.EndSession()

    def CheckOutComponents(self, component_names: List[str]) -> ComponentCheckoutResult:
        self.EnsureRegistered()
        self.EnsureSessionExists()
        if component_names is None or len(component_names) == 0:
            raise ValueError('At least one component must be specified')
        return self._sessionManager.CheckOutComponents(component_names)

    def CheckOutConsumableComponent(self, component_name: str, token_count: Optional[int] = None) -> ComponentCheckoutResult:
        self.EnsureRegistered()
        self.EnsureSessionExists()
        if component_name is None or len(component_name) == 0:
            raise ValueError('Component name must be specified')
        return self._sessionManager.CheckOutConsumableComponent(component_name, token_count)

    def EnsureSessionExists(self):
        if self._sessionManager is None:
            raise ValueError('A session is not active')

    def EnsureRegistered(self):
        if not self._state.Registered:
            raise ValueError('The instance must be registered')

    def GetComponentsStatus(self):
        self.EnsureRegistered()
        self.EnsureSessionExists()
        return self._sessionManager.GetComponentsStatus()

    def GetUserLicense(self) -> UserLicenseResult:
        result = self._webService.GetUserLicense(self._productId, self._userIdentity)
        return UserLicenseResult(result.Success, result.ErrorMessage, result.LicenseKeys)
