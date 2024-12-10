import json
from collections import namedtuple
from typing import Dict, Optional

import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from . import WebHelper, ConnectionSettings
from .jsoncomponent import JSONComponent
from .jsoncomponententitlement import JSONComponentEntitlement
from .server_results import *
from ..UserIdentity import UserIdentity
from .. import InstanceIdentity
from ..InstanceIdentity import InstanceIdentity as II
from ..UserInfo import UserInfo
from ..enumerations.licensing_enumerations import ValidationStatus


class LicensingWebService(object):
    def __init__(self, public_key: str):
        self._publicKey = public_key

    @staticmethod
    def AddCommonData(post_data: Dict[str, object], product_id: UUID, instance_identity: II,
                      user_identity: UserIdentity, user_info: Optional[UserInfo] = None):
        post_data['product_guid'] = str(product_id)
        if not (user_identity is None):
            post_data['user_identity'] = user_identity.Data

        if not (instance_identity is None):
            instance_identity_data = dict()
            if instance_identity.Version != InstanceIdentity.DEFAULT_VERSION:
                instance_identity_data['_version'] = instance_identity.Version
            if instance_identity.MaximumMismatchCount != InstanceIdentity.DEFAULT_MAX_MISMATCH_COUNT:
                instance_identity_data['_max_mismatch_count'] = instance_identity.MaximumMismatchCount

            for key, value in instance_identity.Values.items():
                key_data = dict()
                key_data['value'] = value.Value
                if value.Weight != InstanceIdentity.DEFAULT_WEIGHT:
                    key_data['_weight'] = value.Weight
                if value.CaseSensitive != InstanceIdentity.DEFAULT_CASE_SENSITIVE:
                    key_data['_case_sensitive'] = value.CaseSensitive
                if value.MaxArrayValueDifference != InstanceIdentity.DEFAULT_MAX_ARRAY_VALUE_DIFFERENCE:
                    key_data['_max_array_value_difference'] = value.MaxArrayValueDifference
                instance_identity_data[key] = key_data
            post_data['instance_identity'] = instance_identity_data

        if not (user_info is None):
            user_info_data = dict()
            user_info_data['name'] = user_info.Name
            user_info_data['email'] = user_info.Email
            post_data['user_info'] = user_info_data

    @staticmethod
    def ParseResultDateTime(json_result: any, field: str):
        return datetime.strptime(json_result[field], "%a, %d %b %Y %H:%M:%S %z")

    @staticmethod
    def GetUri(sub_uri: str) -> str:
        host = ConnectionSettings.ConnectionSettings.Host()
        if host.endswith("/"):
            host = host.rstrip("/")
        return host + "/api/v3.2/auth/" + sub_uri

    def GetRSAProvider(self):
        rsa_key = RSA.import_key(self._publicKey)
        # noinspection PyTypeChecker
        return PKCS1_v1_5.new(rsa_key)

    def RegisterAppAsync(self, product_id: UUID, license_key: str, user_info: UserInfo,
                         instance_identity: II, user_identity: UserIdentity) -> RegisterAppResult:
        post_data = dict()
        LicensingWebService.AddCommonData(post_data, product_id, instance_identity, user_identity, user_info)
        post_data['license_key'] = license_key
        uri = LicensingWebService.GetUri("register_app.json")
        rsa_provider = self.GetRSAProvider()
        try:
            result = WebHelper.WebHelper.PostEncryptedAsync(requests, uri, product_id, post_data, rsa_provider)
            json_result = json.JSONDecoder().decode(result)
            if json_result["success"]:
                app_result = RegisterAppResult()
                app_result.Success = True
                app_result.ServerTime = LicensingWebService.ParseResultDateTime(json_result, "time")
                app_result.InstanceId = UUID(hex=json_result["instance_guid"])
                app_result.GracePeriodForValidationFailures = timedelta(seconds=json_result["validation_grace_period"])
                app_result.SessionDuration = timedelta(seconds=json_result["session_duration"])
                app_result.FirstRegisteredAt = LicensingWebService.ParseResultDateTime(json_result,
                                                                                       "first_registered_at")
                app_result.UserId = UUID(hex=json_result["user_guid"])
                return app_result
            else:
                app_result = RegisterAppResult()
                app_result.Success = False
                app_result.ServerTime = LicensingWebService.ParseResultDateTime(json_result, "time")
                app_result.ErrorMessage = json_result["error"]
                return app_result
        except ConnectionError as conn_error:
            app_result = RegisterAppResult()
            app_result.Success = False
            app_result.ErrorMessage = "Error contacting registration service. " + conn_error.strerror
            return app_result
        except Exception as gen_error:
            app_result = RegisterAppResult()
            app_result.Success = False
            app_result.ErrorMessage = "A general error occurred during registration. \
                Please contact the software vendor. " + str(gen_error)
            return app_result

    def BeginAppSessionAsync(self, product_id: UUID, instance_id: UUID, version: str, user_id: Optional[UUID],
                             instance_identity: II = None, user_identity: UserIdentity = None,
                             requested_session_duration: Optional[timedelta] = None) -> BeginAppSessionResult:
        post_data = dict()
        LicensingWebService.AddCommonData(post_data, product_id, instance_identity, user_identity)
        post_data["instance_guid"] = str(instance_id)
        post_data["version"] = version
        if not (user_id is None):
            post_data["user_guid"] = str(user_id)
        if not (requested_session_duration is None):
            post_data["duration"] = str(requested_session_duration.seconds)
        uri = LicensingWebService.GetUri("begin_app_session.json")
        rsa_provider = self.GetRSAProvider()
        try:
            result = WebHelper.WebHelper.PostEncryptedAsync(requests, uri, product_id, post_data, rsa_provider)
            json_result = json.JSONDecoder().decode(result)
            status = ValidationStatus(json_result["status"])
            if status is ValidationStatus.Success:
                app_result = BeginAppSessionResult()
                app_result.Status = status
                app_result.ServerTime = LicensingWebService.ParseResultDateTime(json_result, "time")
                app_result.SessionKey = json_result["session_key"]
                app_result.Features = json_result["features"] or []
                # Deserialize component info if available
                LicensingWebService.parse_components(app_result, json_result)
                # Deserialize component entitlement info if available
                LicensingWebService.parse_component_entitlements(app_result, json_result)
                app_result.AuthToken = json_result["token"]
                app_result.GracePeriodForValidationFailures = timedelta(seconds=json_result["validation_grace_period"])
                app_result.SessionDuration = timedelta(seconds=json_result["session_duration"])
                return app_result
            else:
                app_result = BeginAppSessionResult()
                app_result.Status = status
                app_result.ServerTime = LicensingWebService.ParseResultDateTime(json_result, "time")
                app_result.ErrorMessage = json_result["error"]
                return app_result
        except ConnectionError as conn_error:
            app_result = BeginAppSessionResult()
            app_result.Status = ValidationStatus.ServiceUnreachable
            app_result.ErrorMessage = conn_error.strerror
            return app_result
        except Exception as gen_error:
            app_result = BeginAppSessionResult()
            app_result.Status = ValidationStatus.GeneralError
            app_result.ErrorMessage = str(gen_error)
            return app_result
    def GetUserLicense(self, product_id: UUID, user_identity: UserIdentity) -> GetUserLicenseServerResult:
        post_data = dict()
        LicensingWebService.AddCommonData(post_data, product_id, None, user_identity, None)
        uri = LicensingWebService.GetUri("get_user_license.json")
        rsa_provider = self.GetRSAProvider()
        try:
            result = WebHelper.WebHelper.PostEncryptedAsync(requests, uri, product_id, post_data, rsa_provider)
            json_result = json.JSONDecoder().decode(result)
            if json_result["success"]:
                app_result = GetUserLicenseServerResult()
                app_result.Success = True
                app_result.ServerTime = LicensingWebService.ParseResultDateTime(json_result, "time")
                app_result.Licenses = json_result["licenses"]
                return app_result
            else:
                app_result = GetUserLicenseServerResult()
                app_result.Success = False
                app_result.ServerTime = LicensingWebService.ParseResultDateTime(json_result, "time")
                app_result.ErrorMessage = json_result["error"]
                app_result.Licenses = []
                return app_result
        except ConnectionError as conn_error:
            app_result = GetUserLicenseServerResult()
            app_result.Success = False
            app_result.ErrorMessage = "Error contacting registration service. " + conn_error.strerror
            return app_result
        except Exception as gen_error:
            app_result = GetUserLicenseServerResult()
            app_result.Success = False
            app_result.ErrorMessage = "A general error occurred during registration. \
                Please contact the software vendor. " + str(gen_error)
            return app_result
    @staticmethod
    def parse_component_entitlements(app_result, json_result):
        if json_result.keys().__contains__("component_entitlements"):
            json_component_entitlements: List[JSONComponentEntitlement] = [
                JSONComponentEntitlement(c) for c in json_result["component_entitlements"]]
            app_result.ComponentEntitlements = [jc.Deserialize() for jc in json_component_entitlements]
        else:
            app_result.ComponentEntitlements = []

    @staticmethod
    def parse_components(app_result, json_result):
        if json_result.keys().__contains__("components"):
            json_components: List[JSONComponent] = [JSONComponent(c) for c in json_result["components"]]
            app_result.Components = [jc.Deserialize() for jc in json_components]
        else:
            app_result.Components = []

    def ExtendSession(self, product_id: UUID, token: str,
                      requested_extension_duration: Optional[timedelta] = None) -> ValidatedSessionResult:
        post_data = dict()
        LicensingWebService.AddCommonData(post_data, product_id, None, None, None)
        post_data["token"] = token
        if requested_extension_duration is not None:
            post_data["duration"] = str(requested_extension_duration.seconds)
        uri = LicensingWebService.GetUri("extend_session.json")
        rsa_provider = self.GetRSAProvider()
        try:
            result = WebHelper.WebHelper.PostEncryptedAsync(requests, uri, product_id, post_data, rsa_provider)
            json_result = json.JSONDecoder().decode(result)
            status = ValidationStatus(json_result["status"])
            if status is ValidationStatus.Success:
                app_result = ValidatedSessionResult()
                app_result.Status = status
                app_result.ServerTime = LicensingWebService.ParseResultDateTime(json_result, "time")
                app_result.Features = json_result["features"] or []
                app_result.AuthToken = json_result["token"]
                app_result.GracePeriodForValidationFailures = timedelta(seconds=json_result["validation_grace_period"])
                app_result.SessionDuration = timedelta(seconds=json_result["session_duration"])
                return app_result
            else:
                app_result = ValidatedSessionResult()
                app_result.Status = status
                app_result.ServerTime = LicensingWebService.ParseResultDateTime(json_result, "time")
                app_result.ErrorMessage = json_result["error"]
                return app_result
        except ConnectionError as conn_error:
            app_result = ValidatedSessionResult()
            app_result.Status = ValidationStatus.ServiceUnreachable
            app_result.ErrorMessage = conn_error.strerror
            return app_result
        except Exception as gen_error:
            app_result = ValidatedSessionResult()
            app_result.Status = ValidationStatus.GeneralError
            app_result.ErrorMessage = str(gen_error)
            return app_result

    def CheckOutComponentCommon(self, post_data: dict, uri_part: str, product_id: str) -> CheckOutComponentResult:
        uri = LicensingWebService.GetUri(uri_part)
        rsa_provider = self.GetRSAProvider()
        try:
            result = WebHelper.WebHelper.PostEncryptedAsync(requests, uri, product_id, post_data, rsa_provider)
            json_result = json.JSONDecoder().decode(result)
            status = ValidationStatus(json_result["status"])
            if status is ValidationStatus.Success:
                app_result = CheckOutComponentResult()
                app_result.Status = status
                app_result.ServerTime = LicensingWebService.ParseResultDateTime(json_result, "time")
                LicensingWebService.parse_components(app_result, json_result)
                LicensingWebService.parse_component_entitlements(app_result, json_result)
                return app_result
            else:
                app_result = CheckOutComponentResult()
                app_result.Status = status
                app_result.ServerTime = LicensingWebService.ParseResultDateTime(json_result, "time")
                app_result.ErrorMessage = json_result["error"]
                return app_result
        except ConnectionError as conn_error:
            app_result = CheckOutComponentResult()
            app_result.Status = ValidationStatus.ServiceUnreachable
            app_result.ErrorMessage = conn_error.strerror
            return app_result
        except Exception as gen_error:
            app_result = CheckOutComponentResult()
            app_result.Status = ValidationStatus.GeneralError
            app_result.ErrorMessage = str(gen_error)
            return app_result

    def CheckOutComponents(self, product_id: UUID, session_key: str, components: List[str]) -> CheckOutComponentResult:
        post_data = dict()
        LicensingWebService.AddCommonData(post_data, product_id, None, None, None)
        post_data["session_key"] = session_key
        post_data["components"] = components 
        return self.CheckOutComponentCommon(post_data, "check_out_components.json", product_id)
        
    def CheckOutConsumableComponent(self, product_id: UUID, session_key: str, component: str, token_count: Optional[int] = None) -> CheckOutComponentResult:
        post_data = dict()
        LicensingWebService.AddCommonData(post_data, product_id, None, None, None)
        post_data["session_key"] = session_key
        post_data["component"] = component
        post_data["token_count"] = token_count
        return self.CheckOutComponentCommon(post_data, "check_out_consumable_component.json", product_id)

    def EndSession(self, product_id: UUID, token: str) -> EndSessionResult:
        post_data = dict()
        LicensingWebService.AddCommonData(post_data, product_id, None, None, None)
        post_data["token"] = token
        uri = LicensingWebService.GetUri("end_session.json")
        rsa_provider = self.GetRSAProvider()
        try:
            result = WebHelper.WebHelper.PostEncryptedAsync(requests, uri, product_id, post_data, rsa_provider)
            json_result = json.JSONDecoder().decode(result)
            app_result = EndSessionResult()
            app_result.Success = True
            app_result.ServerTime = LicensingWebService.ParseResultDateTime(json_result, "time")
            return app_result
        except ConnectionError as conn_error:
            app_result = EndSessionResult()
            app_result.Success = False
            app_result.ErrorMessage = conn_error.strerror
            return app_result
        except Exception as gen_error:
            app_result = EndSessionResult()
            app_result.Success = False
            app_result.ErrorMessage = str(gen_error)
            return app_result

    def GetComponentStatus(self, product_id: UUID, session_key: str) -> ComponentsStatusResult:
        post_data = dict()
        LicensingWebService.AddCommonData(post_data, product_id, None, None, None)
        post_data["session_key"] = session_key
        uri = LicensingWebService.GetUri("components_status.json")
        rsa_provider = self.GetRSAProvider()
        try:
            result = WebHelper.WebHelper.PostEncryptedAsync(requests, uri, product_id, post_data, rsa_provider)
            json_result = json.JSONDecoder().decode(result)
            app_result = ComponentsStatusResult()
            app_result.Success = True
            LicensingWebService.parse_components(app_result, json_result)
            LicensingWebService.parse_component_entitlements(app_result, json_result)
            return app_result
        except ConnectionError as conn_error:
            app_result = ComponentsStatusResult()
            app_result.Success = False
            app_result.ErrorMessage = conn_error.strerror
            return app_result
        except Exception as gen_error:
            app_result = ComponentsStatusResult()
            app_result.Success = False
            app_result.ErrorMessage = str(gen_error)
            return app_result
