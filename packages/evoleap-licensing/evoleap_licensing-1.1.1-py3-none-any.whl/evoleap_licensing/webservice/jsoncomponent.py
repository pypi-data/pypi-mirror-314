from datetime import datetime, tzinfo, timedelta
from typing import Dict
import pytz

from ..ComponentInfo import ComponentInfo
from ..enumerations.licensing_enumerations import ComponentLicenseModel

SERVER_TIME_FORMAT = "%a, %d %b %Y %H:%M:%S %z"


class JSONComponent:
    __fields = ["name", "license_model", "tokens_required", "free_trial", "free_trial_expiration",
              "original_tokens_required"]

    def __init__(self, values: Dict[str, object]):
        self.name = ""
        self.license_model = ""
        self.tokens_required = 0
        self.free_trial = False
        self.free_trial_expiration = datetime.min.replace(tzinfo=pytz.utc).strftime(SERVER_TIME_FORMAT)
        self.original_tokens_required = 0
        [self.__setattr__(a, values[a]) for a in self.__class__.__fields if a in values]

    def Deserialize(self) -> ComponentInfo:
        info = ComponentInfo()
        info.Name = self.name
        info.LicenseModel = ComponentLicenseModel.GetValue(self.license_model)
        info.TokensRequired = self.tokens_required
        info.HasFreeTrial = self.free_trial
        info.FreeTrialExpirationTime = datetime.strptime(self.free_trial_expiration, SERVER_TIME_FORMAT)
        info.OriginalTokensRequired = self.original_tokens_required
        return info
