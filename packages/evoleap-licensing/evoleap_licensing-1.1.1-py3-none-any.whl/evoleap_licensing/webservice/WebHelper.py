from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding
import json
import base64
import requests
from typing import Optional, Dict
from uuid import UUID


class ServerReachedWithNonSuccessErrorCodeError(IOError):
    def __init__(self, message: str):
        self._message = message

    @property
    def Message(self):
        return self._message


class WebHelper(object):
    @staticmethod
    def PostEncryptedAsync(client: requests, uri: str, product_id: UUID, data: Dict[str, object],
                           rsa_provider: any):
        key, iv, encrypted_content = WebHelper.CreateEncryptedJsonContent(product_id, data, rsa_provider)
        headers = {'cache-control': "no-cache", 'content-type': "application/json"}
        postResult = client.request("POST", uri, json=encrypted_content, headers=headers)
        if postResult.status_code != 200:
            raise ServerReachedWithNonSuccessErrorCodeError("Unsuccessful call to server");
        crypted_response = base64.decodebytes(postResult.content)
        return WebHelper.DecryptResponse(crypted_response, key, iv)

    @staticmethod
    def CreateEncryptedJsonContent(product_id: UUID, data: Dict[str, object], rsa_provider: any):
        payload_data = dict()
        payload_data["key"] = str(product_id)
        key, iv, data_string = WebHelper.EncryptData(data, rsa_provider)
        payload_data["data"] = data_string
        return key, iv, payload_data

    @staticmethod
    def EncryptData(data: Dict[str, object], rsa_provider: any):
        key = get_random_bytes(16)
        iv = get_random_bytes(16)
        cipher_aes = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
        encrypted_aes_key = rsa_provider.encrypt(key)
        json_encoder = json.JSONEncoder()
        post_string = json_encoder.encode(data)
        input_buffer = post_string.encode("utf-8")
        input_buffer = Padding.pad(input_buffer, AES.block_size)
        crypted_data = cipher_aes.encrypt(input_buffer)
        padding_char = b"\x00"
        final_buffer = b"".join([encrypted_aes_key, padding_char, iv, padding_char, crypted_data])
        return key, cipher_aes.IV, base64.b64encode(final_buffer).decode('utf-8')

    @staticmethod
    def DecryptResponse(crypted_response: bytes, key: bytes, iv: bytes):
        cipher_aes = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
        padded_response = cipher_aes.decrypt(crypted_response)
        final_json_string = Padding.unpad(padded_response, AES.block_size).decode('utf-8')
        return final_json_string
