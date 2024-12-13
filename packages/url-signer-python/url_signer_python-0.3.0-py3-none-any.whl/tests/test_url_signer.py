# pylint: disable=line-too-long
import os
from ioriver.url_signer import UrlSigner


def test_fetch_url():
    expected_signature = "Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly93d3cuZXhhbXBsZS5jb20vc3RyZWFtcy8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxMjM1MDAwfSwiRGF0ZUdyZWF0ZXJUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjEyMzQwMDB9LCJJcEFkZHJlc3MiOnsiQVdTOlNvdXJjZUlwIjoiMTkyLjAuMi4wLzI0In19fV19&Signature=ZcV5KvY27PJl4uefiDVWaFIGSFTLNLgMWyzj40lDejorggJAh0sq6L55Nb2MwETZGUNXDxdpby0uHmP~eOFWB6UJyh1AMKaQxMlFKyWXLS-3GJfnukNtcR6YgPf7k43hapbiylqwitpcojAQhGzrtbRM~QzU2s9exDoR7TTNx4WH77yVkW~1fb3QQQ7d5IiMfeTi7oKlnH1TgRD0zKVHsxDSaUkC9Tp2SLNsQqbbACrFwdK-qb6c9IKxSH70VSpEw0Atx3UuPyNpU8hBVxpEOQyiHCPTpDiNdcSkcL5dMDu86SmqvG8arP2SJ3Cr6q1oyLYby4ce1EtHPxMCnOrzwA__&Key-Pair-Id=1234&FS-Policy=cmVzb3VyY2VzPWh0dHBzJTNBJTJGJTJGd3d3LmV4YW1wbGUuY29tJTJGc3RyZWFtcyUyRiUyQSZzdGFydF90aW1lPTEyMzQwMDAmZW5kX3RpbWU9MTIzNTAwMCZpcF9hZGRyZXNzZXM9MTkyLjAuMi4wJTJGMjQ=&FS-Signature=ED+iPaYgX+tMP/WJrlzAOOOhMZMMOInJWvHGBk3AGPWFl+n5AaUDQiHq3uSZOvM4JreRvOVadj+teyQzdrs8LubyCDFUmHOysgyLaT9CfjHVSinjVKuoPUdTKFgLZbO5nHu0M7Ryq6Mfj3l4yXiNnAv+ekUDyW4Xw+PXe5BWLX+Udwow2HCDqQiUFqrrnR36Ohm2+Z20JkeTrp1yRWLDHRxOPRveFk+4vGSTatkb3km+laO2PdS+ylQ21g4SFAWtYFM5JVMaqQ+jwP2evLywq1/9QwPg+K68FcQVabD6iEBF/tbYBKOoIoTA7/P3DmG0cMAODia3V0GE+4fRhuhGFw==&FS-Key-Id=5678&AK-Signature-token-123=ip=192.0.2.0/24~st=1234000~exp=1235000~acl=https://www.example.com/streams/*~hmac=c38b21ed965fc6e4d774fd576512d5f6516193937a7d2c29cc8728b55c918a4b"
    private_key = None
    encryption_key = "abcdef1234"
    with open(os.path.join(os.path.dirname(__file__), 'private_key.pem'), 'r') as key_file:
        private_key = key_file.read()
    assert private_key is not None

    providers_key_info = {
        "cloudfront_key_id": "1234",
        "fastly_key_id": "5678",
        "akamai_key_id": "token-123"
    }

    policy = {
        "resources": "https://www.example.com/streams/*",
        "condition": {
            "start_time": 1234000,
            "end_time": 1235000,
            "ip_addresses": "192.0.2.0/24"
        }
    }

    singer = UrlSigner(private_key, encryption_key, providers_key_info)
    assert singer.generate_url_signature(policy) == expected_signature
