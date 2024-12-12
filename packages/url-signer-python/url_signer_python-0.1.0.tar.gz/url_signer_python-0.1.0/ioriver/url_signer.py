import json
import base64
import urllib.parse

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from akamai.edgeauth import EdgeAuth

from .key_info import KeyInfo
from .policy import Policy


class UrlSigner:
    def __init__(self, private_key: str, encryption_key: str, providers_key_info: dict):
        self.private_key = bytes(private_key, "utf-8")
        self.encryption_key = encryption_key
        self.providers_key_info = KeyInfo()
        self.providers_key_info.from_dict(providers_key_info)

    def generate_url_signature(self, policy_data: dict):
        policy = Policy()
        policy.from_dict(policy_data)

        signatures = []
        if self.providers_key_info.cloudfront_key_id is not None:
            signatures.append(self._generate_cloudfront_signed_url(policy))
        if self.providers_key_info.fastly_key_id is not None:
            signatures.append(self._generate_fastly_signed_url(policy))
        if self.providers_key_info.akamai_key_id is not None:
            signatures.append(self._generate_akamai_signed_url(policy))

        return "&".join(signatures)

    def _generate_asymetric_signature(self, message: bytes):
        private_key_signer = serialization.load_pem_private_key(
            self.private_key,
            password=None,
            backend=default_backend()
        )
        return private_key_signer.sign(message, padding.PKCS1v15(), hashes.SHA1())

    def _generate_cloudfront_signed_url(self, policy: Policy):
        cf_policy = self._make_cloudfront_policy(policy)
        signature = self._generate_asymetric_signature(cf_policy.encode('utf-8'))

        return f"Policy={self._url_base64_encode_cf(cf_policy.encode('utf-8'))}&" \
            f"Signature={self._url_base64_encode_cf(signature)}&" \
            f"Key-Pair-Id={self.providers_key_info.cloudfront_key_id}"

    def _generate_fastly_signed_url(self, policy: Policy):
        params_dict = {'resources': policy.resources}
        if policy.condition:
            if policy.condition.start_time:
                params_dict['start_time'] = policy.condition.start_time
            if policy.condition.end_time:
                params_dict['end_time'] = policy.condition.end_time
            if policy.condition.ip_addresses:
                params_dict['ip_addresses'] = policy.condition.ip_addresses

        policy_url_encoded = urllib.parse.urlencode(params_dict)
        signature = self._generate_asymetric_signature(policy_url_encoded.encode('utf-8'))

        return f"FS-Policy={self._url_base64_encode(policy_url_encoded.encode('utf-8'))}&" \
            f"FS-Signature={self._url_base64_encode(signature)}&" \
            f"FS-Key-Id={self.providers_key_info.fastly_key_id}"

    def _generate_akamai_signed_url(self, policy: Policy):
        akamai_policy = {
            'key': self.encryption_key,
            'end_time': policy.condition.end_time
        }

        if policy.condition.start_time is not None:
            akamai_policy['start_time'] = policy.condition.start_time

        if policy.condition.ip_addresses is not None:
            akamai_policy['ip'] = policy.condition.ip_addresses

        et = EdgeAuth(**akamai_policy)
        token = et.generate_acl_token(policy.resources)
        return f"AK-Signature-{self.providers_key_info.akamai_key_id}={token}"

    def _make_cloudfront_policy(self, policy: Policy):
        aws_policy = {
            'Statement': [{
                'Resource': policy.resources,
                'Condition': {
                    'DateLessThan': {
                        'AWS:EpochTime': policy.condition.end_time
                    }
                }
            }]
        }

        if policy.condition.start_time is not None:
            aws_policy['Statement'][0]['Condition']['DateGreaterThan'] = {
                "AWS:EpochTime": policy.condition.start_time
            }

        if policy.condition.ip_addresses is not None:
            aws_policy['Statement'][0]['Condition']['IpAddress'] = {
                "AWS:SourceIp": policy.condition.ip_addresses
            }

        return json.dumps(aws_policy).replace(" ", "")

    def _url_base64_encode_cf(self, data: bytes):
        return base64.b64encode(data).replace(b'+', b'-').replace(b'=', b'_').replace(b'/', b'~').decode('utf-8')

    def _url_base64_encode(self, data: bytes):
        return base64.b64encode(data).decode('utf-8')
