from enum import Enum


class ValidationResult(Enum):
    OnlineSuccess = 0,
    OnlineFailure = 1,
    OfflineSuccess = 2,
    OfflineFailure = 3,
    OfflineFailureUserTampering = 4
