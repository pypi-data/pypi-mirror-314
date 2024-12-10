from ..enumerations.licensing_enumerations import SessionState
from uuid import UUID


class ValidatedSessionState:
    _authToken: str
    _sessionKey: str
    _sessionState: SessionState
    # Not supported yet
    _offlineCheckoutKey: str
    _offlineSessionID: UUID

    def __init__(self):
        self._authToken = ""
        self._sessionKey = ""
        self._sessionState = SessionState.NotStarted
        self._offlineCheckoutKey = ""
        self._offlineSessionID = None

    @property
    def AuthToken(self) -> str:
        return self._authToken

    @AuthToken.setter
    def AuthToken(self, value: str):
        setattr(self, "_authToken", value)

    @property
    def SessionKey(self) -> str:
        return self._sessionKey

    @SessionKey.setter
    def SessionKey(self, value: str):
        setattr(self, "_sessionKey", value)

    @property
    def SessionState(self) -> SessionState:
        return self._sessionState

    @SessionState.setter
    def SessionState(self, value: SessionState):
        setattr(self, "_sessionState", value)

    @property
    def OfflineCheckoutKey(self) -> str:
        return self._offlineCheckoutKey

    @OfflineCheckoutKey.setter
    def OfflineCheckoutKey(self, value: str):
        setattr(self, "_offlineCheckoutKey", value)

    @property
    def OfflineSessionID(self) -> UUID:
        return self._offlineSessionID

    @OfflineSessionID.setter
    def OfflineSessionID(self, value: UUID):
        setattr(self, "_offlineSessionID", value)


def fromOther(source: ValidatedSessionState) -> ValidatedSessionState:
    dest = ValidatedSessionState()
    if source is None:
        dest.SessionState = SessionState.NotStarted
        return dest
    dest.AuthToken = source.AuthToken
    dest.SessionKey = source.SessionKey
    dest.SessionState = source.SessionState
    dest.OfflineCheckoutKey = source.OfflineCheckoutKey
    dest.OfflineSessionID = source.OfflineSessionID
    return dest
