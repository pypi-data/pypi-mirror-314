from .SessionControlState import SessionControlState
from uuid import UUID
from ..webservice import server_results
from ..desktop.OfflineSessionInfo import OfflineSessionInfo


class ValidationState(SessionControlState):
    def __init__(self):
        super(ValidationState, self).__init__()
        self._components = []
        self._componentEntitlements = []
        self._componentEntitlementsLoaded = False
        self._componentsLoaded = False
        self._userId = None
        self._instanceId = None
        self._offlineSessions = []

    @staticmethod
    def fromOther(source, dest):
        if dest is None:
            dest = ValidationState()
        if source is None:
            return dest
        if not isinstance(source, ValidationState):
            raise ValueError("source must also be a ValidationState object")
        dest = SessionControlState.fromOther(source, dest)
        dest._components = source.Components
        dest._componentEntitlements = source.ComponentEntitlements
        dest._offlineSessions = list(source._offlineSessions)

        if dest.Registered:
            dest.InstanceId = source.InstanceId
            dest.UserId = source.UserId
            dest.ComponentsLoaded = source.ComponentsLoaded
            dest.ComponentEntitlementsLoaded = source.ComponentEntitlementsLoaded
        return dest

    @property
    def InstanceId(self) -> UUID:
        """
        Gets the instance id of the registered instance
        :rtype: UUID
        """
        return self._instanceId

    @InstanceId.setter
    def InstanceId(self, value: UUID):
        setattr(self, "_instanceId", value)

    @property
    def UserId(self):
        return self._userId

    @UserId.setter
    def UserId(self, value):
        setattr(self, "_userId", value)

    @property
    def ComponentsLoaded(self):
        return self._componentsLoaded

    @ComponentsLoaded.setter
    def ComponentsLoaded(self, value):
        setattr(self, "_componentsLoaded", value)

    @property
    def ComponentEntitlementsLoaded(self):
        return self._componentEntitlementsLoaded

    @ComponentEntitlementsLoaded.setter
    def ComponentEntitlementsLoaded(self, value):
        setattr(self, "_componentEntitlementsLoaded", value)

    Components = property(lambda self: self._components)
    ComponentEntitlements = property(lambda self: self._componentEntitlements)
    ComponentsRO = property(lambda self: list(self._components))
    ComponentEntitlementsRO = property(lambda self: list(self._componentEntitlements))
    ComponentsIfLoaded = property(lambda self: list(self._components) if self.ComponentsLoaded else [])
    ComponentEntitlementsIfLoaded = property(lambda self:
                                             list(self._componentEntitlements)
                                             if self.ComponentEntitlementsLoaded else [])
    OfflineSessions = property(lambda self: list(self._offlineSessions))
    OfflineSessionsUnsafe = property(lambda self: self._offlineSessions)
    def AdditionalUpdateAfterRegistrationSuccess(self, result: server_results.RegisterAppResult):
        super().AdditionalUpdateAfterRegistrationSuccess(result)
        self._instanceId = result.InstanceId
        self._userId = result.UserId
        self.SessionDuration = result.SessionDuration

    def OfflineSession(self, guid: UUID) -> OfflineSessionInfo:
        return next((x for x in self._offlineSessions if x.LocalSessionId == guid), None)
