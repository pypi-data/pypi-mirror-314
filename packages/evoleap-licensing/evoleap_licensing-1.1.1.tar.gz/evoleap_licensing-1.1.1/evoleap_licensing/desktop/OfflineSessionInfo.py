from uuid import UUID
from datetime import datetime
from ..timehandling.UtcDateTime import UtcDateTime
from typing import Optional, Union, List


class OfflineComponentCheckoutInfo:
    _component: str
    _checkoutTime: datetime
    _tokenCount: int

    def __init__(self, component: str, checkout_time: Union[datetime, UtcDateTime], token_count: int):
        self._component = component
        if checkout_time is datetime:
            self._checkoutTime = checkout_time
        elif checkout_time is UtcDateTime:
            self._checkoutTime = checkout_time.AsDateTime()
        self._tokenCount = token_count

    @property
    def Component(self) -> str:
        return self._component

    @Component.setter
    def Component(self, value: str):
        self._component = value

    @property
    def CheckoutTime(self) -> datetime:
        return self._checkoutTime

    @CheckoutTime.setter
    def CheckoutTime(self, value: datetime):
        self._checkoutTime = value

    @property
    def CheckoutTimeUtc(self) -> UtcDateTime:
        return UtcDateTime(self._checkoutTime)

    @CheckoutTimeUtc.setter
    def CheckoutTimeUtc(self, value: UtcDateTime):
        self._checkoutTime = value.AsDateTime()

    @property
    def TokenCount(self) -> int:
        return self._tokenCount

    @TokenCount.setter
    def TokenCount(self, value: int):
        self._tokenCount = value


class OfflineSessionInfo:
    _localSessionId: UUID
    _sessionKey: Union[str, type(None)]
    _startTime: Optional[datetime]
    _endTime: Optional[datetime]
    _componentCheckouts: List[OfflineComponentCheckoutInfo]
    _uploadAttempts: int

    @property
    def LocalSessionId(self) -> UUID:
        return self._localSessionId

    @LocalSessionId.setter
    def LocalSessionId(self, value: UUID):
        self._localSessionId = value

    @property
    def SessionKey(self) -> Union[str, type(None)]:
        return self._sessionKey

    @SessionKey.setter
    def SessionKey(self, value: Union[str, type(None)]):
        self._sessionKey = value

    @property
    def StartTime(self) -> Optional[datetime]:
        return self._startTime

    @StartTime.setter
    def StartTime(self, value: Optional[datetime]):
        self._startTime = value

    @property
    def UtcStartTime(self) -> Optional[UtcDateTime]:
        return UtcDateTime(self._startTime) if self._startTime is not None else None

    @UtcStartTime.setter
    def UtcStartTime(self, value: Optional[UtcDateTime]):
        self._startTime = value.AsDateTime() if value is not None else None

    @property
    def EndTime(self) -> Optional[datetime]:
        return self._endTime

    @EndTime.setter
    def EndTime(self, value: Optional[datetime]):
        self._endTime = value

    @property
    def UtcEndTime(self) -> Optional[UtcDateTime]:
        return UtcDateTime(self._endTime) if self._endTime is not None else None

    @UtcEndTime.setter
    def UtcEndTime(self, value: Optional[UtcDateTime]):
        self._endTime = value.AsDateTime() if value is not None else None

    @property
    def ComponentCheckouts(self) -> List[OfflineComponentCheckoutInfo]:
        return self._componentCheckouts

    @ComponentCheckouts.setter
    def ComponentCheckouts(self, value: List[OfflineComponentCheckoutInfo]):
        self._componentCheckouts = value

    @property
    def UploadAttempts(self) -> int:
        return self._uploadAttempts

    @UploadAttempts.setter
    def UploadAttempts(self, value: int):
        self._uploadAttempts = value

    def AddComponentCheckout(self, info: OfflineComponentCheckoutInfo):
        if self._componentCheckouts is None:
            self._componentCheckouts = [info]
        else:
            self._componentCheckouts.append(info)
