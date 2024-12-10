from enum import Enum


class ComponentLicenseModel(Enum):
    Nothing = 0
    Token = 1
    Session = 2
    ConsumableToken = 3
    Unknown = 4

    @staticmethod
    def GetValue(value: str):
        try:
            return ComponentLicenseModel[value]
        except KeyError:
            return ComponentLicenseModel["Unknown"]


class SessionState(Enum):
    NotStarted = 0
    Active = 1
    Ended = 2
    # added in 4.0
    ActiveOffline = 3
    ActiveOfflineWithOnlineSession = 4
    # added in 5.0
    ActiveOfflineCheckout = 5


class ValidationStatus(Enum):
    # Returned when registration is required before starting a session.
    RegistrationRequired = -101
    UserTamperingDetected = -100
    ServiceUnreachable = -99

    # Statuses above this line are client-only.
    # --------------
    # Statuses below this line are sent by the server

    OfflineCheckoutNotSupported = -16
    InvalidComponent = -15
    InsufficientTokens = -14
    ActivationPending = -13
    SessionRevoked = -12
    NoSeatsAvailable = -11
    InconsistentRegistration = -10
    InconsistentUser = -9
    InstanceNotRegistered = -8
    UserNotRegistered = -7
    InvalidLicenseKey = -6
    InvalidProductId = -5
    InstanceDisabled = -4
    UserDisabled = -3
    LicenseExpired = -2
    GeneralError = -1
    Success = 0


class InvalidReason(Enum):
    Unknown = -1
    NotInvalid = 0
    UserTamperingDetected = 1
    ServiceUnreachable = 2
    LicenseExpired = 3
    SessionRevoked = 4
    NoSeatsAvailable = 5
    InconsistentRegistration = 6
    InconsistentUser = 7
    InstanceNotRegistered = 8
    UserNotRegistered = 9
    InvalidLicenseKey = 10
    InvalidProductId = 11
    InstanceDisabled = 12
    UserDisabled = 13
    ActivationPending = 14
    OfflineCheckoutExpired = 15
    OfflineCheckoutNotSupported = 16
    InsufficientTokens = 17


class ComponentCheckoutFailureReason(Enum):
    Unknown = -1
    NoFailure = 0
    ServiceUnreachable = 1
    UserTamperingDetected = 2
    InsufficientTokens = 3
    InsufficientSessions = 4
    InvalidComponent = 5
