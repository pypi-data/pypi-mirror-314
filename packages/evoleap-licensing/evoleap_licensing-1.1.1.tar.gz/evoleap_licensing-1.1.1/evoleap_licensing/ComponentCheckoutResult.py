from .enumerations.licensing_enumerations import ComponentCheckoutFailureReason


class ComponentCheckoutResult:
    _success: bool
    _failureReason: ComponentCheckoutFailureReason
    _processedOffline: bool

    def __init__(self, success: bool, failure_reason: ComponentCheckoutFailureReason, processed_offline: bool):
        self._success = success
        self._failureReason = failure_reason
        self._processedOffline = processed_offline

    @property
    def Success(self) -> bool:
        return self._success

    @property
    def FailureReason(self) -> ComponentCheckoutFailureReason:
        return self._failureReason

    @property
    def ProcessedOffline(self) -> bool:
        return self._processedOffline

    @classmethod
    def GetSuccess(cls, processed_offline: bool):
        return cls(True, ComponentCheckoutFailureReason.NoFailure, processed_offline)

    @classmethod
    def GetFailure(cls, reason: ComponentCheckoutFailureReason, processed_offline: bool):
        return cls(False, reason, processed_offline)
