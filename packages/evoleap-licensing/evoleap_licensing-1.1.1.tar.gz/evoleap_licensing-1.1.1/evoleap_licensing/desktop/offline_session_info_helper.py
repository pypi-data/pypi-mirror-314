from ..states.ValidationState import ValidationState
from ..states.ValidatedSessionState import ValidatedSessionState
from ..timehandling.UtcDateTime import UtcDateTime
from uuid import UUID, uuid4
from typing import Optional, Union
from .OfflineSessionInfo import OfflineSessionInfo


class OfflineSessionInfoHelper:

    @staticmethod
    def BeginOfflineSession(state: ValidationState, session_state: ValidatedSessionState,
                            start_time: Optional[UtcDateTime], server_session_key: Union[str, type(None)]):
        id = uuid4()
        osi = OfflineSessionInfo()
        osi.LocalSessionId = id
        osi.UtcStartTime = start_time
        osi.SessionKey = server_session_key
        state.OfflineSessionsUnsafe.append(osi)
        session_state.OfflineSessionID = id
        return id

    @staticmethod
    def EndOfflineSession(state: ValidationState, session_state: ValidatedSessionState,
                          end_time: Optional[UtcDateTime]):
        osi = state.OfflineSession(session_state.OfflineSessionID)
        osi.UtcEndTime = end_time
