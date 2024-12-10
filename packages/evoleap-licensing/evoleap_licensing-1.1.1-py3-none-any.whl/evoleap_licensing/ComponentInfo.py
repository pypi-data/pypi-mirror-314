from datetime import datetime
from .enumerations.licensing_enumerations import ComponentLicenseModel
from .timehandling.UtcDateTime import UtcDateTime


class ComponentInfo:
    def __init__(self):
        self._name = None
        self._licenseModel = ComponentLicenseModel.Nothing
        self._tokensRequired = 0
        self._hasFreeTrial = False
        self._freeTrialExpirationTime = datetime.min
        self._originalTokensRequired = 0

    @property
    def Name(self) -> str:
        return self._name

    @Name.setter
    def Name(self, value: str):
        self._name = value

    @property
    def LicenseModel(self) -> ComponentLicenseModel:
        return self._licenseModel

    @LicenseModel.setter
    def LicenseModel(self, value: ComponentLicenseModel):
        self._licenseModel = value

    @property
    def TokensRequired(self) -> int:
        return self._tokensRequired

    @TokensRequired.setter
    def TokensRequired(self, value: int):
        self._tokensRequired = value

    @property
    def HasFreeTrial(self) -> bool:
        return self._hasFreeTrial

    @HasFreeTrial.setter
    def HasFreeTrial(self, value: bool):
        self._hasFreeTrial = value

    @property
    def FreeTrialExpirationTime(self) -> datetime:
        return self._freeTrialExpirationTime

    @FreeTrialExpirationTime.setter
    def FreeTrialExpirationTime(self, value: datetime):
        self._freeTrialExpirationTime = value

    @property
    def OriginalTokensRequired(self) -> int:
        return self._originalTokensRequired

    @OriginalTokensRequired.setter
    def OriginalTokensRequired(self, value: int):
        self._originalTokensRequired = value

    def TokensRequiredAt(self, time: UtcDateTime):
        if self.HasFreeTrial:
            if self.FreeTrialExpirationTime > time.AsDateTime():
                return self.TokensRequired
            else:
                return self.OriginalTokensRequired
        else:
            return self.TokensRequired
